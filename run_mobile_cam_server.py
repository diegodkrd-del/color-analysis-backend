import os
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
