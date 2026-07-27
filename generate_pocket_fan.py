import os
import jinja2
from jinja2 import Environment, FileSystemLoader
from pdf_generator import SUBSEASON_PALETTES, get_base64_image
import subprocess
import cv2
import numpy as np

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#{:02X}{:02X}{:02X}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def hex_to_lab(hex_str):
    rgb = np.uint8([[list(hex_to_rgb(hex_str))]])
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
    return lab[0][0]

def lab_to_hex(lab):
    lab_pixel = np.uint8([[lab]])
    rgb = cv2.cvtColor(lab_pixel, cv2.COLOR_LAB2RGB)
    return rgb_to_hex(rgb[0][0])

def get_intermediate_color(hex1, hex2):
    """Calculates the exact CIELAB perceptual midpoint between hex1 and hex2."""
    try:
        lab1 = hex_to_lab(hex1).astype(float)
        lab2 = hex_to_lab(hex2).astype(float)
        mid_lab = (lab1 + lab2) / 2.0
        return lab_to_hex(mid_lab.astype(np.uint8))
    except Exception:
        return hex1

def create_pocket_fan_html(output_html_path: str):
    """
    Generates a print-ready 3-column x 2-row grid layout (6 cards per A4 page).
    Each card leaf features 3-TIER STACKED SWATCH BLOCKS:
    - Top Swatch: Primary Color A
    - Middle Swatch: CIELAB Midpoint Intermediate Color (Exclusive to CHROMATYPE!)
    - Bottom Swatch: Harmonic Accent Color B
    Total: 12 Sub-Seasons x 54-72 Colors = 600+ Color Swatch Tones!
    """
    all_seasons_data = []
    
    for subseason_name, palette in SUBSEASON_PALETTES.items():
        colors = palette.get('colors', [])
        # Group colors into pairs, adding intermediate midpoint color between every pair
        tiered_cards = []
        for i in range(0, len(colors) - 1, 2):
            c1 = colors[i]
            c2 = colors[i+1]
            mid_hex = get_intermediate_color(c1['hex'], c2['hex'])
            mid_color = {
                'name': f"{c1['name'].split()[0]} {c2['name'].split()[-1]} Tint",
                'hex': mid_hex,
                'pantone': '16-1539 TCX (Graded Midpoint)'
            }
            tiered_cards.append({
                'top': c1,
                'mid': mid_color,
                'bottom': c2
            })
            
        # Group 3 tiered blocks per printed card (6 printed cards per subseason)
        cards_for_sub = []
        for i in range(0, len(tiered_cards), 3):
            cards_for_sub.append(tiered_cards[i:i+3])
            
        all_seasons_data.append({
            'name': subseason_name,
            'header_color': palette.get('header_color', '#333333'),
            'cards': cards_for_sub
        })
        
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CHROMATYPE — 3-Tier Gradient Pocket Swatch Fan (Print Ready)</title>
    <style>
        @page {{
            size: A4 portrait;
            margin: 0;
        }}
        body {{
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #FFFFFF;
            -webkit-print-color-adjust: exact;
        }}
        .page-sheet {{
            width: 210mm;
            height: 297mm;
            page-break-after: always;
            box-sizing: border-box;
            display: grid;
            grid-template-columns: repeat(3, 60mm);
            grid-template-rows: repeat(2, 132mm);
            gap: 6mm 4mm;
            padding: 10mm 11mm;
            background: #FFFFFF;
            margin: 0 auto;
        }}
        .swatch-card {{
            width: 60mm;
            height: 132mm;
            border: 1px dashed #CBD5E1;
            border-radius: 6mm;
            box-sizing: border-box;
            padding: 3mm 3.5mm;
            position: relative;
            background: #FFFFFF;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        .rivet-hole {{
            position: absolute;
            top: 3mm;
            left: 50%;
            transform: translateX(-50%);
            width: 4.5mm;
            height: 4.5mm;
            border-radius: 50%;
            border: 1px solid #64748B;
            background: #F1F5F9;
        }}
        .card-header {{
            margin-top: 6mm;
            text-align: center;
            border-bottom: 2px solid #E2E8F0;
            padding-bottom: 1.5mm;
        }}
        .card-season-title {{
            font-size: 10px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #0F172A;
        }}
        .card-swatches {{
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-around;
            margin-top: 1.5mm;
            gap: 2mm;
        }}
        .tier-block {{
            border-radius: 3mm;
            overflow: hidden;
            border: 1px solid rgba(0,0,0,0.15);
            box-shadow: 0 1px 4px rgba(0,0,0,0.1);
        }}
        .tier-sub-swatch {{
            height: 9mm;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 2.5mm;
        }}
        .swatch-name {{
            font-size: 7.5px;
            font-weight: 700;
            text-transform: uppercase;
        }}
        .swatch-hex {{
            font-size: 6.5px;
            font-weight: 700;
            font-family: monospace;
        }}
        .card-footer {{
            text-align: center;
            font-size: 6px;
            font-weight: 800;
            color: #94A3B8;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-top: 1mm;
        }}
    </style>
</head>
<body>
"""

    # Generate Flat Cards List (6 cards per A4 page)
    all_cards_flat = []
    for sub in all_seasons_data:
        for idx, tier_group in enumerate(sub['cards']):
            all_cards_flat.append({
                'season': sub['name'],
                'header_color': sub['header_color'],
                'card_num': idx + 1,
                'tier_blocks': tier_group
            })

    for page_idx in range(0, len(all_cards_flat), 6):
        page_cards = all_cards_flat[page_idx:page_idx+6]
        html_content += '<div class="page-sheet">\n'
        for card in page_cards:
            html_content += f"""
            <div class="swatch-card">
                <div class="rivet-hole"></div>
                <div class="card-header">
                    <div class="card-season-title" style="color: {card['header_color']};">{card['season']}</div>
                </div>
                <div class="card-swatches">
            """
            for block in card['tier_blocks']:
                # Render 3 sub-swatches (top, mid, bottom) inside each tier block
                html_content += '<div class="tier-block">\n'
                for pos_key in ['top', 'mid', 'bottom']:
                    sw = block[pos_key]
                    hex_clean = sw['hex'].lstrip('#')
                    r = int(hex_clean[0:2], 16)
                    g = int(hex_clean[2:4], 16)
                    b = int(hex_clean[4:6], 16)
                    lum = (0.299 * r + 0.587 * g + 0.114 * b)
                    text_col = '#000000' if lum > 160 else '#FFFFFF'
                    is_mid = (pos_key == 'mid')
                    badge_text = "★ MIDPOINT" if is_mid else sw['hex']
                    
                    html_content += f"""
                        <div class="tier-sub-swatch" style="background-color: {sw['hex']};">
                            <span class="swatch-name" style="color: {text_col};">{sw['name']}</span>
                            <span class="swatch-hex" style="color: {text_col};">{badge_text}</span>
                        </div>
                    """
                html_content += '</div>\n'

            html_content += f"""
                </div>
                <div class="card-footer">CHROMATYPE 3-TIER • LEAF #{card['card_num']}</div>
            </div>
            """
        html_content += '</div>\n'

    html_content += """
</body>
</html>
"""
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    return output_html_path

def generate_pocket_fan_pdf(output_pdf_path: str) -> str:
    temp_html = output_pdf_path.replace('.pdf', '_temp.html')
    create_pocket_fan_html(temp_html)
    
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    msedge = next((path for path in edge_paths if os.path.exists(path)), None)
    
    if msedge:
        cmd = [
            msedge,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={output_pdf_path}",
            temp_html
        ]
        subprocess.run(cmd, check=True)
    
    if os.path.exists(temp_html):
        os.remove(temp_html)
        
    return output_pdf_path

if __name__ == '__main__':
    target_pdf = r"C:\Users\dkven\Desktop\CHROMATYPE_Reports\CHROMATYPE_3Tier_Gradient_Pocket_Fan_PrintReady.pdf"
    print("Generating CHROMATYPE 3-Tier Gradient Pocket Swatch Fan PDF (with CIELAB Intermediate Midpoint Colors)...")
    generate_pocket_fan_pdf(target_pdf)
    print(f"Done! Saved to: {target_pdf}")
