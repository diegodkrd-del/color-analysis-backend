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
 * Version: 2.6.0
 * Author: CHROMATYPE Studio
 * Author URI: https://chromatype.me/
 */

if (!defined('ABSPATH')) {
    exit;
}

class CHROMATYPE_Landing_Plugin {
    public function __construct() {
        add_shortcode('chromatype_landing_page', array($this, 'render_landing_page'));
        add_shortcode('chromatype', array($this, 'render_landing_page'));
        add_shortcode('chromatype_studio', array($this, 'render_landing_page'));
        add_filter('theme_page_templates', array($this, 'add_page_template'));
        add_filter('template_include', array($this, 'load_page_template'));
    }

    public function add_page_template($templates) {
        $templates['chromatype-fullscreen-landing'] = 'CHROMATYPE Landing Page (Full Width)';
        return $templates;
    }

    public function load_page_template($template) {
        if (is_page()) {
            $meta_template = get_post_meta(get_the_ID(), '_wp_page_template', true);
            if ('chromatype-fullscreen-landing' === $meta_template) {
                $plugin_template = plugin_dir_path(__FILE__) . 'templates/landing.php';
                if (file_exists($plugin_template)) {
                    return $plugin_template;
                }
            }
        }
        return $template;
    }

    public function render_landing_page() {
        ob_start();
        $template_path = plugin_dir_path(__FILE__) . 'templates/landing.php';
        if (file_exists($template_path)) {
            include $template_path;
        } else {
            echo '<div style="padding:20px; background:#1c1b19; color:#e8734a; font-weight:bold;">CHROMATYPE Template Loading Error. Please re-install plugin zip.</div>';
        }
        return ob_get_clean();
    }
}

new CHROMATYPE_Landing_Plugin();
"""

with open(os.path.join(plugin_dir, 'chromatype-landing-plugin.php'), 'w', encoding='utf-8') as f:
    f.write(plugin_php)

# Read HTML file and strip nested DOCTYPE/html/body wrappers for shortcode compatibility
html_path = r'C:\Users\dkven\color_analysis_backend\chromatype_wordpress_landing_page.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Make a WordPress shortcode compliant landing.php snippet
# Strip <html><head><body> so it injects perfectly inside entry-content or page templates
wp_snippet = html_content
wp_snippet = wp_snippet.replace('<!DOCTYPE html>', '')
wp_snippet = wp_snippet.replace('<html lang="en">', '')
wp_snippet = wp_snippet.replace('</html>', '')
wp_snippet = wp_snippet.replace('<head>', '')
wp_snippet = wp_snippet.replace('</head>', '')
wp_snippet = wp_snippet.replace('<body class="bg-brand-black text-brand-cream">', '<div class="chromatype-root bg-brand-black text-brand-cream" style="margin-top:-30px; margin-left:-30px; margin-right:-30px;">')
wp_snippet = wp_snippet.replace('</body>', '</div>')

templates_dir = os.path.join(plugin_dir, 'templates')
os.makedirs(templates_dir, exist_ok=True)

with open(os.path.join(templates_dir, 'landing.php'), 'w', encoding='utf-8') as f:
    f.write(wp_snippet)

# Zip up to Desktop
zip_output = r'C:\Users\dkven\Desktop\CHROMATYPE_Reports\chromatype-landing-page-plugin.zip'
with zipfile.ZipFile(zip_output, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(plugin_dir):
        for file in files:
            full_path = os.path.join(root, file)
            arcname = os.path.relpath(full_path, plugin_dir)
            zipf.write(full_path, os.path.join('chromatype-landing-plugin', arcname))

print(f"Created WordPress Shortcode Compatible Plugin Zip: {zip_output} ({os.path.getsize(zip_output)} bytes)")
