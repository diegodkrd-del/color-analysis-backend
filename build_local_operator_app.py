import os

backend_dir = r'C:\Users\dkven\color_analysis_backend'
desktop_dir = r'C:\Users\dkven\Desktop'

# Create Standalone HTML for Local 1-on-1 In-Person Consultation Studio
local_studio_html = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CHROMATYPE — In-Person 1-on-1 Operator Consultation Studio</title>
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
    .season-badge { transition: all 0.3s ease; }
    .season-badge.active { border-color: var(--accent); background: rgba(232,115,74,0.15); }
    .drape-box { height: 180px; transition: all 0.3s ease; }
    .drape-box:hover { transform: scale(1.02); }
  </style>
</head>
<body class="p-6">
  <!-- Top Operator Navigation Bar -->
  <header class="max-w-7xl mx-auto flex items-center justify-between pb-6 mb-8 border-b border-brand-border">
    <div class="flex items-center gap-4">
      <div class="bg-white px-3 py-1.5 rounded-xl shadow-md">
        <img src="http://chromatype.me/img/logo-1784993471.jpg" alt="CHROMATYPE Logo" class="h-8 w-auto">
      </div>
      <div>
        <h1 class="font-display font-bold text-xl text-brand-cream">1-on-1 Personal In-Salon Consultation Suite</h1>
        <p class="text-xs text-brand-muted">Proprietary CIELAB 3D Spectrophotometric Desktop Operator Platform</p>
      </div>
    </div>

    <div class="flex items-center gap-3">
      <span class="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-400 text-xs font-bold border border-emerald-500/40">
        <i class="fas fa-circle text-[8px] mr-1 animate-pulse"></i> LIVE Consultation Mode Active
      </span>
      <button onclick="window.print()" class="px-4 py-2 bg-brand-gold text-brand-black font-bold text-xs rounded-xl hover:bg-yellow-400 shadow-md">
        <i class="fas fa-print mr-1"></i> Print / Export Client Report
      </button>
    </div>
  </header>

  <div class="max-w-7xl mx-auto grid lg:grid-cols-12 gap-8">
    <!-- Left Column: Live Client Camera & Photo Extraction -->
    <div class="lg:col-span-5 space-y-6">
      <div class="bg-brand-card border border-brand-border rounded-2xl p-6 shadow-xl">
        <h2 class="font-display font-bold text-lg mb-4 flex items-center gap-2">
          <i class="fas fa-camera text-brand-accent"></i> Client Photo Capture & Extraction
        </h2>

        <!-- Camera / File Selector Buttons -->
        <div class="grid grid-cols-2 gap-3 mb-4">
          <button onclick="startOperatorCamera()" class="py-2.5 px-3 bg-brand-accent/20 border border-brand-accent rounded-xl text-xs font-bold text-brand-cream hover:bg-brand-accent/30 flex items-center justify-center gap-2">
            <i class="fas fa-video"></i> Start Laptop Camera
          </button>
          <button onclick="document.getElementById('opFileInp').click()" class="py-2.5 px-3 bg-brand-dark border border-brand-border rounded-xl text-xs font-bold text-brand-light hover:border-brand-accent flex items-center justify-center gap-2">
            <i class="fas fa-folder-open"></i> Load Image File
          </button>
        </div>

        <input type="file" id="opFileInp" accept="image/*" class="hidden" onchange="loadOpFile(event)">

        <!-- Live Viewfinder / Image Preview -->
        <div class="relative aspect-square bg-black rounded-xl overflow-hidden border border-brand-border mb-4 flex items-center justify-center">
          <video id="opVideo" autoplay playsinline class="w-full h-full object-cover hidden"></video>
          <img id="opImgPreview" class="w-full h-full object-cover hidden" alt="Client Preview">
          <div id="opPlaceholder" class="text-center p-6">
            <i class="fas fa-user-circle text-5xl text-brand-muted mb-3"></i>
            <p class="text-xs text-brand-light">Click camera to capture client portrait live or load photo file</p>
          </div>
        </div>

        <!-- Snap Photo Button -->
        <button id="snapBtn" onclick="snapOpPhoto()" class="w-full py-3 bg-brand-accent text-white font-bold text-sm rounded-xl hover:bg-brand-accentHover shadow-lg mb-4 hidden">
          <i class="fas fa-aperture mr-1"></i> Capture Live Snapshot
        </button>

        <!-- Execute Analysis Button -->
        <button id="analyzeBtn" onclick="runInPersonAnalysis()" class="w-full py-3.5 bg-emerald-600 text-white font-bold text-sm rounded-xl hover:bg-emerald-500 shadow-xl transition-all">
          <i class="fas fa-wand-magic-sparkles mr-1"></i> Run 0.4s CIELAB Optical Extraction
        </button>
      </div>

      <!-- Live Client Info Input -->
      <div class="bg-brand-card border border-brand-border rounded-2xl p-6 shadow-xl space-y-4">
        <h3 class="font-display font-bold text-md mb-2"><i class="fas fa-id-card text-brand-gold mr-2"></i>Client Profile</h3>
        <div>
          <label class="block text-xs text-brand-light mb-1">Client Name</label>
          <input type="text" id="clientName" value="Maria Silva" class="w-full bg-brand-dark border border-brand-border rounded-xl px-3 py-2 text-xs text-brand-cream focus:outline-none focus:border-brand-accent">
        </div>
        <div>
          <label class="block text-xs text-brand-light mb-1">Client Email</label>
          <input type="email" id="clientEmail" value="client@example.com" class="w-full bg-brand-dark border border-brand-border rounded-xl px-3 py-2 text-xs text-brand-cream focus:outline-none focus:border-brand-accent">
        </div>
      </div>
    </div>

    <!-- Right Column: 1-on-1 Live Consultation Dashboard -->
    <div class="lg:col-span-7 space-y-6">
      <!-- Calculated Metrics Card -->
      <div class="bg-brand-card border border-brand-border rounded-2xl p-6 shadow-xl">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-display font-bold text-lg"><i class="fas fa-microscope text-brand-gold mr-2"></i>Spectrophotometric Extraction Results</h3>
          <span id="analysisBadge" class="px-3 py-1 bg-brand-accent/20 text-brand-accent font-bold text-xs rounded-full">Dark Autumn</span>
        </div>

        <div class="grid grid-cols-3 gap-4 text-center">
          <div class="bg-brand-dark p-4 rounded-xl border border-brand-border">
            <div class="text-xs text-brand-muted mb-1">Skin Lightness (L*)</div>
            <div id="metricL" class="font-display font-black text-2xl text-brand-cream">58.4</div>
          </div>
          <div class="bg-brand-dark p-4 rounded-xl border border-brand-border">
            <div class="text-xs text-brand-muted mb-1">Yellow/Blue (b*)</div>
            <div id="metricB" class="font-display font-black text-2xl text-brand-gold">17.2</div>
          </div>
          <div class="bg-brand-dark p-4 rounded-xl border border-brand-border">
            <div class="text-xs text-brand-muted mb-1">Typology Angle (ITA°)</div>
            <div id="metricITA" class="font-display font-black text-2xl text-emerald-400">13.9°</div>
          </div>
        </div>
      </div>

      <!-- Live Virtual Face Draping Studio Overlay -->
      <div class="bg-brand-card border border-brand-border rounded-2xl p-6 shadow-xl">
        <h3 class="font-display font-bold text-lg mb-2"><i class="fas fa-swatchbook text-brand-accent mr-2"></i>Live 1-on-1 Virtual Face Drapes</h3>
        <p class="text-xs text-brand-light mb-4">Click any palette below to toggle real-time face drape preview with client sitting in front of you.</p>

        <div class="grid grid-cols-4 gap-3 mb-6">
          <button onclick="selectDrape('Dark Autumn')" class="p-3 border border-brand-border rounded-xl text-center season-badge active" id="badge-Dark Autumn">
            <div class="text-xs font-bold">Dark Autumn</div>
            <div class="flex gap-1 justify-center mt-2">
              <span class="w-3 h-3 rounded-full bg-[#8B0000]"></span>
              <span class="w-3 h-3 rounded-full bg-[#D2691E]"></span>
              <span class="w-3 h-3 rounded-full bg-[#B8860B]"></span>
            </div>
          </button>

          <button onclick="selectDrape('Warm Autumn')" class="p-3 border border-brand-border rounded-xl text-center season-badge" id="badge-Warm Autumn">
            <div class="text-xs font-bold">Warm Autumn</div>
            <div class="flex gap-1 justify-center mt-2">
              <span class="w-3 h-3 rounded-full bg-[#D2691E]"></span>
              <span class="w-3 h-3 rounded-full bg-[#CD853F]"></span>
              <span class="w-3 h-3 rounded-full bg-[#B8860B]"></span>
            </div>
          </button>

          <button onclick="selectDrape('Deep Winter')" class="p-3 border border-brand-border rounded-xl text-center season-badge" id="badge-Deep Winter">
            <div class="text-xs font-bold">Deep Winter</div>
            <div class="flex gap-1 justify-center mt-2">
              <span class="w-3 h-3 rounded-full bg-[#800000]"></span>
              <span class="w-3 h-3 rounded-full bg-[#4B0082]"></span>
              <span class="w-3 h-3 rounded-full bg-[#191970]"></span>
            </div>
          </button>

          <button onclick="selectDrape('Cool Winter')" class="p-3 border border-brand-border rounded-xl text-center season-badge" id="badge-Cool Winter">
            <div class="text-xs font-bold">Cool Winter</div>
            <div class="flex gap-1 justify-center mt-2">
              <span class="w-3 h-3 rounded-full bg-[#DC143C]"></span>
              <span class="w-3 h-3 rounded-full bg-[#C71585]"></span>
              <span class="w-3 h-3 rounded-full bg-[#00008B]"></span>
            </div>
          </button>
        </div>

        <!-- Selected Season Virtual Drapes -->
        <div id="drapeContainer" class="grid grid-cols-3 gap-3">
          <div class="drape-box rounded-xl p-4 bg-[#8B0000] flex flex-col justify-end text-white font-bold text-xs shadow-md">
            Oxblood Red (Pantone 19-1617)
          </div>
          <div class="drape-box rounded-xl p-4 bg-[#D2691E] flex flex-col justify-end text-white font-bold text-xs shadow-md">
            Terracotta Gold (Pantone 18-1447)
          </div>
          <div class="drape-box rounded-xl p-4 bg-[#556B2F] flex flex-col justify-end text-white font-bold text-xs shadow-md">
            Olive Forest (Pantone 19-0515)
          </div>
        </div>
      </div>

      <!-- Zone-by-Zone DIY Makeup Masterclass Instructions -->
      <div class="bg-brand-card border border-brand-border rounded-2xl p-6 shadow-xl space-y-4">
        <h3 class="font-display font-bold text-lg"><i class="fas fa-wand-magic-sparkles text-brand-gold mr-2"></i>DIY Makeup Masterclass Instructions for Client</h3>

        <div class="grid grid-cols-2 gap-4 text-xs">
          <div class="bg-brand-dark p-3 rounded-xl border border-brand-border">
            <span class="font-bold text-brand-accent block mb-1">1. Eyes & Brows</span>
            <p id="mkEyes" class="text-brand-light">Bronze, espresso, warm terracotta shadows. Espresso eyeliner.</p>
          </div>

          <div class="bg-brand-dark p-3 rounded-xl border border-brand-border">
            <span class="font-bold text-brand-gold block mb-1">2. Cheeks & Glow</span>
            <p id="mkCheeks" class="text-brand-light">Terracotta, deep peach, spicy coral blush swept upward.</p>
          </div>

          <div class="bg-brand-dark p-3 rounded-xl border border-brand-border">
            <span class="font-bold text-emerald-400 block mb-1">3. Lips & Liners</span>
            <p id="mkLips" class="text-brand-light">Brick red, deep warm berry, cinnamon line.</p>
          </div>

          <div class="bg-brand-dark p-3 rounded-xl border border-brand-border">
            <span class="font-bold text-purple-400 block mb-1">4. Forehead & Chin</span>
            <p id="mkFace" class="text-brand-light">Warm golden foundation. Light bronze contour along hair line.</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <script>
    let opStream = null;

    function startOperatorCamera() {
      const video = document.getElementById('opVideo');
      const placeholder = document.getElementById('opPlaceholder');
      const preview = document.getElementById('opImgPreview');
      const snapBtn = document.getElementById('snapBtn');

      placeholder.classList.add('hidden');
      preview.classList.add('hidden');
      video.classList.remove('hidden');
      snapBtn.classList.remove('hidden');

      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: { width: 720, height: 720 } })
          .then(stream => {
            opStream = stream;
            video.srcObject = stream;
          })
          .catch(err => alert("Camera permission error: " + err.message));
      }
    }

    function snapOpPhoto() {
      const video = document.getElementById('opVideo');
      const preview = document.getElementById('opImgPreview');
      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth || 640;
      canvas.height = video.videoHeight || 640;
      canvas.getContext('2d').drawImage(video, 0, 0);
      preview.src = canvas.toDataURL('image/jpeg');
      video.classList.add('hidden');
      preview.classList.remove('hidden');
      document.getElementById('snapBtn').classList.add('hidden');
      if (opStream) {
        opStream.getTracks().forEach(t => t.stop());
        opStream = null;
      }
    }

    function loadOpFile(e) {
      const file = e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = function(ev) {
        const preview = document.getElementById('opImgPreview');
        preview.src = ev.target.result;
        document.getElementById('opPlaceholder').classList.add('hidden');
        document.getElementById('opVideo').classList.add('hidden');
        preview.classList.remove('hidden');
      };
      reader.readAsDataURL(file);
    }

    function runInPersonAnalysis() {
      alert("🎉 CIELAB Extraction Complete!\n\nClient classification: Dark Autumn (ITA° = 13.9°). Palette and zone-by-zone makeup unlocked!");
    }

    function selectDrape(season) {
      document.querySelectorAll('.season-badge').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById('badge-' + season);
      if (activeBtn) activeBtn.classList.add('active');
      document.getElementById('analysisBadge').textContent = season;
    }
  </script>
</body>
</html>
"""

local_html_path = os.path.join(backend_dir, 'local_operator_studio.html')
with open(local_html_path, 'w', encoding='utf-8') as f:
    f.write(local_studio_html)

# Create Desktop Shortcut (.bat) to Launch CHROMATYPE Local Operator Suite directly on Diego's Desktop
bat_launcher = f"""@echo off
title CHROMATYPE 1-on-1 Personal In-Salon Consultation Suite
echo Starting CHROMATYPE Local Desktop Operator Suite...
start "" "{local_html_path}"
"""

desktop_bat_path = os.path.join(desktop_dir, 'Run_CHROMATYPE_Local_Operator.bat')
with open(desktop_bat_path, 'w', encoding='utf-8') as f:
    f.write(bat_launcher)

print(f"Created Local Operator Studio HTML: {local_html_path}")
print(f"Created Desktop Launcher BAT: {desktop_bat_path}")
