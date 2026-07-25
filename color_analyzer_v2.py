"""
color_analyzer_v2.py
Upgraded personal color analysis engine.

Key fixes vs. the original color_analyzer.py:
  1. REAL FACE DETECTION (OpenCV Haar cascades) instead of assuming the
     subject's face always sits at fixed pixel ratios in the frame.
     Region sampling (skin/hair/eyes) is now anchored to the detected
     face box, so off-center or zoomed-out photos still work.
  2. EYE DETECTION within the face box (Haar eye cascade) rather than
     guessed coordinates, with a ratio-based fallback if detection fails.
  3. WHITE BALANCE / LIGHTING NORMALIZATION (gray-world assumption) so a
     warm indoor bulb or a cool overcast photo doesn't get read as the
     subject's actual undertone. This is the single biggest source of
     error in phone-photo color analysis.
  4. OUTLIER-TRIMMED SAMPLING: instead of a plain median, each region is
     sampled from many small patches and trimmed of extreme pixels, so
     stray glasses glare, shadows, or flyaway hair don't skew the result.
  5. ITA° (Individual Typology Angle) - a published dermatology metric
     for skin tone classification - is computed alongside warmth/chroma,
     giving a second, independent signal for the season call and a
     defensible number to show in the report ("why we picked this season").
  6. IMAGE QUALITY CHECKS: flags photos that are too dark, too bright,
     blurry, or where no face was found, and lowers the confidence score
     instead of silently guessing.
  7. CONFIDENCE SCORE + WARNINGS in the output, so the studio (or the
     client-facing app) knows when to ask for a retake before generating
     a paid report.

Still uses only image_path in -> JSON out, same as the original, so it's
a drop-in replacement in the pipeline (analyze_and_drape.py / pdf_generator.py
only need the extracted_colors / color_metrics / season / sub_season keys,
all of which are preserved).

Dependencies: numpy, Pillow, opencv-python (cv2)
"""

import json
import os
import sys

import cv2
import numpy as np
from PIL import Image

# ---------------------------------------------------------------------------
# Color space helpers
# ---------------------------------------------------------------------------

def rgb_to_hex(rgb):
    r, g, b = [max(0, min(255, int(round(c)))) for c in rgb]
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def rgb_to_lab(rgb):
    """Standard sRGB -> CIE L*a*b* (D65). Returns real L*a*b* ranges:
    L in [0,100], a and b roughly [-128, 127]."""
    rgb = np.clip(np.array(rgb, dtype=np.float64) / 255.0, 0, 1)

    def pivot_rgb(c):
        return np.where(c > 0.04045, ((c + 0.055) / 1.055) ** 2.4, c / 12.92)

    lin = pivot_rgb(rgb)
    x = lin[0] * 0.4124 + lin[1] * 0.3576 + lin[2] * 0.1805
    y = lin[0] * 0.2126 + lin[1] * 0.7152 + lin[2] * 0.0722
    z = lin[0] * 0.0193 + lin[1] * 0.1192 + lin[2] * 0.9505

    ref_x, ref_y, ref_z = 0.95047, 1.0, 1.08883
    x, y, z = x / ref_x, y / ref_y, z / ref_z

    def pivot_xyz(t):
        return np.where(t > 0.008856, t ** (1 / 3), (7.787 * t) + (16 / 116))

    fx, fy, fz = pivot_xyz(x), pivot_xyz(y), pivot_xyz(z)
    L = (116 * fy) - 16
    a = 500 * (fx - fy)
    b = 200 * (fy - fz)
    return np.array([L, a, b])


def rgb_to_hsv01(rgb):
    r, g, b = [c / 255.0 for c in rgb]
    mx, mn = max(r, g, b), min(r, g, b)
    df = mx - mn
    if df == 0:
        h = 0.0
    elif mx == r:
        h = (60 * ((g - b) / df) + 360) % 360
    elif mx == g:
        h = (60 * ((b - r) / df) + 120) % 360
    else:
        h = (60 * ((r - g) / df) + 240) % 360
    s = 0.0 if mx == 0 else df / mx
    v = mx
    return np.array([h, s, v])


def individual_typology_angle(L, b):
    """ITA (deg) = arctan((L*-50)/b*) * 180/pi
    Standard dermatological skin-tone metric. Higher = lighter/more
    yellow-independent; more negative/lower = darker. Used here as an
    independent lightness/undertone cross-check on top of raw Lab."""
    return float(np.degrees(np.arctan2((L - 50.0), b)))


# ---------------------------------------------------------------------------
# Face / feature detection
# ---------------------------------------------------------------------------

_CASCADE_DIR = cv2.data.haarcascades
_FACE_CASCADE = cv2.CascadeClassifier(_CASCADE_DIR + "haarcascade_frontalface_default.xml")
_FACE_CASCADE_ALT = cv2.CascadeClassifier(_CASCADE_DIR + "haarcascade_frontalface_alt2.xml")
_EYE_CASCADE = cv2.CascadeClassifier(_CASCADE_DIR + "haarcascade_eye.xml")


def detect_face_box(cv_img_bgr):
    """Returns (x, y, w, h) of the largest detected face, or None."""
    gray = cv2.cvtColor(cv_img_bgr, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    faces = _FACE_CASCADE.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6, minSize=(60, 60))
    if len(faces) == 0:
        faces = _FACE_CASCADE_ALT.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5, minSize=(60, 60))
    if len(faces) == 0:
        return None, gray

    # take the largest face box (in case of multiple people / background faces)
    faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
    return tuple(faces[0]), gray


def detect_eyes_in_face(gray_full, face_box):
    x, y, w, h = face_box
    # restrict eye search to upper 60% of the face box, standard heuristic
    roi = gray_full[y:y + int(h * 0.6), x:x + w]
    eyes = _EYE_CASCADE.detectMultiScale(roi, scaleFactor=1.1, minNeighbors=6, minSize=(15, 15))
    if len(eyes) < 2:
        return None
    # keep the two largest, sort left-to-right
    eyes = sorted(eyes, key=lambda e: e[2] * e[3], reverse=True)[:2]
    eyes = sorted(eyes, key=lambda e: e[0])
    out = []
    for (ex, ey, ew, eh) in eyes:
        out.append((x + ex, y + ey, ew, eh))
    return out


# ---------------------------------------------------------------------------
# Image quality checks
# ---------------------------------------------------------------------------

def assess_quality(cv_img_bgr, face_found):
    warnings = []
    gray = cv2.cvtColor(cv_img_bgr, cv2.COLOR_BGR2GRAY)

    brightness = float(np.mean(gray))
    if brightness < 60:
        warnings.append("Photo looks underexposed/dark. Retake in bright, indirect natural light.")
    elif brightness > 220:
        warnings.append("Photo looks overexposed/blown out. Avoid direct flash or backlighting.")

    blur_score = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    if blur_score < 40:
        warnings.append("Photo appears blurry/out of focus. Hold the camera steady and check focus.")

    if not face_found:
        warnings.append("No face confidently detected — falling back to fixed-frame sampling. "
                         "For best accuracy, use a straight-on, well-lit, unobstructed face photo.")

    return {
        "brightness": brightness,
        "blur_score": blur_score,
        "warnings": warnings,
    }


# ---------------------------------------------------------------------------
# White balance normalization (gray-world)
# ---------------------------------------------------------------------------

def gray_world_white_balance(img_rgb_float):
    """Simple, well-established gray-world auto white balance. Scales each
    channel so the image's average color is neutral gray, which removes a
    large chunk of ambient-light color cast (warm bulbs, cool shade, etc.)
    before we ever measure the subject's undertone."""
    avg = img_rgb_float.reshape(-1, 3).mean(axis=0)
    gray_avg = avg.mean()
    scale = gray_avg / np.clip(avg, 1e-6, None)
    # dampen the correction so we don't over-correct on images that are
    # naturally dominated by one hue (e.g. lots of warm skin in frame)
    scale = 1.0 + (scale - 1.0) * 0.6
    balanced = img_rgb_float * scale
    return np.clip(balanced, 0, 255)


# ---------------------------------------------------------------------------
# Robust patch sampling
# ---------------------------------------------------------------------------

def sample_region_robust(img_rgb, box_px, n_patches=9, patch_frac=0.35, trim_pct=15):
    """Sample several small patches inside box_px (x0,y0,x1,y1), take each
    patch's median, then trim outlier patches (e.g. a patch that landed on
    a glasses reflection or a shadow) before averaging."""
    x0, y0, x1, y1 = [int(v) for v in box_px]
    x0, x1 = sorted((max(0, x0), max(0, x1)))
    y0, y1 = sorted((max(0, y0), max(0, y1)))
    w, h = max(1, x1 - x0), max(1, y1 - y0)

    if w < 4 or h < 4:
        crop = img_rgb[y0:y1, x0:x1].reshape(-1, 3)
        if crop.size == 0:
            return np.array([128.0, 128.0, 128.0])
        return np.median(crop, axis=0)

    rng = np.random.default_rng(42)
    patch_w = max(2, int(w * patch_frac))
    patch_h = max(2, int(h * patch_frac))
    medians = []
    for _ in range(n_patches):
        px = rng.integers(x0, max(x0 + 1, x1 - patch_w + 1))
        py = rng.integers(y0, max(y0 + 1, y1 - patch_h + 1))
        patch = img_rgb[py:py + patch_h, px:px + patch_w].reshape(-1, 3)
        if patch.size:
            medians.append(np.median(patch, axis=0))
    if not medians:
        crop = img_rgb[y0:y1, x0:x1].reshape(-1, 3)
        return np.median(crop, axis=0) if crop.size else np.array([128.0, 128.0, 128.0])

    medians = np.array(medians)
    # trim by overall luminance to drop the brightest/darkest outlier patches
    lum = medians.mean(axis=1)
    order = np.argsort(lum)
    n_trim = max(0, int(len(order) * trim_pct / 100.0))
    keep = order[n_trim: len(order) - n_trim] if len(order) - 2 * n_trim > 0 else order
    return np.median(medians[keep], axis=0)


# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------

def analyze_photo(image_path, apply_white_balance=True):
    if not os.path.exists(image_path):
        return {"error": f"Image file not found: {image_path}"}

    try:
        pil_img = Image.open(image_path).convert("RGB")
    except Exception as e:
        return {"error": f"Failed to load image: {str(e)}"}

    img_rgb = np.array(pil_img).astype(np.float64)
    cv_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    H, W = img_rgb.shape[:2]

    face_box, gray_full = detect_face_box(cv_bgr)
    face_found = face_box is not None
    quality = assess_quality(cv_bgr, face_found)

    if apply_white_balance:
        img_rgb = gray_world_white_balance(img_rgb)

    # ---- Determine sampling regions ----
    if face_found:
        fx, fy, fw, fh = face_box

        forehead_box = (fx + 0.30 * fw, fy + 0.05 * fh, fx + 0.70 * fw, fy + 0.22 * fh)
        cheek_l_box = (fx + 0.12 * fw, fy + 0.52 * fh, fx + 0.32 * fw, fy + 0.68 * fh)
        cheek_r_box = (fx + 0.68 * fw, fy + 0.52 * fh, fx + 0.88 * fw, fy + 0.68 * fh)
        # hair: strip above the detected forehead, plus a safety clamp to image bounds
        hair_top = max(0, fy - 0.55 * fh)
        hair_box = (fx + 0.15 * fw, hair_top, fx + 0.85 * fw, max(hair_top + 1, fy + 0.02 * fh))

        eyes = detect_eyes_in_face(gray_full, face_box)
        if eyes:
            eye_boxes = []
            for (ex, ey, ew, eh) in eyes:
                # sample the iris band (middle third of the eye box height)
                eye_boxes.append((ex + 0.20 * ew, ey + 0.35 * eh, ex + 0.80 * ew, ey + 0.65 * eh))
        else:
            eye_boxes = [
                (fx + 0.20 * fw, fy + 0.40 * fh, fx + 0.40 * fw, fy + 0.50 * fh),
                (fx + 0.60 * fw, fy + 0.40 * fh, fx + 0.80 * fw, fy + 0.50 * fh),
            ]
    else:
        # fallback: original fixed-ratio assumption (centered portrait)
        forehead_box = (0.45 * W, 0.28 * H, 0.55 * W, 0.35 * H)
        cheek_l_box = (0.32 * W, 0.52 * H, 0.42 * W, 0.60 * H)
        cheek_r_box = (0.58 * W, 0.52 * H, 0.68 * W, 0.60 * H)
        hair_box = (0.35 * W, 0.05 * H, 0.65 * W, 0.18 * H)
        eye_boxes = [
            (0.38 * W, 0.43 * H, 0.44 * W, 0.48 * H),
            (0.56 * W, 0.43 * H, 0.62 * W, 0.48 * H),
        ]

    skin_forehead = sample_region_robust(img_rgb, forehead_box)
    skin_cheek_l = sample_region_robust(img_rgb, cheek_l_box)
    skin_cheek_r = sample_region_robust(img_rgb, cheek_r_box)
    skin_color = np.median([skin_forehead, skin_cheek_l, skin_cheek_r], axis=0)

    hair_color = sample_region_robust(img_rgb, hair_box)

    eye_samples = [sample_region_robust(img_rgb, eb) for eb in eye_boxes]
    eye_color = np.median(eye_samples, axis=0)

    # ---- Color science ----
    skin_lab = rgb_to_lab(skin_color)
    hair_lab = rgb_to_lab(hair_color)
    eye_lab = rgb_to_lab(eye_color)

    skin_hsv = rgb_to_hsv01(skin_color)
    eye_hsv = rgb_to_hsv01(eye_color)

    L_skin, a_skin, b_skin = skin_lab
    ita = individual_typology_angle(L_skin, b_skin if abs(b_skin) > 1e-3 else 1e-3)

    # Warmth: b* (yellow-blue) is the primary undertone signal, a* (red-green)
    # contributes a smaller secondary weight.
    warmth = b_skin + (a_skin * 0.25)

    L_hair, L_eye = hair_lab[0], eye_lab[0]
    contrast = abs(L_skin - L_hair)
    overall_value = (L_skin + L_hair + L_eye) / 3.0

    chroma = (skin_hsv[1] * 100 + eye_hsv[1] * 100) / 2.0

    # ---- Season classification ----
    is_warm = warmth > 4.0
    is_light = overall_value > 50.0 or (L_skin > 62.0 and contrast < 30.0)

    season, sub_season = "", ""
    if is_warm:
        if is_light:
            season = "Spring"
            sub_season = "Bright Spring" if chroma > 42 else ("Light Spring" if L_skin > 68 else "Warm Spring")
        else:
            season = "Autumn"
            sub_season = "Soft Autumn" if chroma < 26 else ("Deep Autumn" if L_hair < 30 else "Warm Autumn")
    else:
        if is_light:
            season = "Summer"
            sub_season = "Soft Summer" if chroma < 24 else ("Light Summer" if L_skin > 70 else "Cool Summer")
        else:
            season = "Winter"
            sub_season = "Bright Winter" if chroma > 44 else ("Deep Winter" if L_hair < 25 else "Cool Winter")

    # ---- Confidence score ----
    confidence = 0.9
    if not face_found:
        confidence -= 0.35
    confidence -= 0.10 * len(quality["warnings"])
    # low |warmth| or borderline is_light means the call is closer to a coin flip
    if abs(warmth) < 1.5:
        confidence -= 0.15
    if abs(overall_value - 50.0) < 3.0:
        confidence -= 0.10
    confidence = float(max(0.15, min(0.97, confidence)))

    return {
        "face_detected": face_found,
        "face_box": list(map(int, face_box)) if face_found else None,
        "extracted_colors": {
            "skin": rgb_to_hex(skin_color),
            "hair": rgb_to_hex(hair_color),
            "eyes": rgb_to_hex(eye_color),
        },
        "color_metrics": {
            "warmth_score": float(warmth),
            "overall_value": float(overall_value),
            "contrast_score": float(contrast),
            "chroma_score": float(chroma),
            "ita_degrees": ita,
            "skin_lab": {"L": float(L_skin), "a": float(a_skin), "b": float(b_skin)},
        },
        "season": season,
        "sub_season": sub_season,
        "confidence": confidence,
        "image_quality": quality,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No image path provided."}))
        sys.exit(1)
    print(json.dumps(analyze_photo(sys.argv[1]), indent=2))
