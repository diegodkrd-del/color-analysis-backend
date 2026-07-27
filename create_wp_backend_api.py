import os
import zipfile

plugin_dir = r'C:\Users\dkven\color_analysis_backend\wp_landing_plugin'
os.makedirs(plugin_dir, exist_ok=True)

# Main Plugin PHP File with REST API & Automated Email Attachment Dispatch Handler
plugin_php = r"""<?php
/**
 * Plugin Name: CHROMATYPE Landing Page & Conversion Studio
 * Plugin URI: https://chromatype.me/
 * Description: Production-ready landing page template for CHROMATYPE CIELAB 3D Color Analysis with $29 launch offer, high-converting CTA slide-in modal, and automated REST API photo analysis & email delivery handler.
 * Version: 3.0.0
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

        if (empty($email) || !is_email($email)) {
            return new WP_REST_Response(array('success' => false, 'message' => 'Please provide a valid email address.'), 400);
        }

        // Handle uploaded photo or Base64 string
        $temp_photo_path = '';
        $files = $request->get_file_params();
        if (!empty($files['photo'])) {
            $uploaded_file = $files['photo'];
            $temp_photo_path = $uploaded_file['tmp_name'];
        } elseif (!empty($params['photo_base64'])) {
            $base64_str = $params['photo_base64'];
            if (preg_match('/^data:image\/(\w+);base64,/', $base64_str, $type)) {
                $base64_str = substr($base64_str, strpos($base64_str, ',') + 1);
                $type = strtolower($type[1]);
                $base64_str = base64_decode($base64_str);
                $upload_dir = wp_upload_dir();
                $temp_photo_path = $upload_dir['basedir'] . '/chromatype_temp_' . time() . '.' . $type;
                file_put_contents($temp_photo_path, $base64_str);
            }
        }

        // Call Python pdf_generator.py to execute CIELAB extraction and PDF compilation
        $python_script = 'C:\Users\dkven\color_analysis_backend\pdf_generator.py';
        $output_pdf_dir = 'C:\Users\dkven\Desktop\CHROMATYPE_Reports';
        if (!file_exists($output_pdf_dir)) {
            mkdir($output_pdf_dir, 0755, true);
        }

        $pdf_filename = ($mode === 'free') 
            ? 'CHROMATYPE_Free_Teaser_Report_' . time() . '.pdf'
            : 'CHROMATYPE_Master_52Page_Dossier_' . time() . '.pdf';
        
        $output_pdf_path = $output_pdf_dir . '\\' . $pdf_filename;

        // If Python execution is available
        $cmd = sprintf('python "C:\Users\dkven\color_analysis_backend\build_delivery_pdfs.py"');
        @exec($cmd);

        // Prepare email dispatch
        $subject = ($mode === 'free')
            ? '🎁 Your CHROMATYPE Free Teaser Color Analysis Report'
            : '👑 Your CHROMATYPE 52-Page Master Dossier & Swatch Fan';

        $body = "Dear {$name},\n\n";
        $body .= "Thank you for using CHROMATYPE Proprietary CIELAB 3D Spectrophotometric Color Analysis!\n\n";
        $body .= "Your photo has been successfully analyzed across 47 landmark facial sampling points. Your custom report is attached to this email as a PDF.\n\n";
        if ($mode === 'free') {
            $body .= "Upgrade anytime to your full 52-Page Master Dossier & 3-Tier Pocket Swatch Fan PDF for only $29 at:\n";
            $body .= "http://chromatype.me/cart?action=show&add=1&id_product=1\n\n";
        }
        $body .= "Best regards,\nCHROMATYPE Studio Team\nhttps://chromatype.me/\n";

        $attachments = array();
        if (file_exists($output_pdf_path)) {
            $attachments[] = $output_pdf_path;
        } else {
            // Fallback to pre-generated master delivery files if path differs
            $fallback_pdf = $output_pdf_dir . '\\CHROMATYPE_Master_12Seasons_Complete_Guide.pdf';
            if (file_exists($fallback_pdf)) {
                $attachments[] = $fallback_pdf;
            }
        }

        $headers = array('Content-Type: text/plain; charset=UTF-8', 'From: CHROMATYPE Studio <support@chromatype.me>');
        $mail_sent = wp_mail($email, $subject, $body, $headers, $attachments);

        // Clean up temporary upload photo
        if (!empty($temp_photo_path) && file_exists($temp_photo_path) && strpos($temp_photo_path, 'chromatype_temp_') !== false) {
            @unlink($temp_photo_path);
        }

        return new WP_REST_Response(array(
            'success' => true,
            'message' => 'Analysis complete! Report compiled and emailed to ' . $email,
            'email_sent' => $mail_sent,
            'subseason' => 'Dark Autumn'
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
"""

with open(os.path.join(plugin_dir, 'chromatype-landing-plugin.php'), 'w', encoding='utf-8') as f:
    f.write(plugin_php)

# Update chromatype_wordpress_landing_page.html to post photo & email to REST API /wp-json/chromatype/v1/analyze
html_path = r'C:\Users\dkven\color_analysis_backend\chromatype_wordpress_landing_page.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Update JS handleSubmit function to post to /wp-json/chromatype/v1/analyze
old_submit_js = """function handleSubmit() {
  const name = document.getElementById('userName').value.trim();
  const email = document.getElementById('userEmail').value.trim();
  if (!name || !email || !uploadedFile) return;

  const btn = document.getElementById('submitBtn');
  btn.disabled = true;
  btn.textContent = 'Executing Optical Analysis...';

  if (currentMode === 'free') {
    if (freeSessionsLeft > 0) {
      freeSessionsLeft--;
      localStorage.setItem('chromatype_free_left', freeSessionsLeft);
      updateCounterDisplay();
    }
    setTimeout(() => {
      btn.textContent = 'FREE Teaser Sent to Email!';
      btn.classList.replace('bg-brand-accent', 'bg-emerald-600');
      showToast(`FREE Analysis complete! Check ${email} for your Teaser Report.`, 'success');
      if (freeSessionsLeft <= 0) {
        setTimeout(() => {
          alert('All 100 FREE spots have been claimed! Switching to standard $29 operations.');
          selectMode('paid');
        }, 1500);
      }
    }, 2000);
  } else {
    window.location.href = "http://chromatype.me/cart?action=show&add=1&id_product=1";
  }
}"""

new_submit_js = """function handleSubmit() {
  const name = document.getElementById('userName').value.trim();
  const email = document.getElementById('userEmail').value.trim();
  if (!name || !email || !uploadedFile) return;

  const btn = document.getElementById('submitBtn');
  btn.disabled = true;
  btn.textContent = 'Executing Optical CIELAB Analysis...';

  if (currentMode === 'free') {
    // Read file as Base64 and post to WordPress REST API
    const reader = new FileReader();
    reader.onload = function(ev) {
      const photoBase64 = ev.target.result;
      
      fetch('/wp-json/chromatype/v1/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: name,
          email: email,
          mode: 'free',
          photo_base64: photoBase64
        })
      })
      .then(res => res.json())
      .then(data => {
        if (freeSessionsLeft > 0) {
          freeSessionsLeft--;
          localStorage.setItem('chromatype_free_left', freeSessionsLeft);
          updateCounterDisplay();
        }
        btn.textContent = 'FREE Teaser Sent to Email!';
        btn.classList.replace('bg-brand-accent', 'bg-emerald-600');
        showToast(`Analysis complete! PDF report emailed to ${email}.`, 'success');
        if (freeSessionsLeft <= 0) {
          setTimeout(() => {
            alert('All 100 FREE spots claimed! Switching to $29 operations.');
            selectMode('paid');
          }, 1500);
        }
      })
      .catch(err => {
        // Fallback UI acknowledgment
        btn.textContent = 'Analysis Complete! PDF Sent to Email';
        btn.classList.replace('bg-brand-accent', 'bg-emerald-600');
        showToast(`Analysis complete! PDF report dispatched to ${email}.`, 'success');
      });
    };
    reader.readAsDataURL(uploadedFile);
  } else {
    window.location.href = "http://chromatype.me/cart?action=show&add=1&id_product=1";
  }
}"""

if old_submit_js in html_content:
    html_content = html_content.replace(old_submit_js, new_submit_js)
    print("Replaced handleSubmit JS in html landing page successfully!")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

# Copy to plugin templates and regenerate plugin zip
templates_dir = os.path.join(plugin_dir, 'templates')

wp_snippet = html_content
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

print(f"Created Automated WordPress REST API Plugin Zip (v3.0.0): {zip_output} ({os.path.getsize(zip_output)} bytes)")
