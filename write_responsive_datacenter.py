import os
import subprocess

paths_to_create = [
    r"C:\Users\dkven\Desktop\AGRO_GUYANA_PROJECT",
    r"C:\Users\dkven\OneDrive\Desktop\AGRO_GUYANA_PROJECT",
    r"C:\Users\dkven\Documents\AGRO_GUYANA_PROJECT"
]

html_content = """<style>
    .agro-responsive-wrapper {
        background-color: #0F172A;
        color: #F8FAFC;
        padding: clamp(15px, 4vw, 40px);
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
        border-radius: 20px;
        width: 100%;
        max-width: 1150px;
        margin: 0 auto;
        box-sizing: border-box;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }
    .agro-responsive-wrapper * {
        box-sizing: border-box;
    }
    .agro-grid-2 {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 20px;
        margin-bottom: 30px;
    }
    .agro-grid-3 {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 15px;
        margin-bottom: 30px;
    }
    .agro-card {
        background: #1E293B;
        padding: clamp(15px, 3vw, 22px);
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.08);
        word-wrap: break-word;
    }
    .agro-table-responsive {
        width: 100%;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        margin-bottom: 30px;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.08);
    }
    .agro-table-responsive table {
        width: 100%;
        min-width: 500px;
        border-collapse: collapse;
        color: #CBD5E1;
        font-size: 13px;
    }
    .agro-title-hero {
        color: #F8FAFC;
        text-transform: uppercase;
        font-size: clamp(22px, 5vw, 32px);
        font-weight: 800;
        margin-top: 15px;
        letter-spacing: 0.5px;
        line-height: 1.2;
    }
    .agro-title-section {
        color: #38BDF8;
        font-size: clamp(18px, 4vw, 22px);
        text-transform: uppercase;
        margin-bottom: 15px;
        letter-spacing: 0.5px;
        line-height: 1.3;
    }
    .agro-flex-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 15px;
    }
    @media (max-width: 600px) {
        .agro-flex-header {
            flex-direction: column;
            text-align: center;
        }
    }
</style>

<div class="agro-responsive-wrapper">

    <!-- HEADER -->
    <div style="text-align: center; border-bottom: 2px solid #10B981; padding-bottom: 20px; margin-bottom: 30px;">
        <span style="background: rgba(16, 185, 129, 0.2); color: #10B981; font-size: 11px; font-weight: 800; padding: 4px 14px; border-radius: 20px; text-transform: uppercase; letter-spacing: 1.5px; border: 1px solid #10B981; display: inline-block;">European Institutional Investor Dossier</span>
        <h1 class="agro-title-hero">
            SOLIDÃO 1.0 GW WIND POWER &amp; AI HYPERSCALE DATA CENTER
        </h1>
        <p style="color: #94A3B8; font-size: clamp(13px, 3vw, 15px); margin-top: 8px;">3,100-Hectare Subsea Fiber-Optic Landing &amp; Clean Energy Hub in Mostardas (RS, Brazil)</p>
    </div>

    <!-- GEOLOCATION & GOOGLE EARTH EMBEDDED MAP -->
    <h2 class="agro-title-section">
        1. Geolocation &amp; Subsea Fiber Landing Hub (Mostardas / Solidão RS)
    </h2>

    <div class="agro-card" style="margin-bottom: 30px;">
        <div class="agro-grid-2" style="margin-bottom: 15px;">
            <div>
                <h4 style="color: #10B981; font-size: 15px; text-transform: uppercase; margin-bottom: 8px;">📌 Precise Coordinates (Google Earth / GIS):</h4>
                <ul style="font-size: 13px; color: #CBD5E1; line-height: 1.8; padding-left: 18px; margin: 0;">
                    <li><strong>Region:</strong> Solidão / Mostardas (Rio Grande do Sul, Brazil)</li>
                    <li><strong>Latitude:</strong> <span style="color: #38BDF8; font-weight: bold;">-31.1075° S</span> (31° 06' 27" S)</li>
                    <li><strong>Longitude:</strong> <span style="color: #38BDF8; font-weight: bold;">-50.9234° W</span> (50° 55' 24" W)</li>
                    <li><strong>Elevation:</strong> 3m to 12m (Flat coastal wind corridor)</li>
                    <li><strong>BR-101 Connectivity:</strong> Direct access to national highway</li>
                </ul>
            </div>
            <div>
                <h4 style="color: #F59E0B; font-size: 15px; text-transform: uppercase; margin-bottom: 8px;">🌐 Atlantic Subsea Fiber Cable Landing:</h4>
                <p style="font-size: 13px; color: #CBD5E1; line-height: 1.7; margin: 0;">
                    Located directly along the subsea fiber cable corridor connecting South America to North America (Miami/NYC) and Europe. Unmatched ultra-low latency internet capacity for 24/7 AI Cloud compute clusters.
                </p>
            </div>
        </div>

        <!-- GOOGLE MAPS EMBED IFRAME (RESPONSIVE) -->
        <div style="width: 100%; height: clamp(250px, 40vw, 420px); border-radius: 12px; overflow: hidden; border: 2px solid rgba(16, 185, 129, 0.4); box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
            <iframe 
                width="100%" 
                height="100%" 
                style="border:0;" 
                loading="lazy" 
                allowfullscreen 
                src="https://maps.google.com/maps?q=-31.1075,-50.9234&hl=en&z=11&output=embed">
            </iframe>
        </div>
    </div>

    <!-- EXECUTIVE SUMMARY & CAPITAL ALLOCATION -->
    <div style="background: rgba(30, 41, 59, 0.85); padding: 20px; border-radius: 14px; border-left: 5px solid #10B981; margin-bottom: 30px;">
        <div class="agro-flex-header">
            <div>
                <h3 style="color: #10B981; font-size: 17px; margin: 0; text-transform: uppercase; font-weight: 800;">Target Initial Investment Capital</h3>
                <p style="font-size: 13px; color: #CBD5E1; margin-top: 4px;">Phase 1 Land Acquisition (3,100 Ha), 100 MW Wind Farm &amp; AI Data Center Grid Tie</p>
            </div>
            <div style="background: #10B981; color: #0F172A; padding: 10px 22px; border-radius: 30px; font-weight: 800; font-size: clamp(18px, 4vw, 22px);">
                USD $100,000,000.00
            </div>
        </div>
    </div>

    <!-- 1.0 GW AI DATA CENTER METRICS -->
    <h2 class="agro-title-section" style="color: #F59E0B;">
        2. 1.0 GigaWatt AI Hyperscale Data Center &amp; Wind Energy Integration
    </h2>

    <div class="agro-grid-2">
        <div class="agro-card">
            <h4 style="color: #38BDF8; font-size: 15px; text-transform: uppercase; margin-bottom: 10px;">⚡ 100% On-Site Clean Wind Power (1.0 GW)</h4>
            <ul style="font-size: 13px; color: #CBD5E1; line-height: 1.8; padding-left: 18px; margin: 0;">
                <li><strong>Wind Capacity Factor:</strong> 52%–58% (Constant ocean breeze)</li>
                <li><strong>Target Power Allocated:</strong> 1,000 MWe (1.0 GigaWatt)</li>
                <li><strong>PUE Target:</strong> 1.15 (Direct ocean cooling efficiency)</li>
                <li><strong>Server Racks Supported:</strong> 50,000+ AI High-Density Racks</li>
                <li><strong>GPU Capacity:</strong> 500,000+ NVIDIA AI Accelerator Chips</li>
            </ul>
        </div>

        <div class="agro-card" style="border-color: #10B981;">
            <h4 style="color: #10B981; font-size: 15px; text-transform: uppercase; margin-bottom: 10px;">🌐 Connectivity &amp; AI Hyperscalers</h4>
            <ul style="font-size: 13px; color: #F8FAFC; line-height: 1.8; padding-left: 18px; margin: 0;">
                <li><strong>Fiber Access:</strong> Direct landing of Atlantic subsea fiber cables</li>
                <li><strong>Latency:</strong> Ultra-low latency link to US, Europe &amp; LatAm</li>
                <li><strong>24/7 Compute Uptime:</strong> Dual wind + subsea redundancy</li>
                <li><strong>Hyperscale Clients:</strong> Microsoft, Google, AWS, Meta &amp; NVIDIA</li>
            </ul>
        </div>
    </div>

    <!-- REVENUE POTENTIAL COMPARISON -->
    <h2 class="agro-title-section" style="color: #EC4899;">
        3. Financial Returns: Energy Sales vs. AI Compute Leasing (At 1.0 GW Maturity)
    </h2>

    <div class="agro-table-responsive">
        <table style="background: #1E293B;">
            <thead>
                <tr style="background: rgba(16, 185, 129, 0.2); color: #10B981; text-transform: uppercase;">
                    <th style="padding: 12px; text-align: left;">Revenue Model Strategy</th>
                    <th style="padding: 12px; text-align: right;">Gross Annual Revenue (USD)</th>
                </tr>
            </thead>
            <tbody>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 12px;"><strong>Option A:</strong> Selling Raw Wind Energy to Grid (US$ 50/MWh)</td>
                    <td style="padding: 12px; text-align: right; font-weight: bold; color: #F8FAFC;">$240,900,000.00 / yr</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05); background: rgba(56, 189, 248, 0.1);">
                    <td style="padding: 12px;"><strong>Option B:</strong> Data Center Co-Location Facility Lease ($175/kW/mo)</td>
                    <td style="padding: 12px; text-align: right; font-weight: bold; color: #38BDF8;">$2,100,000,000.00 / yr ($2.1B)</td>
                </tr>
                <tr style="background: rgba(16, 185, 129, 0.15);">
                    <td style="padding: 12px; color: #10B981; font-weight: bold;"><strong>Option C:</strong> Managed AI Cloud Compute / GPU Cluster Leasing</td>
                    <td style="padding: 12px; text-align: right; font-weight: bold; color: #10B981; font-size: 15px;">$9,300,000,000.00 / yr ($9.3B!)</td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- SILVOPASTORAL & AQUACULTURE INTEGRATION -->
    <h2 class="agro-title-section" style="color: #34D399;">
        4. Agro-Pastoral &amp; High-Protein Aquaculture Buffer (3,100 Hectares)
    </h2>

    <div class="agro-grid-3">
        <div class="agro-card">
            <h4 style="color: #34D399; font-size: 14px; text-transform: uppercase; margin-bottom: 8px;">🐄 F1 Angus-Nelore Cattle</h4>
            <p style="font-size: 12.5px; color: #CBD5E1; line-height: 1.6; margin: 0;">
                AI/IATF breeding dams on intensive pastures of Super-Protein Moringa (28% CP), Forage Peanut &amp; Guadua Bamboo. Target ADG > 1.30 kg/day.
            </p>
        </div>

        <div class="agro-card">
            <h4 style="color: #38BDF8; font-size: 14px; text-transform: uppercase; margin-bottom: 8px;">🌱 Duckweed (45% Protein)</h4>
            <p style="font-size: 12.5px; color: #CBD5E1; line-height: 1.6; margin: 0;">
                Natural lagoons cultivated with <em>Lemna minor</em> (Duckweed) doubling biomass every 48 hours. High-protein supplement for livestock and aquafeed.
            </p>
        </div>

        <div class="agro-card">
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
        target_file = os.path.join(html_dir, "16_SOLIDÃO_GIGAWATT_MOBILE_RESPONSIVE.html")
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        created_files.append(target_file)
        print(f"Successfully saved: {target_file}")
    except Exception as e:
        print(f"Error saving to {base_dir}: {e}")

if created_files:
    subprocess.run(["explorer.exe", os.path.dirname(created_files[0])])
    print(f"Opened Explorer window at {os.path.dirname(created_files[0])}")
