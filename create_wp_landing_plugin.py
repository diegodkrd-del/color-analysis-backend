import os
import zipfile

plugin_dir = r'C:\Users\dkven\color_analysis_backend\wp_landing_plugin'
os.makedirs(plugin_dir, exist_ok=True)

# Main Plugin PHP File
plugin_php = r"""<?php
/**
 * Plugin Name: CHROMATYPE Landing Page & Conversion Studio
 * Plugin URI: https://chromatype.me/
 * Description: Production-ready landing page template for CHROMATYPE CIELAB 3D Color Analysis with $29 launch offer and high-converting CTA slide-in modal.
 * Version: 2.5.0
 * Author: CHROMATYPE Studio
 * Author URI: https://chromatype.me/
 */

if (!defined('ABSPATH')) {
    exit;
}

class CHROMATYPE_Landing_Plugin {
    public function __construct() {
        add_shortcode('chromatype_landing_page', array($this, 'render_landing_page'));
        add_action('template_include', array($this, 'load_page_template'));
    }

    public function render_landing_page() {
        ob_start();
        include plugin_dir_path(__FILE__) + 'templates/landing.php';
        return ob_get_clean();
    }
}

new CHROMATYPE_Landing_Plugin();
"""

with open(os.path.join(plugin_dir, 'chromatype-landing-plugin.php'), 'w', encoding='utf-8') as f:
    f.write(plugin_php)

# Copy landing page HTML to templates folder as landing.php
templates_dir = os.path.join(plugin_dir, 'templates')
os.makedirs(templates_dir, exist_ok=True)

html_path = r'C:\Users\dkven\color_analysis_backend\chromatype_wordpress_landing_page.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

with open(os.path.join(templates_dir, 'landing.php'), 'w', encoding='utf-8') as f:
    f.write(html_content)

# Zip up to Desktop
zip_output = r'C:\Users\dkven\Desktop\CHROMATYPE_Reports\chromatype-landing-page-plugin.zip'
with zipfile.ZipFile(zip_output, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(plugin_dir):
        for file in files:
            full_path = os.path.join(root, file)
            arcname = os.path.relpath(full_path, plugin_dir)
            zipf.write(full_path, os.path.join('chromatype-landing-plugin', arcname))

print(f"Created WordPress Plugin Zip: {zip_output} ({os.path.getsize(zip_output)} bytes)")
