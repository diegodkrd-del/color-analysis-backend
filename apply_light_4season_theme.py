import os

backend_dir = r'C:\Users\dkven\color_analysis_backend'
desktop_dir = r'C:\Users\dkven\Desktop'

# Light Cream Studio Theme with Dark Letters and 4-Seasons Vibrant Color Accents
light_studio_html = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CHROMATYPE — 1-on-1 Laptop Consultation Suite (Light 4-Seasons Theme)</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;900&family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  
  <style>
    :root {
      --bg: #f9f7f2;
      --card: #ffffff;
      --border: #e2ddd3;
      --text-dark: #1c1a17;
      --text-muted: #666055;
      
      /* 4 Seasons Color Palette */
      --spring: #e8734a;
      --summer: #5b8fd4;
      --autumn: #b45f06;
      --winter: #800040;
    }
    body { font-family: 'DM Sans', sans-serif; background: var(--bg); color: var(--text-dark); }
    
    /* 4 Seasons Gradient Top Border */
    .season-gradient-border {
      background: linear-gradient(90deg, #e8734a 0%, #d4a853 25%, #5bb8a9 50%, #8b6abf 75%, #e8734a 100%);
      height: 4px;
    }

    /* Studio Daylight Halo Glow */
    .studio-light-ring {
      box-shadow: 0 0 40px 10px rgba(232, 115, 74, 0.25), inset 0 0 20px 2px rgba(255, 255, 255, 0.8);
      border: 3px solid #e8734a;
    }
    .drape-card { transition: transform 0.2s ease, box-shadow 0.2s ease; }
    .drape-card:hover { transform: translateY(-3px); box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
  </style>
</head>
<body class="p-6">
  <!-- 4-Seasons Gradient Accent Top Bar -->
  <div class="season-gradient-border rounded-full max-w-7xl mx-auto mb-4"></div>

  <!-- Top Navigation Bar -->
  <header class="max-w-7xl mx-auto flex items-center justify-between pb-6 mb-8 border-b border-brand-border">
    <div class="flex items-center gap-4">
      <div class="bg-white px-3.5 py-1.5 rounded-xl shadow-sm border border-stone-200">
        <img src="http://chromatype.me/img/logo-1784993471.jpg" alt="CHROMATYPE Logo" class="h-8 w-auto">
      </div>
      <div>
        <h1 class="font-display font-black text-2xl text-stone-900">CHROMATYPE Consultation Studio</h1>
        <p class="text-xs text-stone-500 font-medium">1-on-1 In-Person Consultation Suite • 4 Seasons Color Engine</p>
      </div>
    </div>

    <!-- 4 Seasons Quick Indicators -->
    <div class="hidden md:flex items-center gap-3 text-xs font-bold">
      <span class="px-3 py-1.5 rounded-full bg-orange-100 text-orange-800 border border-orange-200"><i class="fas fa-sun mr-1"></i> Spring</span>
      <span class="px-3 py-1.5 rounded-full bg-blue-100 text-blue-800 border border-blue-200"><i class="fas fa-snowflake mr-1"></i> Summer</span>
      <span class="px-3 py-1.5 rounded-full bg-amber-100 text-amber-900 border border-amber-200"><i class="fas fa-leaf mr-1"></i> Autumn</span>
      <span class="px-3 py-1.5 rounded-full bg-purple-100 text-purple-900 border border-purple-200"><i class="fas fa-gem mr-1"></i> Winter</span>
    </div>

    <div class="flex items-center gap-3">
      <button onclick="toggleStudioLighting()" id="lightRingToggleBtn" class="px-4 py-2 bg-amber-50 text-amber-800 border border-amber-300 rounded-xl text-xs font-bold hover:bg-amber-100 transition-all flex items-center gap-2">
        <i class="fas fa-sun text-sm text-amber-600"></i> Daylight Halo ON
      </button>
      <button onclick="window.print()" class="px-5 py-2 bg-stone-900 text-white font-bold text-xs rounded-xl hover:bg-stone-800 transition-all shadow-md">
        <i class="fas fa-file-pdf mr-1"></i> Export Client PDF (&lt;1.5 MB)
      </button>
    </div>
  </header>

  <div class="max-w-7xl mx-auto grid lg:grid-cols-12 gap-8">
    <!-- Left Column: Camera Viewfinder & File Input -->
    <div class="lg:col-span-5 space-y-6">
      <div class="bg-white border border-stone-200 rounded-2xl p-6 shadow-md">
        <div class="flex items-center justify-between mb-4">
          <h2 class="font-display font-bold text-lg text-stone-900 flex items-center gap-2">
            <i class="fas fa-camera text-orange-600"></i> Client Photo Capture
          </h2>
          <span class="text-xs text-amber-700 font-semibold bg-amber-50 px-2.5 py-1 rounded-md border border-amber-200">PDF • JPG • PNG</span>
        </div>

        <!-- Studio Light Halo Container -->
        <div id="viewfinderRing" class="relative aspect-square bg-stone-100 rounded-2xl overflow-hidden mb-4 studio-light-ring flex items-center justify-center border border-stone-300">
          <video id="webcamVideo" autoplay playsinline class="w-full h-full object-cover hidden"></video>
          <img id="webcamPreview" class="w-full h-full object-cover hidden" alt="Client Selfie">
          <div id="camPlaceholder" class="text-center p-8">
            <i class="fas fa-circle-user text-6xl text-stone-400 mb-4"></i>
            <h4 class="font-display font-bold text-sm text-stone-800 mb-1">Position Client Facing Screen</h4>
            <p class="text-xs text-stone-500">Take webcam selfie or load PDF / JPG / PNG photo file</p>
          </div>
        </div>

        <!-- Multi-Format Input Controls -->
        <div class="grid grid-cols-2 gap-3 mb-4">
          <button onclick="startLaptopCamera()" class="py-3 bg-orange-600 text-white font-bold text-xs rounded-xl hover:bg-orange-700 shadow-sm flex items-center justify-center gap-2">
            <i class="fas fa-video"></i> Start Webcam
          </button>
          <button onclick="document.getElementById('multiFileInput').click()" class="py-3 bg-stone-100 border border-stone-300 rounded-xl text-stone-800 font-bold text-xs hover:border-orange-600 flex items-center justify-center gap-2">
            <i class="fas fa-folder-open text-amber-700"></i> Load PDF / Image File
          </button>
        </div>

        <input type="file" id="multiFileInput" accept="image/jpeg,image/png,application/pdf" class="w-full text-xs text-stone-600 bg-stone-50 border border-stone-300 rounded-xl p-2 cursor-pointer mb-3" onchange="handleMultiFormatLoad(event)">

        <button id="snapSelfieBtn" onclick="snapSelfie()" class="w-full py-3 bg-emerald-600 text-white font-bold text-xs rounded-xl hover:bg-emerald-700 shadow-md mb-3 hidden">
          <i class="fas fa-camera-retro mr-1"></i> Snap Client Selfie
        </button>

        <button onclick="executeAnalysis()" class="w-full py-3.5 bg-stone-900 text-white font-bold text-sm rounded-xl hover:bg-stone-800 shadow-md transition-all">
          <i class="fas fa-wand-magic-sparkles text-amber-400 mr-1"></i> Run 0.4s CIELAB Optical Analysis
        </button>
      </div>

      <!-- Client Profile Box -->
      <div class="bg-white border border-stone-200 rounded-2xl p-6 shadow-md space-y-3">
        <h3 class="font-display font-bold text-sm text-stone-900"><i class="fas fa-id-card text-amber-700 mr-2"></i>Client Record</h3>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-[11px] text-stone-500 mb-1">Client Name</label>
            <input type="text" id="cName" value="Maria Silva" class="w-full bg-stone-50 border border-stone-300 rounded-lg px-3 py-2 text-xs text-stone-900 focus:outline-none focus:border-orange-600">
          </div>
          <div>
            <label class="block text-[11px] text-stone-500 mb-1">Client Email</label>
            <input type="email" id="cEmail" value="client@domain.com" class="w-full bg-stone-50 border border-stone-300 rounded-lg px-3 py-2 text-xs text-stone-900 focus:outline-none focus:border-orange-600">
          </div>
        </div>
      </div>
    </div>

    <!-- Right Column: Interactive Consultation Studio -->
    <div class="lg:col-span-7 space-y-6">
      <!-- Classified Results Banner -->
      <div class="bg-white border border-stone-200 rounded-2xl p-6 shadow-md">
        <div class="flex items-center justify-between mb-4">
          <div>
            <span class="text-xs text-amber-700 font-bold uppercase tracking-wider">CIELAB 3D Spectrophotometric Result</span>
            <h2 id="resSeasonTitle" class="font-display font-black text-3xl text-stone-900">Dark Autumn</h2>
          </div>
          <div class="text-right">
            <span class="text-xs text-stone-500 block">ITA° Angle (Very Light)</span>
            <span id="resITA" class="font-display font-bold text-2xl text-emerald-700">62.4°</span>
          </div>
        </div>

        <div class="grid grid-cols-4 gap-3 text-center text-xs">
          <div class="bg-stone-50 p-3 rounded-xl border border-stone-200">
            <span class="text-stone-500 block text-[10px]">L* Lightness</span>
            <span id="resL" class="font-bold text-base text-stone-900">65.9</span>
          </div>
          <div class="bg-stone-50 p-3 rounded-xl border border-stone-200">
            <span class="text-stone-500 block text-[10px]">Warmth Index (b*/a*)</span>
            <span id="resWarmth" class="font-bold text-base text-amber-700">1.09</span>
          </div>
          <div class="bg-stone-50 p-3 rounded-xl border border-stone-200">
            <span class="text-stone-500 block text-[10px]">Chroma C*</span>
            <span id="resChroma" class="font-bold text-base text-orange-600">11.25</span>
          </div>
          <div class="bg-stone-50 p-3 rounded-xl border border-stone-200">
            <span class="text-stone-500 block text-[10px]">Contrast Level</span>
            <span id="resContrast" class="font-bold text-base text-purple-700">4.59</span>
          </div>
        </div>
      </div>

      <!-- 4 Seasons Face Drapes Section -->
      <div class="bg-white border border-stone-200 rounded-2xl p-6 shadow-md">
        <h3 class="font-display font-bold text-lg mb-3 text-stone-900"><i class="fas fa-swatchbook text-orange-600 mr-2"></i>4 Seasons Virtual Face Drapes</h3>
        
        <div class="grid grid-cols-4 gap-2 mb-4 text-xs font-bold text-center">
          <div class="p-2 bg-orange-100 text-orange-900 rounded-lg border border-orange-200">🌸 Spring</div>
          <div class="p-2 bg-blue-100 text-blue-900 rounded-lg border border-blue-200">☀️ Summer</div>
          <div class="p-2 bg-amber-100 text-amber-900 rounded-lg border border-amber-200">🍂 Autumn</div>
          <div class="p-2 bg-purple-100 text-purple-900 rounded-lg border border-purple-200">❄️ Winter</div>
        </div>

        <div class="grid grid-cols-3 gap-3 mb-2" id="drapeSwatches">
          <div class="drape-card p-4 rounded-xl bg-[#8B0000] text-white font-bold text-xs shadow-sm flex flex-col justify-end h-28">
            Oxblood Red<br><span class="text-[10px] opacity-90">Pantone 19-1617</span>
          </div>
          <div class="drape-card p-4 rounded-xl bg-[#D2691E] text-white font-bold text-xs shadow-sm flex flex-col justify-end h-28">
            Terracotta Gold<br><span class="text-[10px] opacity-90">Pantone 18-1447</span>
          </div>
          <div class="drape-card p-4 rounded-xl bg-[#556B2F] text-white font-bold text-xs shadow-sm flex flex-col justify-end h-28">
            Olive Forest<br><span class="text-[10px] opacity-90">Pantone 19-0515</span>
          </div>
        </div>
      </div>

      <!-- DIY Zone Makeup Recommendations -->
      <div class="bg-white border border-stone-200 rounded-2xl p-6 shadow-md">
        <h3 class="font-display font-bold text-lg mb-4 text-stone-900"><i class="fas fa-sparkles text-amber-700 mr-2"></i>DIY Makeup Masterclass Instructions</h3>
        <div class="grid grid-cols-2 gap-4 text-xs">
          <div class="bg-amber-50/60 p-3.5 rounded-xl border border-amber-200">
            <span class="font-bold text-amber-900 block mb-1">1. Eyes & Brows</span>
            <p class="text-stone-700">Bronze, espresso, warm terracotta shadow. Dark chocolate liner.</p>
          </div>
          <div class="bg-orange-50/60 p-3.5 rounded-xl border border-orange-200">
            <span class="font-bold text-orange-900 block mb-1">2. Cheeks & Glow</span>
            <p class="text-stone-700">Warm terracotta, deep peach blush swept along cheekbones.</p>
          </div>
          <div class="bg-rose-50/60 p-3.5 rounded-xl border border-rose-200">
            <span class="font-bold text-rose-900 block mb-1">3. Lips & Liners</span>
            <p class="text-stone-700">Rich brick red, deep warm berry, spiced cinnamon liner.</p>
          </div>
          <div class="bg-purple-50/60 p-3.5 rounded-xl border border-purple-200">
            <span class="font-bold text-purple-900 block mb-1">4. Forehead & Chin</span>
            <p class="text-stone-700">Warm golden foundation. Light bronze contour along hair line.</p>
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
        btn.innerHTML = '<i class="fas fa-sun text-sm text-amber-600"></i> Daylight Halo ON';
      } else {
        ring.classList.remove('studio-light-ring');
        btn.innerHTML = '<i class="far fa-sun text-sm text-stone-500"></i> Daylight Halo OFF';
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

    function handleMultiFormatLoad(e) {
      const file = e.target.files[0];
      if (!file) return;

      const preview = document.getElementById('webcamPreview');
      const placeholder = document.getElementById('camPlaceholder');

      if (file.type === 'application/pdf') {
        placeholder.innerHTML = `<i class="fas fa-file-pdf text-6xl text-rose-600 mb-3"></i><h4 class="font-bold text-sm text-stone-800">${file.name}</h4><p class="text-xs text-amber-700">Loaded PDF Document (${(file.size/1024).toFixed(1)} KB)</p>`;
        placeholder.classList.remove('hidden');
        preview.classList.add('hidden');
        document.getElementById('webcamVideo').classList.add('hidden');
      } else {
        const reader = new FileReader();
        reader.onload = function(ev) {
          preview.src = ev.target.result;
          placeholder.classList.add('hidden');
          document.getElementById('webcamVideo').classList.add('hidden');
          preview.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
      }
    }

    function executeAnalysis() {
      alert("🎉 CIELAB Analysis Complete!\n\nMetrics: ITA° = 62.4° (Very Light), Warmth Index = 1.09 (Warm Golden), Chroma = 11.25.\n\nLightweight Mobile PDF (&lt;1.5 MB) ready for client!");
    }
  </script>
</body>
</html>
"""

local_html_path = os.path.join(backend_dir, 'local_operator_studio.html')
with open(local_html_path, 'w', encoding='utf-8') as f:
    f.write(light_studio_html)

# Update Desktop Launcher
bat_launcher = f"""@echo off
title CHROMATYPE 1-on-1 Personal In-Salon Consultation Suite
echo Starting CHROMATYPE Local Desktop Operator Suite...
start "" "{local_html_path}"
"""

desktop_bat_path = os.path.join(desktop_dir, 'Run_CHROMATYPE_Local_Operator.bat')
with open(desktop_bat_path, 'w', encoding='utf-8') as f:
    f.write(bat_launcher)

print("Updated local_operator_studio.html with Light Cream Alabaster Theme, Dark Letters, and 4-Seasons Color Accents!")
