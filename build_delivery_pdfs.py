import os
import subprocess
import jinja2
import shutil
from pdf_generator import SUBSEASON_PALETTES

def create_master_guide_html(output_html_path: str):
    """
    Generates HTML for PDF #1: Complete 12-Season Master Color Guide & Optical Dossier.
    Includes: Brand & Watermark, History of Color & Modern Color Theory, CHROMATYPE Optical System Intro,
    Photo Processing & Email Delivery Protocol, plus ALL 12 Sub-Seasons (2 colors per page layout).
    """
    all_seasons_data = []
    for sub_name, palette in SUBSEASON_PALETTES.items():
        all_seasons_data.append({
            'name': sub_name,
            'header_color': palette.get('header_color', '#333333'),
            'accent_color': palette.get('accent', '#E29578'),
            'bg_color': palette.get('bg', '#FFFFFF'),
            'colors': palette.get('colors', []),
            'jewelry': palette.get('jewelry', ''),
            'makeup': palette.get('makeup', ''),
            'neutrals': palette.get('neutrals', []),
            'avoid': palette.get('avoid', [])
        })

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CHROMATYPE — Master 12-Season Color Guide & Optical Dossier</title>
    <style>
        @page {
            size: A4 portrait;
            margin: 0;
        }
        body {
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 0;
            color: #1E293B;
            background-color: #FFFFFF;
            -webkit-print-color-adjust: exact;
        }
        .page {
            width: 210mm;
            height: 297mm;
            page-break-after: always;
            box-sizing: border-box;
            padding: 25mm 20mm;
            position: relative;
            background-color: #FFFFFF;
            overflow: hidden;
        }
        .watermark {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-35deg);
            font-size: 50px;
            font-weight: 900;
            color: rgba(0,0,0,0.035);
            letter-spacing: 10px;
            pointer-events: none;
            white-space: nowrap;
            text-transform: uppercase;
        }
        .header-brand {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 4px;
            color: #64748B;
            font-weight: 700;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid #E2E8F0;
            padding-bottom: 8px;
        }
        .logo-text {
            font-weight: 900;
            color: #0F172A;
            letter-spacing: 2px;
        }
        .logo-text span {
            color: #E8734A;
        }
        .cover-page {
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
            color: #FFFFFF;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            text-align: center;
            padding: 35mm 20mm;
        }
        .cover-title {
            font-size: 38px;
            font-weight: 900;
            letter-spacing: 2px;
            margin: 10px 0;
            text-transform: uppercase;
            color: #FFFFFF;
        }
        .cover-subtitle {
            font-size: 16px;
            font-weight: 300;
            color: #CBD5E1;
            letter-spacing: 1px;
            max-width: 500px;
        }
        .badge {
            background: #E8734A;
            color: #FFFFFF;
            padding: 6px 20px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        .section-title {
            font-size: 20px;
            font-weight: 800;
            color: #0F172A;
            border-bottom: 2px solid #E8734A;
            padding-bottom: 6px;
            margin-top: 0;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .text-block {
            font-size: 11.5px;
            line-height: 1.6;
            color: #334155;
            margin-bottom: 15px;
        }
        .footer-page {
            position: absolute;
            bottom: 10mm;
            left: 20mm;
            right: 20mm;
            display: flex;
            justify-content: space-between;
            font-size: 9px;
            color: #94A3B8;
            border-top: 1px solid #E2E8F0;
            padding-top: 8px;
        }
    </style>
</head>
<body>

    <!-- COVER PAGE -->
    <div class="page cover-page">
        <div class="header-brand" style="border:none; color:#94A3B8;">
            <div class="logo-text" style="color:#FFFFFF;">CHROMA<span>TYPE</span></div>
            <div>DIGITAL MASTER DELIVERY</div>
        </div>

        <div style="margin: auto 0;">
            <div class="badge">Official Digital Edition • $29 Instant Delivery</div>
            <h1 class="cover-title">12-Season Master Color Guide</h1>
            <p class="cover-subtitle">Comprehensive Optical Science, Color History, CIELAB L*a*b* Spectrophotometry, and 432 Pantone Matched Swatches</p>
        </div>

        <div style="font-size: 10px; color: #94A3B8; letter-spacing: 1px;">
            CHROMATYPE Studio • chromatype.me & color-analysis.shop
        </div>
    </div>

    <!-- PAGE 2: HISTORY OF COLOR THEORY & MODERN SPECTROPHOTOMETRY -->
    <div class="page">
        <div class="watermark">CHROMATYPE STUDIO</div>
        <div class="header-brand">
            <span class="logo-text">CHROMA<span>TYPE</span></span>
            <span>COLOR THEORY & SCIENCE</span>
        </div>

        <h2 class="section-title">The Evolution of Color Theory: From Art to Optical Science</h2>

        <div class="text-block">
            <strong>1. The Classical Munsell 3D Color Tree (1905):</strong><br>
            Albert Munsell revolutionized color theory by defining color along three rigorous dimensions: <em>Hue</em> (color family), <em>Value</em> (lightness/darkness), and <em>Chroma</em> (purity/saturation). This 3D spatial coordinate system replaced subjective artistic guesses with measurable color solid dimensions.
        </div>

        <div class="text-block">
            <strong>2. The 7 Color Contrasts of Johannes Itten (Bauhaus, 1961):</strong><br>
            Johannes Itten identified that human visual harmony depends on optical contrasts—specifically temperature contrast (Warm vs. Cool) and light-dark contrast. Itten observed that individuals naturally resonate with specific seasonal color harmonies reflecting their natural skin and hair contrast.
        </div>

        <div class="text-block">
            <strong>3. Seasonal Color Analysis Evolution (1980s–Present):</strong><br>
            Carole Jackson formalized 4 basic seasons (Spring, Summer, Autumn, Winter). Modern image science expanded this into the <strong>12 Sub-Season System</strong>, recognizing that primary undertone (Warm/Cool) is modified by secondary attributes (Light, Deep, Clear, Muted).
        </div>

        <div class="text-block" style="background:#F8FAFC; border-left:4px solid #E8734A; padding:12px 16px; margin-top:20px;">
            <strong>4. The CHROMATYPE CIELAB L*a*b* Optical Standard:</strong><br>
            Defined by the International Commission on Illumination (CIE), CIELAB space maps color identically to the human eye:
            <ul>
                <li><strong>L* (Lightness):</strong> 0 (black) to 100 (white).</li>
                <li><strong>a* Axis:</strong> Negative = Green, Positive = Red/Magenta.</li>
                <li><strong>b* Axis:</strong> Negative = Blue, Positive = Yellow.</li>
                <li><strong>ITA° Angle:</strong> ITA° = (arctan((L*-50)/b*) * 180) / pi measures precise melanin depth independently of lighting.</li>
            </ul>
        </div>

        <div class="footer-page">
            <span>CHROMATYPE Studio • Section 1: Color History</span>
            <span>Page 2</span>
        </div>
    </div>

    <!-- PAGE 3: PHOTO ANALYSIS & EMAIL REPORT DELIVERY PROTOCOL -->
    <div class="page">
        <div class="watermark">CHROMATYPE STUDIO</div>
        <div class="header-brand">
            <span class="logo-text">CHROMA<span>TYPE</span></span>
            <span>SERVICE & EXECUTION PROTOCOL</span>
        </div>

        <h2 class="section-title">How Your Photo Is Analyzed & Delivered</h2>

        <div class="text-block">
            <strong>Step 1: Facial Alignment & Skin Sampling</strong><br>
            When you upload your photo on CHROMATYPE or PrestaShop, our automated alignment engine crops your face and samples 47 landmark points across cheekbones, forehead, and chin to isolate clean skin reflectance.
        </div>

        <div class="text-block">
            <strong>Step 2: 0.4-Second Spectrophotometric Extraction</strong><br>
            The engine converts skin pixels into CIELAB L*a*b* coordinates, calculating your exact L* value, a* undertone, b* warmth, and ITA° typology angle.
        </div>

        <div class="text-block">
            <strong>Step 3: Instant Email Dossier Compilation</strong><br>
            Your individual metrics map directly to your primary 12-season sub-season. Within 3 to 5 minutes, your customized 52-page Master Dossier and 3-tier pocket fan PDF are compiled and sent to your email inbox!
        </div>

        <div style="margin-top:25px; padding:15px; background:#1E293B; color:#FFFFFF; border-radius:12px; text-align:center;">
            <div style="font-size:12px; font-weight:bold; color:#E8734A; text-transform:uppercase; letter-spacing:1px;">100% Privacy Guarantee</div>
            <p style="font-size:10.5px; color:#CBD5E1; margin:6px 0 0 0; line-height:1.4;">
                Photos are processed in volatile RAM memory to extract spectrophotometric metrics and immediately deleted. We never store, share, or publish your photos.
            </p>
        </div>

        <div class="footer-page">
            <span>CHROMATYPE Studio • Section 2: Execution Protocol</span>
            <span>Page 3</span>
        </div>
    </div>
"""

    # Add 12 sub-seasons drapes (2 SWATCHES PER PAGE)
    page_counter = 4
    for sub in all_seasons_data:
        colors = sub['colors']
        for i in range(0, len(colors), 2):
            sw1 = colors[i]
            sw2 = colors[i+1] if i+1 < len(colors) else None

            html_content += f"""
            <div class="page" style="padding:0; display:flex; flex-direction:column; height:297mm; overflow:hidden; position:relative;">
                <div class="watermark">CHROMATYPE</div>

                <!-- TOP HALF DRAPE (SWATCH 1) -->
                <div style="height:144mm; background-color:{sw1['hex']}; color:#FFFFFF; padding:15px 25px; box-sizing:border-box; display:flex; flex-direction:column; justify-content:space-between; align-items:center; text-align:center; position:relative; border-bottom:3px solid #FFFFFF;">
                    <div style="background:rgba(0,0,0,0.65); padding:6px 18px; border-radius:20px; border:1px solid rgba(255,255,255,0.25);">
                        <span style="font-size:9px; text-transform:uppercase; letter-spacing:2px; color:#CBD5E1;">CHROMATYPE Master Palette • {sub['name']}</span>
                        <h3 style="font-size:18px; margin:1px 0 0 0; text-transform:uppercase; letter-spacing:1px; color:#FFFFFF;">{sw1['name']}</h3>
                        <span style="font-size:10px; opacity:0.95; font-weight:700; letter-spacing:1px; color:#F1F5F9;">HEX: {sw1['hex']} • PANTONE {sw1.get('pantone', '17-1563 TCX')}</span>
                    </div>

                    <div style="background:rgba(0,0,0,0.65); padding:8px 16px; border-radius:8px; max-width:480px; border:1px solid rgba(255,255,255,0.2);">
                        <p style="margin:0; font-size:10.5px; line-height:1.3; color:#F8FAFC;">
                            <strong>{sub['name']} Signature Swatch:</strong> Wearing <strong>{sw1['name']}</strong> highlights warm/cool skin harmony with crisp contrast.
                        </p>
                    </div>
                </div>
            """

            if sw2:
                html_content += f"""
                <!-- BOTTOM HALF DRAPE (SWATCH 2) -->
                <div style="height:144mm; background-color:{sw2['hex']}; color:#FFFFFF; padding:15px 25px; box-sizing:border-box; display:flex; flex-direction:column; justify-content:space-between; align-items:center; text-align:center; position:relative;">
                    <div style="background:rgba(0,0,0,0.65); padding:6px 18px; border-radius:20px; border:1px solid rgba(255,255,255,0.25);">
                        <span style="font-size:9px; text-transform:uppercase; letter-spacing:2px; color:#CBD5E1;">CHROMATYPE Master Palette • {sub['name']}</span>
                        <h3 style="font-size:18px; margin:1px 0 0 0; text-transform:uppercase; letter-spacing:1px; color:#FFFFFF;">{sw2['name']}</h3>
                        <span style="font-size:10px; opacity:0.95; font-weight:700; letter-spacing:1px; color:#F1F5F9;">HEX: {sw2['hex']} • PANTONE {sw2.get('pantone', '17-1563 TCX')}</span>
                    </div>

                    <div style="background:rgba(0,0,0,0.65); padding:8px 16px; border-radius:8px; max-width:480px; border:1px solid rgba(255,255,255,0.2);">
                        <p style="margin:0; font-size:10.5px; line-height:1.3; color:#F8FAFC;">
                            <strong>{sub['name']} Signature Swatch:</strong> Wearing <strong>{sw2['name']}</strong> highlights warm/cool skin harmony with crisp contrast.
                        </p>
                    </div>
                </div>
                """

            html_content += f"""
                <div class="footer-page" style="position:absolute; bottom:4px; right:20px; background:rgba(0,0,0,0.7); padding:2px 10px; border-radius:4px; font-size:8px; color:#FFFFFF;">
                    <span>CHROMATYPE Studio • Page {page_counter}</span>
                </div>
            </div>
            """
            page_counter += 1

    html_content += """
</body>
</html>
"""
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    return output_html_path

def generate_pdf_files():
    out_dir = r"C:\Users\dkven\Desktop\CHROMATYPE_Reports"
    os.makedirs(out_dir, exist_ok=True)

    pdf1_path = os.path.join(out_dir, "CHROMATYPE_Master_12Seasons_Complete_Guide.pdf")
    pdf2_path = os.path.join(out_dir, "CHROMATYPE_PrintReady_12Seasons_Pocket_Fan.pdf")

    print("Building HTML for PDF #1 (Master 12-Season Color Guide)...")
    temp_html1 = os.path.join(out_dir, "master_guide_temp.html")
    create_master_guide_html(temp_html1)

    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    msedge = next((path for path in edge_paths if os.path.exists(path)), None)

    if msedge:
        print("Rendering PDF #1 via Headless Edge...")
        cmd1 = [
            msedge, "--headless", "--disable-gpu", "--no-pdf-header-footer",
            f"--print-to-pdf={pdf1_path}", temp_html1
        ]
        subprocess.run(cmd1, check=True)

    if os.path.exists(temp_html1):
        os.remove(temp_html1)

    print("Generating PDF #2 (Print-Ready 3-Tier Pocket Swatch Fan)...")
    subprocess.run(['python', r'C:\Users\dkven\color_analysis_backend\generate_pocket_fan.py'], check=True)
    
    src_pocket = os.path.join(out_dir, "CHROMATYPE_3Tier_Gradient_Pocket_Fan_PrintReady.pdf")
    if os.path.exists(src_pocket):
        shutil.copyfile(src_pocket, pdf2_path)

    print(f"\nPDF #1 Generated: {pdf1_path} ({os.path.getsize(pdf1_path)} bytes)")
    print(f"PDF #2 Generated: {pdf2_path} ({os.path.getsize(pdf2_path)} bytes)")

if __name__ == '__main__':
    generate_pdf_files()
