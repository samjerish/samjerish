import sys

def create_button(name, filename, color1, color2, icon_path, icon_scale, icon_translate, text_x):
    svg_template = f"""<?xml version="1.0" encoding="utf-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 160 50" width="160" height="50">
  <style>
    .text {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
      font-size: 15px;
      font-weight: bold;
      fill: #ffffff;
      letter-spacing: 0.5px;
    }}
  </style>
  <defs>
    <linearGradient id="grad_{name}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{color1}" />
      <stop offset="100%" stop-color="{color2}" />
      <animate attributeName="x1" values="0%;100%;0%" dur="3s" repeatCount="indefinite" />
      <animate attributeName="x2" values="100%;0%;100%" dur="3s" repeatCount="indefinite" />
    </linearGradient>
    <linearGradient id="grad2_{name}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{color2}" />
      <stop offset="100%" stop-color="{color1}" />
      <animate attributeName="x1" values="100%;0%;100%" dur="3s" repeatCount="indefinite" />
      <animate attributeName="x2" values="0%;100%;0%" dur="3s" repeatCount="indefinite" />
    </linearGradient>
  </defs>
  
  <!-- Outer glowing ring -->
  <rect x="5" y="5" width="150" height="40" rx="20" fill="none" stroke="url(#grad_{name})" stroke-width="4" opacity="0.6">
    <animate attributeName="opacity" values="0.3;0.8;0.3" dur="2s" repeatCount="indefinite" />
    <animate attributeName="stroke-width" values="3;6;3" dur="2s" repeatCount="indefinite" />
  </rect>
  
  <!-- Main Button Background -->
  <rect x="5" y="5" width="150" height="40" rx="20" fill="#0d1117" stroke="url(#grad2_{name})" stroke-width="2" />
  
  <!-- Icon -->
  <g transform="translate({icon_translate}) scale({icon_scale})" fill="url(#grad_{name})">
    {icon_path}
  </g>
  
  <!-- Text -->
  <text x="{text_x}" y="31" class="text">{name}</text>
</svg>"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(svg_template)

if __name__ == "__main__":
    email_path = '<path d="M2.002 5.884L10 9.882l7.998-3.998A2 2 0 0016 4H4a2 2 0 00-1.998 1.884z"/><path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>'
    # using simple viewBox 0 0 20 20 path for email above
    
    linkedin_path = '<path d="M4.98 3.5c0 1.381-1.11 2.5-2.48 2.5s-2.48-1.119-2.48-2.5c0-1.38 1.11-2.5 2.48-2.5s2.48 1.12 2.48 2.5zm.02 4.5h-5v16h5v-16zm7.982 0h-4.968v16h4.969v-8.399c0-4.67 6.029-5.052 6.029 0v8.399h4.988v-10.131c0-7.88-8.922-7.593-11.018-3.714v-2.155z"/>'
    
    instagram_path = '<path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/>'
    
    create_button("Email", "email.svg", "#D14836", "#FF7A59", email_path, "1.1", "15, 14", "45")
    create_button("LinkedIn", "linkedin.svg", "#0077B5", "#00A0DC", linkedin_path, "0.8", "16, 14", "45")
    create_button("Instagram", "instagram.svg", "#833AB4", "#FD1D1D", instagram_path, "0.85", "15, 14", "45")
