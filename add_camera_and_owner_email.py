import os
import zipfile

# 1. Update WordPress plugin PHP file to route all analysis emails to dkvendemais@gmail.com
plugin_dir = r'C:\Users\dkven\color_analysis_backend\wp_landing_plugin'
os.makedirs(plugin_dir, exist_ok=True)

plugin_php = r"""<?php
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
"""

with open(os.path.join(plugin_dir, 'chromatype-landing-plugin.php'), 'w', encoding='utf-8') as f:
    f.write(plugin_php)

# 2. Update HTML landing page to add Camera Capture Modal & HTML5 Camera API
html_path = r'C:\Users\dkven\color_analysis_backend\chromatype_wordpress_landing_page.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Add Camera Capture Modal to HTML body
camera_modal_html = """
<!-- Camera Capture Modal -->
<div id="cameraModal" class="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4 hidden">
  <div class="bg-brand-card border border-brand-border rounded-2xl max-w-lg w-full p-6 text-center relative">
    <button onclick="closeCameraModal()" class="absolute top-4 right-4 text-brand-muted hover:text-brand-cream text-lg"><i class="fas fa-times"></i></button>
    <h3 class="font-display font-bold text-xl text-brand-cream mb-2">Take Live Selfie</h3>
    <p class="text-brand-light text-xs mb-4">Position your face in good natural light facing the camera.</p>
    
    <div class="relative w-full aspect-square bg-black rounded-xl overflow-hidden mb-4 border border-brand-border">
      <video id="cameraVideo" autoplay playsinline class="w-full h-full object-cover"></video>
      <canvas id="cameraCanvas" class="hidden"></canvas>
    </div>

    <div class="flex gap-3">
      <button onclick="closeCameraModal()" class="flex-1 py-3 border border-brand-border rounded-xl text-brand-light font-bold text-sm hover:border-brand-muted">Cancel</button>
      <button onclick="snapPhoto()" class="flex-1 py-3 bg-brand-accent text-white rounded-xl font-bold text-sm hover:bg-brand-accentHover shadow-lg"><i class="fas fa-camera mr-2"></i>Snap Photo</button>
    </div>
  </div>
</div>
"""

if 'id="cameraModal"' not in html_content:
    html_content = html_content.replace('<!-- Toast Notification -->', camera_modal_html + '\n\n<!-- Toast Notification -->')

# Add Live Camera Button to Photo Upload Zone
upload_zone_replacement = """<!-- Photo Upload & Camera Selector Zone -->
      <div class="mb-6">
        <label class="block text-brand-light text-sm font-medium mb-2">Provide Your Selfie (Natural Daylight)</label>
        
        <div class="grid grid-cols-2 gap-3 mb-3">
          <button type="button" onclick="openCameraModal()" class="py-3 px-4 bg-brand-dark border border-brand-border rounded-xl text-brand-cream font-semibold text-xs hover:border-brand-accent transition-colors flex items-center justify-center gap-2">
            <i class="fas fa-camera text-brand-accent text-sm"></i> Take Live Selfie
          </button>
          <button type="button" onclick="document.getElementById('photoInput').click()" class="py-3 px-4 bg-brand-dark border border-brand-border rounded-xl text-brand-cream font-semibold text-xs hover:border-brand-accent transition-colors flex items-center justify-center gap-2">
            <i class="fas fa-folder-open text-brand-gold text-sm"></i> Upload Photo File
          </button>
        </div>

        <div id="uploadZone" class="border-2 border-dashed border-brand-border rounded-xl p-6 text-center cursor-pointer hover:border-brand-accent transition-colors" onclick="document.getElementById('photoInput').click()">
          <div id="uploadPlaceholder">
            <i class="fas fa-cloud-arrow-up text-2xl text-brand-muted mb-2"></i>
            <p class="text-brand-light text-xs mb-1">Click to browse or drag & drop image here</p>
            <p class="text-brand-muted text-[10px]">JPG or PNG under 10MB — no filters, natural daylight</p>
          </div>
          <div id="uploadPreview" class="hidden">
            <img id="previewImg" class="max-h-44 mx-auto rounded-lg mb-2 object-cover" alt="Preview">
            <p id="previewName" class="text-brand-light text-xs font-mono"></p>
          </div>
        </div>
        <input type="file" id="photoInput" accept="image/jpeg,image/png" class="hidden" onchange="handleFileSelect(event)">
      </div>"""

start_zone = html_content.find('<!-- Photo Upload Zone -->')
end_zone = html_content.find('<!-- Submit CTA Button -->')

if start_zone != -1 and end_zone != -1:
    html_content = html_content[:start_zone] + upload_zone_replacement + '\n\n      ' + html_content[end_zone:]

# Add Camera JS Functions
camera_js = """
// HTML5 Camera Capture Functions
let cameraStream = null;

function openCameraModal() {
  const modal = document.getElementById('cameraModal');
  const video = document.getElementById('cameraVideo');
  modal.classList.remove('hidden');

  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user', width: { ideal: 720 }, height: { ideal: 720 } } })
      .then(stream => {
        cameraStream = stream;
        video.srcObject = stream;
      })
      .catch(err => {
        alert('Could not access camera. Please allow camera permissions or upload a photo file.');
        closeCameraModal();
      });
  } else {
    alert('Camera API not supported on this browser. Please upload a photo file.');
    closeCameraModal();
  }
}

function closeCameraModal() {
  const modal = document.getElementById('cameraModal');
  modal.classList.add('hidden');
  if (cameraStream) {
    cameraStream.getTracks().forEach(track => track.stop());
    cameraStream = null;
  }
}

function snapPhoto() {
  const video = document.getElementById('cameraVideo');
  const canvas = document.getElementById('cameraCanvas');
  const ctx = canvas.getContext('2d');

  canvas.width = video.videoWidth || 640;
  canvas.height = video.videoHeight || 640;
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  const dataUrl = canvas.toDataURL('image/jpeg', 0.9);
  
  // Convert DataURL to File object for uploadedFile
  fetch(dataUrl)
    .then(res => res.blob())
    .then(blob => {
      uploadedFile = new File([blob], "camera_selfie.jpg", { type: "image/jpeg" });
      document.getElementById('previewImg').src = dataUrl;
      document.getElementById('previewName').textContent = "camera_selfie.jpg (Live Snapshot)";
      document.getElementById('uploadPlaceholder').classList.add('hidden');
      document.getElementById('uploadPreview').classList.remove('hidden');
      checkFormReady();
      closeCameraModal();
    });
}
"""

if 'function openCameraModal()' not in html_content:
    html_content = html_content.replace('// File upload handling', camera_js + '\n\n// File upload handling')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Updated chromatype_wordpress_landing_page.html with Live Camera Modal & dkvendemais@gmail.com email routing!")

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

print(f"Created Updated WordPress Plugin Zip (v3.2.0): {zip_output} ({os.path.getsize(zip_output)} bytes)")
