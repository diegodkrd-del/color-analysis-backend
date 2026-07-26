<?php
/**
 * Plugin Name: CHROMATYPE — Interactive HSL Color Studio & 12-Season Matrix
 * Plugin URI: https://chromatype.me
 * Description: Interactive Personal Color Analysis Studio plugin for WordPress. Features real-time HSL color mixing (Hue, Saturation, Lightness), 360° radial palette wheel with client face portrait, 4-season spectrum match levers (Winter, Autumn, Summer, Spring), and a filterable 432-color reference grid matrix.
 * Version: 1.0.0
 * Author: CHROMATYPE Team
 * Author URI: https://chromatype.me
 * License: GPLv2 or later
 */

if (!defined('ABSPATH')) {
    exit; // Exit if accessed directly
}

function chromatype_color_mixer_shortcode($atts) {
    ob_start();
    ?>
    <div id="chromatype-wp-app" style="width: 100%; max-width: 1200px; margin: 0 auto; font-family: 'Outfit', sans-serif;">
        <iframe src="<?php echo plugins_url('studio_app.html', __FILE__); ?>" style="width: 100%; height: 950px; border: none; border-radius: 16px; box-shadow: 0 15px 35px rgba(0,0,0,0.2);" title="CHROMATYPE Color Studio"></iframe>
    </div>
    <?php
    return ob_get_clean();
}
add_shortcode('chromatype_color_mixer', 'chromatype_color_mixer_shortcode');
