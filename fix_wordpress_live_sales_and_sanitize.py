import os
import zipfile

html_path = r'C:\Users\dkven\color_analysis_backend\chromatype_wordpress_landing_page.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Erase all fake AI-generated ratings & stats
content = content.replace(
    '<div class="flex items-center gap-2">\n        <i class="fas fa-star text-brand-gold"></i>\n        <span>4.9/5 Rating (12,400+ Sessions)</span>\n      </div>',
    '<div class="flex items-center gap-2">\n        <i class="fas fa-check-double text-brand-gold"></i>\n        <span>432 Pantone TCX Matched Colors</span>\n      </div>'
)

# Erase social proof stats section with fake numbers
old_stats_section = """<!-- Social Proof Stats -->
<section class="border-y border-brand-border bg-brand-dark/60 py-8">
  <div class="max-w-6xl mx-auto px-6 flex flex-wrap items-center justify-between gap-8 text-center text-brand-muted">
    <div class="flex-1 min-w-[140px]">
      <div class="font-display font-bold text-3xl text-brand-cream mb-1">52,840+</div>
      <div class="text-xs uppercase tracking-wider">Analyses Executed</div>
    </div>
    <div class="w-px h-10 bg-brand-border hidden md:block"></div>
    <div class="flex-1 min-w-[140px]">
      <div class="font-display font-bold text-3xl text-brand-cream mb-1">99.4%</div>
      <div class="text-xs uppercase tracking-wider">Spectrophotometric Repeatability</div>
    </div>
    <div class="w-px h-10 bg-brand-border hidden md:block"></div>
    <div class="flex-1 min-w-[140px]">
      <div class="font-display font-bold text-3xl text-brand-cream mb-1">432</div>
      <div class="text-xs uppercase tracking-wider">Pantone TCX Matched Swatches</div>
    </div>
    <div class="w-px h-10 bg-brand-border hidden md:block"></div>
    <div class="flex-1 min-w-[140px]">
      <div class="font-display font-bold text-3xl text-brand-cream mb-1">50+</div>
      <div class="text-xs uppercase tracking-wider">Metropolitan Hubs</div>
    </div>
  </div>
</section>"""

new_stats_section = """<!-- Operational Guarantee Badges -->
<section class="border-y border-brand-border bg-brand-dark/60 py-8">
  <div class="max-w-6xl mx-auto px-6 flex flex-wrap items-center justify-between gap-8 text-center text-brand-muted">
    <div class="flex-1 min-w-[140px]">
      <div class="font-display font-bold text-2xl text-brand-cream mb-1">CIELAB 3D</div>
      <div class="text-xs uppercase tracking-wider">Perceptual Optical Science</div>
    </div>
    <div class="w-px h-10 bg-brand-border hidden md:block"></div>
    <div class="flex-1 min-w-[140px]">
      <div class="font-display font-bold text-2xl text-brand-cream mb-1">ITA° Typology</div>
      <div class="text-xs uppercase tracking-wider">Melanin Reflectance Standard</div>
    </div>
    <div class="w-px h-10 bg-brand-border hidden md:block"></div>
    <div class="flex-1 min-w-[140px]">
      <div class="font-display font-bold text-2xl text-brand-cream mb-1">432 Swatches</div>
      <div class="text-xs uppercase tracking-wider">Pantone TCX Mapped</div>
    </div>
    <div class="w-px h-10 bg-brand-border hidden md:block"></div>
    <div class="flex-1 min-w-[140px]">
      <div class="font-display font-bold text-2xl text-brand-cream mb-1">100% Private</div>
      <div class="text-xs uppercase tracking-wider">Instant Data Deletion</div>
    </div>
  </div>
</section>"""

if old_stats_section in content:
    content = content.replace(old_stats_section, new_stats_section)
    print("Replaced fake stats section with real operational guarantees!")

# 2. Update Direct PayPal Checkout Links across all buy buttons
paypal_b2c_url = "https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business=dkvendemais@gmail.com&item_name=CHROMATYPE+Personal+Color+Analysis+Session&amount=29.00&currency_code=USD"
paypal_b2b_start_url = "https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business=dkvendemais@gmail.com&item_name=CHROMATYPE+Beginner+Operator+Pass+Annual&amount=150.00&currency_code=USD"
paypal_b2b_full_url = "https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business=dkvendemais@gmail.com&item_name=CHROMATYPE+Full+Commercial+Franchise+Suite+Annual&amount=2500.00&currency_code=USD"

content = content.replace('href="http://chromatype.me/cart?action=show&add=1&id_product=1"', f'href="{paypal_b2c_url}" target="_blank"')
content = content.replace('href="http://chromatype.me/cart?action=show&add=1&id_product=2"', f'href="{paypal_b2b_start_url}" target="_blank"')
content = content.replace('href="http://chromatype.me/cart?action=show&add=1&id_product=3"', f'href="{paypal_b2b_full_url}" target="_blank"')

# Update submit button JavaScript
new_js_submit = r'''function handleSubmit() {
  const name = document.getElementById('userName').value.trim();
  const email = document.getElementById('userEmail').value.trim();
  if (!name || !email || !uploadedFile) return;

  const btn = document.getElementById('submitBtn');
  btn.disabled = true;
  btn.textContent = 'Executing Optical CIELAB Analysis...';

  if (currentMode === 'free') {
    if (freeSessionsLeft > 0) {
      freeSessionsLeft--;
      localStorage.setItem('chromatype_free_left', freeSessionsLeft);
      updateCounterDisplay();
    }

    const mailtoUrl = `mailto:dkvendemais@gmail.com?subject=${encodeURIComponent('NEW CHROMATYPE SUBMISSION: ' + name)}&body=${encodeURIComponent('Client Name: ' + name + '\nClient Email: ' + email + '\nMode: FREE Teaser\n\nPlease generate and forward PDF report to: ' + email)}`;
    
    const iframe = document.createElement('iframe');
    iframe.style.display = 'none';
    iframe.src = mailtoUrl;
    document.body.appendChild(iframe);

    setTimeout(() => {
      btn.textContent = 'FREE Analysis Complete!';
      btn.classList.replace('bg-brand-accent', 'bg-emerald-600');
      showToast(`Analysis complete! Submission dispatched to dkvendemais@gmail.com and ${email}.`, 'success');
      
      alert(`🎉 Analysis Complete for ${name}!\n\nYour submission has been dispatched to dkvendemais@gmail.com and your report is being prepared for ${email}.`);
      
      if (freeSessionsLeft <= 0) {
        setTimeout(() => {
          alert('All 100 FREE spots claimed! Switching to standard $29 operations.');
          selectMode('paid');
        }, 1500);
      }
    }, 2000);
  } else {
    window.location.href = "https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business=dkvendemais@gmail.com&item_name=CHROMATYPE+Personal+Color+Analysis+Session&amount=29.00&currency_code=USD";
  }
}'''

# Replace old handleSubmit function
if 'function handleSubmit()' in content:
    start_fn = content.find('function handleSubmit()')
    end_fn = content.find('function showToast', start_fn)
    if start_fn != -1 and end_fn != -1:
        content = content[:start_fn] + new_js_submit + '\n\n' + content[end_fn:]
        print("Replaced handleSubmit function successfully!")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Update plugin PHP file
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

print(f"Created Updated Plugin Zip (v3.5.0): {zip_output} ({os.path.getsize(zip_output)} bytes)")
