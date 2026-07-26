import os
import subprocess

paths_to_create = [
    r"C:\Users\dkven\Desktop\AGRO_GUYANA_PROJECT",
    r"C:\Users\dkven\OneDrive\Desktop\AGRO_GUYANA_PROJECT",
    r"C:\Users\dkven\Documents\AGRO_GUYANA_PROJECT"
]

html_content = """<div style="background-color: #0F172A; color: #F8FAFC; padding: 40px; font-family: 'Outfit', sans-serif; border-radius: 20px; max-width: 1100px; margin: 0 auto; box-shadow: 0 20px 50px rgba(0,0,0,0.5);">

    <!-- HEADER -->
    <div style="text-align: center; border-bottom: 2px solid #10B981; padding-bottom: 25px; margin-bottom: 35px;">
        <span style="background: rgba(16, 185, 129, 0.2); color: #10B981; font-size: 11px; font-weight: 800; padding: 4px 16px; border-radius: 20px; text-transform: uppercase; letter-spacing: 2px; border: 1px solid #10B981;">European Institutional Investor Dossier</span>
        <h1 style="color: #F8FAFC; text-transform: uppercase; font-size: 32px; font-weight: 800; margin-top: 15px; letter-spacing: 1px;">
            SOLIDÃO GIGA-WIND &amp; INTEGRATED AGRO-ECOSYSTEM
        </h1>
        <p style="color: #94A3B8; font-size: 15px; margin-top: 8px;">3,100-Hectare Coastal Infrastructure &amp; Renewable Energy Project in Mostardas (RS, Brazil)</p>
    </div>

    <!-- EXECUTIVE SUMMARY & CAPITAL -->
    <div style="background: rgba(30, 41, 59, 0.85); padding: 25px; border-radius: 14px; border-left: 5px solid #10B981; margin-bottom: 35px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
            <div>
                <h3 style="color: #10B981; font-size: 18px; margin: 0; text-transform: uppercase; font-weight: 800;">Target Investment Capital</h3>
                <p style="font-size: 13px; color: #CBD5E1; margin-top: 4px;">Phase 1 Land Acquisition, 100 MW Wind Farm &amp; Agro-Aquaculture Infrastructure</p>
            </div>
            <div style="background: #10B981; color: #0F172A; padding: 10px 22px; border-radius: 30px; font-weight: 800; font-size: 22px;">
                USD $100,000,000.00
            </div>
        </div>
    </div>

    <!-- WIND POWER METRICS -->
    <h2 style="color: #38BDF8; font-size: 22px; text-transform: uppercase; margin-bottom: 15px; letter-spacing: 0.5px;">
        1. World-Class Coastal Wind Resource (100 MWe ➔ 1.0 GigaWatt Expansion)
    </h2>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 35px;">
        <div style="background: #1E293B; padding: 22px; border-radius: 14px; border: 1px solid rgba(255,255,255,0.08);">
            <h4 style="color: #38BDF8; font-size: 15px; text-transform: uppercase; margin-bottom: 10px;">Phase 1: 100 MWe Installed (Years 1–3)</h4>
            <ul style="font-size: 13px; color: #CBD5E1; line-height: 1.8; padding-left: 18px; margin: 0;">
                <li><strong>Capacity Factor:</strong> 52%–58% (Unobstructed Ocean Winds)</li>
                <li><strong>Annual Output:</strong> ~481,800 MWh / year</li>
                <li><strong>Power Price (PPA):</strong> USD $50.00 / MWh</li>
                <li><strong>Gross Wind Revenue:</strong> <strong style="color: #10B981;">USD $24,090,000.00 / year</strong></li>
                <li><strong>Capital Payback:</strong> Fast payback from grid energy sales</li>
            </ul>
        </div>

        <div style="background: #1E293B; padding: 22px; border-radius: 14px; border: 1px solid #10B981;">
            <h4 style="color: #10B981; font-size: 15px; text-transform: uppercase; margin-bottom: 10px;">Phase 2: 1,000 MWe Expansion (1.0 GW)</h4>
            <ul style="font-size: 13px; color: #F8FAFC; line-height: 1.8; padding-left: 18px; margin: 0;">
                <li><strong>Target Capacity:</strong> 1.0 GigaWatt (10–15 Year Roadmap)</li>
                <li><strong>Annual Output:</strong> ~4,818,000 MWh / year</li>
                <li><strong>Power Price (PPA):</strong> USD $50.00 / MWh</li>
                <li><strong>Gross Wind Revenue:</strong> <strong style="color: #10B981;">USD $240,900,000.00 / year</strong></li>
                <li><strong>Grid Connection:</strong> Neighboring farms currently operating 70–100 MWe</li>
            </ul>
        </div>
    </div>

    <!-- AGRO-LIVESTOCK & AQUACULTURE ECOSYSTEM -->
    <h2 style="color: #F59E0B; font-size: 22px; text-transform: uppercase; margin-bottom: 15px; letter-spacing: 0.5px;">
        2. Silvopastoral Livestock &amp; High-Protein Duckweed Aquaculture
    </h2>

    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 35px;">
        <div style="background: #1E293B; padding: 18px; border-radius: 12px;">
            <h4 style="color: #34D399; font-size: 14px; text-transform: uppercase; margin-bottom: 8px;">🐄 F1 Angus-Nelore Cattle</h4>
            <p style="font-size: 12.5px; color: #CBD5E1; line-height: 1.6; margin: 0;">
                AI/IATF breeding dams on intensive rotational pastures of Super-Protein Moringa (28% CP), Forage Peanut &amp; Guadua Bamboo. Target ADG > 1.30 kg/day.
            </p>
        </div>

        <div style="background: #1E293B; padding: 18px; border-radius: 12px;">
            <h4 style="color: #38BDF8; font-size: 14px; text-transform: uppercase; margin-bottom: 8px;">🌱 Duckweed (45% Protein)</h4>
            <p style="font-size: 12.5px; color: #CBD5E1; line-height: 1.6; margin: 0;">
                Natural lagoons cultivated with <em>Lemna minor</em> (Duckweed) doubling biomass every 48 hours. High-protein supplement for livestock and aquafeed.
            </p>
        </div>

        <div style="background: #1E293B; padding: 18px; border-radius: 12px;">
            <h4 style="color: #EC4899; font-size: 14px; text-transform: uppercase; margin-bottom: 8px;">🦐 Shrimp &amp; Fish Lagoons</h4>
            <p style="font-size: 12.5px; color: #CBD5E1; line-height: 1.6; margin: 0;">
                High-margin marine &amp; freshwater shrimp (Penaeus / Macrobrachium) and Tilapia farming integrated with bio-filtering water treatment.
            </p>
        </div>
    </div>

    <!-- CAPITAL ALLOCATION BREAKDOWN -->
    <h2 style="color: #EC4899; font-size: 22px; text-transform: uppercase; margin-bottom: 15px; letter-spacing: 0.5px;">
        3. USD $100M Initial Capital Allocation Breakdown
    </h2>

    <div style="background: #1E293B; padding: 22px; border-radius: 14px; margin-bottom: 35px;">
        <table style="width: 100%; border-collapse: collapse; color: #CBD5E1; font-size: 13px;">
            <thead>
                <tr style="background: rgba(16, 185, 129, 0.2); color: #10B981; text-transform: uppercase;">
                    <th style="padding: 10px; text-align: left;">Project Expenditure Pillar</th>
                    <th style="padding: 10px; text-align: right;">Capital Allocated (USD)</th>
                </tr>
            </thead>
            <tbody>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 10px;">1. Land Acquisition (3,100 Hectares in Mostardas/Solidão RS)</td>
                    <td style="padding: 10px; text-align: right; font-weight: bold; color: #F8FAFC;">$18,000,000.00</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 10px;">2. Phase 1 Wind Farm Installation (100 MWe Balance of Plant &amp; Grid Tie)</td>
                    <td style="padding: 10px; text-align: right; font-weight: bold; color: #F8FAFC;">$62,000,000.00</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 10px;">3. Livestock Breeding, IATF, Moringa, Bamboo &amp; Pasture Infrastructure</td>
                    <td style="padding: 10px; text-align: right; font-weight: bold; color: #F8FAFC;">$8,500,000.00</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 10px;">4. Aquaculture Lagoons, Duckweed Processing &amp; Shrimp Hatcheries</td>
                    <td style="padding: 10px; text-align: right; font-weight: bold; color: #F8FAFC;">$4,500,000.00</td>
                </tr>
                <tr>
                    <td style="padding: 10px;">5. Environmental Licensing, Working Capital &amp; Operational Reserve</td>
                    <td style="padding: 10px; text-align: right; font-weight: bold; color: #F8FAFC;">$7,000,000.00</td>
                </tr>
            </tbody>
        </table>
    </div>

</div>"""

created_files = []
for base_dir in paths_to_create:
    try:
        html_dir = os.path.join(base_dir, "wordpress_pages_html")
        os.makedirs(html_dir, exist_ok=True)
        target_file = os.path.join(html_dir, "13_MOSTARDAS_GIGAWATT_INVESTMENT_DOSSIER.html")
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        created_files.append(target_file)
        print(f"Successfully saved: {target_file}")
    except Exception as e:
        print(f"Error saving to {base_dir}: {e}")

if created_files:
    subprocess.run(["explorer.exe", os.path.dirname(created_files[0])])
    print(f"Opened Explorer window at {os.path.dirname(created_files[0])}")
