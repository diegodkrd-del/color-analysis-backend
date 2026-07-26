import os
import subprocess

paths_to_create = [
    r"C:\Users\dkven\Desktop\AGRO_GUYANA_PROJECT",
    r"C:\Users\dkven\OneDrive\Desktop\AGRO_GUYANA_PROJECT",
    r"C:\Users\dkven\Documents\AGRO_GUYANA_PROJECT"
]

html_content = """<div style="background-color: #0F172A; color: #F8FAFC; padding: 40px; font-family: 'Outfit', sans-serif; border-radius: 20px; max-width: 1150px; margin: 0 auto; box-shadow: 0 20px 50px rgba(0,0,0,0.5);">

    <!-- HEADER -->
    <div style="text-align: center; border-bottom: 2px solid #10B981; padding-bottom: 25px; margin-bottom: 35px;">
        <span style="background: rgba(16, 185, 129, 0.2); color: #10B981; font-size: 11px; font-weight: 800; padding: 4px 16px; border-radius: 20px; text-transform: uppercase; letter-spacing: 2px; border: 1px solid #10B981;">European Institutional Investor &amp; Hyperscale Dossier</span>
        <h1 style="color: #F8FAFC; text-transform: uppercase; font-size: 32px; font-weight: 800; margin-top: 15px; letter-spacing: 1px;">
            SOLIDÃO 1.0 GW WIND POWER &amp; AI HYPERSCALE DATA CENTER
        </h1>
        <p style="color: #94A3B8; font-size: 15px; margin-top: 8px;">3,100-Hectare Subsea Fiber-Optic Landing &amp; Clean Energy Hub in Mostardas (RS, Brazil)</p>
    </div>

    <!-- EXECUTIVE SUMMARY & CAPITAL ALLOCATION -->
    <div style="background: rgba(30, 41, 59, 0.85); padding: 25px; border-radius: 14px; border-left: 5px solid #10B981; margin-bottom: 35px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
            <div>
                <h3 style="color: #10B981; font-size: 18px; margin: 0; text-transform: uppercase; font-weight: 800;">Target Initial Investment Capital</h3>
                <p style="font-size: 13px; color: #CBD5E1; margin-top: 4px;">Phase 1 Land Acquisition (3,100 Ha), 100 MW Wind Farm &amp; AI Data Center Grid Tie</p>
            </div>
            <div style="background: #10B981; color: #0F172A; padding: 10px 22px; border-radius: 30px; font-weight: 800; font-size: 22px;">
                USD $100,000,000.00
            </div>
        </div>
    </div>

    <!-- 1.0 GW AI DATA CENTER & SUBSEA FIBER SYNERGY -->
    <h2 style="color: #38BDF8; font-size: 22px; text-transform: uppercase; margin-bottom: 15px; letter-spacing: 0.5px;">
        1. 1.0 GigaWatt AI Hyperscale Data Center &amp; Subsea Cable Infrastructure
    </h2>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 35px;">
        <div style="background: #1E293B; padding: 22px; border-radius: 14px; border: 1px solid rgba(255,255,255,0.08);">
            <h4 style="color: #38BDF8; font-size: 15px; text-transform: uppercase; margin-bottom: 10px;">⚡ 100% On-Site Clean Wind Power (1.0 GW)</h4>
            <ul style="font-size: 13px; color: #CBD5E1; line-height: 1.8; padding-left: 18px; margin: 0;">
                <li><strong>Wind Capacity Factor:</strong> 52%–58% (Constant ocean breeze)</li>
                <li><strong>Target Power Allocated:</strong> 1,000 MWe (1.0 GigaWatt)</li>
                <li><strong>PUE Target:</strong> 1.15 (Direct ocean cooling efficiency)</li>
                <li><strong>Server Racks Supported:</strong> 50,000+ AI High-Density Racks</li>
                <li><strong>GPU Capacity:</strong> 500,000+ NVIDIA AI Accelerator Chips</li>
            </ul>
        </div>

        <div style="background: #1E293B; padding: 22px; border-radius: 14px; border: 1px solid #10B981;">
            <h4 style="color: #10B981; font-size: 15px; text-transform: uppercase; margin-bottom: 10px;">🌐 Subsea Fiber Cable &amp; Ultra-Low Latency</h4>
            <ul style="font-size: 13px; color: #F8FAFC; line-height: 1.8; padding-left: 18px; margin: 0;">
                <li><strong>Fiber Access:</strong> Direct landing of transatlantic subsea fiber cables</li>
                <li><strong>Connectivity:</strong> Ultra-low latency link to US, Europe &amp; LatAm</li>
                <li><strong>24/7 Compute Uptime:</strong> Dual wind + subsea redundancy</li>
                <li><strong>Hyperscale Clients:</strong> Ideal for Microsoft, Google, AWS, Meta &amp; NVIDIA</li>
            </ul>
        </div>
    </div>

    <!-- REVENUE POTENTIAL COMPARISON -->
    <h2 style="color: #F59E0B; font-size: 22px; text-transform: uppercase; margin-bottom: 15px; letter-spacing: 0.5px;">
        2. Financial Returns: Energy Sales vs. AI Compute Leasing (At 1.0 GW Maturity)
    </h2>

    <div style="background: #1E293B; padding: 22px; border-radius: 14px; margin-bottom: 35px;">
        <table style="width: 100%; border-collapse: collapse; color: #CBD5E1; font-size: 13px;">
            <thead>
                <tr style="background: rgba(16, 185, 129, 0.2); color: #10B981; text-transform: uppercase;">
                    <th style="padding: 10px; text-align: left;">Revenue Model Strategy</th>
                    <th style="padding: 10px; text-align: right;">Gross Annual Revenue (USD)</th>
                </tr>
            </thead>
            <tbody>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 10px;"><strong>Option A:</strong> Selling Raw Wind Energy to Grid (US$ 50/MWh)</td>
                    <td style="padding: 10px; text-align: right; font-weight: bold; color: #F8FAFC;">$240,900,000.00 / yr</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05); background: rgba(56, 189, 248, 0.1);">
                    <td style="padding: 10px;"><strong>Option B:</strong> Data Center Co-Location Facility Lease ($175/kW/mo)</td>
                    <td style="padding: 10px; text-align: right; font-weight: bold; color: #38BDF8;">$2,100,000,000.00 / yr ($2.1B)</td>
                </tr>
                <tr style="background: rgba(16, 185, 129, 0.15);">
                    <td style="padding: 10px; color: #10B981; font-weight: bold;"><strong>Option C:</strong> Managed AI Cloud Compute / GPU Cluster Leasing</td>
                    <td style="padding: 10px; text-align: right; font-weight: bold; color: #10B981; font-size: 15px;">$9,300,000,000.00 / yr ($9.3B!)</td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- SILVOPASTORAL & AQUACULTURE INTEGRATION -->
    <h2 style="color: #EC4899; font-size: 22px; text-transform: uppercase; margin-bottom: 15px; letter-spacing: 0.5px;">
        3. Agro-Pastoral &amp; High-Protein Aquaculture Buffer (3,100 Hectares)
    </h2>

    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 35px;">
        <div style="background: #1E293B; padding: 18px; border-radius: 12px;">
            <h4 style="color: #34D399; font-size: 14px; text-transform: uppercase; margin-bottom: 8px;">🐄 F1 Angus-Nelore Cattle</h4>
            <p style="font-size: 12.5px; color: #CBD5E1; line-height: 1.6; margin: 0;">
                AI/IATF breeding dams on intensive pastures of Super-Protein Moringa (28% CP), Forage Peanut &amp; Guadua Bamboo. Target ADG > 1.30 kg/day.
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

</div>"""

created_files = []
for base_dir in paths_to_create:
    try:
        html_dir = os.path.join(base_dir, "wordpress_pages_html")
        os.makedirs(html_dir, exist_ok=True)
        target_file = os.path.join(html_dir, "14_SOLIDÃO_GIGAWATT_AI_DATACENTER_DOSSIER.html")
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        created_files.append(target_file)
        print(f"Successfully saved: {target_file}")
    except Exception as e:
        print(f"Error saving to {base_dir}: {e}")

if created_files:
    subprocess.run(["explorer.exe", os.path.dirname(created_files[0])])
    print(f"Opened Explorer window at {os.path.dirname(created_files[0])}")
