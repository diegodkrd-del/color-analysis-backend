import os
import subprocess

pdf_script = r'C:\Users\dkven\color_analysis_backend\build_delivery_pdfs.py'

# Execute build_delivery_pdfs.py to compile the complete 52-page 12-Season Master Guide PDF
cmd = f'python "{pdf_script}"'
res = subprocess.run(cmd, shell=True, capture_output=True, text=True)

print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)

output_dir = r'C:\Users\dkven\Desktop\CHROMATYPE_Reports'
master_pdf = os.path.join(output_dir, 'CHROMATYPE_Master_12Seasons_Complete_Guide.pdf')
diego_pdf = os.path.join(output_dir, 'CHROMATYPE_Report_Diego_Kasper.pdf')

if os.path.exists(master_pdf):
    print(f"Master 12-Season Complete Guide PDF size: {os.path.getsize(master_pdf)} bytes")
    # Copy to Diego Kasper named report for reference
    import shutil
    shutil.copyfile(master_pdf, diego_pdf)
    print(f"Copied to CHROMATYPE_Report_Diego_Kasper.pdf: {diego_pdf} ({os.path.getsize(diego_pdf)} bytes)")
