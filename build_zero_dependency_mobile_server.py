import os

backend_dir = r'C:\Users\dkven\color_analysis_backend'
server_script_path = os.path.join(backend_dir, 'run_mobile_cam_server.py')

server_code = r'''import os
import json
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

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

PHONE_HTML = """<!DOCTYPE html>
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
</html>"""

class MobileCamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/mobile_cam':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(PHONE_HTML.encode('utf-8'))
        elif parsed.path == '/get_frame':
            global latest_frame
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            resp = json.dumps({'image': latest_frame})
            self.wfile.write(resp.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == '/upload_frame':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                global latest_frame
                latest_frame = data.get('image')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(b'{"status":"ok"}')
            except Exception:
                self.send_response(400)
                self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    print(f"🚀 CHROMATYPE ZERO-DEPENDENCY SERVER STARTED at {STREAM_URL}")
    server = HTTPServer(('0.0.0.0', PORT), MobileCamHandler)
    server.serve_forever()
'''

with open(server_script_path, 'w', encoding='utf-8') as f:
    f.write(server_code)

print("Saved pure Python http.server script run_mobile_cam_server.py!")
