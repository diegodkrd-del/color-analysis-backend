<?php
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
