import os
import zipfile
import shutil

backend_dir = r'C:\Users\dkven\color_analysis_backend'
desktop_dir = r'C:\Users\dkven\Desktop'

html_path = os.path.join(backend_dir, 'chromatype_wordpress_landing_page.html')
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Make sure 4-Photo Intake & Makeup Masterclass are fully integrated in chromatype_wordpress_landing_page.html
plugin_dir = os.path.join(backend_dir, 'wp_landing_plugin')
templates_dir = os.path.join(plugin_dir, 'templates')
os.makedirs(templates_dir, exist_ok=True)

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
 * Description: Production-ready landing page template for CHROMATYPE CIELAB 3D Color Analysis with $29 launch offer, 4-photo intake (face, hand, iris, mucosa), live camera capture, direct PayPal links, hand/nail polish white paper matching, 432 Pantone TCX drapes, and DIY makeup masterclass blueprint.
 * Version: 7.0.0
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

# Create Zip at root Desktop & Reports folder
zip_output_desktop = os.path.join(desktop_dir, 'chromatype-landing-page-plugin.zip')
zip_output_reports = os.path.join(desktop_dir, 'CHROMATYPE_Reports', 'chromatype-landing-page-plugin.zip')

with zipfile.ZipFile(zip_output_desktop, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(single_php_file, 'chromatype-landing-page.php')

shutil.copyfile(zip_output_desktop, zip_output_reports)

print(f"Created Updated WordPress Plugin Zip (v7.0.0): {zip_output_desktop} ({os.path.getsize(zip_output_desktop)} bytes)")
