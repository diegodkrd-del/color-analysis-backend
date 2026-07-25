<?php
/**
 * Personal Color Analysis - WordPress Integration Snippet
 * 
 * Instructions:
 * 1. Replace YOUR_RENDER_SERVICE_URL with your actual Render URL (e.g. https://color-analysis-backend.onrender.com).
 * 2. Add this file's contents to your theme's functions.php or via the "Code Snippets" plugin in WordPress.
 */

// CONFIGURATION
define('COLOR_ANALYSIS_API_URL', 'https://YOUR_RENDER_SERVICE_URL.onrender.com/webhook/analyze');

/**
 * OPTION 1: WPForms Integration Hook
 * Triggered automatically when WPForms form is submitted.
 * Form requirements:
 * - File Upload Field (Photo)
 * - Email Field
 */
add_action('wpforms_process_complete', 'send_wpforms_to_color_analysis_api', 10, 4);
function send_wpforms_to_color_analysis_api($fields, $entry, $form_data, $entry_id) {
    $email = '';
    $photo_path = '';

    // Find email and file upload fields dynamically
    foreach ($fields as $field) {
        if ($field['type'] === 'email') {
            $email = sanitize_email($field['value']);
        }
        if ($field['type'] === 'file-upload' && !empty($field['value'])) {
            // Retrieve upload file path on server
            if (isset($field['value_raw'][0]['value'])) {
                $photo_path = get_attached_file($field['value_raw'][0]['attachment_id']);
            }
        }
    }

    if (!empty($email) && !empty($photo_path) && file_exists($photo_path)) {
        // Send asynchronously to Python API on Render
        $args = array(
            'body' => array(
                'email' => $email,
                'file'  => curl_file_create($photo_path, mime_content_type($photo_path), basename($photo_path))
            ),
            'timeout' => 5, // Don't block user wait time
        );

        $ch = curl_init(COLOR_ANALYSIS_API_URL);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, array(
            'email' => $email,
            'file'  => new CURLFile($photo_path, mime_content_type($photo_path), basename($photo_path))
        ));
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 3);
        curl_exec($ch);
        curl_close($ch);
    }
}

/**
 * OPTION 2: Shortcode for Custom HTML/JS Form
 * Usage in WordPress page/post: [color_analysis_form]
 */
add_shortcode('color_analysis_form', 'render_color_analysis_frontend_form');
function render_color_analysis_frontend_form() {
    ob_start();
    ?>
    <div id="color-analysis-container" style="max-width: 500px; margin: 20px auto; font-family: sans-serif; padding: 25px; border-radius: 12px; background: #fafafa; border: 1px solid #eaeaea;">
        <h3 style="margin-top: 0; color: #333; text-align: center;">Get Your Personal Color Analysis</h3>
        <p style="font-size: 14px; color: #666; text-align: center; margin-bottom: 20px;">Upload a clear portrait photo in natural light. We'll send your 3-page customized PDF report directly to your email.</p>
        
        <form id="color-analysis-form" enctype="multipart/form-data">
            <div style="margin-bottom: 15px;">
                <label style="display: block; margin-bottom: 5px; font-weight: bold; font-size: 14px;">Your Email Address:</label>
                <input type="email" name="email" id="ca_email" required style="width: 100%; padding: 10px; border-radius: 6px; border: 1px solid #ccc; box-sizing: border-box;" placeholder="you@example.com">
            </div>
            
            <div style="margin-bottom: 20px;">
                <label style="display: block; margin-bottom: 5px; font-weight: bold; font-size: 14px;">Upload Your Photo (JPG/PNG):</label>
                <input type="file" name="file" id="ca_file" accept="image/*" required style="width: 100%; padding: 8px; border-radius: 6px; border: 1px solid #ccc; box-sizing: border-box;">
            </div>
            
            <button type="submit" id="ca_submit_btn" style="width: 100%; padding: 12px; background: #10B981; color: white; border: none; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer;">
                Analyze My Colors & Send PDF
            </button>
        </form>
        
        <div id="ca_status_msg" style="display: none; margin-top: 15px; padding: 12px; border-radius: 6px; font-size: 14px; text-align: center;"></div>
    </div>

    <script>
    document.getElementById('color-analysis-form').addEventListener('submit', function(e) {
        e.preventDefault();
        var form = e.target;
        var submitBtn = document.getElementById('ca_submit_btn');
        var statusMsg = document.getElementById('ca_status_msg');
        
        var formData = new FormData(form);
        submitBtn.disabled = true;
        submitBtn.innerText = 'Uploading & Processing...';
        statusMsg.style.display = 'block';
        statusMsg.style.background = '#E0F2FE';
        statusMsg.style.color = '#0369A1';
        statusMsg.innerText = 'Submitting photo... Please wait.';

        fetch('<?php echo esc_url(COLOR_ANALYSIS_API_URL); ?>', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            submitBtn.innerText = 'Analyze My Colors & Send PDF';
            submitBtn.disabled = false;
            if(data.status === 'success') {
                statusMsg.style.background = '#D1FAE5';
                statusMsg.style.color = '#065F46';
                statusMsg.innerText = 'Success! ' + data.message;
                form.reset();
            } else {
                statusMsg.style.background = '#FEE2E2';
                statusMsg.style.color = '#991B1B';
                statusMsg.innerText = 'Error submitting. Please try again.';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            submitBtn.innerText = 'Analyze My Colors & Send PDF';
            submitBtn.disabled = false;
            statusMsg.style.background = '#FEE2E2';
            statusMsg.style.color = '#991B1B';
            statusMsg.innerText = 'Network error. Please try again.';
        });
    });
    </script>
    <?php
    return ob_get_clean();
}
