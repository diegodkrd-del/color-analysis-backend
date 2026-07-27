import os
import zipfile
import shutil

plugin_dir = r'C:\Users\dkven\color_analysis_backend\wp_landing_plugin'
os.makedirs(plugin_dir, exist_ok=True)

# Build a single-file standalone plugin: chromatype-landing-page.php
# This puts everything inside ONE .php file so WordPress CANNOT fail to upload or read it!
html_path = r'C:\Users\dkven\color_analysis_backend\chromatype_wordpress_landing_page.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

wp_snippet = html_content
wp_snippet = wp_snippet.replace('<!DOCTYPE html>', '')
wp_snippet = wp_snippet.replace('<html lang="en">', '')
wp_snippet = wp_snippet.replace('</html>', '')
wp_snippet = wp_snippet.replace('<head>', '')
wp_snippet = wp_snippet.replace('</head>', '')
wp_snippet = wp_snippet.replace('<body class="bg-brand-black text-brand-cream">', '<div class="chromatype-root bg-brand-black text-brand-cream" style="margin-top:-30px; margin-left:-30px; margin-right:-30px;">')
wp_snippet = wp_snippet.replace('</body>', '</div>')

single_plugin_php = f"""<?php
/**
 * Plugin Name: CHROMATYPE Landing Page Studio
 * Plugin URI: https://chromatype.me/
 * Description: Standalone production landing page template for CHROMATYPE CIELAB 3D Color Analysis with $29 launch offer, live camera capture, direct PayPal links, and CTA slide-in modal.
 * Version: 4.0.0
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

print(f"Created Bulletproof Single-File WordPress Plugin Zip: {zip_output} ({os.path.getsize(zip_output)} bytes)")
