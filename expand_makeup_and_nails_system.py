import os
import zipfile

html_path = r'C:\Users\dkven\color_analysis_backend\chromatype_wordpress_landing_page.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Make sure makeup_nails_section is present
makeup_nails_section = """<!-- Face Makeup & Nail Polish Masterclass Section -->
<section id="makeup-nails" class="py-24 relative bg-brand-dark/50 border-t border-brand-border">
  <div class="max-w-6xl mx-auto px-6 relative z-10">
    <div class="text-center mb-16 reveal">
      <span class="text-brand-accent text-sm font-semibold tracking-widest uppercase">Zone-by-Zone Precision</span>
      <h2 class="font-display font-extrabold text-4xl md:text-5xl text-brand-cream mt-2 mb-4">DIY Facial Makeup & Nail Polish Masterclass</h2>
      <p class="text-brand-light text-lg max-w-2xl mx-auto">Learn exact techniques for eyes, cheeks, lips, forehead, chin, and hands so any woman can apply her customized palette like a professional makeup artist.</p>
    </div>

    <!-- 4-Zone Face Breakdown Grid -->
    <div class="grid md:grid-cols-4 gap-6 mb-16">
      <div class="bg-brand-card border border-brand-border rounded-2xl p-6 text-center reveal">
        <div class="w-12 h-12 rounded-full bg-brand-accent/20 border border-brand-accent/40 flex items-center justify-center mx-auto mb-4 text-brand-accent text-xl"><i class="fas fa-eye"></i></div>
        <h4 class="font-display font-bold text-lg text-brand-cream mb-2">1. Eyes & Brows</h4>
        <p class="text-brand-light text-xs leading-relaxed">Shadow contrast, liner undertones, and mascara depth matched to iris reflectance.</p>
      </div>

      <div class="bg-brand-card border border-brand-border rounded-2xl p-6 text-center reveal" style="transition-delay:0.1s;">
        <div class="w-12 h-12 rounded-full bg-brand-gold/20 border border-brand-gold/40 flex items-center justify-center mx-auto mb-4 text-brand-gold text-xl"><i class="fas fa-smile"></i></div>
        <h4 class="font-display font-bold text-lg text-brand-cream mb-2">2. Cheeks & Glow</h4>
        <p class="text-brand-light text-xs leading-relaxed">Blush undertones (coral, peach, rose, plum) and cheekbone highlight placement.</p>
      </div>

      <div class="bg-brand-card border border-brand-border rounded-2xl p-6 text-center reveal" style="transition-delay:0.2s;">
        <div class="w-12 h-12 rounded-full bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center mx-auto mb-4 text-emerald-400 text-xl"><i class="fas fa-kiss-beam"></i></div>
        <h4 class="font-display font-bold text-lg text-brand-cream mb-2">3. Lips & Liners</h4>
        <p class="text-brand-light text-xs leading-relaxed">Lipstick, lip gloss, and liner shades matched to natural lip mucosa tone.</p>
      </div>

      <div class="bg-brand-card border border-brand-border rounded-2xl p-6 text-center reveal" style="transition-delay:0.3s;">
        <div class="w-12 h-12 rounded-full bg-purple-500/20 border border-purple-500/40 flex items-center justify-center mx-auto mb-4 text-purple-400 text-xl"><i class="fas fa-hand-sparkles"></i></div>
        <h4 class="font-display font-bold text-lg text-brand-cream mb-2">4. Hands & Nails</h4>
        <p class="text-brand-light text-xs leading-relaxed">Upload a hand photo on white paper to test nail polish colors live against your hand skin.</p>
      </div>
    </div>

    <!-- Hand & Nail Upload Module -->
    <div class="bg-brand-card border-2 border-dashed border-brand-gold/40 rounded-2xl p-8 max-w-3xl mx-auto text-center reveal">
      <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-brand-gold/40 bg-brand-gold/10 text-brand-gold text-xs font-bold uppercase tracking-wider mb-4">
        <i class="fas fa-hand-sparkles"></i> Hand & Nail Polish Matching Module
      </div>
      <h3 class="font-display font-bold text-2xl text-brand-cream mb-2">Upload Hand Photo on Flat White Paper</h3>
      <p class="text-brand-light text-sm max-w-lg mx-auto mb-6">
        Place your hand flat on a clean white sheet of paper and take a photo. Our CIELAB algorithm isolates nail bed reflectance against calibrated white ($L^*=100$) to project your top 6 nail polish shades!
      </p>

      <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
        <button type="button" onclick="triggerFileSelect()" class="px-8 py-3.5 bg-brand-gold text-brand-black font-bold text-sm rounded-xl hover:bg-brand-goldLight transition-all shadow-lg">
          <i class="fas fa-camera mr-2"></i>Upload Hand Photo on White Paper
        </button>
      </div>
    </div>
  </div>
</section>"""

if 'id="makeup-nails"' not in content:
    content = content.replace('<!-- CIELAB Technology Section -->', makeup_nails_section + '\n\n<!-- CIELAB Technology Section -->')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Update plugin PHP file
plugin_dir = r'C:\Users\dkven\color_analysis_backend\wp_landing_plugin'
templates_dir = os.path.join(plugin_dir, 'templates')

wp_snippet = content
wp_snippet = wp_snippet.replace('<!DOCTYPE html>', '')
wp_snippet = wp_snippet.replace('<html lang="en">', '')
wp_snippet = wp_snippet.replace('</html>', '')
wp_snippet = wp_snippet.replace('<head>', '')
wp_snippet = wp_snippet.replace('</head>', '')
wp_snippet = wp_snippet.replace('<body class="bg-brand-black text-brand-cream">', '<div class="chromatype-root bg-brand-black text-brand-cream" style="margin-top:-30px; margin-left:-30px; margin-right:-30px;">')
wp_snippet = wp_snippet.replace('</body>', '</div>')

with open(os.path.join(templates_dir, 'landing.php'), 'w', encoding='utf-8') as f:
    f.write(wp_snippet)

single_plugin_php = f"""<?php
/**
 * Plugin Name: CHROMATYPE Landing Page Studio
 * Plugin URI: https://chromatype.me/
 * Description: Standalone production landing page template for CHROMATYPE CIELAB 3D Color Analysis with $29 launch offer, live camera capture, direct PayPal links, hand/nail polish white paper matching, and DIY makeup masterclass blueprint.
 * Version: 6.0.0
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

print(f"Created Updated WordPress Plugin Zip (v6.0.0): {zip_output} ({os.path.getsize(zip_output)} bytes)")
