import os

backend_dir = r'C:\Users\dkven\color_analysis_backend'
studio_path = os.path.join(backend_dir, 'local_operator_studio.html')

with open(studio_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Make Client Profile Intake Box (Name & Email) prominent at the very top of the left column
prominent_client_box = """<!-- PROMINENT CLIENT PROFILE INTAKE BOX -->
      <div class="bg-white border-2 border-orange-500/40 rounded-2xl p-6 shadow-lg space-y-4">
        <div class="flex items-center justify-between border-b border-stone-200 pb-3">
          <h3 class="font-display font-black text-lg text-stone-900 flex items-center gap-2">
            <i class="fas fa-id-card text-orange-600 text-xl"></i> Active Client Profile Record
          </h3>
          <span class="text-[10px] font-bold uppercase tracking-wider text-orange-700 bg-orange-50 px-2.5 py-1 rounded-md border border-orange-200">Required</span>
        </div>
        
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-xs font-bold text-stone-800 mb-1.5">Client Full Name *</label>
            <input type="text" id="cName" placeholder="e.g. Maria Silva" value="Maria Silva" class="w-full bg-stone-50 border border-stone-300 rounded-xl px-4 py-3 text-sm text-stone-900 font-semibold focus:outline-none focus:border-orange-600 focus:bg-white shadow-sm">
          </div>
          <div>
            <label class="block text-xs font-bold text-stone-800 mb-1.5">Client Email Address *</label>
            <input type="email" id="cEmail" placeholder="client@domain.com" value="client@domain.com" class="w-full bg-stone-50 border border-stone-300 rounded-xl px-4 py-3 text-sm text-stone-900 font-semibold focus:outline-none focus:border-orange-600 focus:bg-white shadow-sm">
          </div>
        </div>
      </div>"""

# Remove old small client profile box if present
if '<!-- PROMINENT CLIENT PROFILE INTAKE BOX -->' not in content:
    old_client_box = """<!-- Client Profile Box -->
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
      </div>"""

    if old_client_box in content:
        content = content.replace(old_client_box, '')

    start_left_col = content.find('<div class="lg:col-span-5 space-y-6">')
    if start_left_col != -1:
        content = content[:start_left_col + len('<div class="lg:col-span-5 space-y-6">')] + '\n' + prominent_client_box + '\n' + content[start_left_col + len('<div class="lg:col-span-5 space-y-6">'):]

with open(studio_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Placed Prominent Client Profile Intake Box (Name & Email) at the top of local_operator_studio.html!")
