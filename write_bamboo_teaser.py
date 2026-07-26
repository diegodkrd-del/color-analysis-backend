import os
import subprocess

paths_to_create = [
    r"C:\Users\dkven\Desktop\AGRO_GUYANA_PROJECT",
    r"C:\Users\dkven\OneDrive\Desktop\AGRO_GUYANA_PROJECT",
    r"C:\Users\dkven\Documents\AGRO_GUYANA_PROJECT"
]

html_content = """<div style="background-color: #0F172A; color: #F8FAFC; padding: 40px; font-family: 'Outfit', sans-serif; border-radius: 20px; max-width: 1080px; margin: 0 auto; box-shadow: 0 20px 40px rgba(0,0,0,0.5);">

    <!-- HEADER -->
    <div style="text-align: center; border-bottom: 2px solid #10B981; padding-bottom: 20px; margin-bottom: 30px;">
        <span style="background: rgba(16, 185, 129, 0.2); color: #10B981; font-size: 11px; font-weight: 800; padding: 4px 14px; border-radius: 20px; text-transform: uppercase; letter-spacing: 1.5px; border: 1px solid #10B981;">Confidential Investment Teaser</span>
        <h1 style="color: #F8FAFC; text-transform: uppercase; font-size: 30px; font-weight: 800; margin-top: 15px; letter-spacing: 1px;">
            HIGH-YIELD LIVESTOCK, FORAGE &amp; BAMBOO ENERGY ECOSYSTEM
        </h1>
        <p style="color: #94A3B8; font-size: 15px; margin-top: 8px;">100-Acre Pilot Engine &amp; 5,000-Acre Regional Industrial Network in Guyana</p>
    </div>

    <!-- EXECUTIVE OVERVIEW -->
    <div style="background: rgba(30, 41, 59, 0.8); padding: 25px; border-radius: 14px; border-left: 4px solid #10B981; margin-bottom: 30px;">
        <h3 style="color: #10B981; font-size: 18px; margin-bottom: 8px; text-transform: uppercase;">Executive Summary</h3>
        <p style="font-size: 14px; color: #CBD5E1; line-height: 1.7; margin: 0;">
            This project deploys a high-yielding biological model integrating a <strong>native Brazilian super-protein tree species (28–32% CP)</strong>, <strong>elite Guadua Bamboo from Acre (Northern Brazil)</strong>, and Artificial Insemination (AI/IATF) livestock management. The system operates a high-capacity breeding engine supplying live pregnant F1 heifers, finished premium bulls, mechanized bamboo forage, and off-grid bio-electricity across Guyana.
        </p>
    </div>

    <!-- LIVESTOCK REPRODUCTIVE METRICS -->
    <h2 style="color: #38BDF8; font-size: 20px; text-transform: uppercase; margin-bottom: 15px; letter-spacing: 0.5px;">
        1. Livestock Reproduction &amp; Growth Velocity
    </h2>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px;">
        <!-- 100 ACRE PILOT -->
        <div style="background: #1E293B; padding: 22px; border-radius: 14px; border: 1px solid rgba(255,255,255,0.08);">
            <h4 style="color: #38BDF8; font-size: 15px; text-transform: uppercase; margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 6px;">
                100-Acre Breeding Engine
            </h4>
            <ul style="font-size: 13px; color: #CBD5E1; line-height: 1.8; padding-left: 18px; margin: 0;">
                <li><strong>Breeding Herd:</strong> 200 Nelore Dams (100% AI / IATF)</li>
                <li><strong>Calving Output:</strong> ~175 F1 Angus Calves / year (88% rate)</li>
                <li><strong>Live Heifer Supply:</strong> 85 Pregnant F1 Heifers/yr for expansion</li>
                <li><strong>Bull Finishing:</strong> 85 Steers finished at 18–20 months</li>
                <li><strong>Growth Target:</strong> 1.10 kg to 1.35 kg / day gain</li>
            </ul>
        </div>

        <!-- 5,000 ACRE REGIONAL SCALING -->
        <div style="background: #1E293B; padding: 22px; border-radius: 14px; border: 1px solid #10B981;">
            <h4 style="color: #10B981; font-size: 15px; text-transform: uppercase; margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 6px;">
                5,000-Acre Scaled Network
            </h4>
            <ul style="font-size: 13px; color: #F8FAFC; line-height: 1.8; padding-left: 18px; margin: 0;">
                <li><strong>Breeding Herd:</strong> 2,500 Active Dams</li>
                <li><strong>Annual Calving Volume:</strong> 2,100+ F1 Angus-Nelore Calves</li>
                <li><strong>Live Breeding Supply:</strong> 1,000+ Pregnant Heifers / yr</li>
                <li><strong>Caricom Beef Supply:</strong> 1,000+ Fattened Bulls / yr</li>
                <li><strong>Slaughter Weight:</strong> 520 kg – 560 kg average</li>
            </ul>
        </div>
    </div>

    <!-- BAMBOO SILVICULTURE & MECHANIZED ENERGY -->
    <h2 style="color: #34D399; font-size: 20px; text-transform: uppercase; margin-bottom: 15px; letter-spacing: 0.5px;">
        2. Acre Guadua Bamboo Silviculture &amp; Mechanized Bio-Energy
    </h2>

    <div style="background: #1E293B; padding: 22px; border-radius: 14px; margin-bottom: 30px;">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div>
                <h4 style="color: #34D399; font-size: 14px; text-transform: uppercase; margin-bottom: 8px;">🌱 Propagation &amp; Mechanized Forage</h4>
                <p style="font-size: 13px; color: #CBD5E1; line-height: 1.6; margin: 0;">
                    Sourced from elite <em>Guadua angustifolia</em> genetics in Acre (Northern Brazil) and micro-propagated in Lethem. Mechanized forage harvesters cut young foliage (14%–18% CP) to supply high-fiber roughage for cattle rations.
                </p>
            </div>
            <div>
                <h4 style="color: #F59E0B; font-size: 14px; text-transform: uppercase; margin-bottom: 8px;">⚡ Renewable Bio-Power &amp; Seedlings</h4>
                <p style="font-size: 13px; color: #CBD5E1; line-height: 1.6; margin: 0;">
                    Mechanized chipping of mature bamboo culms feeds gasifier thermal boilers, producing <strong>100% off-grid electricity</strong> for pumps and processing. The nursery outputs 1,000,000+ tubette seedlings/yr for regional windbreaks and fencing.
                </p>
            </div>
        </div>
    </div>

    <!-- INTEGRATED FEED RATION BALANCING -->
    <h2 style="color: #F59E0B; font-size: 20px; text-transform: uppercase; margin-bottom: 15px; letter-spacing: 0.5px;">
        3. Integrated Nutritional Ration (Calf Weaning to Adult Finishing)
    </h2>

    <div style="background: #1E293B; padding: 22px; border-radius: 14px; margin-bottom: 35px;">
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;">
            <div style="background: rgba(15, 23, 42, 0.6); padding: 15px; border-radius: 10px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">
                <div style="color: #10B981; font-size: 18px; font-weight: 800;">60% Base</div>
                <div style="font-size: 12px; font-weight: bold; color: #F8FAFC; margin-top: 4px;">Super-Protein Tree Forage</div>
                <div style="font-size: 11px; color: #94A3B8; margin-top: 4px;">28%–32% CP Fresh Biomass</div>
            </div>

            <div style="background: rgba(15, 23, 42, 0.6); padding: 15px; border-radius: 10px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">
                <div style="color: #34D399; font-size: 18px; font-weight: 800;">20% Fiber</div>
                <div style="font-size: 12px; font-weight: bold; color: #F8FAFC; margin-top: 4px;">Guadua Bamboo Foliage</div>
                <div style="font-size: 11px; color: #94A3B8; margin-top: 4px;">Mechanized Cut Effective Fiber</div>
            </div>

            <div style="background: rgba(15, 23, 42, 0.6); padding: 15px; border-radius: 10px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">
                <div style="color: #F59E0B; font-size: 18px; font-weight: 800;">20% Energy</div>
                <div style="font-size: 12px; font-weight: bold; color: #F8FAFC; margin-top: 4px;">Local Grain Starch</div>
                <div style="font-size: 11px; color: #94A3B8; margin-top: 4px;">Corn / Sorghum / Broken Rice</div>
            </div>
        </div>
    </div>

    <!-- DISCRETE PRICING & DOSSIER ACCESS FOOTER -->
    <div style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
        <div style="max-width: 650px;">
            <div style="font-size: 12px; font-weight: bold; color: #94A3B8; text-transform: uppercase; letter-spacing: 1px;">
                Phase 1 Technical Dossier &amp; Supply Chain Release
            </div>
            <div style="font-size: 11.5px; color: #64748B; margin-top: 4px; line-height: 1.5;">
                Includes exact botanical species identification, pre-inoculated seed supplier contacts in Brazil, cold-chain transport protocols, and step-by-step planting manuals to your farm in Guyana.
            </div>
        </div>
        <div style="text-align: right; background: rgba(15, 23, 42, 0.8); padding: 10px 18px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1);">
            <span style="font-size: 10px; color: #94A3B8; text-transform: uppercase; display: block;">Phase 1 Retainer</span>
            <span style="font-size: 18px; font-weight: 800; color: #10B981;">USD $2,000.00</span>
            <span style="font-size: 9px; color: #64748B; display: block; margin-top: 2px;">Payable via Zelle / PIX / Gy$</span>
        </div>
    </div>

</div>"""

created_files = []
for base_dir in paths_to_create:
    try:
        html_dir = os.path.join(base_dir, "wordpress_pages_html")
        os.makedirs(html_dir, exist_ok=True)
        target_file = os.path.join(html_dir, "11_ULTIMATE_TEASER_ENGLISH_BAMBOO.html")
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        created_files.append(target_file)
        print(f"Successfully saved: {target_file}")
    except Exception as e:
        print(f"Error saving to {base_dir}: {e}")

if created_files:
    subprocess.run(["explorer.exe", os.path.dirname(created_files[0])])
    print(f"Opened Explorer window at {os.path.dirname(created_files[0])}")
