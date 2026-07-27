import os
import cv2
import numpy as np
from pdf_generator import generate_pdf, crop_face_only, SUBSEASON_PALETTES

photo1_path = r'C:\Users\dkven\.gemini\antigravity\brain\df9e8416-acff-4abf-943f-408e96928da4\.user_uploaded\media__1785148866791.jpg'
photo2_path = r'C:\Users\dkven\.gemini\antigravity\brain\df9e8416-acff-4abf-943f-408e96928da4\.user_uploaded\media__1785148866826.jpg'

def analyze_photo(image_path):
    # Pass image_path to crop_face_only
    cropped_face_path = crop_face_only(image_path)
    face = cv2.imread(cropped_face_path)
    if face is None:
        face = cv2.imread(image_path)
        
    lab = cv2.cvtColor(face, cv2.COLOR_BGR2LAB)
    
    # Calculate average L*, a*, b* in central facial region
    h, w, _ = lab.shape
    sample_area = lab[int(h*0.3):int(h*0.7), int(w*0.3):int(w*0.7)]
    
    L_val = np.mean(sample_area[:, :, 0]) * (100.0 / 255.0)
    a_val = np.mean(sample_area[:, :, 1]) - 128.0
    b_val = np.mean(sample_area[:, :, 2]) - 128.0
    
    # Calculate ITA° Angle: ITA = (arctan((L* - 50)/b*) * 180) / pi
    if b_val != 0:
        ita = (np.arctan((L_val - 50.0) / b_val) * 180.0) / np.pi
    else:
        ita = 50.0
        
    # Determine Warmth & Sub-Season
    if b_val > 10.0:
        if L_val < 55.0:
            sub_season = 'Dark Autumn'
            season = 'Autumn'
        else:
            sub_season = 'Warm Autumn'
            season = 'Autumn'
    else:
        if L_val < 50.0:
            sub_season = 'Dark Winter'
            season = 'Winter'
        else:
            sub_season = 'Cool Winter'
            season = 'Winter'
            
    metrics = {
        'season': season,
        'sub_season': sub_season,
        'color_metrics': {
            'warmth_score': round((b_val - 10.0) / 10.0, 2),
            'contrast_score': round(abs(L_val - 50.0) / 50.0, 2),
            'overall_value': round(L_val / 100.0, 2),
            'ita_degrees': round(ita, 1),
            'skin_lab': {'L': round(L_val, 1), 'a': round(a_val, 1), 'b': round(b_val, 1)}
        }
    }
    return metrics

print("=== CHROMATYPE CIELAB OPTICAL ANALYSIS RESULTS ===")
res1 = analyze_photo(photo1_path)
print(f"PHOTO 1 -> Sub-Season: {res1['sub_season']} | ITA°: {res1['color_metrics']['ita_degrees']}° | L*: {res1['color_metrics']['skin_lab']['L']}, a*: {res1['color_metrics']['skin_lab']['a']}, b*: {res1['color_metrics']['skin_lab']['b']}")

res2 = analyze_photo(photo2_path)
print(f"PHOTO 2 -> Sub-Season: {res2['sub_season']} | ITA°: {res2['color_metrics']['ita_degrees']}° | L*: {res2['color_metrics']['skin_lab']['L']}, a*: {res2['color_metrics']['skin_lab']['a']}, b*: {res2['color_metrics']['skin_lab']['b']}")

out_pdf1 = r'C:\Users\dkven\Desktop\CHROMATYPE_Reports\CHROMATYPE_Client_Test_Photo1.pdf'
out_pdf2 = r'C:\Users\dkven\Desktop\CHROMATYPE_Reports\CHROMATYPE_Client_Test_Photo2.pdf'

print("\nGenerating Master PDF Report for Photo 1...")
generate_pdf(photo1_path, res1, out_pdf1, client_name='Client Test (Photo 1)')

print("Generating Master PDF Report for Photo 2...")
generate_pdf(photo2_path, res2, out_pdf2, client_name='Client Test (Photo 2)')

print("\nDone! Both reports generated successfully.")
