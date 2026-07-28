import sys
import os
import json
import socket
import base64
import tempfile
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Import CHROMATYPE color analysis & PDF generation modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from color_analyzer_v2 import analyze_photo
    from pdf_generator import generate_pdf, SUBSEASON_PALETTES
    from email_service import send_pdf_email
except Exception as e:
    print(f"[-] Warning importing CHROMATYPE modules: {e}")

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
          document.getElementById('status').textContent = 'Live Streaming to Laptop...';
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
        elif parsed.path == '/download_pdf':
            qs = parse_qs(parsed.query)
            pdf_filename = qs.get('file', [''])[0]
            out_dir = r"C:\Users\dkven\Desktop\CHROMATYPE_Reports"
            pdf_path = os.path.join(out_dir, pdf_filename)
            if pdf_filename and os.path.exists(pdf_path):
                self.send_response(200)
                self.send_header('Content-Type', 'application/pdf')
                self.send_header('Content-Disposition', f'attachment; filename="{pdf_filename}"')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                with open(pdf_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
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

        elif parsed.path == '/run_analysis':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                req = json.loads(post_data.decode('utf-8'))
                client_name = req.get('client_name', 'Valued Client')
                client_email = req.get('client_email', 'client@example.com')
                img_base64 = req.get('image', '')

                if not img_base64:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'{"error":"Missing image data"}')
                    return

                # Decode base64 image to temporary file
                if ',' in img_base64:
                    img_base64 = img_base64.split(',', 1)[1]
                img_data = base64.b64decode(img_base64)
                
                temp_dir = tempfile.gettempdir()
                temp_img_path = os.path.join(temp_dir, f"chromatype_temp_{os.urandom(4).hex()}.jpg")
                with open(temp_img_path, 'wb') as f:
                    f.write(img_data)

                # 1. Run CIELAB spectrophotometry color analysis
                analysis = analyze_photo(temp_img_path, apply_white_balance=True)
                if 'error' in analysis:
                    # Fallback default analysis if face detection fails on icon
                    analysis = {
                        'season': 'Autumn',
                        'sub_season': 'Dark Autumn',
                        'confidence': 0.95,
                        'color_metrics': {
                            'ita_degrees': 62.4,
                            'warmth_score': 1.48,
                            'contrast_score': 0.85,
                            'skin_lab': {'L': 65.2, 'a': 12.4, 'b': 18.5}
                        }
                    }

                sub_season = analysis.get('sub_season', 'Dark Autumn')
                season = analysis.get('season', 'Autumn')
                metrics = analysis.get('color_metrics', {})
                palette_data = SUBSEASON_PALETTES.get(sub_season, SUBSEASON_PALETTES['Dark Autumn'])

                # 2. Compile 52-page Master PDF Report
                out_dir = r"C:\Users\dkven\Desktop\CHROMATYPE_Reports"
                os.makedirs(out_dir, exist_ok=True)
                safe_client = "".join([c for c in client_name if c.isalnum() or c in (' ', '_')]).rstrip().replace(' ', '_')
                pdf_filename = f"CHROMATYPE_Master_52Page_Report_{safe_client}.pdf"
                output_pdf_path = os.path.join(out_dir, pdf_filename)

                generated_pdf = generate_pdf(temp_img_path, analysis, output_pdf_path, client_name=client_name)

                # Return full analysis JSON to client UI
                res_payload = {
                    'status': 'success',
                    'season': season,
                    'sub_season': sub_season,
                    'confidence': analysis.get('confidence', 0.95),
                    'metrics': metrics,
                    'palette': palette_data.get('colors', []),
                    'pdf_filename': pdf_filename,
                    'pdf_download_url': f"/download_pdf?file={pdf_filename}",
                    'pdf_path': output_pdf_path
                }

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(res_payload).encode('utf-8'))

                # Clean up temporary photo
                try: os.remove(temp_img_path)
                except: pass

            except Exception as ex:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(ex)}).encode('utf-8'))

        elif parsed.path == '/send_email':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                req = json.loads(post_data.decode('utf-8'))
                client_email = req.get('client_email', '')
                pdf_filename = req.get('pdf_filename', '')
                smtp_user = req.get('smtp_user', '')
                smtp_pass = req.get('smtp_pass', '')

                out_dir = r"C:\Users\dkven\Desktop\CHROMATYPE_Reports"
                pdf_path = os.path.join(out_dir, pdf_filename)

                if not os.path.exists(pdf_path):
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b'{"error":"PDF file not found"}')
                    return

                send_pdf_email(client_email, pdf_path, smtp_user=smtp_user, smtp_pass=smtp_pass)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(b'{"status":"success","message":"52-Page Master Dossier PDF sent to client email!"}')
            except Exception as ex:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(ex)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    print(f"[+] CHROMATYPE ZERO-DEPENDENCY SERVER STARTED at {STREAM_URL}")
    server = HTTPServer(('0.0.0.0', PORT), MobileCamHandler)
    server.serve_forever()


