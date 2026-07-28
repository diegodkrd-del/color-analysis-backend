import os
import re

pdf_gen_path = r'C:\Users\dkven\color_analysis_backend\pdf_generator.py'
with open(pdf_gen_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Formula Audit and Fix in pdf_generator.py
# Standardize metrics:
# 1. ITA° = arctan((L* - 50) / b*) * (180 / pi)
# 2. Warmth Index = b* / a* (Yellow-to-Red ratio: >1.0 = Warm Golden, <1.0 = Cool Rosy)
# 3. Chroma C* = sqrt(a*^2 + b*^2)
# 4. Contrast Delta = (L*_skin - L*_hair) / 10

cielab_math_fix = """
import math

def calculate_cielab_dermatology_metrics(L, a, b, L_hair=25.0):
    \"\"\"
    Clinically accurate dermatological skin-tone classification (Chardon et al.)
    \"\"\"
    # 1. ITA° (Individual Typology Angle)
    b_val = b if b != 0 else 0.001
    ita_rad = math.atan((L - 50.0) / b_val)
    ita_deg = ita_rad * (180.0 / math.pi)

    # 2. Warmth Index (b*/a* Yellow-to-Red ratio)
    a_val = a if a != 0 else 0.001
    warmth_index = round(b / a_val, 2)

    # 3. Chroma C* (Color Saturation / Vividness)
    chroma = round(math.sqrt(a**2 + b**2), 2)

    # 4. Hue Angle h° in degrees
    hue_rad = math.atan2(b, a)
    hue_deg = round((hue_rad * (180.0 / math.pi)) % 360.0, 1)

    # 5. Contrast Level (L*_skin - L*_hair luminance delta)
    contrast_level = round(abs(L - L_hair) / 10.0, 2)

    # Dermatological ITA Skin Category (Chardon Scale)
    if ita_deg > 55.0:
        ita_category = "Very Light"
    elif ita_deg > 41.0:
        ita_category = "Light"
    elif ita_deg > 28.0:
        ita_category = "Intermediate"
    elif ita_deg > 10.0:
        ita_category = "Tan"
    elif ita_deg > -30.0:
        ita_category = "Brown"
    else:
        ita_category = "Dark"

    return {
        'ITA': round(ita_deg, 1),
        'ITA_Category': ita_category,
        'Warmth_Index': warmth_index,
        'Chroma': chroma,
        'Hue_Angle': hue_deg,
        'Contrast_Level': contrast_level
    }
"""

if 'def calculate_cielab_dermatology_metrics' not in code:
    code += "\n\n" + cielab_math_fix
    with open(pdf_gen_path, 'w', encoding='utf-8') as f:
        f.write(code)

print("Updated CIELAB dermatological metrics math in pdf_generator.py successfully!")
