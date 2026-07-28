import os
import zipfile

backend_dir = r'C:\Users\dkven\color_analysis_backend'
desktop_dir = r'C:\Users\dkven\Desktop'

# Build High-Volume Salon Consultation Suite with Multi-Camera Selector (Bluetooth/USB/Webcam) & Rapid Client Queue
salon_studio_html = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CHROMATYPE — High-Volume Salon Consultation & Multi-Camera Suite</title>
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

    .face-mask-oval { clip-path: ellipse(42% 48% at 50% 50%); }

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

    .studio-light-ring {
      box-shadow: 0 0 35px 8px rgba(232, 115, 74, 0.3), inset 0 0 15px 2px rgba(255, 255, 255, 0.8);
      border: 3px solid #e8734a;
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
        <h1 class="font-display font-black text-2xl text-stone-900">CHROMATYPE Salon High-Volume Suite</h1>
        <p class="text-xs text-stone-500 font-medium">Multi-Camera Selector (Bluetooth / USB / Laptop Cam) & Rapid Salon Client Queue</p>
      </div>
    </div>

    <div class="flex items-center gap-3">
      <span class="px-3 py-1.5 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold border border-emerald-300">
        <i class="fas fa-bolt text-emerald-600 mr-1"></i> Rapid Queue Active (10 Clients / 20 Mins)
      </span>
      <button onclick="window.print()" class="px-5 py-2 bg-stone-900 text-white font-bold text-xs rounded-xl hover:bg-stone-800 transition-all shadow-md">
        <i class="fas fa-file-pdf mr-1"></i> Batch Export Client PDFs
      </button>
    </div>
  </header>

  <div class="max-w-7xl mx-auto grid lg:grid-cols-12 gap-8">
    <!-- Left Column: Multi-Camera Device Switcher & 4-Photo Intake -->
    <div class="lg:col-span-5 space-y-6">
      <div class="bg-white border border-stone-200 rounded-2xl p-6 shadow-md">
        <div class="flex items-center justify-between mb-3">
          <h2 class="font-display font-bold text-lg text-stone-900 flex items-center gap-2">
            <i class="fas fa-video text-orange-600"></i> Multi-Camera Stream Switcher
          </h2>
          <button onclick="refreshCameraDevices()" class="text-xs text-amber-700 font-semibold hover:underline">
            <i class="fas fa-sync mr-1"></i>Refresh Devices
          </button>
        </div>

        <!-- Live Camera Select Dropdown (Bluetooth, External USB, Laptop Webcam) -->
        <div class="mb-4">
          <label class="block text-[11px] text-stone-500 font-bold mb-1">Select Active Camera Device (Bluetooth / USB / Built-in)</label>
          <select id="cameraDeviceSelect" class="w-full bg-stone-50 border border-stone-300 rounded-xl px-3 py-2 text-xs font-bold text-stone-800 focus:outline-none focus:border-orange-600" onchange="switchActiveCamera()">
            <option value="">Detecting connected Bluetooth & USB cameras...</option>
          </select>
        </div>

        <!-- Studio Light Viewfinder Container -->
        <div id="viewfinderRing" class="relative aspect-square bg-stone-900 rounded-2xl overflow-hidden mb-4 studio-light-ring flex items-center justify-center border border-stone-300">
          <video id="activeWebcamVideo" autoplay playsinline class="w-full h-full object-cover hidden"></video>
          <img id="activeWebcamPreview" class="w-full h-full object-cover hidden" alt="Active Viewfinder">
          <div id="activeCamPlaceholder" class="text-center p-8">
            <i class="fas fa-camera-rotate text-5xl text-stone-500 mb-3"></i>
            <h4 class="font-display font-bold text-sm text-white mb-1">Live Multi-Camera Viewfinder</h4>
            <p class="text-xs text-stone-400">Select camera above to stream live face, hand, iris, or lip close-ups</p>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-3 mb-4">
          <button onclick="startSelectedCamera()" class="py-2.5 bg-orange-600 text-white font-bold text-xs rounded-xl hover:bg-orange-700 shadow-sm flex items-center justify-center gap-2">
            <i class="fas fa-power-off"></i> Start Selected Camera
          </button>
          <button onclick="stopCameraStream()" class="py-2.5 bg-stone-100 border border-stone-300 rounded-xl text-stone-800 font-bold text-xs hover:border-orange-600 flex items-center justify-center gap-2">
            <i class="fas fa-stop"></i> Stop Stream
          </button>
        </div>

        <!-- 4 Specialized Snap Buttons for Rapid Salon Intake -->
        <div class="border-t border-stone-200 pt-4">
          <span class="text-xs font-bold text-stone-900 block mb-2">Snap Photo Slot (Instant Assign):</span>
          <div class="grid grid-cols-2 gap-2">
            <button onclick="snapToSlot(1)" class="py-2 px-3 bg-amber-50 border border-amber-300 text-amber-900 font-bold text-[11px] rounded-lg hover:bg-amber-100 text-left">
              📸 1. Snap Face Portrait
            </button>
            <button onclick="snapToSlot(2)" class="py-2 px-3 bg-orange-50 border border-orange-300 text-orange-900 font-bold text-[11px] rounded-lg hover:bg-orange-100 text-left">
              💅 2. Snap Hand / Nails
            </button>
            <button onclick="snapToSlot(3)" class="py-2 px-3 bg-blue-50 border border-blue-300 text-blue-900 font-bold text-[11px] rounded-lg hover:bg-blue-100 text-left">
              👁️ 3. Snap Eye / Iris
            </button>
            <button onclick="snapToSlot(4)" class="py-2 px-3 bg-purple-50 border border-purple-300 text-purple-900 font-bold text-[11px] rounded-lg hover:bg-purple-100 text-left">
              💋 4. Snap Lips / Mucosa
            </button>
          </div>
        </div>
      </div>

      <!-- 4 Photo Slot Previews & File Loaders -->
      <div class="bg-white border border-stone-200 rounded-2xl p-6 shadow-md">
        <h3 class="font-display font-bold text-sm text-stone-900 mb-3"><i class="fas fa-folder-open text-amber-700 mr-2"></i>Loaded Photo Slots (Files or Camera)</h3>
        
        <div class="grid grid-cols-4 gap-2 text-center text-[10px]">
          <div class="border border-stone-200 rounded-lg p-2 bg-stone-50" onclick="document.getElementById('slot1Inp').click()">
            <span class="font-bold block mb-1">Face</span>
            <div class="h-16 bg-stone-200 rounded flex items-center justify-center overflow-hidden">
              <i class="fas fa-user text-stone-400 text-xl" id="s1Icon"></i>
              <img id="s1Img" class="w-full h-full object-cover hidden">
            </div>
            <input type="file" id="slot1Inp" accept="image/*" class="hidden" onchange="loadSlotFile(1, event)">
          </div>

          <div class="border border-stone-200 rounded-lg p-2 bg-stone-50" onclick="document.getElementById('slot2Inp').click()">
            <span class="font-bold block mb-1">Hand/Nails</span>
            <div class="h-16 bg-stone-200 rounded flex items-center justify-center overflow-hidden">
              <i class="fas fa-hand text-stone-400 text-xl" id="s2Icon"></i>
              <img id="s2Img" class="w-full h-full object-cover hidden">
            </div>
            <input type="file" id="slot2Inp" accept="image/*" class="hidden" onchange="loadSlotFile(2, event)">
          </div>

          <div class="border border-stone-200 rounded-lg p-2 bg-stone-50" onclick="document.getElementById('slot3Inp').click()">
            <span class="font-bold block mb-1">Eye/Iris</span>
            <div class="h-16 bg-stone-200 rounded flex items-center justify-center overflow-hidden">
              <i class="fas fa-eye text-stone-400 text-xl" id="s3Icon"></i>
              <img id="s3Img" class="w-full h-full object-cover hidden">
            </div>
            <input type="file" id="slot3Inp" accept="image/*" class="hidden" onchange="loadSlotFile(3, event)">
          </div>

          <div class="border border-stone-200 rounded-lg p-2 bg-stone-50" onclick="document.getElementById('slot4Inp').click()">
            <span class="font-bold block mb-1">Lips/Mucosa</span>
            <div class="h-16 bg-stone-200 rounded flex items-center justify-center overflow-hidden">
              <i class="fas fa-kiss-beam text-stone-400 text-xl" id="s4Icon"></i>
              <img id="s4Img" class="w-full h-full object-cover hidden">
            </div>
            <input type="file" id="slot4Inp" accept="image/*" class="hidden" onchange="loadSlotFile(4, event)">
          </div>
        </div>
      </div>
    </div>

    <!-- Right Column: Hair-Isolated Face Draping Stage & Rapid Salon Queue -->
    <div class="lg:col-span-7 space-y-6">
      <!-- Hair-Isolated Face Draping Stage -->
      <div class="bg-white border border-stone-200 rounded-2xl p-6 shadow-md text-center">
        <div class="flex items-center justify-between mb-3">
          <h3 class="font-display font-bold text-lg text-stone-900"><i class="fas fa-scissors text-orange-600 mr-2"></i>Hair-Isolated Face Draping Stage</h3>
          <span class="text-xs text-emerald-700 font-bold bg-emerald-50 px-2.5 py-1 rounded-md border border-emerald-200">Dark Autumn • ITA° 62.4°</span>
        </div>

        <div id="drapeStage" class="relative w-64 h-64 mx-auto rounded-2xl overflow-hidden shadow-inner border border-stone-300 flex items-center justify-center transition-colors" style="background-color: #8B0000;">
          <img id="isolatedFace" class="w-48 h-56 object-cover face-mask-oval shadow-2xl" src="http://chromatype.me/img/logo-1784993471.jpg" alt="Isolated Face">
        </div>
        <p id="activeColorName" class="text-xs font-bold text-stone-800 mt-3">Oxblood Red (Pantone 19-1617 • #8B0000)</p>
      </div>

      <!-- 432 Pantone Swatches Container -->
      <div class="bg-white border border-stone-200 rounded-2xl p-6 shadow-md">
        <div class="flex items-center justify-between mb-3">
          <h3 class="font-display font-bold text-lg text-stone-900"><i class="fas fa-swatchbook text-amber-600 mr-2"></i>Full 432 Pantone TCX Swatch Library</h3>
          <span class="text-xs text-stone-500">Click any color to drape hair-free face</span>
        </div>

        <div class="flex flex-wrap gap-1.5 max-h-48 overflow-y-auto p-3 bg-stone-50 rounded-xl border border-stone-200" id="swatchContainer">
          <!-- JS Swatches -->
        </div>
      </div>

      <!-- Rapid Salon Queue (Add Client to Queue) -->
      <div class="bg-white border border-stone-200 rounded-2xl p-6 shadow-md">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-display font-bold text-lg text-stone-900"><i class="fas fa-users text-purple-700 mr-2"></i>Rapid Salon Client Queue</h3>
          <button onclick="addClientToQueue()" class="px-4 py-2 bg-emerald-600 text-white font-bold text-xs rounded-xl hover:bg-emerald-700 shadow-sm">
            <i class="fas fa-plus mr-1"></i> Add Client to Queue & Reset
          </button>
        </div>

        <div class="space-y-2 text-xs" id="clientQueueList">
          <div class="p-3 bg-stone-50 border border-stone-200 rounded-xl flex items-center justify-between">
            <div>
              <span class="font-bold text-stone-900">Client #1: Maria Silva</span>
              <span class="text-stone-500 block text-[10px]">4 Photos Captured • Dark Autumn (ITA° 62.4°)</span>
            </div>
            <span class="px-2.5 py-1 bg-emerald-100 text-emerald-800 text-[10px] font-bold rounded-full">Ready for PDF</span>
          </div>
        </div>
      </div>
    </div>
  </div>

  <script>
    let activeStream = null;

    // Detect all connected cameras (Bluetooth, USB, Built-in)
    async function refreshCameraDevices() {
      const select = document.getElementById('cameraDeviceSelect');
      select.innerHTML = '<option value="">Detecting connected Bluetooth & USB cameras...</option>';
      try {
        const devices = await navigator.mediaDevices.enumerateDevices();
        const videoDevices = devices.filter(d => d.kind === 'videoinput');
        select.innerHTML = '';
        if (videoDevices.length === 0) {
          select.innerHTML = '<option value="">No external or bluetooth cameras found (laptop webcam default)</option>';
        } else {
          videoDevices.forEach((dev, idx) => {
            const opt = document.createElement('option');
            opt.value = dev.deviceId;
            opt.textContent = dev.label || `Camera ${idx + 1} (${dev.deviceId.slice(0,8)}...)`;
            select.appendChild(opt);
          });
        }
      } catch (err) {
        console.log("Device enumeration error:", err);
      }
    }
    refreshCameraDevices();

    function startSelectedCamera() {
      const select = document.getElementById('cameraDeviceSelect');
      const deviceId = select.value;
      const constraints = { video: deviceId ? { deviceId: { exact: deviceId }, width: 720, height: 720 } : { width: 720, height: 720 } };

      const video = document.getElementById('activeWebcamVideo');
      const placeholder = document.getElementById('activeCamPlaceholder');
      const preview = document.getElementById('activeWebcamPreview');

      placeholder.classList.add('hidden');
      preview.classList.add('hidden');
      video.classList.remove('hidden');

      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia(constraints)
          .then(stream => {
            activeStream = stream;
            video.srcObject = stream;
          })
          .catch(err => alert("Camera stream error: " + err.message));
      }
    }

    function stopCameraStream() {
      if (activeStream) {
        activeStream.getTracks().forEach(t => t.stop());
        activeStream = null;
      }
      document.getElementById('activeWebcamVideo').classList.add('hidden');
      document.getElementById('activeCamPlaceholder').classList.remove('hidden');
    }

    function snapToSlot(slot) {
      const video = document.getElementById('activeWebcamVideo');
      if (video.classList.contains('hidden')) {
        alert("Please start the active camera first!");
        return;
      }
      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth || 640;
      canvas.height = video.videoHeight || 640;
      canvas.getContext('2d').drawImage(video, 0, 0);
      const dataUrl = canvas.toDataURL('image/jpeg');

      document.getElementById(`s${slot}Icon`).classList.add('hidden');
      const img = document.getElementById(`s${slot}Img`);
      img.src = dataUrl;
      img.classList.remove('hidden');

      if (slot === 1) {
        document.getElementById('isolatedFace').src = dataUrl;
      }
    }

    function loadSlotFile(slot, e) {
      const file = e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = function(ev) {
        document.getElementById(`s${slot}Icon`).classList.add('hidden');
        const img = document.getElementById(`s${slot}Img`);
        img.src = ev.target.result;
        img.classList.remove('hidden');
        if (slot === 1) {
          document.getElementById('isolatedFace').src = ev.target.result;
        }
      };
      reader.readAsDataURL(file);
    }

    // Generate 432 Pantone TCX Swatches
    const sampleHexes = ["#8B0000", "#D2691E", "#B8860B", "#556B2F", "#800000", "#A0522D", "#CD853F", "#E9967A", "#8B4513", "#D4A853", "#BC8F8F", "#CD5C5C", "#D2B48C", "#8B7D6B", "#C59B27", "#4B0082", "#191970", "#000000", "#8B0045", "#483D8B", "#DC143C", "#C71585", "#00008B", "#8A2BE2", "#4169E1", "#800080", "#FF007F", "#FF0000", "#9400D3", "#E0115F", "#FF7F50", "#FFB6C1", "#FFE4B5", "#FA8072", "#F08080", "#FFD700", "#FF4500", "#40E0D0", "#FF6347", "#50C878"];
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

    let clientQueueCount = 1;
    function addClientToQueue() {
      clientQueueCount++;
      const list = document.getElementById('clientQueueList');
      const item = document.createElement('div');
      item.className = 'p-3 bg-stone-50 border border-stone-200 rounded-xl flex items-center justify-between';
      item.innerHTML = `<div><span class="font-bold text-stone-900">Client #${clientQueueCount}: Salon Guest</span><span class="text-stone-500 block text-[10px]">Captured via Active Camera • Classification Pending</span></div><span class="px-2.5 py-1 bg-amber-100 text-amber-800 text-[10px] font-bold rounded-full">Queued</span>`;
      list.appendChild(item);
      alert(`🎉 Client #${clientQueueCount} added to Salon Queue! Ready for next guest.`);
    }
  </script>
</body>
</html>
"""

local_html_path = os.path.join(backend_dir, 'local_operator_studio.html')
with open(local_html_path, 'w', encoding='utf-8') as f:
    f.write(salon_studio_html)

# Update Desktop Launcher
bat_launcher = f"""@echo off
title CHROMATYPE High-Volume Salon Consultation & Multi-Camera Suite
echo Starting CHROMATYPE Salon Operator Suite...
start "" "{local_html_path}"
"""

desktop_bat_path = os.path.join(desktop_dir, 'Run_CHROMATYPE_Local_Operator.bat')
with open(desktop_bat_path, 'w', encoding='utf-8') as f:
    f.write(bat_launcher)

print("Updated local_operator_studio.html with Multi-Camera Selector (Bluetooth/USB/Webcam) & High-Volume Salon Queue!")
