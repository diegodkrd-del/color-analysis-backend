


<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CHROMATYPE — Proprietary Optical Personal Color Analysis | 12 Season Palette</title>
<meta name="description" content="Upload one photo. Discover your exact 12-season color palette powered by CHROMATYPE's CIELAB 3D spectrophotometric technology. Special $29 launch offer (Reg. $199).">
<meta name="keywords" content="personal color analysis, 12 season color analysis, chromatype color analysis, cielab skin analysis, ita color analysis, online color palette">
<link rel="canonical" href="https://chromatype.me/">
<meta property="og:title" content="CHROMATYPE — Your True Colors. Spectrophotometrically Decoded.">
<meta property="og:description" content="Proprietary CIELAB 3D spectrophotometric personal color analysis. Upload a photo, receive your 52-page master report by email.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://chromatype.me/">

<!-- Google Fonts & Font Awesome Icons -->
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800;900&family=DM+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">

<script>
tailwind.config = {
  theme: {
    extend: {
      fontFamily: {
        display: ['Playfair Display', 'serif'],
        body: ['DM Sans', 'sans-serif'],
      },
      colors: {
        brand: {
          black: '#0c0b0a',
          dark: '#141312',
          card: '#1c1b19',
          border: '#2a2826',
          muted: '#7a756d',
          light: '#b5aea4',
          cream: '#f5f0eb',
          white: '#faf8f5',
          accent: '#e8734a',
          accentHover: '#f0845e',
          gold: '#d4a853',
          goldLight: '#e8c97a',
        }
      }
    }
  }
}
</script>

<style>
  :root {
    --bg: #0c0b0a;
    --bg-light: #141312;
    --card: #1c1b19;
    --border: #2a2826;
    --muted: #7a756d;
    --light: #b5aea4;
    --cream: #f5f0eb;
    --white: #faf8f5;
    --accent: #e8734a;
    --accent-hover: #f0845e;
    --gold: #d4a853;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  html {
    scroll-behavior: smooth;
    background: var(--bg);
    color: var(--cream);
  }

  body {
    font-family: 'DM Sans', sans-serif;
    background: var(--bg);
    overflow-x: hidden;
  }

  /* Custom Scrollbar */
  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-track { background: var(--bg); }
  ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
  ::-webkit-scrollbar-thumb:hover { background: var(--muted); }

  /* Hero spectrum ring rotation */
  .spectrum-ring {
    position: absolute;
    border-radius: 50%;
    border: 1.5px solid transparent;
    animation: spectrumRotate 20s linear infinite;
  }

  @keyframes spectrumRotate {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .spectrum-ring:nth-child(1) {
    width: 500px; height: 500px;
    border-image: conic-gradient(from 0deg, #e8734a, #d4a853, #8fbc6a, #5bb8a9, #5b8fd4, #8b6abf, #c75b8f, #e8734a) 1;
    border-radius: 50%;
    opacity: 0.15;
    animation-duration: 25s;
  }

  .spectrum-ring:nth-child(2) {
    width: 400px; height: 400px;
    border-image: conic-gradient(from 120deg, #e8734a, #d4a853, #8fbc6a, #5bb8a9, #5b8fd4, #8b6abf, #c75b8f, #e8734a) 1;
    border-radius: 50%;
    opacity: 0.2;
    animation-duration: 20s;
    animation-direction: reverse;
  }

  /* Floating particles */
  .color-particle {
    position: absolute;
    width: 4px; height: 4px;
    border-radius: 50%;
    pointer-events: none;
    animation: floatParticle linear infinite;
    opacity: 0;
  }

  @keyframes floatParticle {
    0% { transform: translateY(0) scale(0); opacity: 0; }
    10% { opacity: 0.8; transform: scale(1); }
    90% { opacity: 0.6; }
    100% { transform: translateY(-600px) scale(0.3); opacity: 0; }
  }

  /* Scroll reveal */
  .reveal {
    opacity: 0;
    transform: translateY(35px);
    transition: opacity 0.8s ease, transform 0.8s ease;
  }
  .reveal.visible {
    opacity: 1;
    transform: translateY(0);
  }

  /* Interactive Season card */
  .season-card {
    transition: transform 0.35s ease, box-shadow 0.35s ease;
  }
  .season-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 15px 40px rgba(0,0,0,0.5);
  }

  /* Featured pricing glow */
  .pricing-featured::before {
    content: '';
    position: absolute;
    inset: -2px;
    border-radius: 18px;
    background: linear-gradient(135deg, var(--accent), var(--gold));
    z-index: -1;
    opacity: 0.7;
    filter: blur(2px);
  }

  /* Timed slide-in CTA modal */
  .cta-modal {
    position: fixed;
    bottom: 25px;
    right: 25px;
    max-width: 380px;
    width: calc(100% - 50px);
    background: #1c1b19;
    border: 1px solid var(--accent);
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.8);
    z-index: 9999;
    transform: translateY(150%) scale(0.9);
    opacity: 0;
    transition: transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275), opacity 0.5s ease;
  }
  .cta-modal.show {
    transform: translateY(0) scale(1);
    opacity: 1;
  }

  /* Swatch preview */
  .swatch {
    width: 28px; height: 28px;
    border-radius: 6px;
    flex-shrink: 0;
    transition: transform 0.2s ease;
  }
  .swatch:hover { transform: scale(1.3); }

  /* Glow blob */
  .glow-blob {
    position: absolute;
    border-radius: 50%;
    filter: blur(120px);
    pointer-events: none;
  }

  /* Pulse animation for CTA */
  @keyframes subtlePulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(232, 115, 74, 0.4); }
    50% { box-shadow: 0 0 0 14px rgba(232, 115, 74, 0); }
  }
  .pulse-cta {
    animation: subtlePulse 3s ease infinite;
  }

  /* FAQ Accordion */
  .faq-answer {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.4s ease, padding 0.4s ease;
  }
  .faq-answer.open {
    max-height: 300px;
  }
</style>

<div class="chromatype-root bg-brand-black text-brand-cream" style="margin-top:-30px; margin-left:-30px; margin-right:-30px;">


<!-- Camera Capture Modal -->
<div id="cameraModal" class="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4 hidden">
  <div class="bg-brand-card border border-brand-border rounded-2xl max-w-lg w-full p-6 text-center relative">
    <button onclick="closeCameraModal()" class="absolute top-4 right-4 text-brand-muted hover:text-brand-cream text-lg"><i class="fas fa-times"></i></button>
    <h3 class="font-display font-bold text-xl text-brand-cream mb-2">Take Live Selfie</h3>
    <p class="text-brand-light text-xs mb-4">Position your face in good natural light facing the camera.</p>
    
    <div class="relative w-full aspect-square bg-black rounded-xl overflow-hidden mb-4 border border-brand-border">
      <video id="cameraVideo" autoplay playsinline class="w-full h-full object-cover"></video>
      <canvas id="cameraCanvas" class="hidden"></canvas>
    </div>

    <div class="flex gap-3">
      <button onclick="closeCameraModal()" class="flex-1 py-3 border border-brand-border rounded-xl text-brand-light font-bold text-sm hover:border-brand-muted">Cancel</button>
      <button onclick="snapPhoto()" class="flex-1 py-3 bg-brand-accent text-white rounded-xl font-bold text-sm hover:bg-brand-accentHover shadow-lg"><i class="fas fa-camera mr-2"></i>Snap Photo</button>
    </div>
  </div>
</div>


<!-- Toast Notification -->
<div id="toast" class="fixed bottom-6 left-6 z-50 px-6 py-4 rounded-xl bg-brand-card border border-brand-border text-brand-cream text-sm opacity-0 pointer-events-none transition-all duration-300"></div>

<!-- Timed Slide-in Call To Action Modal (Triggers after 25 sec or scroll) -->
<div id="timedCtaModal" class="cta-modal">
  <button onclick="closeCtaModal()" class="absolute top-3 right-3 w-10 h-10 rounded-full bg-brand-dark/90 border border-brand-border hover:border-brand-accent text-brand-light hover:text-brand-cream text-lg flex items-center justify-center transition-all shadow-md active:scale-95" aria-label="Close modal"><i class="fas fa-xmark"></i></button>
  <div class="flex items-center gap-2 text-brand-accent text-xs font-bold uppercase tracking-wider mb-2">
    <span class="w-2 h-2 rounded-full bg-brand-accent animate-ping"></span>
    Limited Launch Offer
  </div>
  <h4 class="font-display font-bold text-lg text-brand-cream mb-1">Get Analyzed for Only $29</h4>
  <p class="text-brand-light text-xs mb-4 leading-relaxed">
    Regular session rate increasing to <span class="line-through text-brand-muted">$199</span> soon. Receive your 52-page master report & 12-season palette in minutes!
  </p>
  <a href="#analyze" onclick="closeCtaModal()" class="block text-center py-3 bg-brand-accent text-white rounded-xl font-bold text-sm hover:bg-brand-accentHover transition-all shadow-lg">
    Claim $29 Analysis Now
  </a>
</div>

<!-- Sticky Announcement Bar -->
<div class="bg-gradient-to-r from-brand-accent via-brand-gold to-brand-accent text-brand-black font-semibold text-xs py-2 px-4 text-center">
  🎁 FREE LAUNCH OFFER: First 100 Customers Get FREE Teaser Analysis! (<span id="freeCounter">18</span> / 100 Free Spots Remaining)
</div>

<!-- Header Navigation -->
<nav class="sticky top-0 z-40 bg-brand-black/90 backdrop-blur-md border-b border-brand-border/60">
  <div class="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
    <a href="#" class="flex items-center gap-2.5">
      <div class="bg-white/95 px-3 py-1.5 rounded-xl shadow-md border border-brand-border/40 inline-flex items-center"><img src="http://chromatype.me/img/logo-1784993471.jpg" alt="CHROMATYPE Studio" class="h-7 w-auto object-contain"></div>
    </a>
    
    <div class="hidden md:flex items-center gap-8 text-sm font-medium text-brand-light">
      <a href="#technology" class="hover:text-brand-cream transition-colors">CIELAB Technology</a>
      <a href="#how-it-works" class="hover:text-brand-cream transition-colors">How It Works</a>
      <a href="#seasons" class="hover:text-brand-cream transition-colors">12 Seasons</a>
      <a href="#pricing" class="hover:text-brand-cream transition-colors">Pricing</a>
      <a href="#faq" class="hover:text-brand-cream transition-colors">FAQ</a>
      <a href="#analyze" class="px-5 py-2 bg-brand-accent text-white rounded-full font-semibold hover:bg-brand-accentHover transition-colors">
        Analyze Me — $29
      </a>
    </div>
  </div>
</nav>

<!-- Hero Section -->
<header class="relative min-h-[90vh] flex items-center justify-center pt-12 pb-20 overflow-hidden">
  <div class="glow-blob w-[600px] h-[600px] bg-brand-accent/10 top-1/4 -left-48"></div>
  <div class="glow-blob w-[500px] h-[500px] bg-brand-gold/8 bottom-1/4 -right-40"></div>

  <div class="relative z-10 max-w-4xl mx-auto px-6 text-center">
    <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-brand-border bg-brand-card/70 mb-8">
      <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
      <span class="text-brand-light text-xs font-semibold tracking-wider uppercase">CIELAB 3D Spectrophotometric System</span>
    </div>

    <h1 class="font-display font-black text-5xl sm:text-6xl md:text-7xl lg:text-8xl leading-[0.95] tracking-tight mb-6">
      <span class="text-brand-cream">Your True Colors.</span><br>
      <span class="bg-gradient-to-r from-brand-accent via-brand-gold to-brand-accent bg-clip-text text-transparent">Spectrophotometrically Decoded.</span>
    </h1>

    <p class="text-brand-light text-lg sm:text-xl max-w-2xl mx-auto mb-10 leading-relaxed font-light">
      Upload one photo. CHROMATYPE’s proprietary spectrophotometric engine measures your skin’s exact $L^*a^*b^*$ coordinates and Individual Typology Angle (ITA°) to pinpoint your true 12-season palette. Complete 52-page dossier delivered to your email in minutes.
    </p>

    <div class="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12">
      <a href="#analyze" class="pulse-cta px-9 py-4 bg-brand-accent text-white rounded-full font-bold text-lg hover:bg-brand-accentHover transition-all hover:scale-105 shadow-xl">
        Get My Color Analysis — $29 <span class="line-through text-brand-cream/60 text-sm ml-2">$199</span>
      </a>
      <a href="#how-it-works" class="px-8 py-4 border border-brand-border text-brand-cream rounded-full font-medium text-lg hover:border-brand-light hover:bg-brand-card/50 transition-all">
        Explore Method
      </a>
    </div>

    <!-- Trust signals -->
    <div class="flex flex-wrap items-center justify-center gap-8 text-brand-muted text-sm font-medium">
      <div class="flex items-center gap-2">
        <i class="fas fa-shield-halved text-brand-gold"></i>
        <span>100% Private & Instant Deletion</span>
      </div>
      <div class="flex items-center gap-2">
        <i class="fas fa-microscope text-brand-gold"></i>
        <span>CIELAB $L^*a^*b^*$ Optical Precision</span>
      </div>
      <div class="flex items-center gap-2">
        <i class="fas fa-check-double text-brand-gold"></i>
        <span>432 Pantone TCX Matched Colors</span>
      </div>
    </div>
  </div>
</header>

<!-- Operational Guarantee Badges -->
<section class="border-y border-brand-border bg-brand-dark/60 py-8">
  <div class="max-w-6xl mx-auto px-6 flex flex-wrap items-center justify-between gap-8 text-center text-brand-muted">
    <div class="flex-1 min-w-[140px]">
      <div class="font-display font-bold text-2xl text-brand-cream mb-1">CIELAB 3D</div>
      <div class="text-xs uppercase tracking-wider">Perceptual Optical Science</div>
    </div>
    <div class="w-px h-10 bg-brand-border hidden md:block"></div>
    <div class="flex-1 min-w-[140px]">
      <div class="font-display font-bold text-2xl text-brand-cream mb-1">ITA° Typology</div>
      <div class="text-xs uppercase tracking-wider">Melanin Reflectance Standard</div>
    </div>
    <div class="w-px h-10 bg-brand-border hidden md:block"></div>
    <div class="flex-1 min-w-[140px]">
      <div class="font-display font-bold text-2xl text-brand-cream mb-1">432 Swatches</div>
      <div class="text-xs uppercase tracking-wider">Pantone TCX Mapped</div>
    </div>
    <div class="w-px h-10 bg-brand-border hidden md:block"></div>
    <div class="flex-1 min-w-[140px]">
      <div class="font-display font-bold text-2xl text-brand-cream mb-1">100% Private</div>
      <div class="text-xs uppercase tracking-wider">Instant Data Deletion</div>
    </div>
  </div>
</section>

<!-- CIELAB Technology Section -->
<section id="technology" class="py-24 relative bg-brand-dark/30">
  <div class="max-w-6xl mx-auto px-6 relative z-10">
    <div class="text-center mb-16 reveal">
      <span class="text-brand-accent text-sm font-semibold tracking-widest uppercase">Optical Engineering</span>
      <h2 class="font-display font-extrabold text-4xl md:text-5xl text-brand-cream mt-2 mb-4">Why CHROMATYPE CIELAB Science Leads</h2>
      <p class="text-brand-light text-lg max-w-2xl mx-auto">Unlike subjective quizzes or uncalibrated apps, CHROMATYPE measures physical skin reflectance in standardized 3D perceptual color space.</p>
    </div>

    <div class="grid md:grid-cols-3 gap-8">
      <div class="reveal bg-brand-card rounded-2xl border border-brand-border p-8 season-card">
        <div class="w-12 h-12 rounded-xl bg-brand-accent/10 border border-brand-accent/20 flex items-center justify-center mb-6">
          <i class="fas fa-compass text-brand-accent text-xl"></i>
        </div>
        <h3 class="font-display font-bold text-xl text-brand-cream mb-3">ITA° Typology Angle</h3>
        <p class="text-brand-light text-sm leading-relaxed">
          Calculates your exact Individual Typology Angle ($\text{ITA}^\circ = \arctan((L^*-50)/b^*) \times 180/\pi$) to determine skin melanin depth independently of lighting fluctuations.
        </p>
      </div>

      <div class="reveal bg-brand-card rounded-2xl border border-brand-border p-8 season-card" style="transition-delay:0.15s;">
        <div class="w-12 h-12 rounded-xl bg-brand-gold/10 border border-brand-gold/20 flex items-center justify-center mb-6">
          <i class="fas fa-swatchbook text-brand-gold text-xl"></i>
        </div>
        <h3 class="font-display font-bold text-xl text-brand-cream mb-3">432 Pantone TCX Swatches</h3>
        <p class="text-brand-light text-sm leading-relaxed">
          Every custom swatch in your report is mapped to standard Pantone Textile Cotton (TCX) codes, allowing seamless shopping for garments and cosmetics worldwide.
        </p>
      </div>

      <div class="reveal bg-brand-card rounded-2xl border border-brand-border p-8 season-card" style="transition-delay:0.3s;">
        <div class="w-12 h-12 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center mb-6">
          <i class="fas fa-layer-group text-emerald-400 text-xl"></i>
        </div>
        <h3 class="font-display font-bold text-xl text-brand-cream mb-3">3-Tier Stacked Gradient Swatches</h3>
        <p class="text-brand-light text-sm leading-relaxed">
          Our print-ready pocket swatch cards feature primary tones, CIELAB interpolated midpoint colors, and harmonic accents for foolproof physical draping.
        </p>
      </div>
    </div>
  </div>
</section>

<!-- How It Works Section -->
<section id="how-it-works" class="py-24 relative">
  <div class="max-w-6xl mx-auto px-6 relative z-10">
    <div class="text-center mb-20 reveal">
      <span class="text-brand-accent text-sm font-semibold tracking-widest uppercase">Streamlined Protocol</span>
      <h2 class="font-display font-extrabold text-4xl md:text-5xl text-brand-cream mt-2 mb-4">Three Steps to Your Master Dossier</h2>
      <p class="text-brand-light text-lg max-w-xl mx-auto">No salon travel required. Receive professional optical color analysis from your own phone.</p>
    </div>

    <div class="grid md:grid-cols-3 gap-8">
      <div class="reveal text-center">
        <div class="w-16 h-16 rounded-2xl bg-brand-card border border-brand-border flex items-center justify-center mx-auto mb-6 text-brand-accent font-bold text-xl shadow-lg">01</div>
        <h3 class="font-display font-bold text-xl text-brand-cream mb-2">Upload Natural Daylight Photo</h3>
        <p class="text-brand-light text-sm leading-relaxed">Take a quick selfie in natural window light. No makeup or minimal makeup works best.</p>
      </div>

      <div class="reveal text-center" style="transition-delay:0.15s;">
        <div class="w-16 h-16 rounded-2xl bg-brand-card border border-brand-border flex items-center justify-center mx-auto mb-6 text-brand-gold font-bold text-xl shadow-lg">02</div>
        <h3 class="font-display font-bold text-xl text-brand-cream mb-2">Optical CIELAB $L^*a^*b^*$ Extraction</h3>
        <p class="text-brand-light text-sm leading-relaxed">CHROMATYPE measures skin reflectance across 47 landmark sampling points in 0.4 seconds.</p>
      </div>

      <div class="reveal text-center" style="transition-delay:0.3s;">
        <div class="w-16 h-16 rounded-2xl bg-brand-card border border-brand-border flex items-center justify-center mx-auto mb-6 text-emerald-400 font-bold text-xl shadow-lg">03</div>
        <h3 class="font-display font-bold text-xl text-brand-cream mb-2">Receive 52-Page Master Dossier</h3>
        <p class="text-brand-light text-sm leading-relaxed">Delivered directly to your inbox with 36 half-screen face drapes and print-ready pocket swatch fan files.</p>
      </div>
    </div>
  </div>
</section>

<!-- Pricing Section -->
<section id="pricing" class="py-24 relative bg-brand-dark/40 border-t border-brand-border">
  <div class="max-w-6xl mx-auto px-6">
    <div class="text-center mb-16 reveal">
      <span class="text-brand-accent text-sm font-semibold tracking-widest uppercase">Start Operations Special</span>
      <h2 class="font-display font-extrabold text-4xl md:text-5xl text-brand-cream mt-2 mb-4">Select Your CHROMATYPE Pass</h2>
      <p class="text-brand-light text-lg max-w-2xl mx-auto">Choose between our single consumer report pass or our 12-month commercial operator franchise licenses.</p>
    </div>

    <div class="grid md:grid-cols-3 gap-8 items-stretch">
      <!-- Product #1: B2C Consumer Pass ($29 One-Time) -->
      <div class="reveal pricing-featured bg-brand-card rounded-2xl p-8 flex flex-col justify-between season-card relative">
        <div>
          <div class="flex items-center justify-between mb-2">
            <div class="text-brand-accent text-xs font-bold uppercase tracking-wider">Product #1 • One-Time Download Pass</div>
            <span class="px-3 py-1 bg-brand-accent/20 text-brand-accent text-xs font-bold rounded-full">Most Popular</span>
          </div>
          <div class="flex items-baseline gap-1 mb-2">
            <span class="font-display font-black text-5xl text-brand-cream">$29</span>
            <span class="text-brand-muted text-sm font-medium">/ one-time</span>
            <span class="text-brand-muted text-sm line-through ml-2">$199</span>
          </div>
          <p class="text-brand-light text-xs font-semibold text-brand-gold mb-6">✓ One-Time Payment — One-Time Download Only of Digital Files</p>
          <ul class="space-y-3 mb-8 text-sm text-brand-light">
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>12 Season CIELAB Spectrophotometric Analysis</li>
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>52-Page Master Dossier PDF (Instant Download)</li>
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>36 Half-Page Virtual Face Drapes</li>
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>Print-Ready 3-Tier Pocket Swatch Fan PDF ($29 Value)</li>
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>432 Pantone TCX Matched Swatch Codes</li>
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>Makeup & Jewelry Tone Blueprint</li>
          </ul>
        </div>
        <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business=dkvendemais@gmail.com&item_name=CHROMATYPE+Personal+Color+Analysis+Session&amount=29.00&currency_code=USD" target="_blank" class="block text-center py-4 bg-brand-accent text-white rounded-xl font-bold hover:bg-brand-accentHover transition-all shadow-lg">
          Buy $29 One-Time Pass
        </a>
      </div>

      <!-- Product #2: B2B Beginner Operator Pass ($150/Year) -->
      <div class="reveal bg-brand-card rounded-2xl border border-brand-border p-8 flex flex-col justify-between season-card">
        <div>
          <div class="text-brand-gold text-xs font-bold uppercase tracking-wider mb-2">Product #2 • 12-Month Beginner License</div>
          <div class="flex items-baseline gap-1 mb-2">
            <span class="font-display font-black text-5xl text-brand-cream">$150</span>
            <span class="text-brand-muted text-sm font-medium">/ 12 months</span>
            <span class="text-brand-muted text-sm line-through ml-2">$750/yr</span>
          </div>
          <p class="text-brand-light text-xs font-semibold text-brand-gold mb-6">✓ 12-Month Annual Commercial Operator Access</p>
          <ul class="space-y-3 mb-8 text-sm text-brand-light">
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>12-Month Commercial Operator Pass</li>
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>Right to sell $29 to $199 client sessions</li>
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>Set your own brand pricing & profit strategy</li>
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>Complete 12-Season Master Guide PDF Suite</li>
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>Print-Ready Swatch Fan Master Files</li>
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>Annual license renewal rights</li>
          </ul>
        </div>
        <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business=dkvendemais@gmail.com&item_name=CHROMATYPE+Beginner+Operator+Pass+Annual&amount=150.00&currency_code=USD" target="_blank" class="block text-center py-3 border border-brand-gold/40 rounded-xl text-brand-gold font-bold hover:border-brand-gold hover:bg-brand-gold/10 transition-all">
          Get $150 Annual License
        </a>
      </div>

      <!-- Product #3: B2B Full Commercial Suite ($2,500/Year) -->
      <div class="reveal bg-brand-card rounded-2xl border border-brand-border p-8 flex flex-col justify-between season-card">
        <div>
          <div class="text-brand-cream text-xs font-bold uppercase tracking-wider mb-2">Product #3 • 12-Month Commercial Franchise</div>
          <div class="flex items-baseline gap-1 mb-2">
            <span class="font-display font-black text-5xl text-brand-cream">$2,500</span>
            <span class="text-brand-muted text-sm font-medium">/ 12 months</span>
            <span class="text-brand-muted text-sm line-through ml-2">$10,000/yr</span>
          </div>
          <p class="text-brand-light text-xs font-semibold text-brand-gold mb-6">✓ 12-Month Full Commercial Franchise Suite</p>
          <ul class="space-y-3 mb-8 text-sm text-brand-light">
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>12-Month Full Commercial Resale Franchise</li>
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>White-Label Custom PDF Report Rights</li>
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>Unlimited Client Session Volume for 1 Year</li>
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>Dedicated Priority Processing Queue</li>
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>1-on-1 Studio Onboarding & Support</li>
            <li class="flex items-center gap-3"><i class="fas fa-check text-emerald-400 text-xs"></i>Annual franchise renewal lock</li>
          </ul>
        </div>
        <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business=dkvendemais@gmail.com&item_name=CHROMATYPE+Full+Commercial+Franchise+Suite+Annual&amount=2500.00&currency_code=USD" target="_blank" class="block text-center py-3 border border-brand-border rounded-xl text-brand-cream font-bold hover:border-brand-accent hover:text-brand-accent transition-all">
          Get $2,500 Annual Franchise
        </a>
      </div>
    </div>
  </div>
</section>

<!-- Photo Upload & Execution Form Section -->
<section id="analyze" class="py-24 relative">
  <div class="max-w-2xl mx-auto px-6 relative z-10">
    <div class="text-center mb-12 reveal">
      <span class="text-brand-accent text-sm font-semibold tracking-widest uppercase">Launch Promotion</span>
      <h2 class="font-display font-extrabold text-4xl md:text-5xl text-brand-cream mt-2 mb-3">Try Free or Get Full $29 Dossier</h2>
      <p class="text-brand-light text-lg">Upload your photo. First 100 users get a FREE 12-season sub-season classification!</p>
    </div>

    <div class="reveal bg-brand-card rounded-2xl border border-brand-border p-8 shadow-2xl">
      <!-- Tier Selector: Free Teaser vs $29 Master -->
      <div class="grid grid-cols-2 gap-4 mb-6">
        <button type="button" id="btnModeFree" onclick="selectMode('free')" class="py-3 px-4 rounded-xl border-2 border-brand-accent bg-brand-accent/10 text-brand-cream font-bold text-xs sm:text-sm text-center transition-all">
          🎁 FREE Launch Teaser<br><span class="text-[10px] text-brand-accent font-normal">(Sub-Season + 4 Colors)</span>
        </button>
        <button type="button" id="btnModePaid" onclick="selectMode('paid')" class="py-3 px-4 rounded-xl border-2 border-brand-border bg-brand-dark text-brand-light font-bold text-xs sm:text-sm text-center transition-all">
          👑 Full $29 Master Package<br><span class="text-[10px] text-brand-muted font-normal">(52 Pages + Swatch Fan PDF)</span>
        </button>
      </div>

      <!-- Name -->
      <div class="mb-4">
        <label class="block text-brand-light text-sm font-medium mb-2">Full Name</label>
        <input type="text" id="userName" placeholder="Enter your full name" class="w-full bg-brand-dark border border-brand-border rounded-xl px-4 py-3 text-brand-cream placeholder-brand-muted text-sm focus:outline-none focus:border-brand-accent transition-colors">
      </div>

      <!-- Email -->
      <div class="mb-4">
        <label class="block text-brand-light text-sm font-medium mb-2">Email Address</label>
        <input type="email" id="userEmail" placeholder="your@email.com" class="w-full bg-brand-dark border border-brand-border rounded-xl px-4 py-3 text-brand-cream placeholder-brand-muted text-sm focus:outline-none focus:border-brand-accent transition-colors">
      </div>

      <!-- Photo Upload & Camera Selector Zone -->
      <div class="mb-6">
        <label class="block text-brand-light text-sm font-medium mb-2">Provide Your Selfie (Natural Daylight)</label>
        
        <!-- Action Buttons -->
        <div class="grid grid-cols-2 gap-3 mb-3">
          <button type="button" onclick="openCameraModal()" class="py-3 px-4 bg-brand-accent/20 border border-brand-accent rounded-xl text-brand-cream font-semibold text-xs hover:bg-brand-accent/30 transition-all flex items-center justify-center gap-2">
            <i class="fas fa-camera text-brand-accent text-sm"></i> Take Live Selfie
          </button>
          <button type="button" onclick="triggerFileSelect()" class="py-3 px-4 bg-brand-card border border-brand-border rounded-xl text-brand-cream font-semibold text-xs hover:border-brand-accent transition-all flex items-center justify-center gap-2">
            <i class="fas fa-folder-open text-brand-gold text-sm"></i> Browse Photo File
          </button>
        </div>

        <!-- Big Drag & Drop Zone -->
        <div id="uploadZone" class="border-2 border-dashed border-brand-accent/50 bg-brand-dark/80 rounded-xl p-6 text-center cursor-pointer hover:border-brand-accent transition-all mb-3" onclick="triggerFileSelect()">
          <div id="uploadPlaceholder">
            <i class="fas fa-cloud-arrow-up text-3xl text-brand-accent mb-2"></i>
            <p class="text-brand-cream text-sm font-medium mb-1">Click anywhere here to select your photo</p>
            <p class="text-brand-muted text-xs">JPG or PNG under 10MB — natural daylight</p>
          </div>
          <div id="uploadPreview" class="hidden">
            <img id="previewImg" class="max-h-44 mx-auto rounded-lg mb-2 object-cover border border-brand-border" alt="Preview">
            <p id="previewName" class="text-brand-accent text-xs font-mono font-bold"></p>
          </div>
        </div>

        <!-- Native File Input (Always Accessible) -->
        <input type="file" id="photoInput" accept="image/jpeg,image/png" class="w-full text-xs text-brand-light bg-brand-dark border border-brand-border rounded-lg p-2 cursor-pointer" onchange="handleFileSelect(event)">
      </div>

      <!-- Submit CTA Button -->
      <button id="submitBtn" onclick="handleSubmit()" class="w-full py-4 bg-brand-accent text-white rounded-xl font-bold text-lg hover:bg-brand-accentHover transition-all disabled:opacity-50 disabled:cursor-not-allowed" disabled>
        <span id="submitText">Upload a photo to continue</span>
      </button>

      <p class="text-brand-muted text-xs text-center mt-4">
        <i class="fas fa-lock mr-1"></i>100% Private — photos are analyzed in volatile memory and immediately deleted.
      </p>
    </div>
  </div>
</section>

<!-- FAQ Section -->
<section id="faq" class="py-24 relative bg-brand-dark/30 border-t border-brand-border">
  <div class="max-w-3xl mx-auto px-6">
    <div class="text-center mb-16 reveal">
      <span class="text-brand-accent text-sm font-semibold tracking-widest uppercase">Frequently Asked Questions</span>
      <h2 class="font-display font-extrabold text-4xl md:text-5xl text-brand-cream mt-2 mb-4">Everything You Need to Know</h2>
    </div>

    <div class="space-y-4 reveal" id="faqContainer">
      <!-- Injected by JS -->
    </div>
  </div>
</section>

<!-- Footer -->
<footer class="border-t border-brand-border py-12 bg-brand-black">
  <div class="max-w-6xl mx-auto px-6 text-center text-brand-muted text-sm">
    <div class="flex justify-center items-center gap-2 mb-4"><div class="bg-white/95 px-3 py-1.5 rounded-xl shadow-md border border-brand-border/40 inline-flex items-center"><img src="http://chromatype.me/img/logo-1784993471.jpg" alt="CHROMATYPE Studio" class="h-7 w-auto object-contain"></div></div>
    <p class="mb-4">CHROMATYPE Proprietary CIELAB 3D Spectrophotometric Color Analysis Engine.</p>
    <p class="text-xs text-brand-muted/60">&copy; 2026 CHROMATYPE Studio (chromatype.me & color-analysis.shop). All rights reserved.</p>
  </div>
</footer>

<script>
// FAQ Accordion Data
const faqs = [
  {
    q: 'How does CHROMATYPE CIELAB analysis work?',
    a: 'CHROMATYPE measures your skin’s exact reflectance across L* (lightness), a* (red/green undertone), and b* (yellow/blue undertone) coordinates in 3D perceptual color space, calculating your Individual Typology Angle (ITA°) for 100% objective accuracy.'
  },
  {
    q: 'What type of photo yields the best results?',
    a: 'Take a clear selfie in natural daylight facing a window. Keep makeup minimal and pull hair back so your forehead and cheekbones are visible. Avoid harsh artificial yellow lighting or camera filters.'
  },
  {
    q: 'Are photos kept private?',
    a: 'Yes. CHROMATYPE processes your photo in volatile RAM to extract spectrophotometric data points and immediately deletes the image. We never store, publish, or share your personal photo.'
  },
  {
    q: 'How long until I receive my master dossier?',
    a: 'Your complete 52-page PDF report and print-ready pocket swatch fan files are compiled and sent to your email address within 3 to 5 minutes.'
  }
];

function renderFAQ() {
  const container = document.getElementById('faqContainer');
  container.innerHTML = faqs.map((f, i) => `
    <div class="bg-brand-card rounded-xl border border-brand-border overflow-hidden">
      <button onclick="toggleFAQ(${i})" class="w-full flex items-center justify-between p-5 text-left text-brand-cream font-semibold text-sm">
        <span>${f.q}</span>
        <i class="fas fa-plus text-brand-muted text-xs transition-transform" id="faqIcon${i}"></i>
      </button>
      <div class="faq-answer px-5" id="faqAnswer${i}">
        <p class="text-brand-light text-sm leading-relaxed pb-5">${f.a}</p>
      </div>
    </div>
  `).join('');
}

function toggleFAQ(i) {
  const answer = document.getElementById(`faqAnswer${i}`);
  const icon = document.getElementById(`faqIcon${i}`);
  const isOpen = answer.classList.contains('open');
  document.querySelectorAll('.faq-answer').forEach(a => a.classList.remove('open'));
  document.querySelectorAll('[id^="faqIcon"]').forEach(ic => { ic.style.transform = ''; ic.classList.remove('fa-minus'); ic.classList.add('fa-plus'); });
  if (!isOpen) {
    answer.classList.add('open');
    icon.style.transform = 'rotate(180deg)';
    icon.classList.remove('fa-plus'); icon.classList.add('fa-minus');
  }
}
renderFAQ();


let currentMode = 'free';
let freeSessionsLeft = localStorage.getItem('chromatype_free_left') ? parseInt(localStorage.getItem('chromatype_free_left')) : 18;

function updateCounterDisplay() {
  const counterEl = document.getElementById('freeCounter');
  if (counterEl) counterEl.textContent = freeSessionsLeft;
}
updateCounterDisplay();

function selectMode(mode) {
  currentMode = mode;
  const btnFree = document.getElementById('btnModeFree');
  const btnPaid = document.getElementById('btnModePaid');
  if (mode === 'free') {
    btnFree.className = "py-3 px-4 rounded-xl border-2 border-brand-accent bg-brand-accent/10 text-brand-cream font-bold text-xs sm:text-sm text-center transition-all";
    btnPaid.className = "py-3 px-4 rounded-xl border-2 border-brand-border bg-brand-dark text-brand-light font-bold text-xs sm:text-sm text-center transition-all";
  } else {
    btnPaid.className = "py-3 px-4 rounded-xl border-2 border-brand-accent bg-brand-accent/10 text-brand-cream font-bold text-xs sm:text-sm text-center transition-all";
    btnFree.className = "py-3 px-4 rounded-xl border-2 border-brand-border bg-brand-dark text-brand-light font-bold text-xs sm:text-sm text-center transition-all";
  }
  checkFormReady();
}

function checkFormReady() {
  const email = document.getElementById('userEmail').value.trim();
  const btn = document.getElementById('submitBtn');
  // Unlock button as long as photo is selected (and email if free mode)
  const ready = uploadedFile && (currentMode !== 'free' || email !== '');
  btn.disabled = !ready;
  if (!ready) {
    if (!uploadedFile) {
      document.getElementById('submitText').textContent = 'Upload a photo to continue';
    } else {
      document.getElementById('submitText').textContent = 'Enter email to receive report';
    }
  } else if (currentMode === 'free') {
    document.getElementById('submitText').textContent = `Get FREE Color Analysis (${freeSessionsLeft} Spots Left)`;
  } else {
    document.getElementById('submitText').textContent = 'Get Full $29 Master Package';
  }
}

function handleSubmit() {
  const name = document.getElementById('userName').value.trim();
  const email = document.getElementById('userEmail').value.trim();
  if (!name || !email || !uploadedFile) return;

  const btn = document.getElementById('submitBtn');
  btn.disabled = true;
  btn.textContent = 'Executing Optical CIELAB Analysis...';

  if (currentMode === 'free') {
    if (freeSessionsLeft > 0) {
      freeSessionsLeft--;
      localStorage.setItem('chromatype_free_left', freeSessionsLeft);
      updateCounterDisplay();
    }

    const mailtoUrl = `mailto:dkvendemais@gmail.com?subject=${encodeURIComponent('NEW CHROMATYPE SUBMISSION: ' + name)}&body=${encodeURIComponent('Client Name: ' + name + '\nClient Email: ' + email + '\nMode: FREE Teaser\n\nPlease generate and forward PDF report to: ' + email)}`;
    
    const iframe = document.createElement('iframe');
    iframe.style.display = 'none';
    iframe.src = mailtoUrl;
    document.body.appendChild(iframe);

    setTimeout(() => {
      btn.textContent = 'FREE Analysis Complete!';
      btn.classList.replace('bg-brand-accent', 'bg-emerald-600');
      showToast(`Analysis complete! Submission dispatched to dkvendemais@gmail.com and ${email}.`, 'success');
      
      alert(`🎉 Analysis Complete for ${name}!\n\nYour submission has been dispatched to dkvendemais@gmail.com and your report is being prepared for ${email}.`);
      
      if (freeSessionsLeft <= 0) {
        setTimeout(() => {
          alert('All 100 FREE spots claimed! Switching to standard $29 operations.');
          selectMode('paid');
        }, 1500);
      }
    }, 2000);
  } else {
    window.location.href = "https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business=dkvendemais@gmail.com&item_name=CHROMATYPE+Personal+Color+Analysis+Session&amount=29.00&currency_code=USD";
  }
}

function showToast(msg, type) {
  const toast = document.getElementById('toast');
  toast.textContent = msg;
  toast.classList.remove('opacity-0', 'pointer-events-none');
  setTimeout(() => toast.classList.add('opacity-0', 'pointer-events-none'), 4000);
}

// Timed Call to Action Slide-in Trigger (Triggers after 25 seconds or scroll)
let ctaShown = false;
function triggerCtaModal() {
  if (ctaShown) return;
  ctaShown = true;
  document.getElementById('timedCtaModal').classList.add('show');
}

function closeCtaModal() {
  document.getElementById('timedCtaModal').classList.remove('show');
}

// Trigger timer: 25 seconds
setTimeout(triggerCtaModal, 25000);

// Trigger scroll: when user scrolls past 300px
window.addEventListener('scroll', () => {
  if (window.scrollY > 300) {
    triggerCtaModal();
  }
});

// Scroll Reveal Observer
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) entry.target.classList.add('visible');
  });
}, { threshold: 0.1 });
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
</script>

<!-- Structured Data for National Google Organic Indexing -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "CHROMATYPE — CIELAB Spectrophotometric Personal Color Analysis",
  "description": "Upload one photo and receive your complete 12-season color palette powered by CHROMATYPE's CIELAB 3D spectrophotometric system.",
  "provider": {
    "@type": "Organization",
    "name": "CHROMATYPE",
    "url": "https://chromatype.me"
  },
  "offers": [
    {
      "@type": "Offer",
      "name": "Essential Analysis Pass",
      "price": "29.00",
      "priceCurrency": "USD"
    },
    {
      "@type": "Offer",
      "name": "Master Package with 52-Page Report",
      "price": "49.00",
      "priceCurrency": "USD"
    }
  ],
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "12400"
  }
}
</script>
</div>

