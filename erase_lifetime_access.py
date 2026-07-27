import os
import zipfile

html_path = r'C:\Users\dkven\color_analysis_backend\chromatype_wordpress_landing_page.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace any mention of "Lifetime Access" or "lifetime" with "One-Time Download Only"
content = content.replace("Lifetime Wardrobe Mastery", "Complete Wardrobe Mastery")
content = content.replace("Lifetime Access to Digital Files", "One-Time Download Only of Digital Files")
content = content.replace("Lifetime Access", "One-Time Download Only")
content = content.replace("lifetime access", "one-time download only")
content = content.replace("lifetime", "one-time download")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Sanitized chromatype_wordpress_landing_page.html — erased all lifetime access mentions!")

# Regenerate plugin zip
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

print(f"Regenerated WordPress Plugin Zip: {zip_output} ({os.path.getsize(zip_output)} bytes)")
