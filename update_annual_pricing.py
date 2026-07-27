import os
import zipfile

html_path = r'C:\Users\dkven\color_analysis_backend\chromatype_wordpress_landing_page.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Updated Pricing Section with explicit 12-Month Annual License periods for $150/yr and $2500/yr
pricing_replacement = """<!-- Pricing Section -->
<section id="pricing" class="py-24 relative bg-brand-dark/40 border-t border-brand-border">
  <div class="max-w-6xl mx-auto px-6">
    <div class="text-center mb-16 reveal">
      <span class="text-brand-accent text-sm font-semibold tracking-widest uppercase">Start Operations Special</span>
      <h2 class="font-display font-extrabold text-4xl md:text-5xl text-brand-cream mt-2 mb-4">Select Your CHROMATYPE Pass</h2>
      <p class="text-brand-light text-lg max-w-2xl mx-auto">Choose between our single consumer report pass or our 12-month commercial operator franchise licenses.</p>
    </div>

    <div class="grid md:grid-cols-3 gap-8 items-stretch">
      <!-- Product #1: B2C Consumer Pass ($29 One-Time) -->
      <div class="reveal pricing-featured bg-brand-card rounded-2xl p-8 flex flex-col justify-between season-card relative">
        <div>
          <div class="flex items-center justify-between mb-2">
            <div class="text-brand-accent text-xs font-bold uppercase tracking-wider">Product #1 • One-Time Download Pass</div>
            <span class="px-3 py-1 bg-brand-accent/20 text-brand-accent text-xs font-bold rounded-full">Most Popular</span>
          </div>
          <div class="flex items-baseline gap-1 mb-2">
            <span class="font-display font-black text-5xl text-brand-cream">$29</span>
            <span class="text-brand-muted text-sm font-medium">/ one-time</span>
            <span class="text-brand-muted text-sm line-through ml-2">$199</span>
          </div>
          <p class="text-brand-light text-xs font-semibold text-brand-gold mb-6">✓ One-Time Payment — Lifetime Access to Digital Files</p>
          <ul class="space-y-3 mb-8 text-sm text-brand-light">
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>12 Season CIELAB Spectrophotometric Analysis</li>
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>52-Page Master Dossier PDF (Instant Download)</li>
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>36 Half-Page Virtual Face Drapes</li>
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>Print-Ready 3-Tier Pocket Swatch Fan PDF ($29 Value)</li>
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>432 Pantone TCX Matched Swatch Codes</li>
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>Makeup & Jewelry Tone Blueprint</li>
          </ul>
        </div>
        <a href="http://chromatype.me/cart?action=show&add=1&id_product=1" class="block text-center py-4 bg-brand-accent text-white rounded-xl font-bold hover:bg-brand-accentHover transition-all shadow-lg">
          Buy $29 One-Time Pass
        </a>
      </div>

      <!-- Product #2: B2B Beginner Operator Pass ($150/Year) -->
      <div class="reveal bg-brand-card rounded-2xl border border-brand-border p-8 flex flex-col justify-between season-card">
        <div>
          <div class="text-brand-gold text-xs font-bold uppercase tracking-wider mb-2">Product #2 • 12-Month Beginner License</div>
          <div class="flex items-baseline gap-1 mb-2">
            <span class="font-display font-black text-5xl text-brand-cream">$150</span>
            <span class="text-brand-muted text-sm font-medium">/ 12 months</span>
            <span class="text-brand-muted text-sm line-through ml-2">$750/yr</span>
          </div>
          <p class="text-brand-light text-xs font-semibold text-brand-gold mb-6">✓ 12-Month Annual Commercial Operator Access</p>
          <ul class="space-y-3 mb-8 text-sm text-brand-light">
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>12-Month Commercial Operator Pass</li>
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>Right to sell $29 to $199 client sessions</li>
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>Set your own brand pricing & profit strategy</li>
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>Complete 12-Season Master Guide PDF Suite</li>
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>Print-Ready Swatch Fan Master Files</li>
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>Annual license renewal rights</li>
          </ul>
        </div>
        <a href="http://chromatype.me/cart?action=show&add=1&id_product=2" class="block text-center py-3 border border-brand-gold/40 rounded-xl text-brand-gold font-bold hover:border-brand-gold hover:bg-brand-gold/10 transition-all">
          Get $150 Annual License
        </a>
      </div>

      <!-- Product #3: B2B Full Commercial Suite ($2,500/Year) -->
      <div class="reveal bg-brand-card rounded-2xl border border-brand-border p-8 flex flex-col justify-between season-card">
        <div>
          <div class="text-brand-cream text-xs font-bold uppercase tracking-wider mb-2">Product #3 • 12-Month Commercial Franchise</div>
          <div class="flex items-baseline gap-1 mb-2">
            <span class="font-display font-black text-5xl text-brand-cream">$2,500</span>
            <span class="text-brand-muted text-sm font-medium">/ 12 months</span>
            <span class="text-brand-muted text-sm line-through ml-2">$10,000/yr</span>
          </div>
          <p class="text-brand-light text-xs font-semibold text-brand-gold mb-6">✓ 12-Month Full Commercial Franchise Suite</p>
          <ul class="space-y-3 mb-8 text-sm text-brand-light">
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>12-Month Full Commercial Resale Franchise</li>
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>White-Label Custom PDF Report Rights</li>
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>Unlimited Client Session Volume for 1 Year</li>
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>Dedicated Priority Processing Queue</li>
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>1-on-1 Studio Onboarding & Support</li>
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>Annual franchise renewal lock</li>
          </ul>
        </div>
        <a href="http://chromatype.me/cart?action=show&add=1&id_product=3" class="block text-center py-3 border border-brand-border rounded-xl text-brand-cream font-bold hover:border-brand-accent hover:text-brand-accent transition-all">
          Get $2,500 Annual Franchise
        </a>
      </div>
    </div>
  </div>
</section>"""

start_idx = content.find('<!-- Pricing Section -->')
end_idx = content.find('<!-- Photo Upload & Execution Form Section -->')

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + pricing_replacement + '\n\n' + content[end_idx:]

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated chromatype_wordpress_landing_page.html with 12-Month Annual License periods!")

# Regenerate plugin zip
plugin_dir = r'C:\Users\dkven\color_analysis_backend\wp_landing_plugin'
templates_dir = os.path.join(plugin_dir, 'templates')

wp_snippet = content
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
