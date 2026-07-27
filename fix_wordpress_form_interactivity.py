import os
import zipfile

html_path = r'C:\Users\dkven\color_analysis_backend\chromatype_wordpress_landing_page.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the Photo Upload Zone with a fail-safe, ultra-clear interactive zone with Native File Picker + Demo Sample Photo button
interactive_form_zone = """<!-- Photo Upload & Camera Selector Zone -->
      <div class="mb-6">
        <label class="block text-brand-light text-sm font-medium mb-2">Provide Your Selfie (Natural Daylight)</label>
        
        <!-- Action Buttons -->
        <div class="grid grid-cols-2 gap-3 mb-3">
          <button type="button" onclick="openCameraModal()" class="py-3 px-4 bg-brand-accent/20 border border-brand-accent rounded-xl text-brand-cream font-semibold text-xs hover:bg-brand-accent/30 transition-all flex items-center justify-center gap-2">
            <i class="fas fa-camera text-brand-accent text-sm"></i> Take Live Selfie
          </button>
          <button type="button" onclick="triggerFileSelect()" class="py-3 px-4 bg-brand-card border border-brand-border rounded-xl text-brand-cream font-semibold text-xs hover:border-brand-accent transition-all flex items-center justify-center gap-2">
            <i class="fas fa-folder-open text-brand-gold text-sm"></i> Browse Photo File
          </button>
        </div>

        <!-- Big Drag & Drop Zone -->
        <div id="uploadZone" class="border-2 border-dashed border-brand-accent/50 bg-brand-dark/80 rounded-xl p-6 text-center cursor-pointer hover:border-brand-accent transition-all mb-3" onclick="triggerFileSelect()">
          <div id="uploadPlaceholder">
            <i class="fas fa-cloud-arrow-up text-3xl text-brand-accent mb-2"></i>
            <p class="text-brand-cream text-sm font-medium mb-1">Click anywhere here to select your photo</p>
            <p class="text-brand-muted text-xs">JPG or PNG under 10MB — natural daylight</p>
          </div>
          <div id="uploadPreview" class="hidden">
            <img id="previewImg" class="max-h-44 mx-auto rounded-lg mb-2 object-cover border border-brand-border" alt="Preview">
            <p id="previewName" class="text-brand-accent text-xs font-mono font-bold"></p>
          </div>
        </div>

        <!-- Native File Input (Always Accessible) -->
        <input type="file" id="photoInput" accept="image/jpeg,image/png" class="w-full text-xs text-brand-light bg-brand-dark border border-brand-border rounded-lg p-2 cursor-pointer" onchange="handleFileSelect(event)">
      </div>"""

start_zone = content.find('<!-- Photo Upload & Camera Selector Zone -->')
end_zone = content.find('<!-- Submit CTA Button -->')

if start_zone != -1 and end_zone != -1:
    content = content[:start_zone] + interactive_form_zone + '\n\n      ' + content[end_zone:]

# Update JS helper function triggerFileSelect
js_trigger = """
function triggerFileSelect() {
  const inp = document.getElementById('photoInput');
  if (inp) inp.click();
}
"""

if 'function triggerFileSelect()' not in content:
    content = content.replace('let uploadedFile = null;', js_trigger + '\n\nlet uploadedFile = null;')

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

single_plugin_php = f"""<?php
/**
 * Plugin Name: CHROMATYPE Landing Page Studio
 * Plugin URI: https://chromatype.me/
 * Description: Standalone production landing page template for CHROMATYPE CIELAB 3D Color Analysis with $29 launch offer, live camera capture, direct PayPal links, and CTA slide-in modal.
 * Version: 4.5.0
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

print(f"Created Fail-Safe WordPress Plugin Zip (v4.5.0): {zip_output} ({os.path.getsize(zip_output)} bytes)")
