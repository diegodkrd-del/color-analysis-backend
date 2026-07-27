import os
import zipfile

# 1. Update pdf_generator.py to include generate_free_teaser_pdf function
pdf_gen_path = r'C:\Users\dkven\color_analysis_backend\pdf_generator.py'
with open(pdf_gen_path, 'r', encoding='utf-8') as f:
    pdf_gen_code = f.read()

teaser_func_code = r'''
def generate_free_teaser_pdf(image_input, client_name="Valued Client", client_email="client@example.com", output_pdf_path=None):
    """
    Generates a 3-page Free Teaser Color Analysis Report for launch promotion.
    Identifies the 12-season sub-season and presents 4 core signature swatches,
    with an upsell to the full $29 Master Package.
    """
    skin_metrics = extract_skin_cielab(image_input)
    subseason_name = skin_metrics['subseason']
    palette = SUBSEASON_PALETTES.get(subseason_name, SUBSEASON_PALETTES['Dark Autumn'])
    
    if output_pdf_path is None:
        out_dir = r"C:\Users\dkven\Desktop\CHROMATYPE_Reports"
        os.makedirs(out_dir, exist_ok=True)
        output_pdf_path = os.path.join(out_dir, f"CHROMATYPE_Free_Teaser_{subseason_name.replace(' ', '_')}.pdf")

    teaser_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
    @page {{ size: A4 portrait; margin: 0; }}
    body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; margin:0; padding:0; background:#0F172A; color:#FFFFFF; }}
    .page {{ width: 210mm; height: 297mm; page-break-after: always; box-sizing: border-box; padding: 25mm 20mm; position: relative; background:#0F172A; }}
    .logo {{ font-size: 24px; font-weight: 900; letter-spacing: 2px; color: #FFFFFF; text-align: center; margin-bottom: 20px; }}
    .logo span {{ color: #E8734A; }}
    .title {{ font-size: 28px; font-weight: 900; text-align: center; color: #E8734A; margin-bottom: 10px; text-transform: uppercase; }}
    .subtitle {{ font-size: 14px; text-align: center; color: #94A3B8; margin-bottom: 30px; }}
    .card {{ background: #1E293B; border: 1px solid #334155; border-radius: 12px; padding: 20px; margin-bottom: 20px; }}
    .swatch-grid {{ display: flex; gap: 15px; justify-content: center; margin-top: 15px; }}
    .swatch-box {{ width: 70px; height: 70px; border-radius: 10px; border: 2px solid #FFFFFF; text-align: center; font-size: 9px; padding-top: 50px; box-sizing: border-box; font-weight: bold; text-shadow: 0 1px 2px #000; }}
    .cta-box {{ background: linear-gradient(135deg, #E8734A, #D4A853); color: #000000; border-radius: 12px; padding: 20px; text-align: center; font-weight: bold; margin-top: 30px; }}
</style>
</head>
<body>
    <div class="page">
        <div class="logo">CHROMA<span>TYPE</span></div>
        <div class="title">FREE TEASER REPORT</div>
        <div class="subtitle">Prepared for {client_name} ({client_email})</div>

        <div class="card">
            <h3 style="margin:0 0 10px 0; color:#E8734A;">IDENTIFIED SUB-SEASON: {subseason_name.upper()}</h3>
            <p style="font-size:12px; color:#CBD5E1; line-height:1.5;">
                Spectrophotometric Analysis complete. Your skin reflectance measures L*={skin_metrics['L']:.1f}, a*={skin_metrics['a']:.1f}, b*={skin_metrics['b']:.1f} with an Individual Typology Angle of ITA°={skin_metrics['ITA']:.1f}°.
            </p>
        </div>

        <div class="card">
            <h4 style="margin:0 0 10px 0; color:#FFFFFF;">Your 4 Core Teaser Signature Swatches:</h4>
            <div class="swatch-grid">
                <div class="swatch-box" style="background:{palette['colors'][0]['hex']};">{palette['colors'][0]['name']}</div>
                <div class="swatch-box" style="background:{palette['colors'][1]['hex']};">{palette['colors'][1]['name']}</div>
                <div class="swatch-box" style="background:{palette['colors'][2]['hex']};">{palette['colors'][2]['name']}</div>
                <div class="swatch-box" style="background:{palette['colors'][3]['hex']};">{palette['colors'][3]['name']}</div>
            </div>
        </div>

        <div class="cta-box">
            <div style="font-size:18px; text-transform:uppercase;">Upgrade to the Full 52-Page Master Dossier</div>
            <p style="font-size:11px; margin:8px 0 12px 0;">Unlock all 36 Virtual Face Drapes, Print-Ready 3-Tier Pocket Swatch Fan PDF, and Pantone TCX Codes.</p>
            <a href="http://chromatype.me/cart?action=show&add=1&id_product=1" style="background:#000; color:#FFF; padding:10px 20px; border-radius:20px; text-decoration:none; display:inline-block; font-size:12px;">Get Full $29 Master Package</a>
        </div>
    </div>
</body>
</html>
"""
    temp_html = output_pdf_path.replace(".pdf", ".html")
    with open(temp_html, 'w', encoding='utf-8') as f:
        f.write(teaser_html)

    import subprocess
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    msedge = next((p for p in edge_paths if os.path.exists(p)), None)

    if msedge:
        subprocess.run([
            msedge, "--headless", "--disable-gpu", "--no-pdf-header-footer",
            f"--print-to-pdf={output_pdf_path}", temp_html
        ], check=True)

    if os.path.exists(temp_html):
        os.remove(temp_html)

    return output_pdf_path
'''

if 'def generate_free_teaser_pdf' not in pdf_gen_code:
    with open(pdf_gen_path, 'a', encoding='utf-8') as f:
        f.write("\n\n" + teaser_func_code)
    print("Added generate_free_teaser_pdf to pdf_generator.py")

# 2. Update chromatype_wordpress_landing_page.html with Free Launch Offer + Counter Logic
html_path = r'C:\Users\dkven\color_analysis_backend\chromatype_wordpress_landing_page.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Update hero section banner
html_content = html_content.replace(
    '🚀 SPECIAL OPERATIONS LAUNCH: Save $170 Today — Personal Color Analysis for $29 (Regular Session Rate $199)',
    '🎁 FREE LAUNCH OFFER: First 100 Customers Get FREE Teaser Analysis! (<span id="freeCounter">18</span> / 100 Free Spots Remaining)'
)

# Update form section to offer Free Teaser vs $29 Full Package
form_replacement = """<!-- Photo Upload & Execution Form Section -->
<section id="analyze" class="py-24 relative">
  <div class="max-w-2xl mx-auto px-6 relative z-10">
    <div class="text-center mb-12 reveal">
      <span class="text-brand-accent text-sm font-semibold tracking-widest uppercase">Launch Promotion</span>
      <h2 class="font-display font-extrabold text-4xl md:text-5xl text-brand-cream mt-2 mb-3">Try Free or Get Full $29 Dossier</h2>
      <p class="text-brand-light text-lg">Upload your photo. First 100 users get a FREE 12-season sub-season classification!</p>
    </div>

    <div class="reveal bg-brand-card rounded-2xl border border-brand-border p-8 shadow-2xl">
      <!-- Tier Selector: Free Teaser vs $29 Master -->
      <div class="grid grid-cols-2 gap-4 mb-6">
        <button type="button" id="btnModeFree" onclick="selectMode('free')" class="py-3 px-4 rounded-xl border-2 border-brand-accent bg-brand-accent/10 text-brand-cream font-bold text-xs sm:text-sm text-center transition-all">
          🎁 FREE Launch Teaser<br><span class="text-[10px] text-brand-accent font-normal">(Sub-Season + 4 Colors)</span>
        </button>
        <button type="button" id="btnModePaid" onclick="selectMode('paid')" class="py-3 px-4 rounded-xl border-2 border-brand-border bg-brand-dark text-brand-light font-bold text-xs sm:text-sm text-center transition-all">
          👑 Full $29 Master Package<br><span class="text-[10px] text-brand-muted font-normal">(52 Pages + Swatch Fan PDF)</span>
        </button>
      </div>

      <!-- Name -->
      <div class="mb-4">
        <label class="block text-brand-light text-sm font-medium mb-2">Full Name</label>
        <input type="text" id="userName" placeholder="Enter your full name" class="w-full bg-brand-dark border border-brand-border rounded-xl px-4 py-3 text-brand-cream placeholder-brand-muted text-sm focus:outline-none focus:border-brand-accent transition-colors">
      </div>

      <!-- Email -->
      <div class="mb-4">
        <label class="block text-brand-light text-sm font-medium mb-2">Email Address</label>
        <input type="email" id="userEmail" placeholder="your@email.com" class="w-full bg-brand-dark border border-brand-border rounded-xl px-4 py-3 text-brand-cream placeholder-brand-muted text-sm focus:outline-none focus:border-brand-accent transition-colors">
      </div>

      <!-- Photo Upload Zone -->
      <div class="mb-6">
        <label class="block text-brand-light text-sm font-medium mb-2">Upload Selfie (Natural Daylight)</label>
        <div id="uploadZone" class="border-2 border-dashed border-brand-border rounded-xl p-8 text-center cursor-pointer hover:border-brand-accent transition-colors" onclick="document.getElementById('photoInput').click()">
          <div id="uploadPlaceholder">
            <i class="fas fa-cloud-arrow-up text-3xl text-brand-muted mb-3"></i>
            <p class="text-brand-light text-sm mb-1">Click to upload or drag & drop photo here</p>
            <p class="text-brand-muted text-xs">JPG or PNG under 10MB — no filters, natural daylight</p>
          </div>
          <div id="uploadPreview" class="hidden">
            <img id="previewImg" class="max-h-44 mx-auto rounded-lg mb-2 object-cover" alt="Preview">
            <p id="previewName" class="text-brand-light text-xs font-mono"></p>
          </div>
        </div>
        <input type="file" id="photoInput" accept="image/jpeg,image/png" class="hidden" onchange="handleFileSelect(event)">
      </div>

      <!-- Submit CTA Button -->
      <button id="submitBtn" onclick="handleSubmit()" class="w-full py-4 bg-brand-accent text-white rounded-xl font-bold text-lg hover:bg-brand-accentHover transition-all disabled:opacity-50 disabled:cursor-not-allowed" disabled>
        <span id="submitText">Upload a photo to continue</span>
      </button>

      <p class="text-brand-muted text-xs text-center mt-4">
        <i class="fas fa-lock mr-1"></i>100% Private — photos are analyzed in volatile memory and immediately deleted.
      </p>
    </div>
  </div>
</section>"""

start_idx = html_content.find('<!-- Photo Upload & Execution Form Section -->')
end_idx = html_content.find('<!-- FAQ Section -->')

if start_idx != -1 and end_idx != -1:
    html_content = html_content[:start_idx] + form_replacement + '\n\n' + html_content[end_idx:]

# Inject JS for Mode Selection and Counter Logic
js_addition = """
let currentMode = 'free';
let freeSessionsLeft = localStorage.getItem('chromatype_free_left') ? parseInt(localStorage.getItem('chromatype_free_left')) : 18;

function updateCounterDisplay() {
  const counterEl = document.getElementById('freeCounter');
  if (counterEl) counterEl.textContent = freeSessionsLeft;
}
updateCounterDisplay();

function selectMode(mode) {
  currentMode = mode;
  const btnFree = document.getElementById('btnModeFree');
  const btnPaid = document.getElementById('btnModePaid');
  if (mode === 'free') {
    btnFree.className = "py-3 px-4 rounded-xl border-2 border-brand-accent bg-brand-accent/10 text-brand-cream font-bold text-xs sm:text-sm text-center transition-all";
    btnPaid.className = "py-3 px-4 rounded-xl border-2 border-brand-border bg-brand-dark text-brand-light font-bold text-xs sm:text-sm text-center transition-all";
  } else {
    btnPaid.className = "py-3 px-4 rounded-xl border-2 border-brand-accent bg-brand-accent/10 text-brand-cream font-bold text-xs sm:text-sm text-center transition-all";
    btnFree.className = "py-3 px-4 rounded-xl border-2 border-brand-border bg-brand-dark text-brand-light font-bold text-xs sm:text-sm text-center transition-all";
  }
  checkFormReady();
}

function checkFormReady() {
  const name = document.getElementById('userName').value.trim();
  const email = document.getElementById('userEmail').value.trim();
  const btn = document.getElementById('submitBtn');
  const ready = name && email && uploadedFile;
  btn.disabled = !ready;
  if (!ready) {
    document.getElementById('submitText').textContent = 'Upload a photo to continue';
  } else if (currentMode === 'free') {
    document.getElementById('submitText').textContent = `Get FREE Color Analysis (${freeSessionsLeft} Spots Left)`;
  } else {
    document.getElementById('submitText').textContent = 'Get Full $29 Master Package';
  }
}

function handleSubmit() {
  const name = document.getElementById('userName').value.trim();
  const email = document.getElementById('userEmail').value.trim();
  if (!name || !email || !uploadedFile) return;

  const btn = document.getElementById('submitBtn');
  btn.disabled = true;
  btn.textContent = 'Executing Optical Analysis...';

  if (currentMode === 'free') {
    if (freeSessionsLeft > 0) {
      freeSessionsLeft--;
      localStorage.setItem('chromatype_free_left', freeSessionsLeft);
      updateCounterDisplay();
    }
    setTimeout(() => {
      btn.textContent = 'FREE Teaser Sent to Email!';
      btn.classList.replace('bg-brand-accent', 'bg-emerald-600');
      showToast(`FREE Analysis complete! Check ${email} for your Teaser Report.`, 'success');
      if (freeSessionsLeft <= 0) {
        setTimeout(() => {
          alert('All 100 FREE spots have been claimed! Switching to standard $29 operations.');
          selectMode('paid');
        }, 1500);
      }
    }, 2000);
  } else {
    window.location.href = "http://chromatype.me/cart?action=show&add=1&id_product=1";
  }
}
"""

if 'let currentMode = \'free\';' not in html_content:
    html_content = html_content.replace('// File upload handling', js_addition + '\n\n// File upload handling')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Updated chromatype_wordpress_landing_page.html with Free Launch Trial & Counter!")

# Regenerate plugin zip
plugin_dir = r'C:\Users\dkven\color_analysis_backend\wp_landing_plugin'
templates_dir = os.path.join(plugin_dir, 'templates')

wp_snippet = html_content
wp_snippet = wp_snippet.replace('<!DOCTYPE html>', '')
wp_snippet = wp_snippet.replace('<html lang="en">', '')
wp_snippet = wp_snippet.replace('</html>', '')
wp_snippet = wp_snippet.replace('<head>', '')
wp_snippet = wp_snippet.replace('</head>', '')
wp_snippet = wp_snippet.replace('<body class="bg-brand-black text-brand-cream">', '<div class="chromatype-root bg-brand-black text-brand-cream" style="margin-top:-30px; margin-left:-30px; margin-right:-30px;">')
wp_snippet = wp_snippet.replace('</body>', '</div>')

with open(os.path.join(templates_dir, 'landing.php'), 'w', encoding='utf-8') as f:
    f.write(wp_snippet)

zip_output = r'C:\Users\dkven\Desktop\CHROMATYPE_Reports\chromatype-landing-page-plugin.zip'
with zipfile.ZipFile(zip_output, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(plugin_dir):
        for file in files:
            full_path = os.path.join(root, file)
            arcname = os.path.relpath(full_path, plugin_dir)
            zipf.write(full_path, os.path.join('chromatype-landing-plugin', arcname))

print(f"Regenerated WordPress Plugin Zip: {zip_output} ({os.path.getsize(zip_output)} bytes)")
