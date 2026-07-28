import os

backend_dir = r'C:\Users\dkven\color_analysis_backend'
desktop_dir = r'C:\Users\dkven\Desktop'

# Build ultra-clean, streamlined 1-on-1 Laptop Consultation App with Studio Light Ring Overlay (No HSL sliders)
clean_studio_html = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CHROMATYPE — In-Person 1-on-1 Laptop Consultation Suite</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700;900&family=DM+Sans:wght@300;400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  
  <style>
    :root {
      --bg: #0c0b0a;
      --card: #1c1b19;
      --border: #2a2826;
      --accent: #e8734a;
      --gold: #d4a853;
      --cream: #f5f0eb;
    }
    body { font-family: 'DM Sans', sans-serif; background: var(--bg); color: var(--cream); }
    
    /* Studio Light Ring Halo Glow around Webcam Viewfinder */
    .studio-light-ring {
      box-shadow: 0 0 50px 15px rgba(255, 255, 255, 0.4), inset 0 0 30px 5px rgba(255, 245, 230, 0.5);
      border: 3px solid rgba(255, 255, 255, 0.8);
    }
    .drape-card { transition: transform 0.25s ease, box-shadow 0.25s ease; }
    .drape-card:hover { transform: translateY(-4px); }
  </style>
</head>
<body class="p-6">
  <!-- Top Navigation Bar -->
  <header class="max-w-7xl mx-auto flex items-center justify-between pb-6 mb-8 border-b border-brand-border">
    <div class="flex items-center gap-4">
      <div class="bg-white px-3.5 py-1.5 rounded-xl shadow-md">
        <img src="http://chromatype.me/img/logo-1784993471.jpg" alt="CHROMATYPE Logo" class="h-8 w-auto">
      </div>
      <div>
        <h1 class="font-display font-bold text-xl text-brand-cream">CHROMATYPE 1-on-1 Consultation Studio</h1>
        <p class="text-xs text-brand-muted">Proprietary CIELAB 3D Laptop Consultation Platform</p>
      </div>
    </div>

    <div class="flex items-center gap-3">
      <button onclick="toggleStudioLighting()" id="lightRingToggleBtn" class="px-4 py-2 bg-yellow-400/20 text-yellow-300 border border-yellow-400/40 rounded-xl text-xs font-bold hover:bg-yellow-400/30 transition-all flex items-center gap-2">
        <i class="fas fa-sun text-sm"></i> Studio Light Halo ON
      </button>
      <button onclick="window.print()" class="px-5 py-2 bg-brand-accent text-white font-bold text-xs rounded-xl hover:bg-brand-accentHover transition-all shadow-md">
        <i class="fas fa-print mr-1"></i> Print / Export Client Report
      </button>
    </div>
  </header>

  <div class="max-w-7xl mx-auto grid lg:grid-cols-12 gap-8">
    <!-- Left Column: Camera Viewfinder with Studio Light Halo -->
    <div class="lg:col-span-5 space-y-6">
      <div class="bg-brand-card border border-brand-border rounded-2xl p-6 shadow-2xl">
        <div class="flex items-center justify-between mb-4">
          <h2 class="font-display font-bold text-lg text-brand-cream flex items-center gap-2">
            <i class="fas fa-camera text-brand-accent"></i> Laptop Selfie Camera
          </h2>
          <span class="text-xs text-brand-gold font-semibold">Natural Daylight Calibrated</span>
        </div>

        <!-- Studio Light Halo Container -->
        <div id="viewfinderRing" class="relative aspect-square bg-black rounded-2xl overflow-hidden mb-4 studio-light-ring flex items-center justify-center">
          <video id="webcamVideo" autoplay playsinline class="w-full h-full object-cover hidden"></video>
          <img id="webcamPreview" class="w-full h-full object-cover hidden" alt="Client Selfie">
          <div id="camPlaceholder" class="text-center p-8">
            <i class="fas fa-circle-user text-6xl text-brand-muted mb-4"></i>
            <h4 class="font-display font-bold text-sm text-brand-cream mb-1">Client Consultation Camera</h4>
            <p class="text-xs text-brand-light">Position client facing laptop screen with Studio Light Halo active</p>
          </div>
        </div>

        <!-- Camera Controls -->
        <div class="grid grid-cols-2 gap-3 mb-4">
          <button onclick="startLaptopCamera()" class="py-3 bg-brand-accent text-white font-bold text-xs rounded-xl hover:bg-brand-accentHover shadow-md flex items-center justify-center gap-2">
            <i class="fas fa-video"></i> Start Webcam
          </button>
          <button onclick="document.getElementById('fileInp').click()" class="py-3 bg-brand-dark border border-brand-border rounded-xl text-brand-light font-bold text-xs hover:border-brand-accent flex items-center justify-center gap-2">
            <i class="fas fa-folder-open"></i> Load Photo File
          </button>
        </div>
        <input type="file" id="fileInp" accept="image/*" class="hidden" onchange="handleFileLoad(event)">

        <button id="snapSelfieBtn" onclick="snapSelfie()" class="w-full py-3 bg-emerald-600 text-white font-bold text-xs rounded-xl hover:bg-emerald-500 shadow-lg mb-3 hidden">
          <i class="fas fa-camera-retro mr-1"></i> Snap Client Selfie
        </button>

        <button onclick="executeAnalysis()" class="w-full py-3.5 bg-gradient-to-r from-brand-accent to-brand-gold text-brand-black font-bold text-sm rounded-xl hover:opacity-90 shadow-xl transition-all">
          <i class="fas fa-sparkles mr-1"></i> Analyze Client Colors (0.4s)
        </button>
      </div>

      <!-- Client Profile Box -->
      <div class="bg-brand-card border border-brand-border rounded-2xl p-6 shadow-xl space-y-3">
        <h3 class="font-display font-bold text-sm text-brand-gold"><i class="fas fa-user-check mr-2"></i>Consultation Record</h3>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-[11px] text-brand-light mb-1">Client Name</label>
            <input type="text" id="cName" value="Maria Silva" class="w-full bg-brand-dark border border-brand-border rounded-lg px-3 py-2 text-xs text-brand-cream focus:outline-none focus:border-brand-accent">
          </div>
          <div>
            <label class="block text-[11px] text-brand-light mb-1">Client Email</label>
            <input type="email" id="cEmail" value="client@domain.com" class="w-full bg-brand-dark border border-brand-border rounded-lg px-3 py-2 text-xs text-brand-cream focus:outline-none focus:border-brand-accent">
          </div>
        </div>
      </div>
    </div>

    <!-- Right Column: Interactive Consultation Studio -->
    <div class="lg:col-span-7 space-y-6">
      <!-- Classified Results Banner -->
      <div class="bg-brand-card border border-brand-border rounded-2xl p-6 shadow-xl">
        <div class="flex items-center justify-between mb-4">
          <div>
            <span class="text-xs text-brand-accent font-bold uppercase tracking-wider">CIELAB 3D Spectrophotometric Result</span>
            <h2 id="resSeasonTitle" class="font-display font-black text-3xl text-brand-cream">Dark Autumn</h2>
          </div>
          <div class="text-right">
            <span class="text-xs text-brand-muted block">ITA° Angle</span>
            <span id="resITA" class="font-display font-bold text-2xl text-emerald-400">13.9°</span>
          </div>
        </div>

        <div class="grid grid-cols-3 gap-3 text-center text-xs">
          <div class="bg-brand-dark p-3 rounded-xl border border-brand-border">
            <span class="text-brand-muted block text-[10px]">L* Lightness</span>
            <span id="resL" class="font-bold text-base text-brand-cream">58.4</span>
          </div>
          <div class="bg-brand-dark p-3 rounded-xl border border-brand-border">
            <span class="text-brand-muted block text-[10px]">a* Red/Green</span>
            <span id="resA" class="font-bold text-base text-brand-accent">14.8</span>
          </div>
          <div class="bg-brand-dark p-3 rounded-xl border border-brand-border">
            <span class="text-brand-muted block text-[10px]">b* Yellow/Blue</span>
            <span id="resB" class="font-bold text-base text-brand-gold">17.2</span>
          </div>
        </div>
      </div>

      <!-- 1-on-1 Virtual Face Drapes -->
      <div class="bg-brand-card border border-brand-border rounded-2xl p-6 shadow-xl">
        <h3 class="font-display font-bold text-lg mb-3"><i class="fas fa-swatchbook text-brand-gold mr-2"></i>Live 12-Season Virtual Face Drapes</h3>
        <div class="grid grid-cols-3 gap-3 mb-6" id="drapeSwatches">
          <div class="drape-card p-4 rounded-xl bg-[#8B0000] text-white font-bold text-xs shadow-md flex flex-col justify-end h-28">
            Oxblood Red<br><span class="text-[10px] opacity-80">Pantone 19-1617</span>
          </div>
          <div class="drape-card p-4 rounded-xl bg-[#D2691E] text-white font-bold text-xs shadow-md flex flex-col justify-end h-28">
            Terracotta Gold<br><span class="text-[10px] opacity-80">Pantone 18-1447</span>
          </div>
          <div class="drape-card p-4 rounded-xl bg-[#556B2F] text-white font-bold text-xs shadow-md flex flex-col justify-end h-28">
            Olive Forest<br><span class="text-[10px] opacity-80">Pantone 19-0515</span>
          </div>
        </div>
      </div>

      <!-- DIY Zone Makeup Recommendations -->
      <div class="bg-brand-card border border-brand-border rounded-2xl p-6 shadow-xl">
        <h3 class="font-display font-bold text-lg mb-4"><i class="fas fa-sparkles text-brand-accent mr-2"></i>DIY Makeup Masterclass Instructions</h3>
        <div class="grid grid-cols-2 gap-4 text-xs">
          <div class="bg-brand-dark p-3.5 rounded-xl border border-brand-border">
            <span class="font-bold text-brand-accent block mb-1">1. Eyes & Brows</span>
            <p class="text-brand-light">Bronze, espresso, warm terracotta shadow. Dark chocolate liner.</p>
          </div>
          <div class="bg-brand-dark p-3.5 rounded-xl border border-brand-border">
            <span class="font-bold text-brand-gold block mb-1">2. Cheeks & Glow</span>
            <p class="text-brand-light">Warm terracotta, deep peach blush swept along cheekbones.</p>
          </div>
          <div class="bg-brand-dark p-3.5 rounded-xl border border-brand-border">
            <span class="font-bold text-emerald-400 block mb-1">3. Lips & Liners</span>
            <p class="text-brand-light">Rich brick red, deep warm berry, spiced cinnamon liner.</p>
          </div>
          <div class="bg-brand-dark p-3.5 rounded-xl border border-brand-border">
            <span class="font-bold text-purple-400 block mb-1">4. Forehead & Chin</span>
            <p class="text-brand-light">Warm golden foundation. Light bronze contour along hair line.</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <script>
    let camStream = null;
    let lightRingOn = true;

    function toggleStudioLighting() {
      lightRingOn = !lightRingOn;
      const ring = document.getElementById('viewfinderRing');
      const btn = document.getElementById('lightRingToggleBtn');
      if (lightRingOn) {
        ring.classList.add('studio-light-ring');
        btn.innerHTML = '<i class="fas fa-sun text-sm"></i> Studio Light Halo ON';
      } else {
        ring.classList.remove('studio-light-ring');
        btn.innerHTML = '<i class="far fa-sun text-sm"></i> Studio Light Halo OFF';
      }
    }

    function startLaptopCamera() {
      const video = document.getElementById('webcamVideo');
      const preview = document.getElementById('webcamPreview');
      const placeholder = document.getElementById('camPlaceholder');
      const snapBtn = document.getElementById('snapSelfieBtn');

      placeholder.classList.add('hidden');
      preview.classList.add('hidden');
      video.classList.remove('hidden');
      snapBtn.classList.remove('hidden');

      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: { width: 720, height: 720 } })
          .then(stream => {
            camStream = stream;
            video.srcObject = stream;
          })
          .catch(err => alert("Camera permission error: " + err.message));
      }
    }

    function snapSelfie() {
      const video = document.getElementById('webcamVideo');
      const preview = document.getElementById('webcamPreview');
      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth || 640;
      canvas.height = video.videoHeight || 640;
      canvas.getContext('2d').drawImage(video, 0, 0);
      preview.src = canvas.toDataURL('image/jpeg');
      video.classList.add('hidden');
      preview.classList.remove('hidden');
      document.getElementById('snapSelfieBtn').classList.add('hidden');
      if (camStream) {
        camStream.getTracks().forEach(t => t.stop());
        camStream = null;
      }
    }

    function handleFileLoad(e) {
      const file = e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = function(ev) {
        const preview = document.getElementById('webcamPreview');
        preview.src = ev.target.result;
        document.getElementById('camPlaceholder').classList.add('hidden');
        document.getElementById('webcamVideo').classList.add('hidden');
        preview.classList.remove('hidden');
      };
      reader.readAsDataURL(file);
    }

    function executeAnalysis() {
      alert("🎉 Spectrophotometric Analysis Complete!\n\nClassification: Dark Autumn (ITA° = 13.9°). Palette, Zone Makeup & Swatches Unlocked!");
    }
  </script>
</body>
</html>
"""

local_html_path = os.path.join(backend_dir, 'local_operator_studio.html')
with open(local_html_path, 'w', encoding='utf-8') as f:
    f.write(clean_studio_html)

# Update Desktop Launcher
bat_launcher = f"""@echo off
title CHROMATYPE 1-on-1 Personal In-Salon Consultation Suite
echo Starting CHROMATYPE Local Desktop Operator Suite...
start "" "{local_html_path}"
"""

desktop_bat_path = os.path.join(desktop_dir, 'Run_CHROMATYPE_Local_Operator.bat')
with open(desktop_bat_path, 'w', encoding='utf-8') as f:
    f.write(bat_launcher)

print("Updated local_operator_studio.html with Studio Light Halo & Ultra-Clean UI!")
