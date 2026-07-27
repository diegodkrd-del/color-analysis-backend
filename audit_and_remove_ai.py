import os
import re

files_to_check = [
    r'C:\Users\dkven\color_analysis_backend\templates\report.html',
    r'C:\Users\dkven\color_analysis_backend\pdf_generator.py',
    r'C:\Users\dkven\color_analysis_backend\studio_gui.py',
    r'C:\Users\dkven\color_analysis_backend\chromatype_interactive_color_studio.html',
    r'C:\Users\dkven\color_analysis_backend\generate_pocket_fan.py'
]

replacements = [
    (r'\bAI Primary Match Recommendation\b', 'Primary Match Recommendation'),
    (r'\bAI Primary Match\b', 'Primary Match'),
    (r'\bAI Recommendation\b', 'Primary Recommendation'),
    (r'\bAI Powered\b', 'Spectrophotometric Powered'),
    (r'\bAI Engine\b', 'Optical Engine'),
    (r'\bAI Analysis\b', 'CIELAB Optical Analysis'),
    (r'\bAI\b', 'Optical')
]

for file_path in files_to_check:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        for pattern, repl in replacements:
            content = re.sub(pattern, repl, content, flags=re.IGNORECASE)
            
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Sanitized AI references in: {file_path}")
        else:
            print(f"No AI references found in: {file_path}")
