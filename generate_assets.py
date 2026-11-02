import os

ASSETS_DIR = r"C:\Users\gkedi\.gemini\antigravity\scratch\turnitout-humanizer\assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

# 1. Glyphs & Favicon (Square Icon)
FAVICON_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <defs>
    <linearGradient id="unbotifyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#6366F1"/>
      <stop offset="50%" stop-color="#8B5CF6"/>
      <stop offset="100%" stop-color="#06B6D4"/>
    </linearGradient>
    <linearGradient id="sparkGrad" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#F43F5E"/>
      <stop offset="100%" stop-color="#FB923C"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.5" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Dark Rounded Chassis -->
  <rect width="64" height="64" rx="16" fill="#0A0D14"/>
  <rect x="0.75" y="0.75" width="62.5" height="62.5" rx="15.25" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="1.5"/>

  <!-- Unbotify Monogram: Structured U breaking into Organic Spark -->
  <!-- Left stem: Geometric/Formulaic -->
  <path d="M 18 16 L 18 36 C 18 45 25 50 34 50 C 43 50 50 44 50 35 L 50 26" 
        fill="none" 
        stroke="url(#unbotifyGrad)" 
        stroke-width="6.5" 
        stroke-linecap="round" 
        stroke-linejoin="round"/>

  <!-- Expressive Human Spark Accent: Unlocking freedom -->
  <path d="M 44 14 Q 50 20 44 26 Q 38 20 44 14 Z" 
        fill="url(#sparkGrad)" 
        filter="url(#glow)"/>
</svg>'''

# 2. Standalone Brand Mark (Square)
LOGO_MARK_SVG = FAVICON_SVG

# 3. Full Brand Banner (Horizontal Logo + Text + Tagline)
LOGO_FULL_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 120" width="480" height="120">
  <defs>
    <linearGradient id="markGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#6366F1"/>
      <stop offset="50%" stop-color="#8B5CF6"/>
      <stop offset="100%" stop-color="#06B6D4"/>
    </linearGradient>
    <linearGradient id="textGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#CBD5E1"/>
    </linearGradient>
    <linearGradient id="sparkFull" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#F43F5E"/>
      <stop offset="100%" stop-color="#FB923C"/>
    </linearGradient>
  </defs>

  <!-- Left Icon Mark -->
  <g transform="translate(10, 10)">
    <rect width="100" height="100" rx="26" fill="#0E1320"/>
    <rect x="1" y="1" width="98" height="98" rx="25" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="1.5"/>
    
    <!-- Stylized U Path -->
    <path d="M 28 26 L 28 56 C 28 71 39 78 52 78 C 65 78 76 70 76 56 L 76 42" 
          fill="none" 
          stroke="url(#markGrad)" 
          stroke-width="10" 
          stroke-linecap="round" 
          stroke-linejoin="round"/>
          
    <!-- Spark Element -->
    <path d="M 68 22 Q 78 30 68 38 Q 58 30 68 22 Z" 
          fill="url(#sparkFull)"/>
  </g>

  <!-- Wordmark & Tagline -->
  <g transform="translate(132, 30)">
    <text x="0" y="44" 
          font-family="system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, sans-serif" 
          font-size="44" 
          font-weight="900" 
          letter-spacing="2.5" 
          fill="url(#textGrad)">UNBOTIFY</text>
    
    <text x="2" y="70" 
          font-family="system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, sans-serif" 
          font-size="14.5" 
          font-weight="600" 
          letter-spacing="1.2" 
          fill="#94A3B8">Less formula. More expression.</text>
  </g>
</svg>'''

with open(os.path.join(ASSETS_DIR, "favicon.svg"), "w", encoding="utf-8") as f:
    f.write(FAVICON_SVG)

with open(os.path.join(ASSETS_DIR, "logo-mark.svg"), "w", encoding="utf-8") as f:
    f.write(LOGO_MARK_SVG)

with open(os.path.join(ASSETS_DIR, "logo.svg"), "w", encoding="utf-8") as f:
    f.write(LOGO_FULL_SVG)

print("Unbotify SVG assets created successfully.")

