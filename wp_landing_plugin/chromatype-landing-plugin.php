<?php
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
