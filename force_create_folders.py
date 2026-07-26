import os
import subprocess

paths_to_create = [
    r"C:\Users\dkven\Desktop\AGRO_GUYANA_PROJECT",
    r"C:\Users\dkven\OneDrive\Desktop\AGRO_GUYANA_PROJECT",
    r"C:\Users\dkven\Documents\AGRO_GUYANA_PROJECT"
]

html_content = """<div style="background-color: #0F172A; color: #F8FAFC; padding: 40px; font-family: sans-serif; border-radius: 20px; max-width: 1000px; margin: 0 auto; box-shadow: 0 20px 40px rgba(0,0,0,0.5);">
    <div style="text-align: center; border-bottom: 2px solid #10B981; padding-bottom: 20px; margin-bottom: 30px;">
        <span style="background: #EF4444; color: #FFF; font-size: 11px; font-weight: 800; padding: 4px 12px; border-radius: 20px; text-transform: uppercase;">Confidential Teaser</span>
        <h1 style="color: #10B981; text-transform: uppercase; font-size: 28px; font-weight: 800; margin-top: 15px;">HIGH-PROTEIN FORAGE & ACCELERATED FATTENING SYSTEM (100 ACRES)</h1>
        <p style="color: #94A3B8; font-size: 14px;">Brazilian High-Yield Agronomic Technology for Guyana Livestock Production</p>
    </div>
    <div style="background: rgba(30, 41, 59, 0.8); padding: 20px; border-radius: 12px; border-left: 4px solid #F59E0B; margin-bottom: 30px;">
        <h3 style="color: #F59E0B; font-size: 16px;">🔒 INDUSTRIAL PROPERTY PROTECTION NOTICE</h3>
        <p style="font-size: 13px; color: #CBD5E1;">The exact scientific names of the super-protein tree species, inoculants, and direct seed suppliers are protected trade secrets. Complete agronomic specifications will be released upon delivery of the Full Project Dossier (Phase 1).</p>
    </div>
    <h2 style="color: #38BDF8; font-size: 20px;">1. 100-Acre Yield & Carrying Capacity</h2>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px;">
        <div style="background: #1E293B; padding: 20px; border-radius: 12px;">
            <h4 style="color: #EF4444;">Traditional Pasture (Baseline)</h4>
            <ul style="font-size: 13px; color: #94A3B8;">
                <li>Crude Protein: 7% to 9%</li>
                <li>Capacity: 40 to 50 Head</li>
                <li>Slaughter Age: 36 to 42 Months</li>
            </ul>
        </div>
        <div style="background: #1E293B; padding: 20px; border-radius: 12px; border: 1px solid #10B981;">
            <h4 style="color: #10B981;">New Bio-Engineered System</h4>
            <ul style="font-size: 13px; color: #F8FAFC;">
                <li>Crude Protein: 18% to 32%</li>
                <li>Breeding Capacity: 240 Cows + Calves</li>
                <li>Finishing Capacity: 320 Bulls / Year</li>
                <li>Slaughter Age: 18 to 20 Months</li>
            </ul>
        </div>
    </div>
    <div style="background: rgba(16, 185, 129, 0.1); border: 2px solid #10B981; padding: 25px; border-radius: 16px; text-align: center;">
        <h3 style="color: #10B981;">Access Complete Project Dossier (Phase 1)</h3>
        <div style="font-size: 32px; font-weight: 800; color: #FFFFFF;">USD $2,000.00</div>
        <p style="font-size: 13px; color: #CBD5E1;">Includes exact botanical species identification, direct contacts of seed producers in Brazil, cold-chain logistics plans, customs clearance procedures, and step-by-step planting manuals to your farm in Guyana.</p>
        <div style="font-size: 12px; color: #94A3B8;">Payment Methods: Zelle (USA) | PIX (Brazil) | Gy$ (Georgetown)</div>
    </div>
</div>"""

created_folders = []
for base_dir in paths_to_create:
    try:
        html_dir = os.path.join(base_dir, "wordpress_pages_html")
        os.makedirs(html_dir, exist_ok=True)

        with open(os.path.join(base_dir, "README.txt"), "w", encoding="utf-8") as f:
            f.write("AGRO-GUYANA PROJECT CONFIDENTIAL TEASER")

        with open(os.path.join(html_dir, "09_TEASER_ENGLISH_PHASE1.html"), "w", encoding="utf-8") as f:
            f.write(html_content)
        
        created_folders.append(base_dir)
        print(f"Successfully created: {base_dir}")
    except Exception as e:
        print(f"Could not write to {base_dir}: {e}")

# Automatically pop up Windows File Explorer right to the folder!
if created_folders:
    subprocess.run(["explorer.exe", created_folders[0]])
    print(f"Opened Explorer window at {created_folders[0]}")
