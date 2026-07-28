import os

backend_dir = r'C:\Users\dkven\color_analysis_backend'
desktop_dir = r'C:\Users\dkven\Desktop'

# Create Python Flask Server script for QR Code Phone Camera Stream: run_mobile_cam_server.py
server_code = """import os
import socket
from flask import Flask, render_template_string, request, Response

app = Flask(__name__)

latest_frame = None

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

LOCAL_IP = get_local_ip()
PORT = 5000
STREAM_URL = f"http://{LOCAL_IP}:{PORT}/mobile_cam"

PHONE_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CHROMATYPE Mobile Camera Streamer</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
</head>
<body class="bg-black text-white min-h-screen flex flex-col items-center justify-between p-4 font-sans text-center">
  <div class="pt-4">
    <h2 class="text-xl font-bold text-orange-500"><i class="fas fa-camera mr-2"></i>CHROMATYPE Mobile Cam</h2>
    <p class="text-xs text-gray-400">Streaming live HD video to your laptop</p>
  </div>

  <div class="relative w-full max-w-sm aspect-square bg-gray-900 rounded-2xl overflow-hidden border-2 border-orange-500 my-4">
    <video id="v" autoplay playsinline class="w-full h-full object-cover"></video>
    <canvas id="c" class="hidden"></canvas>
  </div>

  <div class="w-full max-w-sm pb-6 space-y-3">
    <button onclick="startCam()" class="w-full py-3 bg-orange-600 text-white font-bold rounded-xl shadow-lg text-sm">
      <i class="fas fa-video mr-2"></i>Start Phone Camera
    </button>
    <p id="status" class="text-xs text-emerald-400 font-semibold">Ready to stream</p>
  </div>

  <script>
    let streaming = false;
    function startCam() {
      const video = document.getElementById('v');
      navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment', width: 720, height: 720 } })
        .then(stream => {
          video.srcObject = stream;
          streaming = true;
          document.getElementById('status').textContent = '🟢 Live Streaming to Laptop...';
          setInterval(sendFrame, 150);
        })
        .catch(err => alert("Camera Error: " + err.message));
    }

    function sendFrame() {
      if (!streaming) return;
      const video = document.getElementById('v');
      const canvas = document.getElementById('c');
      canvas.width = video.videoWidth || 640;
      canvas.height = video.videoHeight || 640;
      canvas.getContext('2d').drawImage(video, 0, 0);
      const dataUrl = canvas.toDataURL('image/jpeg', 0.6);

      fetch('/upload_frame', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: dataUrl })
      }).catch(e => {});
    }
  </script>
</body>
</html>'''

@app.route('/mobile_cam')
def mobile_cam():
    return render_template_string(PHONE_HTML)

@app.route('/upload_frame', methods=['POST'])
def upload_frame():
    global latest_frame
    data = request.get_json()
    if data and 'image' in data:
        latest_frame = data['image']
    return {'status': 'ok'}

@app.route('/get_frame')
def get_frame():
    global latest_frame
    return {'image': latest_frame}

if __name__ == '__main__':
    print(f"🚀 CHROMATYPE QR CODE SERVER STARTED at {STREAM_URL}")
    app.run(host='0.0.0.0', port=PORT, debug=False)
"""

server_script_path = os.path.join(backend_dir, 'run_mobile_cam_server.py')
with open(server_script_path, 'w', encoding='utf-8') as f:
    f.write(server_code)

# 2. Update local_operator_studio.html with QR Code image generator & Live Polling Frame
studio_path = os.path.join(backend_dir, 'local_operator_studio.html')
with open(studio_path, 'r', encoding='utf-8') as f:
    html = f.read()

qr_modal_update = """
<!-- QR Code Phone Camera Connect Modal -->
<div id="phoneCamModal" class="fixed inset-0 z-50 bg-black/80 flex items-center justify-center p-4 hidden">
  <div class="bg-white border border-stone-200 rounded-2xl max-w-md w-full p-6 text-center relative shadow-2xl">
    <button onclick="closePhoneCamModal()" class="absolute top-4 right-4 text-stone-400 hover:text-stone-700 text-lg"><i class="fas fa-times"></i></button>
    
    <div class="w-12 h-12 rounded-full bg-orange-100 text-orange-600 flex items-center justify-center mx-auto mb-3 text-xl"><i class="fas fa-qrcode"></i></div>
    <h3 class="font-display font-bold text-xl text-stone-900 mb-1">Scan QR Code with Cell Phone</h3>
    <p class="text-xs text-stone-500 mb-4">Open your cell phone camera app and scan this QR code to stream HD video live to your laptop:</p>

    <!-- QR Code Image Generator -->
    <div class="bg-white p-4 border border-stone-300 rounded-2xl inline-block mb-4 shadow-sm">
      <img id="qrCodeImg" class="w-48 h-48 mx-auto" alt="Scan QR Code to Connect Phone">
    </div>

    <p id="qrUrlText" class="text-xs font-mono font-bold text-orange-700 bg-orange-50 p-2 rounded-lg border border-orange-200 mb-4">http://127.0.0.1:5000/mobile_cam</p>

    <div class="flex gap-2">
      <button onclick="startPhoneStreamReceiver()" class="flex-1 py-3 bg-emerald-600 text-white text-xs font-bold rounded-xl hover:bg-emerald-700 shadow-md">
        <i class="fas fa-play mr-1"></i> Start Receiving Live Stream
      </button>
      <button onclick="closePhoneCamModal()" class="py-3 px-4 bg-stone-200 text-stone-800 text-xs font-bold rounded-xl hover:bg-stone-300">Close</button>
    </div>
  </div>
</div>
"""

qr_js_update = """
let phonePollingInterval = null;

function openPhoneCamModal() {
  document.getElementById('phoneCamModal').classList.remove('hidden');
  
  const streamUrl = "http://" + (window.location.hostname || "127.0.0.1") + ":5000/mobile_cam";
  document.getElementById('qrUrlText').textContent = streamUrl;
  
  const qrApi = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(streamUrl)}`;
  document.getElementById('qrCodeImg').src = qrApi;
}

function closePhoneCamModal() {
  document.getElementById('phoneCamModal').classList.add('hidden');
}

function startPhoneStreamReceiver() {
  closePhoneCamModal();
  const video = document.getElementById('activeWebcamVideo');
  const preview = document.getElementById('activeWebcamPreview');
  const placeholder = document.getElementById('activeCamPlaceholder');

  placeholder.classList.add('hidden');
  video.classList.add('hidden');
  preview.classList.remove('hidden');

  if (phonePollingInterval) clearInterval(phonePollingInterval);

  phonePollingInterval = setInterval(() => {
    fetch('http://' + (window.location.hostname || "127.0.0.1") + ':5000/get_frame')
      .then(res => res.json())
      .then(data => {
        if (data.image) {
          preview.src = data.image;
        }
      }).catch(e => {});
  }, 150);

  alert("🟢 Connected to Cell Phone Camera Stream!");
}
"""

if 'id="phoneCamModal"' in html:
    start_m = html.find('<!-- Cell Phone Camera Connect Modal -->')
    end_m = html.find('<!-- Header -->')
    if start_m != -1 and end_m != -1:
        html = html[:start_m] + qr_modal_update + '\n\n' + html[end_m:]

if 'function openPhoneCamModal()' in html:
    start_j = html.find('function openPhoneCamModal()')
    end_j = html.find('function refreshCameraDevices()', start_j)
    if start_j != -1 and end_j != -1:
        html = html[:start_j] + qr_js_update + '\n\n' + html[end_j:]

with open(studio_path, 'w', encoding='utf-8') as f:
    f.write(html)

# Update Desktop Launcher BAT file to start BOTH Python QR Code Server & Laptop App
bat_launcher = f"""@echo off
title CHROMATYPE QR Code Mobile Camera & Laptop Suite
echo Starting CHROMATYPE Local QR Code Mobile Camera Server...
start python "{server_script_path}"
timeout /t 2 >nul
echo Launching Laptop Operator Suite...
start "" "{studio_path}"
"""

desktop_bat_path = os.path.join(desktop_dir, 'Run_CHROMATYPE_Local_Operator.bat')
with open(desktop_bat_path, 'w', encoding='utf-8') as f:
    f.write(bat_launcher)

print("Created QR Code Mobile Cam Server & updated Run_CHROMATYPE_Local_Operator.bat successfully!")
