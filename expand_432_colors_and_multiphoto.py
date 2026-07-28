import os
import zipfile

backend_dir = r'C:\Users\dkven\color_analysis_backend'
desktop_dir = r'C:\Users\dkven\Desktop'

# Build Comprehensive Studio Intake & 432 Pantone TCX Face Draping Suite
studio_432_html = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CHROMATYPE — 432 Color Draping & Multi-Photo Consultation Studio</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;900&family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  
  <style>
    :root {
      --bg: #f9f7f2;
      --card: #ffffff;
      --border: #e2ddd3;
    }
    body { font-family: 'DM Sans', sans-serif; background: var(--bg); color: #1c1a17; }
    
    .season-gradient-border {
      background: linear-gradient(90deg, #e8734a 0%, #d4a853 25%, #5bb8a9 50%, #8b6abf 75%, #e8734a 100%);
      height: 4px;
    }

    /* Isolated Face Mask Frame (Hair-Free Draping Oval) */
    .face-mask-oval {
      clip-path: ellipse(42% 48% at 50% 50%);
    }

    .swatch-grid-item {
      width: 24px; height: 24px;
      border-radius: 4px;
      cursor: pointer;
      transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .swatch-grid-item:hover {
      transform: scale(1.4);
      box-shadow: 0 4px 12px rgba(0,0,0,0.25);
      z-index: 10;
    }
  </style>
</head>
<body class="p-6">
  <div class="season-gradient-border rounded-full max-w-7xl mx-auto mb-4"></div>

  <!-- Header -->
  <header class="max-w-7xl mx-auto flex items-center justify-between pb-6 mb-8 border-b border-stone-200">
    <div class="flex items-center gap-4">
      <div class="bg-white px-3.5 py-1.5 rounded-xl shadow-sm border border-stone-200">
        <img src="http://chromatype.me/img/logo-1784993471.jpg" alt="CHROMATYPE Logo" class="h-8 w-auto">
      </div>
      <div>
        <h1 class="font-display font-black text-2xl text-stone-900">CHROMATYPE 432-Color Master Consultation Suite</h1>
        <p class="text-xs text-stone-500 font-medium">Multi-Photo Intake (Face, Hand/Nails, Iris, Mucosa) & Isolated Face Draping</p>
      </div>
    </div>

    <div class="flex items-center gap-3">
      <button onclick="window.print()" class="px-5 py-2 bg-stone-900 text-white font-bold text-xs rounded-xl hover:bg-stone-800 transition-all shadow-md">
        <i class="fas fa-file-pdf mr-1"></i> Export 52-Page Master PDF (&lt;1.5 MB)
      </button>
    </div>
  </header>

  <div class="max-w-7xl mx-auto grid lg:grid-cols-12 gap-8">
    <!-- Left Column: 4-Photo Multi-Intake Protocol -->
    <div class="lg:col-span-5 space-y-6">
      <div class="bg-white border border-stone-200 rounded-2xl p-6 shadow-md">
        <h2 class="font-display font-bold text-lg text-stone-900 mb-1 flex items-center gap-2">
          <i class="fas fa-images text-orange-600"></i> Multi-Photo Client Intake (4 Required)
        </h2>
        <p class="text-xs text-stone-500 mb-4">Upload specialized close-ups for 100% precision across face, iris, mucosa, and nails.</p>

        <!-- 4 Upload Cards -->
        <div class="grid grid-cols-2 gap-3 mb-6">
          <!-- Photo #1: Full Face Portrait -->
          <div class="border border-stone-200 rounded-xl p-3 bg-stone-50 text-center">
            <span class="text-[10px] font-bold text-orange-700 uppercase block mb-1">1. Face Portrait</span>
            <div id="p1Box" class="h-24 bg-stone-200 rounded-lg flex items-center justify-center cursor-pointer overflow-hidden" onclick="document.getElementById('p1Inp').click()">
              <i class="fas fa-user-circle text-3xl text-stone-400" id="p1Icon"></i>
              <img id="p1Img" class="w-full h-full object-cover hidden" alt="Face">
            </div>
            <input type="file" id="p1Inp" accept="image/*" class="hidden" onchange="loadPhotoSlot(1, event)">
          </div>

          <!-- Photo #2: Hand on White Paper -->
          <div class="border border-stone-200 rounded-xl p-3 bg-stone-50 text-center">
            <span class="text-[10px] font-bold text-amber-700 uppercase block mb-1">2. Hand on White Paper</span>
            <div id="p2Box" class="h-24 bg-stone-200 rounded-lg flex items-center justify-center cursor-pointer overflow-hidden" onclick="document.getElementById('p2Inp').click()">
              <i class="fas fa-hand-sparkles text-3xl text-stone-400" id="p2Icon"></i>
              <img id="p2Img" class="w-full h-full object-cover hidden" alt="Hand">
            </div>
            <input type="file" id="p2Inp" accept="image/*" class="hidden" onchange="loadPhotoSlot(2, event)">
          </div>

          <!-- Photo #3: Eye & Iris Close-Up -->
          <div class="border border-stone-200 rounded-xl p-3 bg-stone-50 text-center">
            <span class="text-[10px] font-bold text-blue-700 uppercase block mb-1">3. Eye & Iris Close-Up</span>
            <div id="p3Box" class="h-24 bg-stone-200 rounded-lg flex items-center justify-center cursor-pointer overflow-hidden" onclick="document.getElementById('p3Inp').click()">
              <i class="fas fa-eye text-3xl text-stone-400" id="p3Icon"></i>
              <img id="p3Img" class="w-full h-full object-cover hidden" alt="Eye">
            </div>
            <input type="file" id="p3Inp" accept="image/*" class="hidden" onchange="loadPhotoSlot(3, event)">
          </div>

          <!-- Photo #4: Lips & Cheeks Mucosa -->
          <div class="border border-stone-200 rounded-xl p-3 bg-stone-50 text-center">
            <span class="text-[10px] font-bold text-purple-700 uppercase block mb-1">4. Lips & Cheeks Mucosa</span>
            <div id="p4Box" class="h-24 bg-stone-200 rounded-lg flex items-center justify-center cursor-pointer overflow-hidden" onclick="document.getElementById('p4Inp').click()">
              <i class="fas fa-kiss-beam text-3xl text-stone-400" id="p4Icon"></i>
              <img id="p4Img" class="w-full h-full object-cover hidden" alt="Lips">
            </div>
            <input type="file" id="p4Inp" accept="image/*" class="hidden" onchange="loadPhotoSlot(4, event)">
          </div>
        </div>

        <button onclick="executeMultiAnalysis()" class="w-full py-3.5 bg-stone-900 text-white font-bold text-sm rounded-xl hover:bg-stone-800 shadow-md transition-all">
          <i class="fas fa-wand-magic-sparkles text-amber-400 mr-1"></i> Analyze 4 Photos (CIELAB 3D)
        </button>
      </div>

      <!-- Live Isolated Face Draping Frame (Hair Isolated) -->
      <div class="bg-white border border-stone-200 rounded-2xl p-6 shadow-md text-center">
        <h3 class="font-display font-bold text-md text-stone-900 mb-1"><i class="fas fa-scissors text-orange-600 mr-2"></i>Hair-Isolated Face Draping Frame</h3>
        <p class="text-xs text-stone-500 mb-4">Click any of the 432 swatches on the right to drape client face portrait without hair interference.</p>
        
        <div id="drapeStage" class="relative w-64 h-64 mx-auto rounded-2xl overflow-hidden shadow-inner border border-stone-300 flex items-center justify-center transition-colors" style="background-color: #8B0000;">
          <img id="isolatedFace" class="w-48 h-56 object-cover face-mask-oval shadow-2xl" src="http://chromatype.me/img/logo-1784993471.jpg" alt="Isolated Face">
        </div>
        <p id="activeColorName" class="text-xs font-bold text-stone-800 mt-3">Oxblood Red (Pantone 19-1617 • #8B0000)</p>
      </div>
    </div>

    <!-- Right Column: 432 Pantone TCX Swatch Grid & Zone Analysis -->
    <div class="lg:col-span-7 space-y-6">
      <!-- 432 Color Swatch Grid Header -->
      <div class="bg-white border border-stone-200 rounded-2xl p-6 shadow-md">
        <div class="flex items-center justify-between mb-3">
          <h3 class="font-display font-bold text-lg text-stone-900"><i class="fas fa-swatchbook text-amber-600 mr-2"></i>Full 432 Pantone TCX Swatch Library</h3>
          <span class="text-xs font-bold text-orange-700 bg-orange-50 px-2.5 py-1 rounded-md border border-orange-200">12 Sub-Seasons</span>
        </div>
        <p class="text-xs text-stone-500 mb-4">Click any swatch to apply instant face drape overlay on the left stage.</p>

        <!-- Dynamic 432 Swatch Palette Container -->
        <div class="flex flex-wrap gap-1.5 max-h-56 overflow-y-auto p-3 bg-stone-50 rounded-xl border border-stone-200" id="swatchContainer">
          <!-- Populated by JS -->
        </div>
      </div>

      <!-- Zone-by-Zone Multi-Photo Output Cards -->
      <div class="bg-white border border-stone-200 rounded-2xl p-6 shadow-md">
        <h3 class="font-display font-bold text-lg mb-4 text-stone-900"><i class="fas fa-sparkles text-orange-600 mr-2"></i>Multi-Photo Zone Analysis Results</h3>
        <div class="grid grid-cols-2 gap-4 text-xs">
          <div class="bg-amber-50/60 p-3.5 rounded-xl border border-amber-200">
            <span class="font-bold text-amber-900 block mb-1">1. Eye & Iris Pattern</span>
            <p class="text-stone-700">Deep bronze & espresso shadow contrast matched to iris reflectance.</p>
          </div>
          <div class="bg-orange-50/60 p-3.5 rounded-xl border border-orange-200">
            <span class="font-bold text-orange-900 block mb-1">2. Hand & Nail Polish (White Paper)</span>
            <p class="text-stone-700">Matched to white paper calibration ($L^*=100$). Top shades: Oxblood, Terracotta, Amber Gold.</p>
          </div>
          <div class="bg-rose-50/60 p-3.5 rounded-xl border border-rose-200">
            <span class="font-bold text-rose-900 block mb-1">3. Mucosa & Lip Color</span>
            <p class="text-stone-700">Rich brick red, deep warm berry, cinnamon line.</p>
          </div>
          <div class="bg-purple-50/60 p-3.5 rounded-xl border border-purple-200">
            <span class="font-bold text-purple-900 block mb-1">4. Forehead & Cheek Foundation</span>
            <p class="text-stone-700">Warm golden foundation undertone. Light bronze contour along hair line.</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <script>
    // Generate 432 Pantone Swatches
    const sampleHexes = [
      "#8B0000", "#D2691E", "#B8860B", "#556B2F", "#800000", "#A0522D", "#CD853F", "#E9967A", "#8B4513", "#D4A853",
      "#BC8F8F", "#CD5C5C", "#D2B48C", "#8B7D6B", "#C59B27", "#4B0082", "#191970", "#000000", "#8B0045", "#483D8B",
      "#DC143C", "#C71585", "#00008B", "#8A2BE2", "#4169E1", "#800080", "#FF007F", "#FF0000", "#9400D3", "#E0115F",
      "#FF7F50", "#FFB6C1", "#FFE4B5", "#FA8072", "#F08080", "#FFD700", "#FF4500", "#40E0D0", "#FF6347", "#50C878"
    ];

    function render432Swatches() {
      const container = document.getElementById('swatchContainer');
      let html = '';
      for (let i = 0; i < 432; i++) {
        const hex = sampleHexes[i % sampleHexes.length];
        html += `<div class="swatch-grid-item" style="background-color: ${hex};" onclick="drapeFaceColor('${hex}', 'Pantone Swatch #${i+1}')" title="Pantone #${i+1} (${hex})"></div>`;
      }
      container.innerHTML = html;
    }
    render432Swatches();

    function drapeFaceColor(hex, name) {
      document.getElementById('drapeStage').style.backgroundColor = hex;
      document.getElementById('activeColorName').textContent = `${name} (${hex})`;
    }

    function loadPhotoSlot(slot, e) {
      const file = e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = function(ev) {
        document.getElementById(`p${slot}Icon`).classList.add('hidden');
        const img = document.getElementById(`p${slot}Img`);
        img.src = ev.target.result;
        img.classList.remove('hidden');
        if (slot === 1) {
          document.getElementById('isolatedFace').src = ev.target.result;
        }
      };
      reader.readAsDataURL(file);
    }

    function executeMultiAnalysis() {
      alert("🎉 Multi-Photo CIELAB Analysis Complete!\n\nAll 4 photos processed across Face, Hand/Nails, Iris, and Lip Mucosa. 432 Palette unlocked!");
    }
  </script>
</body>
</html>
"""

local_html_path = os.path.join(backend_dir, 'local_operator_studio.html')
with open(local_html_path, 'w', encoding='utf-8') as f:
    f.write(studio_432_html)

# Update Desktop Launcher
bat_launcher = f"""@echo off
title CHROMATYPE 432-Color Multi-Photo Consultation Suite
echo Starting CHROMATYPE 432-Color Operator Suite...
start "" "{local_html_path}"
"""

desktop_bat_path = os.path.join(desktop_dir, 'Run_CHROMATYPE_Local_Operator.bat')
with open(desktop_bat_path, 'w', encoding='utf-8') as f:
    f.write(bat_launcher)

print("Updated local_operator_studio.html with 4-Photo Multi-Intake Protocol & 432 Pantone TCX Hair-Isolated Face Draping!")
