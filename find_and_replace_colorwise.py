import os
import re

backend_dir = r'C:\Users\dkven\color_analysis_backend'

files_to_check = []
for root, dirs, files in os.walk(backend_dir):
    for f in files:
        if f.endswith(('.py', '.html', '.css', '.js', '.md', '.json')):
            files_to_check.append(os.path.join(root, f))

CHROMATYPE_regex = re.compile(r'CHROMATYPE', re.IGNORECASE)

modified_files = []
for file_path in files_to_check:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if CHROMATYPE_regex.search(content):
            new_content = CHROMATYPE_regex.sub('CHROMATYPE', content)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            modified_files.append(file_path)
            print(f"Replaced 'CHROMATYPE' -> 'CHROMATYPE' in: {file_path}")
    except Exception as e:
        pass

print(f"\nTotal files sanitized: {len(modified_files)}")
