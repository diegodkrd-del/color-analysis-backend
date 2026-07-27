import os
import zipfile

html_path = r'C:\Users\dkven\color_analysis_backend\chromatype_wordpress_landing_page.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace small X button with a large, prominent, touch-friendly circular button
old_button = '<button onclick="closeCtaModal()" class="absolute top-3 right-3 text-brand-muted hover:text-brand-cream text-sm"><i class="fas fa-times"></i></button>'
new_button = '<button onclick="closeCtaModal()" class="absolute top-3 right-3 w-10 h-10 rounded-full bg-brand-dark/90 border border-brand-border hover:border-brand-accent text-brand-light hover:text-brand-cream text-lg flex items-center justify-center transition-all shadow-md active:scale-95" aria-label="Close modal"><i class="fas fa-xmark"></i></button>'

if old_button in content:
    content = content.replace(old_button, new_button)
    print("Replaced close button successfully!")
else:
    # Fallback search for close button inside timedCtaModal
    content = content.replace('<i class="fas fa-times"></i>', '<i class="fas fa-xmark text-lg"></i>')
    print("Updated X icon style")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Update WordPress plugin template & zip
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

zip_output = r'C:\Users\dkven\Desktop\CHROMATYPE_Reports\chromatype-landing-page-plugin.zip'
with zipfile.ZipFile(zip_output, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(plugin_dir):
        for file in files:
            full_path = os.path.join(root, file)
            arcname = os.path.relpath(full_path, plugin_dir)
            zipf.write(full_path, os.path.join('chromatype-landing-plugin', arcname))

print(f"Updated WordPress Plugin Zip: {zip_output} ({os.path.getsize(zip_output)} bytes)")
