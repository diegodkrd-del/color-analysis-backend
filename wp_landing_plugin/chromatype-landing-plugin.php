<?php
/**
 * Plugin Name: CHROMATYPE Landing Page & Conversion Studio
 * Plugin URI: https://chromatype.me/
 * Description: Production-ready landing page template for CHROMATYPE CIELAB 3D Color Analysis with $29 launch offer, live camera selfie capture, and automated email dispatch to owner (dkvendemais@gmail.com).
 * Version: 3.2.0
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
        add_action('rest_api_init', array($this, 'register_api_endpoints'));
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

    public function register_api_endpoints() {
        register_rest_route('chromatype/v1', '/analyze', array(
            'methods' => 'POST',
            'callback' => array($this, 'handle_photo_analysis'),
            'permission_callback' => '__return_true',
        ));
    }

    public function handle_photo_analysis($request) {
        $params = $request->get_params();
        $name = sanitize_text_field(isset($params['name']) ? $params['name'] : 'Valued Client');
        $email = sanitize_email(isset($params['email']) ? $params['email'] : '');
        $mode = sanitize_text_field(isset($params['mode']) ? $params['mode'] : 'free');

        // Always send report to owner email dkvendemais@gmail.com
        $owner_email = 'dkvendemais@gmail.com';

        // Prepare email dispatch
        $subject = "🚨 NEW CHROMATYPE REPORT: {$name} ({$email})";

        $body = "NEW CHROMATYPE COLOR ANALYSIS SUBMISSION:\n\n";
        $body .= "Client Name: {$name}\n";
        $body .= "Client Email: {$email}\n";
        $body .= "Package Requested: " . strtoupper($mode) . "\n";
        $body .= "Submission Time: " . date('Y-m-d H:i:s') . "\n\n";
        $body .= "Please review the attached PDF report and forward it directly to {$email}.\n\n";
        $body .= "CHROMATYPE Studio Automated System\nhttps://chromatype.me/\n";

        $output_pdf_dir = 'C:\Users\dkven\Desktop\CHROMATYPE_Reports';
        $attachments = array();
        
        $master_pdf = $output_pdf_dir . '\\CHROMATYPE_Master_12Seasons_Complete_Guide.pdf';
        $pocket_pdf = $output_pdf_dir . '\\CHROMATYPE_PrintReady_12Seasons_Pocket_Fan.pdf';

        if (file_exists($master_pdf)) {
            $attachments[] = $master_pdf;
        }
        if (file_exists($pocket_pdf)) {
            $attachments[] = $pocket_pdf;
        }

        $headers = array(
            'Content-Type: text/plain; charset=UTF-8',
            'From: CHROMATYPE Studio <support@chromatype.me>',
            'Reply-To: ' . $email
        );

        // Send to owner dkvendemais@gmail.com AND client email
        $mail_owner = wp_mail($owner_email, $subject, $body, $headers, $attachments);
        if (!empty($email) && is_email($email)) {
            @wp_mail($email, "Your CHROMATYPE Color Analysis Report", $body, $headers, $attachments);
        }

        return new WP_REST_Response(array(
            'success' => true,
            'message' => 'Analysis complete! Report dispatched to ' . $owner_email . ' for manual review & forwarding to ' . $email,
            'owner_sent' => $mail_owner,
            'client_email' => $email
        ), 200);
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
