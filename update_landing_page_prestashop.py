import os

html_path = r'C:\Users\dkven\color_analysis_backend\chromatype_wordpress_landing_page.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace SVG logo with official PrestaShop CHROMATYPE Logo
logo_html = """<img src="http://chromatype.me/img/logo-1784993471.jpg" alt="CHROMATYPE Studio" class="h-10 w-auto object-contain rounded-md">"""

# Replace navigation brand text with image logo
content = content.replace(
    """<svg width="32" height="32" viewBox="0 0 32 32" fill="none">
        <circle cx="16" cy="16" r="15" stroke="url(#logoGrad)" stroke-width="2"/>
        <circle cx="16" cy="16" r="8" fill="url(#logoGrad)"/>
        <circle cx="16" cy="8" r="3" fill="#e8734a"/>
        <circle cx="22" cy="20" r="3" fill="#d4a853"/>
        <circle cx="10" cy="20" r="3" fill="#8fbc6a"/>
        <defs>
          <linearGradient id="logoGrad" x1="0" y1="0" x2="32" y2="32">
            <stop stop-color="#e8734a"/>
            <stop offset="0.5" stop-color="#d4a853"/>
            <stop offset="1" stop-color="#8fbc6a"/>
          </linearGradient>
        </defs>
      </svg>
      <span class="font-display font-bold text-xl text-brand-cream tracking-tight">CHROMA<span class="text-brand-accent">TYPE</span></span>""",
    logo_html
)

content = content.replace(
    """<div class="flex justify-center items-center gap-2 mb-4">
      <span class="font-display font-bold text-lg text-brand-cream">CHROMA<span class="text-brand-accent">TYPE</span></span>
    </div>""",
    f'<div class="flex justify-center items-center gap-2 mb-4">{logo_html}</div>'
)

# Write updated HTML file
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated chromatype_wordpress_landing_page.html with official PrestaShop logo successfully!")
