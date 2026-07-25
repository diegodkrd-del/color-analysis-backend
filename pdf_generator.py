from jinja2 import Environment, FileSystemLoader
import os
import subprocess
import base64

SUBSEASON_PALETTES = {
    # SPRING SUBSEASONS
    "Light Spring": {
        "bg": "#FAF4ED",
        "accent": "#E29578",
        "header_color": "#D47A60",
        "jewelry": "Yellow Gold, Light Rose Gold, Polished Brass",
        "makeup": "Peach lip gloss, soft coral blush, champagne shimmer eyeshadow",
        "contrast": "Low to Medium contrast with luminous light tones",
        "neutrals": ["Ivory", "Soft Camel", "Warm Light Gray"],
        "avoid": ["Heavy Black", "Deep Charcoal", "Dark Burgundy", "Pure Cold White"],
        "colors": [
            {"name": "Peach Fuzz", "hex": "#FFBE98"},
            {"name": "Warm Coral", "hex": "#FF7F67"},
            {"name": "Buttercup Yellow", "hex": "#FFDE59"},
            {"name": "Soft Pistachio", "hex": "#B5E7A0"},
            {"name": "Light Aquamarine", "hex": "#7FE5D9"},
            {"name": "Golden Honey", "hex": "#F4C430"},
            {"name": "Apricot Shimmer", "hex": "#FBCEB1"},
            {"name": "Warm Turquoise", "hex": "#40E0D0"},
            {"name": "Periwinkle Warm", "hex": "#8C9EFF"},
            {"name": "Flamingo Pink", "hex": "#FC8EAC"},
            {"name": "Light Sage", "hex": "#BCCEB4"},
            {"name": "Creamy Ivory", "hex": "#FFFDD0"}
        ]
    },
    "Warm Spring": {
        "bg": "#FAF3E0",
        "accent": "#E65100",
        "header_color": "#BF360C",
        "jewelry": "Rich 18k Yellow Gold, Warm Bronze",
        "makeup": "Warm terracotta lipstick, warm amber blush, bronze eyeshadow",
        "contrast": "Medium contrast with golden vibrant undertones",
        "neutrals": ["Warm Chocolate", "Golden Camel", "Cream"],
        "avoid": ["Cool Fuchsia", "Icy Blue", "Charcoal Gray", "Pure Black"],
        "colors": [
            {"name": "Vibrant Poppy", "hex": "#FF4500"},
            {"name": "Golden Mango", "hex": "#FFB300"},
            {"name": "Warm Coral", "hex": "#FF6F59"},
            {"name": "Tropical Turquoise", "hex": "#00A896"},
            {"name": "Bright Lime", "hex": "#7CB342"},
            {"name": "Warm Terracotta", "hex": "#D84315"},
            {"name": "Saffron Yellow", "hex": "#F4C430"},
            {"name": "Warm Salmon Pink", "hex": "#FF8A65"},
            {"name": "Bright Teal", "hex": "#00897B"},
            {"name": "Golden Wheat", "hex": "#E5C158"},
            {"name": "Tangerine", "hex": "#F57C00"},
            {"name": "Olive Gold", "hex": "#9E9D24"}
        ]
    },
    "Bright Spring": {
        "bg": "#FFF8F0",
        "accent": "#FF1744",
        "header_color": "#D50000",
        "jewelry": "Bright High-Polish Yellow Gold, Clear Crystal",
        "makeup": "Bright coral-red lipstick, warm clear pink blush, luminous eyeshadow",
        "contrast": "High contrast with clear, striking warm colors",
        "neutrals": ["Clear Warm Black", "Ivory White", "Camel"],
        "avoid": ["Muted Gray", "Dusty Mauve", "Muddy Brown", "Washed-out Beige"],
        "colors": [
            {"name": "Electric Coral", "hex": "#FF3D00"},
            {"name": "Bright Turquoise", "hex": "#00E5FF"},
            {"name": "Canary Yellow", "hex": "#FFEA00"},
            {"name": "Hot Pink Warm", "hex": "#FF1744"},
            {"name": "Vibrant Emerald", "hex": "#00E676"},
            {"name": "Bright Poppy", "hex": "#F44336"},
            {"name": "Luminous Violet", "hex": "#651FFF"},
            {"name": "Sunny Marigold", "hex": "#FFC400"},
            {"name": "Clear Aqua", "hex": "#1DE9B6"},
            {"name": "Warm Tangerine", "hex": "#FF9100"},
            {"name": "Bright Fuchsia", "hex": "#F50057"},
            {"name": "Pure Warm White", "hex": "#FFFDF7"}
        ]
    },
    # SUMMER SUBSEASONS
    "Light Summer": {
        "bg": "#F4F7FB",
        "accent": "#5C6BC0",
        "header_color": "#3F51B5",
        "jewelry": "Sterline Silver, White Gold, Rose Quartz",
        "makeup": "Rose pink lip balm, soft mauve blush, cool lavender eyeshadow",
        "contrast": "Low contrast with delicate, cool light tones",
        "neutrals": ["Soft Blue-Gray", "Icy Gray", "Off-White"],
        "avoid": ["Warm Mustard", "Golden Orange", "Heavy Black", "Dark Espresso"],
        "colors": [
            {"name": "Soft Rose", "hex": "#FFB6C1"},
            {"name": "Sky Blue", "hex": "#87CEEB"},
            {"name": "Lavender Mist", "hex": "#E6E6FA"},
            {"name": "Cool Mint", "hex": "#A8E6CF"},
            {"name": "Dusty Pink", "hex": "#D8BFD8"},
            {"name": "Periwinkle", "hex": "#CCCCFF"},
            {"name": "Light Slate", "hex": "#778899"},
            {"name": "Soft Orchid", "hex": "#DA70D6"},
            {"name": "Powder Blue", "hex": "#B0E0E6"},
            {"name": "Icy Aqua", "hex": "#AFEEEE"},
            {"name": "Lilac Rose", "hex": "#C8A2C8"},
            {"name": "Pearl Gray", "hex": "#E5E8E8"}
        ]
    },
    "Cool Summer": {
        "bg": "#F0F4F8",
        "accent": "#1E88E5",
        "header_color": "#1565C0",
        "jewelry": "Bright Platinum, Polish Sterling Silver, Pearls",
        "makeup": "Cool berry pink lipstick, plum-rose blush, cool slate gray eyeshadow",
        "contrast": "Medium to High contrast with cool ocean & plum undertones",
        "neutrals": ["Cool Navy", "Charcoal Gray", "Crisp Cool White"],
        "avoid": ["Golden Yellow", "Warm Bronze", "Rust Orange", "Terracotta"],
        "colors": [
            {"name": "Classic Sapphire", "hex": "#0F52BA"},
            {"name": "Cool Raspberry", "hex": "#C2185B"},
            {"name": "Ocean Blue", "hex": "#1976D2"},
            {"name": "Deep Orchid", "hex": "#8E24AA"},
            {"name": "Plum Rose", "hex": "#880E4F"},
            {"name": "Cool Emerald", "hex": "#00796B"},
            {"name": "Cornflower Blue", "hex": "#64B5F6"},
            {"name": "Dusty Teal", "hex": "#00838F"},
            {"name": "Cool Mauve", "hex": "#7B1FA2"},
            {"name": "Soft Slate", "hex": "#546E7A"},
            {"name": "Icy Lavender", "hex": "#D1C4E9"},
            {"name": "Pure Silver Gray", "hex": "#90A4AE"}
        ]
    },
    "Soft Summer": {
        "bg": "#F5F5F7",
        "accent": "#6D4C41",
        "header_color": "#4E342E",
        "jewelry": "Muted Antique Silver, Brushed Pewter, Soft Rose Gold",
        "makeup": "Dusty rose lip color, muted berry blush, smoky taupe eyeshadow",
        "contrast": "Low to Medium contrast with muted smoky cool tones",
        "neutrals": ["Smoky Quartz", "Muted Navy", "Soft Charcoal"],
        "avoid": ["Electric Neon Colors", "Bright Orange", "Vibrant Yellow", "Pure Scarlet Red"],
        "colors": [
            {"name": "Dusty Rose", "hex": "#D4A5A5"},
            {"name": "Sage Green", "hex": "#8A9A86"},
            {"name": "Smoky Blue", "hex": "#6B8E23"},
            {"name": "Soft Plum", "hex": "#705335"},
            {"name": "Muted Teal", "hex": "#4A7C59"},
            {"name": "Taupe Gray", "hex": "#8B8589"},
            {"name": "Dusty Lavender", "hex": "#AC92EC"},
            {"name": "Muted Cocoa", "hex": "#795548"},
            {"name": "Soft Denim", "hex": "#5C6BC0"},
            {"name": "Rosewood", "hex": "#9E2A2B"},
            {"name": "Cool Olive", "hex": "#556B2F"},
            {"name": "Seafoam Muted", "hex": "#73A9AD"}
        ]
    },
    # AUTUMN SUBSEASONS
    "Soft Autumn": {
        "bg": "#FAF5EF",
        "accent": "#8D6E63",
        "header_color": "#5D4037",
        "jewelry": "Brushed Antique Gold, Matte Brass, Copper",
        "makeup": "Warm dusty rose lip, muted peach blush, warm taupe/gold eyeshadow",
        "contrast": "Low to Medium contrast with warm earthy muted tones",
        "neutrals": ["Muted Camel", "Warm Taupe", "Soft Cream"],
        "avoid": ["Vibrant Fuchsia", "Neon Yellow", "Stark Cold Black", "Electric Blue"],
        "colors": [
            {"name": "Soft Terracotta", "hex": "#C06C84"},
            {"name": "Warm Sage", "hex": "#99B898"},
            {"name": "Golden Taupe", "hex": "#AF8D6A"},
            {"name": "Muted Apricot", "hex": "#F8B195"},
            {"name": "Olive Green", "hex": "#6C7A89"},
            {"name": "Soft Rust", "hex": "#B85B56"},
            {"name": "Dusty Turquoise", "hex": "#6C5B7B"},
            {"name": "Warm Rosewood", "hex": "#A8605D"},
            {"name": "Sand Dune", "hex": "#D1A784"},
            {"name": "Warm Khaki", "hex": "#8B8742"},
            {"name": "Honey Bronze", "hex": "#C29B38"},
            {"name": "Soft Forest", "hex": "#4A6B5D"}
        ]
    },
    "Warm Autumn": {
        "bg": "#FCF5EB",
        "accent": "#D84315",
        "header_color": "#BF360C",
        "jewelry": "Rich 24k Yellow Gold, Polished Copper, Amber",
        "makeup": "Warm copper/brick lipstick, warm cinnamon blush, golden brown eyeshadow",
        "contrast": "Medium to High contrast with rich golden earthy warmth",
        "neutrals": ["Deep Chocolate Brown", "Rich Golden Camel", "Warm Cream"],
        "avoid": ["Icy Blue", "Cool Fuchsia", "Silver Gray", "Stark White"],
        "colors": [
            {"name": "Spiced Rust", "hex": "#D35400"},
            {"name": "Mustard Yellow", "hex": "#E67E22"},
            {"name": "Deep Olive", "hex": "#27AE60"},
            {"name": "Burnt Orange", "hex": "#E65100"},
            {"name": "Warm Pumpkin", "hex": "#F39C12"},
            {"name": "Forest Moss", "hex": "#1E8449"},
            {"name": "Copper Bronze", "hex": "#B7950B"},
            {"name": "Cinnamon Brown", "hex": "#7E5109"},
            {"name": "Warm Burgundy", "hex": "#922B21"},
            {"name": "Warm Teal", "hex": "#117864"},
            {"name": "Golden Ochre", "hex": "#D4AC0D"},
            {"name": "Terracotta Brick", "hex": "#A04000"}
        ]
    },
    "Dark Autumn": {
        "bg": "#FAF3EC",
        "accent": "#4E342E",
        "header_color": "#3E2723",
        "jewelry": "Dark Antique Gold, Burnished Bronze, Heavy Copper",
        "makeup": "Deep berry red lipstick, rich bronzer blush, deep chocolate eyeshadow",
        "contrast": "High contrast with dark, deep warm tones",
        "neutrals": ["Deep Espresso Brown", "Dark Warm Olive", "Rich Cream"],
        "avoid": ["Light Pastel Pink", "Icy Lavender", "Pale Mint", "Dusty Gray"],
        "colors": [
            {"name": "Deep Mahogany", "hex": "#4A154B"},
            {"name": "Spiced Chestnut", "hex": "#6E2C00"},
            {"name": "Dark Forest Green", "hex": "#145A32"},
            {"name": "Deep Auburn", "hex": "#7B1FA2"},
            {"name": "Rich Plum Warm", "hex": "#512DA8"},
            {"name": "Dark Rust", "hex": "#900C3F"},
            {"name": "Golden Espresso", "hex": "#3E2723"},
            {"name": "Deep Teal", "hex": "#004D40"},
            {"name": "Midnight Warm Blue", "hex": "#1A237E"},
            {"name": "Burnished Orange", "hex": "#D84315"},
            {"name": "Rich Mustard", "hex": "#F57F17"},
            {"name": "Deep Wine", "hex": "#581845"}
        ]
    },
    # WINTER SUBSEASONS
    "Dark Winter": {
        "bg": "#F4F6F9",
        "accent": "#263238",
        "header_color": "#1A237E",
        "jewelry": "Heavy Platinum, High-Polish White Gold, Hematite",
        "makeup": "Deep wine red lipstick, cool plum blush, deep charcoal eyeshadow",
        "contrast": "High contrast with deep, dark cool tones",
        "neutrals": ["Pure Obsidian Black", "Midnight Blue", "Icy White"],
        "avoid": ["Golden Orange", "Warm Mustard", "Camel Brown", "Peach"],
        "colors": [
            {"name": "Pure Black", "hex": "#000000"},
            {"name": "Midnight Navy", "hex": "#0D47A1"},
            {"name": "Deep Crimson", "hex": "#B71C1C"},
            {"name": "Emerald Green", "hex": "#004D40"},
            {"name": "Imperial Violet", "hex": "#4A148C"},
            {"name": "Charcoal Gray", "hex": "#263238"},
            {"name": "Royal Pine", "hex": "#00695C"},
            {"name": "Deep Burgundy", "hex": "#880E4F"},
            {"name": "Icy Violet", "hex": "#E1BEE7"},
            {"name": "Deep Plum", "hex": "#311B92"},
            {"name": "Cold Slate", "hex": "#455A64"},
            {"name": "Crisp Pure White", "hex": "#FFFFFF"}
        ]
    },
    "Cool Winter": {
        "bg": "#F0F4F8",
        "accent": "#0D47A1",
        "header_color": "#01579B",
        "jewelry": "Bright High-Polish Silver, Platinum, Diamonds",
        "makeup": "Cool true red / magenta lipstick, cool pink blush, silver-gray eyeshadow",
        "contrast": "Very High contrast with vivid cool icy undertones",
        "neutrals": ["Pure Cold Black", "Icy Silver", "Crisp Pure White"],
        "avoid": ["Golden Brown", "Bronze", "Orange", "Warm Mustard", "Rust"],
        "colors": [
            {"name": "Royal Sapphire", "hex": "#1565C0"},
            {"name": "True Ruby Red", "hex": "#D50000"},
            {"name": "Bright Fuchsia", "hex": "#C51162"},
            {"name": "Icy Blue", "hex": "#80D8FF"},
            {"name": "Cold Emerald", "hex": "#00BFA5"},
            {"name": "Deep Magenta", "hex": "#AA00FF"},
            {"name": "Steel Gray", "hex": "#37474F"},
            {"name": "Bright Cobalt", "hex": "#2979FF"},
            {"name": "Icy Pink", "hex": "#FF80AB"},
            {"name": "Pure White", "hex": "#FFFFFF"},
            {"name": "Electric Indigo", "hex": "#304FFE"},
            {"name": "Midnight Black", "hex": "#121212"}
        ]
    },
    "Bright Winter": {
        "bg": "#F8F9FA",
        "accent": "#D500F9",
        "header_color": "#AA00FF",
        "jewelry": "Bright High-Polish Platinum, Clear Crystals, Diamond",
        "makeup": "Vivid magenta red lipstick, bright cool pink blush, luminous eyeshadow",
        "contrast": "Maximum contrast with electrifying cool vivid tones",
        "neutrals": ["Blackest Black", "Icy White", "Cool Granite"],
        "avoid": ["Muted Earthy Brown", "Dusty Khaki", "Warm Beige", "Muddy Olive"],
        "colors": [
            {"name": "Electric Fuchsia", "hex": "#F50057"},
            {"name": "Vibrant Cyan", "hex": "#00E5FF"},
            {"name": "Bright Magenta", "hex": "#D500F9"},
            {"name": "Acid Lime Cool", "hex": "#76FF03"},
            {"name": "Pure Scarlett", "hex": "#FF1744"},
            {"name": "Bright Electric Blue", "hex": "#2979FF"},
            {"name": "Icy Aqua", "hex": "#1DE9B6"},
            {"name": "Shocking Pink", "hex": "#FF4081"},
            {"name": "Vibrant Violet", "hex": "#651FFF"},
            {"name": "Crisp White", "hex": "#FFFFFF"},
            {"name": "Jet Black", "hex": "#0A0A0A"},
            {"name": "Bright Emerald", "hex": "#00E676"}
        ]
    }
}

# Fallback seasonal mapping if subseason is generic
GENERIC_SEASON_MAP = {
    "Spring": "Warm Spring",
    "Summer": "Cool Summer",
    "Autumn": "Warm Autumn",
    "Winter": "Cool Winter"
}

def get_palette_data(season: str, sub_season: str) -> dict:
    """Helper to retrieve palette data matching sub_season or season fallback."""
    if sub_season in SUBSEASON_PALETTES:
        return SUBSEASON_PALETTES[sub_season]
    elif season in SUBSEASON_PALETTES:
        return SUBSEASON_PALETTES[season]
    elif season in GENERIC_SEASON_MAP:
        return SUBSEASON_PALETTES[GENERIC_SEASON_MAP[season]]
    else:
        return SUBSEASON_PALETTES["Warm Spring"]

import base64

def get_base64_image(image_path: str) -> str:
    """Encodes an image file as a base64 data URI for reliable PDF rendering."""
    if not os.path.exists(image_path):
        return ""
    mime_type = "image/png" if image_path.lower().endswith(".png") else "image/jpeg"
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"

from PIL import Image, ImageOps

def ensure_upright_image(image_path: str) -> str:
    """Corrects EXIF orientation so the client face is always standing upright."""
    if not os.path.exists(image_path):
        return image_path
    try:
        img = Image.open(image_path)
        img = ImageOps.exif_transpose(img)
        out_dir = os.path.dirname(os.path.abspath(image_path))
        upright_path = os.path.join(out_dir, "_upright_" + os.path.basename(image_path))
        if not upright_path.lower().endswith((".png", ".jpg", ".jpeg")):
            upright_path += ".png"
        img.save(upright_path)
        return upright_path
    except Exception as e:
        print(f"Orientation fix note: {e}")
        return image_path

import cv2
import numpy as np

def crop_face_only(image_path: str) -> str:
    """Detects face and crops tightly to ONLY the face and hair (removing shoulders, neck, and clothing)."""
    if not os.path.exists(image_path):
        return image_path
    try:
        cv_img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if cv_img is None:
            return image_path
            
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        
        _CASCADE_DIR = cv2.data.haarcascades
        _FACE_CASCADE = cv2.CascadeClassifier(_CASCADE_DIR + "haarcascade_frontalface_default.xml")
        faces = _FACE_CASCADE.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
        
        if len(faces) == 0:
            return image_path
            
        faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
        (fx, fy, fw, fh) = faces[0]
        
        # Calculate tight face+hair crop box (margin: 40% top for hair, 20% sides, 8% bottom for chin)
        h_img, w_img = gray.shape[:2]
        crop_top = max(0, int(fy - fh * 0.40))
        crop_bottom = min(h_img, int(fy + fh * 1.08))
        crop_left = max(0, int(fx - fw * 0.25))
        crop_right = min(w_img, int(fx + fw * 1.25))
        
        cropped_cv = cv_img[crop_top:crop_bottom, crop_left:crop_right]
        
        out_dir = os.path.dirname(os.path.abspath(image_path))
        face_only_path = os.path.join(out_dir, "_face_only_" + os.path.basename(image_path))
        if not face_only_path.lower().endswith((".png", ".jpg", ".jpeg")):
            face_only_path += ".png"
            
        cv2.imwrite(face_only_path, cropped_cv)
        return face_only_path
    except Exception as e:
        print(f"Face crop note: {e}")
        return image_path

def generate_pdf(image_path: str, analysis_data: dict, output_pdf_path: str, client_name: str = "Valued Client") -> str:
    """
    Generates a multi-page PDF report based on the color analysis data.
    Uses Microsoft Edge Headless or WeasyPrint for pixel-perfect PDF output.
    """
    # 1. Ensure client photo is upright
    image_path = ensure_upright_image(image_path)
    
    # 2. Crop tightly to face & hair (removing shoulders/neck/clothing)
    image_path = crop_face_only(image_path)
    
    # 3. Ensure 100% transparent background cutout
    try:
        from background_remover import remove_background
        temp_cutout = output_pdf_path.replace('.pdf', '_bg_cutout.png')
        remove_background(image_path, temp_cutout)
        if os.path.exists(temp_cutout) and os.path.getsize(temp_cutout) > 1000:
            image_path = temp_cutout
    except Exception as bg_err:
        print(f"Background removal note: {bg_err}")
    
    season = analysis_data.get('season', 'Spring') or 'Spring'
    sub_season = analysis_data.get('sub_season', season) or season
    metrics = analysis_data.get('color_metrics', {
        'warmth_score': 0.0, 'contrast_score': 0.0, 'overall_value': 0.0, 'ita_degrees': 0.0
    })
    
    palette_info = get_palette_data(season, sub_season)
    
    out_dir = os.path.dirname(output_pdf_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(os.path.join(current_dir, 'templates')))
    template = env.get_template('report.html')
    
    # Base64 encode image for 100% reliable PDF embedding
    base64_img = get_base64_image(image_path)
    if not base64_img:
        abs_img_path = f"file:///{os.path.abspath(image_path).replace(chr(92), '/')}"
    else:
        abs_img_path = base64_img
    
    ita_val = metrics.get('ita_degrees', 0.0)
    if ita_val > 55.0:
        ita_category = "Very Light (ITA° > 55°)"
    elif ita_val > 41.0:
        ita_category = "Light / Fair (ITA° 41° - 55°)"
    elif ita_val > 28.0:
        ita_category = "Intermediate (ITA° 28° - 41°)"
    elif ita_val > 10.0:
        ita_category = "Tan (ITA° 10° - 28°)"
    elif ita_val > -30.0:
        ita_category = "Brown / Dark (ITA° -30° - 10°)"
    else:
        ita_category = "Very Dark (ITA° < -30°)"

    skin_lab_dict = metrics.get('skin_lab', {'L': 65.0, 'a': 12.0, 'b': 18.0})

    html_out = template.render(
        client_name=client_name,
        season=season,
        sub_season=sub_season,
        image_path=abs_img_path,
        metrics=metrics,
        ita_category=ita_category,
        skin_lab=skin_lab_dict,
        season_bg_color=palette_info["bg"],
        accent_color=palette_info["accent"],
        header_color=palette_info["header_color"],
        jewelry=palette_info["jewelry"],
        makeup=palette_info["makeup"],
        contrast=palette_info["contrast"],
        neutrals=palette_info["neutrals"],
        avoid_colors=palette_info["avoid"],
        palette=palette_info["colors"]
    )
    
    # 1. Try Microsoft Edge Headless PDF rendering on Windows (Pixel Perfect)
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if not os.path.exists(edge_path):
        edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
        
    if os.path.exists(edge_path):
        try:
            temp_html = output_pdf_path.replace(".pdf", "_temp.html")
            with open(temp_html, "w", encoding="utf-8") as f:
                f.write(html_out)
                
            html_url = "file:///" + os.path.abspath(temp_html).replace("\\", "/")
            cmd = [
                edge_path,
                "--headless=new",
                f"--print-to-pdf={output_pdf_path}",
                "--no-pdf-header-footer",
                "--print-to-pdf-no-header",
                html_url
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
            if os.path.exists(temp_html):
                try: os.remove(temp_html)
                except: pass
                
            if os.path.exists(output_pdf_path) and os.path.getsize(output_pdf_path) > 1000:
                print(f"Generated pixel-perfect PDF via Headless Edge: {output_pdf_path}")
                return output_pdf_path
        except Exception as edge_err:
            print(f"Headless Edge PDF fallback error: {edge_err}")

    # 2. Try WeasyPrint
    try:
        from weasyprint import HTML
        HTML(string=html_out, base_url=current_dir).write_pdf(output_pdf_path)
        print(f"Generated PDF report via WeasyPrint at: {output_pdf_path}")
        return output_pdf_path
    except Exception as e:
        # 3. Fallback to HTML
        print("Saving HTML report fallback.")
        html_path = output_pdf_path.replace(".pdf", ".html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_out)
        return html_path

