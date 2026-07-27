import os
import subprocess

def create_resume_pdf():
    out_dir = r"C:\Users\dkven\Desktop\CHROMATYPE_Reports"
    os.makedirs(out_dir, exist_ok=True)
    
    html_path = os.path.join(out_dir, "diego_resume_print.html")
    pdf_path = os.path.join(out_dir, "Diego_Kasper_Romero_Diaz_Executive_Resume_PrintReady.pdf")

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>DIEGO KASPER ROMERO DIAZ — Executive Resume</title>
<style>
    @page {
        size: Letter portrait;
        margin: 12mm 15mm 12mm 15mm;
    }
    body {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #1E293B;
        background: #FFFFFF;
        margin: 0;
        padding: 0;
        font-size: 10pt;
        line-height: 1.4;
        -webkit-print-color-adjust: exact;
    }
    .page-break {
        page-break-before: always;
        padding-top: 5mm;
    }
    .header {
        border-bottom: 2px solid #0F172A;
        padding-bottom: 8px;
        margin-bottom: 12px;
    }
    .name {
        font-size: 22pt;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin: 0 0 2px 0;
    }
    .title-line {
        font-size: 11pt;
        font-weight: 700;
        color: #E8734A;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    .contact-bar {
        font-size: 8.5pt;
        color: #475569;
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-bottom: 4px;
    }
    .contact-item {
        display: inline-flex;
        align-items: center;
    }
    .contact-item strong {
        color: #0F172A;
        margin-right: 3px;
    }
    .section-title {
        font-size: 11pt;
        font-weight: 800;
        color: #0F172A;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-bottom: 1px solid #CBD5E1;
        padding-bottom: 3px;
        margin-top: 12px;
        margin-bottom: 8px;
    }
    .summary-box {
        font-size: 9.5pt;
        color: #334155;
        text-align: justify;
        line-height: 1.45;
        margin-bottom: 10px;
    }
    .grid-2col {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px 16px;
        font-size: 9pt;
        margin-bottom: 10px;
    }
    .grid-item {
        background: #F8FAFC;
        border-left: 3px solid #E8734A;
        padding: 4px 8px;
        border-radius: 0 4px 4px 0;
    }
    .grid-item strong {
        color: #0F172A;
        display: block;
        font-size: 9.5pt;
    }
    .job-block {
        margin-bottom: 10px;
    }
    .job-header {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-bottom: 2px;
    }
    .company {
        font-size: 10.5pt;
        font-weight: 800;
        color: #0F172A;
    }
    .job-title {
        font-size: 9.5pt;
        font-weight: 700;
        color: #E8734A;
    }
    .date-location {
        font-size: 9pt;
        font-weight: 700;
        color: #64748B;
    }
    .job-desc {
        font-size: 9pt;
        color: #334155;
        margin-bottom: 4px;
        font-style: italic;
    }
    ul.bullets {
        margin: 0 0 6px 16px;
        padding: 0;
        font-size: 9pt;
        color: #334155;
    }
    ul.bullets li {
        margin-bottom: 3px;
        line-height: 1.35;
    }
    .lang-badge {
        display: inline-block;
        background: #0F172A;
        color: #FFFFFF;
        font-size: 8pt;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 12px;
        margin-right: 4px;
    }
</style>
</head>
<body>

    <!-- PAGE 1 -->
    <div class="header">
        <div class="name">DIEGO KASPER ROMERO DIAZ</div>
        <div class="title-line">Director of International Operations | Global Timber & Lumber Sourcing Executive</div>
        <div class="contact-bar">
            <span class="contact-item"><strong>USA:</strong> 1696 Carrington Pointe, Tucker, GA 30084</span>
            <span class="contact-item"><strong>BR:</strong> Porto Alegre, RS 91910-251</span>
        </div>
        <div class="contact-bar">
            <span class="contact-item"><strong>Email:</strong> kasper@dktimber.com | dkvendemais@gmail.com</span>
            <span class="contact-item"><strong>US Cell:</strong> +1 (470) 406-7080</span>
            <span class="contact-item"><strong>BR Cell:</strong> +55 51 99107-4142</span>
        </div>
        <div class="contact-bar" style="margin-top:4px;">
            <span class="lang-badge">English: Fluent</span>
            <span class="lang-badge">Spanish: Native/Fluent</span>
            <span class="lang-badge">Portuguese: Native/Fluent</span>
            <span style="font-weight:700; color:#E8734A; font-size:8.5pt;">• Global Travel Ready (90%) • US B1/B2 Visa</span>
        </div>
    </div>

    <div class="section-title">Executive Profile</div>
    <div class="summary-box">
        <strong>Trilingual Operations & Supply Chain Executive (English / Spanish / Portuguese)</strong> with 30+ years of cross-border experience driving multi-million dollar timber sourcing, sawmill network expansion, ocean freight logistics, and international trade between Latin America, the United States, and global markets. Hands-on leader skilled at bridging North American buyers with Latin American forestry mills, managing 15,000-hectare timber concessions, supervising 100+ industrial personnel, and orchestrating full supply chains from forest harvest to port delivery and 3PL warehouse distribution. Recognized for negotiating high-value contracts, cutting freight overhead by 12%+, and operating with complete autonomy across international jurisdictions.
    </div>

    <div class="section-title">Core Expertise & Technical Competencies</div>
    <div class="grid-2col">
        <div class="grid-item">
            <strong>Global Timber & Lumber Sourcing</strong>
            Yellow Pine, Hardwoods, Plywood, Sawmill Network Development (20+ Certified Mills across LATAM).
        </div>
        <div class="grid-item">
            <strong>Trilingual Commercial Negotiation</strong>
            English, Spanish, Portuguese (Fluent C-level executive negotiations, contract drafting, cross-border deals).
        </div>
        <div class="grid-item">
            <strong>Cross-Border Supply Chain & Logistics</strong>
            Ocean Freight, Port Operations, Transloading, Customs & Phytosanitary Compliance, 3PL/Inland Rail.
        </div>
        <div class="grid-item">
            <strong>Forestry Concession & Mill Leadership</strong>
            Industrial Mill Oversight, Harvesting Schedules, Production Planning, Quality Assurance (QA/QC).
        </div>
        <div class="grid-item">
            <strong>International Business Development</strong>
            Distributor Network Expansion, LATAM-to-US Import/Export Channels, B2B & B2C Strategy.
        </div>
        <div class="grid-item">
            <strong>Advanced Digital & E-Commerce Tools</strong>
            Financial Modeling, Advanced Excel, CRM, E-Commerce (Wayfair, Amazon Seller Central), AI Operations (Antigravity), WordPress, SEO, Google/Meta Ads.
        </div>
    </div>

    <div class="section-title">Selected Executive Achievements</div>
    <ul class="bullets">
        <li><strong>Engineered LATAM-to-US Lumber Export Pipelines:</strong> Architected and managed end-to-end supply chains sourcing raw and processed lumber from South American sawmills for major US distribution channels.</li>
        <li><strong>Cost Reduction & Logistics Optimization:</strong> Reduced international freight and logistics overhead by <strong>12%</strong> via route consolidation, carrier tariff negotiation, and streamlined port transloading.</li>
        <li><strong>Expanded Supplier Network:</strong> Developed and audited a network of <strong>20+ certified sawmills</strong> across Brazil and neighboring LATAM countries, enforcing strict export quality standards.</li>
        <li><strong>Forestry Concession Leadership:</strong> Directed operations for a <strong>15,000-hectare forestry concession</strong> and industrial mill, leading 100+ operations, logistics, and mill personnel.</li>
        <li><strong>Cross-Border Efficiency:</strong> Improved on-time container delivery rates by <strong>20%</strong> by resolving recurring customs and port bottleneck friction points.</li>
    </ul>

    <div class="section-title">Professional Experience</div>

    <div class="job-block">
        <div class="job-header">
            <span class="company">DK TIMBER <span class="job-title">— Director, International Operations & Lumber Sourcing Agent</span></span>
            <span class="date-location">Americas (Remote) | 2010 – Present</span>
        </div>
        <div class="job-desc">Direct end-to-end international sourcing, procurement, and cross-border logistics operations connecting South American timber producers with US and global import markets.</div>
        <ul class="bullets">
            <li><strong>Supplier & Mill Operations:</strong> Architected and managed a supplier ecosystem of 20+ sawmills across Brazil and LATAM, supervising production schedules, dimensional standards, and quality control.</li>
            <li><strong>End-to-End Export Logistics:</strong> Executed full export cycles including inland truck freight, Brazilian port handling, ocean freight booking, US port clearance, and final 3PL distribution.</li>
            <li><strong>Commercial Negotiations:</strong> Represented global clients in high-stakes contract negotiations with mill owners, ocean carriers, freight forwarders, and institutional buyers in English, Spanish, and Portuguese.</li>
            <li><strong>Marketplace Consortium Model:</strong> Designed a collaborative export consortium allowing small-to-midsize Latin American sawmills to aggregate volume and sell directly on US e-commerce platforms (Wayfair, Amazon Seller Central).</li>
        </ul>
    </div>

    <!-- PAGE 2 BREAK -->
    <div class="page-break"></div>

    <div class="job-block">
        <div class="job-header">
            <span class="company">MCVANTAGE BROKERAGE SERVICES LLC <span class="job-title">— Procurement & Logistics Agent</span></span>
            <span class="date-location">USA / LATAM (Remote) | 2010 – 2020</span>
        </div>
        <div class="job-desc">Managed US import operations for Latin American timber and forest products, overseeing ocean shipping, customs clearance, and inland distribution.</div>
        <ul class="bullets">
            <li>Directed ocean freight shipping, container logistics, transloading operations, and rail/truck distribution across major US ports of entry.</li>
            <li>Negotiated competitive carrier tariffs and container volume allocations, achieving a 12% reduction in landed logistics costs.</li>
            <li>Resolved complex customs clearance, phytosanitary compliance, and supply chain bottlenecks to maintain uninterrupted delivery schedules.</li>
        </ul>
    </div>

    <div class="job-block">
        <div class="job-header">
            <span class="company">CLENERGEN CORP. <span class="job-title">— Operations Manager – Renewable Energy Projects</span></span>
            <span class="date-location">UK / USA / LATAM | 2006 – 2010</span>
        </div>
        <div class="job-desc">Directed international operational logistics and supplier coordination for biomass renewable energy development projects.</div>
        <ul class="bullets">
            <li>Managed multi-jurisdictional vendor and contractor relationships across North America, South America, and Europe.</li>
            <li>Ensured compliance with international forestry biomass feedstock standards and environmental regulations.</li>
        </ul>
    </div>

    <div class="job-block">
        <div class="job-header">
            <span class="company">YAMATA <span class="job-title">— Sales Manager – Americas</span></span>
            <span class="date-location">USA / China / LATAM | 2003 – 2005</span>
        </div>
        <div class="job-desc">Led regional commercial distribution and network expansion across North and South America.</div>
        <ul class="bullets">
            <li>Served as the primary strategic liaison between China corporate headquarters and LATAM regional operations.</li>
            <li>Expanded distributor networks across LATAM, driving regional sales volume growth and market penetration.</li>
        </ul>
    </div>

    <div class="job-block">
        <div class="job-header">
            <span class="company">MADERAS DEL ORINOCO <span class="job-title">— Vice President – Mill Operations & Forestry Concession</span></span>
            <span class="date-location">Venezuela | 2000 – 2003</span>
        </div>
        <div class="job-desc">Executive oversight of a major industrial wood processing mill and 15,000-hectare commercial forestry concession.</div>
        <ul class="bullets">
            <li>Directed daily harvesting schedules, industrial mill processing, inventory control, and workforce management for 100+ employees.</li>
            <li>Ensured strict compliance with international sustainable forestry standards and safety mandates.</li>
        </ul>
    </div>

    <div class="job-block">
        <div class="job-header">
            <span class="company">ZWILLING J.A. HENCKELS <span class="job-title">— Commercial Supervisor</span></span>
            <span class="date-location">Latin America | 1994 – 1999</span>
        </div>
        <ul class="bullets">
            <li>Supervised regional commercial operations, distributor performance, and retail network expansion across LATAM.</li>
        </ul>
    </div>

    <div class="section-title">Education & Academic Credentials</div>
    <div class="job-block">
        <div class="company" style="font-size:10pt;">Instituto Universitario de Nuevas Profesiones <span style="font-weight:normal; color:#475569;">— Venezuela</span></div>
        <div style="font-size:9pt; color:#334155;">Coursework Completed in International Business & Foreign Trade</div>
    </div>

    <div class="section-title">Languages & Technical Systems Summary</div>
    <div class="summary-box" style="margin-bottom:0;">
        <p style="margin:0 0 4px 0;"><strong>Languages:</strong> English (Fluent C-level & Technical), Spanish (Native/Fluent), Portuguese (Native/Fluent).</p>
        <p style="margin:0;"><strong>Software & Digital Infrastructure:</strong> Advanced Financial & Operational Modeling (Excel), CRM Platforms, E-Commerce Systems (Wayfair, Amazon Seller Central), AI Operational Systems (Antigravity), Web Development (WordPress), SEO Optimization, Google Ads, Meta Ads & Digital Campaign Development.</p>
    </div>

</body>
</html>
"""

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    msedge = next((p for p in edge_paths if os.path.exists(p)), None)

    if msedge:
        cmd = [
            msedge, "--headless", "--disable-gpu", "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_path}", html_path
        ]
        subprocess.run(cmd, check=True)
        print(f"Generated Executive 2-Page PDF: {pdf_path} ({os.path.getsize(pdf_path)} bytes)")

if __name__ == '__main__':
    create_resume_pdf()
