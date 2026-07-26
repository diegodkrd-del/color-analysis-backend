import os
import jinja2
from jinja2 import Environment, FileSystemLoader
from pdf_generator import SUBSEASON_PALETTES, get_base64_image
import subprocess

def create_pocket_fan_html(output_html_path: str):
    """
    Generates a print-ready Pocket Swatch Fan HTML containing all 12 sub-seasons x 36 colors = 432 swatches.
    Formatted as slim vertical cards (60mm x 180mm) with rivet hole guidelines for printing and laminating.
    """
    all_seasons_data = []
    
    for subseason_name, palette in SUBSEASON_PALETTES.items():
        colors = palette.get('colors', [])
        # Group colors into cards of 6 swatches per card (6 swatches x 6 cards = 36 colors per subseason)
        cards = []
        for i in range(0, len(colors), 6):
            cards.append(colors[i:i+6])
            
        all_seasons_data.append({
            'name': subseason_name,
            'header_color': palette.get('header_color', '#333333'),
            'accent_color': palette.get('accent', '#E29578'),
            'bg_color': palette.get('bg', '#FFFFFF'),
            'cards': cards
        })
        
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CHROMATYPE — Print-Ready 12-Season Pocket Swatch Fan</title>
    <style>
        @page {{
            size: A4 portrait;
            margin: 10mm;
        }}
        body {{
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #F8FAFC;
            -webkit-print-color-adjust: exact;
        }}
        .page-sheet {{
            width: 190mm;
            height: 277mm;
            page-break-after: always;
            box-sizing: border-box;
            display: flex;
            flex-wrap: wrap;
            align-content: flex-start;
            gap: 5mm;
            padding: 5mm;
            background: #FFFFFF;
            margin: 0 auto;
        }}
        .swatch-card {{
            width: 58mm;
            height: 125mm;
            border: 1px dashed #CBD5E1;
            border-radius: 8mm;
            box-sizing: border-box;
            padding: 4mm;
            position: relative;
            background: #FFFFFF;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        .rivet-hole {{
            position: absolute;
            top: 4mm;
            left: 50%;
            transform: translateX(-50%);
            width: 5mm;
            height: 5mm;
            border-radius: 50%;
            border: 1px solid #94A3B8;
            background: #F1F5F9;
        }}
        .card-header {{
            margin-top: 7mm;
            text-align: center;
            border-bottom: 2px solid #E2E8F0;
            padding-bottom: 2mm;
        }}
        .card-season-title {{
            font-size: 11px;
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
            margin-top: 2mm;
        }}
        .swatch-item {{
            height: 12mm;
            border-radius: 3mm;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 3mm;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .swatch-name {{
            font-size: 8px;
            font-weight: 700;
            text-transform: uppercase;
            text-shadow: 0 1px 2px rgba(0,0,0,0.4);
            color: #FFFFFF;
        }}
        .swatch-hex {{
            font-size: 7px;
            font-weight: 600;
            font-family: monospace;
            text-shadow: 0 1px 2px rgba(0,0,0,0.4);
            color: #FFFFFF;
        }}
        .card-footer {{
            text-align: center;
            font-size: 6.5px;
            font-weight: 700;
            color: #94A3B8;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-top: 1mm;
        }}
    </style>
</head>
<body>
"""

    # Generate Pages (3 cards per row x 2 rows = 6 cards per A4 page)
    all_cards_flat = []
    for sub in all_seasons_data:
        for idx, card_colors in enumerate(sub['cards']):
            all_cards_flat.append({
                'season': sub['name'],
                'header_color': sub['header_color'],
                'card_num': idx + 1,
                'colors': card_colors
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
            for sw in card['colors']:
                # Decide text color based on luminance
                hex_clean = sw['hex'].lstrip('#')
                r = int(hex_clean[0:2], 16)
                g = int(hex_clean[2:4], 16)
                b = int(hex_clean[4:6], 16)
                lum = (0.299 * r + 0.587 * g + 0.114 * b)
                text_col = '#000000' if lum > 160 else '#FFFFFF'

                html_content += f"""
                    <div class="swatch-item" style="background-color: {sw['hex']};">
                        <span class="swatch-name" style="color: {text_col}; text-shadow: none;">{sw['name']}</span>
                        <span class="swatch-hex" style="color: {text_col}; text-shadow: none;">{sw['hex']}</span>
                    </div>
                """
            html_content += f"""
                </div>
                <div class="card-footer">CHROMATYPE • POCKET FAN #{card['card_num']}</div>
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
    target_pdf = r"C:\Users\dkven\Desktop\CHROMATYPE_Reports\CHROMATYPE_Pocket_Color_Fan_12Seasons_PrintReady.pdf"
    print("Generating Print-Ready Pocket Swatch Fan PDF...")
    generate_pocket_fan_pdf(target_pdf)
    print(f"Done! Saved to: {target_pdf}")
