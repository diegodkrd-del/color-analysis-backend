import os
import zipfile

html_path = r'C:\Users\dkven\color_analysis_backend\chromatype_wordpress_landing_page.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix Logo Styling (remove giant white box overlay)
old_logo_nav = '<img src="http://chromatype.me/img/logo-1784993471.jpg" alt="CHROMATYPE Studio" class="h-10 w-auto object-contain rounded-md">'
new_logo_nav = '<div class="bg-white/95 px-3 py-1.5 rounded-xl shadow-md border border-brand-border/40 inline-flex items-center"><img src="http://chromatype.me/img/logo-1784993471.jpg" alt="CHROMATYPE Studio" class="h-7 w-auto object-contain"></div>'

if old_logo_nav in content:
    content = content.replace(old_logo_nav, new_logo_nav)

# 2. Make Full Name optional so the Submit Button UNLOCKS IMMEDIATELY as soon as Email + Photo are selected
old_check_ready_js = """function checkFormReady() {
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
}"""

new_check_ready_js = """function checkFormReady() {
  const email = document.getElementById('userEmail').value.trim();
  const btn = document.getElementById('submitBtn');
  // Unlock button as long as photo is selected (and email if free mode)
  const ready = uploadedFile && (currentMode !== 'free' || email !== '');
  btn.disabled = !ready;
  if (!ready) {
    if (!uploadedFile) {
      document.getElementById('submitText').textContent = 'Upload a photo to continue';
    } else {
      document.getElementById('submitText').textContent = 'Enter email to receive report';
    }
  } else if (currentMode === 'free') {
    document.getElementById('submitText').textContent = `Get FREE Color Analysis (${freeSessionsLeft} Spots Left)`;
  } else {
    document.getElementById('submitText').textContent = 'Get Full $29 Master Package';
  }
}"""

if old_check_ready_js in content:
    content = content.replace(old_check_ready_js, new_check_ready_js)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Update plugin PHP file & single-file PHP plugin
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

single_plugin_php = f"""<?php
/**
 * Plugin Name: CHROMATYPE Landing Page Studio
 * Plugin URI: https://chromatype.me/
 * Description: Standalone production landing page template for CHROMATYPE CIELAB 3D Color Analysis with $29 launch offer, live camera capture, direct PayPal links, and CTA slide-in modal.
 * Version: 5.0.0
 * Author: CHROMATYPE Studio
 * Author URI: https://chromatype.me/
 */

if (!defined('ABSPATH')) {{
    exit;
}}

class CHROMATYPE_Standalone_Plugin {{
    public function __construct() {{
        add_shortcode('chromatype_landing_page', array($this, 'render_landing'));
        add_shortcode('chromatype', array($this, 'render_landing'));
        add_shortcode('chromatype_studio', array($this, 'render_landing'));
    }}

    public function render_landing() {{
        ob_start();
        ?>
        {wp_snippet}
        <?php
        return ob_get_clean();
    }}
}}

new CHROMATYPE_Standalone_Plugin();
"""

single_php_file = os.path.join(plugin_dir, 'chromatype-landing-page.php')
with open(single_php_file, 'w', encoding='utf-8') as f:
    f.write(single_plugin_php)

# Create Bulletproof Zip at root Desktop
zip_output = r'C:\Users\dkven\Desktop\chromatype-landing-page-plugin.zip'
with zipfile.ZipFile(zip_output, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(single_php_file, 'chromatype-landing-page.php')

print(f"Created Updated WordPress Plugin Zip (v5.0.0): {zip_output} ({os.path.getsize(zip_output)} bytes)")
