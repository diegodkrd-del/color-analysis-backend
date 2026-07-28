import os
import shutil
import time

backend_dir = r'C:\Users\dkven\color_analysis_backend'
desktop_dir = r'C:\Users\dkven\Desktop'

# Copy latest run_mobile_cam_server.py, local_operator_studio.html, and BAT launcher
local_html = os.path.join(backend_dir, 'local_operator_studio.html')
desktop_html = os.path.join(desktop_dir, 'local_operator_studio.html')
shutil.copyfile(local_html, desktop_html)

bat_launcher = f"""@echo off
title CHROMATYPE QR Code Mobile Camera & Laptop Suite
echo Starting CHROMATYPE Local QR Code Mobile Camera Server...
start python "{os.path.join(backend_dir, 'run_mobile_cam_server.py')}"
timeout /t 2 >nul
echo Launching Laptop Operator Suite...
start "" "{local_html}"
"""

desktop_bat = os.path.join(desktop_dir, 'Run_CHROMATYPE_Local_Operator.bat')
with open(desktop_bat, 'w', encoding='utf-8') as f:
    f.write(bat_launcher)

print(f"Refreshed Desktop files at timestamp {time.strftime('%H:%M:%S')}:")
print(f" - {desktop_bat} ({os.path.getsize(desktop_bat)} bytes)")
print(f" - {desktop_html} ({os.path.getsize(desktop_html)} bytes)")
