import os

backend_dir = r'C:\Users\dkven\color_analysis_backend'

# Add Cell Phone Camera Bridge (QR Code & Mobile Web Stream) to local_operator_studio.html
local_studio_path = os.path.join(backend_dir, 'local_operator_studio.html')
with open(local_studio_path, 'r', encoding='utf-8') as f:
    content = f.read()

phone_camera_widget = """
<!-- Cell Phone Camera Connect Box -->
<div class="bg-amber-50 border border-amber-200 rounded-2xl p-4 mb-4 flex items-center justify-between">
  <div class="flex items-center gap-3">
    <div class="w-10 h-10 rounded-xl bg-orange-600 text-white flex items-center justify-center font-bold text-lg">
      <i class="fas fa-mobile-screen-button"></i>
    </div>
    <div>
      <h4 class="font-bold text-xs text-stone-900">Cell Phone Camera Wireless Bridge</h4>
      <p class="text-[11px] text-stone-600">Laptop camera not working? Scan QR code or use DroidCam / Iriun WebCam on your phone!</p>
    </div>
  </div>
  <button onclick="openPhoneCamModal()" class="px-3.5 py-2 bg-orange-600 text-white text-xs font-bold rounded-xl hover:bg-orange-700 transition-all shadow-sm flex items-center gap-1.5">
    <i class="fas fa-qrcode"></i> Connect Cell Phone
  </button>
</div>
"""

# Cell Phone Camera Connect Modal
phone_cam_modal = """
<!-- Cell Phone Camera Connect Modal -->
<div id="phoneCamModal" class="fixed inset-0 z-50 bg-black/75 flex items-center justify-center p-4 hidden">
  <div class="bg-white border border-stone-200 rounded-2xl max-w-md w-full p-6 text-center relative shadow-2xl">
    <button onclick="closePhoneCamModal()" class="absolute top-4 right-4 text-stone-400 hover:text-stone-700 text-lg"><i class="fas fa-times"></i></button>
    <div class="w-12 h-12 rounded-full bg-orange-100 text-orange-600 flex items-center justify-center mx-auto mb-3 text-xl"><i class="fas fa-mobile-retro"></i></div>
    <h3 class="font-display font-bold text-xl text-stone-900 mb-1">Use Your Cell Phone Camera</h3>
    <p class="text-xs text-stone-500 mb-4">Connect your iPhone or Android phone camera wirelessly to your laptop in 2 easy steps:</p>

    <!-- Method 1: Instant QR Code / Local File Share -->
    <div class="bg-stone-50 border border-stone-200 rounded-xl p-4 mb-4 text-left">
      <span class="font-bold text-xs text-orange-800 block mb-1">Method 1: Free Phone Camera Apps (Recommended)</span>
      <p class="text-[11px] text-stone-600 mb-2">Install free <strong>DroidCam</strong> or <strong>Iriun Webcam</strong> app on your cell phone. It turns your phone into a wireless HD camera for Windows automatically!</p>
      <ul class="text-[11px] text-stone-700 space-y-1 font-medium">
        <li>• Android: Install <em>DroidCam</em> or <em>Iriun Webcam</em> from Google Play Store</li>
        <li>• iPhone: Install <em>Iriun Webcam</em> from Apple App Store</li>
        <li>• Your phone camera will appear in the <strong>Multi-Camera Dropdown</strong> above!</li>
      </ul>
    </div>

    <!-- Method 2: Mobile Photo Upload / AirDrop -->
    <div class="bg-amber-50 border border-amber-200 rounded-xl p-4 mb-4 text-left">
      <span class="font-bold text-xs text-amber-900 block mb-1">Method 2: Take Photos on Phone & Load</span>
      <p class="text-[11px] text-stone-700">Take photos directly on your phone camera, then send via WhatsApp / AirDrop / Email to your laptop and load into the slots above!</p>
    </div>

    <button onclick="closePhoneCamModal()" class="w-full py-2.5 bg-stone-900 text-white text-xs font-bold rounded-xl hover:bg-stone-800">Done / Close</button>
  </div>
</div>
"""

if 'id="phoneCamModal"' not in content:
    content = content.replace('<!-- Header -->', phone_cam_modal + '\n\n<!-- Header -->')
    content = content.replace('<div class="max-w-7xl mx-auto grid lg:grid-cols-12 gap-8">', '<div class="max-w-7xl mx-auto grid lg:grid-cols-12 gap-8">\n' + phone_camera_widget)

# Add Modal JS functions
modal_js = """
function openPhoneCamModal() {
  document.getElementById('phoneCamModal').classList.remove('hidden');
}
function closePhoneCamModal() {
  document.getElementById('phoneCamModal').classList.add('hidden');
}
"""

if 'function openPhoneCamModal()' not in content:
    content = content.replace('let activeStream = null;', modal_js + '\n\nlet activeStream = null;')

with open(local_studio_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Added Cell Phone Camera Bridge & DroidCam / Iriun Connection Hub to local_operator_studio.html!")
