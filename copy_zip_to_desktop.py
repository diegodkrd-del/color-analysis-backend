import shutil
import os

src_zip = r'C:\Users\dkven\Desktop\CHROMATYPE_Reports\chromatype-landing-page-plugin.zip'

desktop_root_zip = r'C:\Users\dkven\Desktop\chromatype-landing-page-plugin.zip'
backend_root_zip = r'C:\Users\dkven\color_analysis_backend\chromatype-landing-page-plugin.zip'

shutil.copyfile(src_zip, desktop_root_zip)
shutil.copyfile(src_zip, backend_root_zip)

print(f"Copied plugin zip to Desktop root: {desktop_root_zip} ({os.path.getsize(desktop_root_zip)} bytes)")
print(f"Copied plugin zip to Backend root: {backend_root_zip} ({os.path.getsize(backend_root_zip)} bytes)")
