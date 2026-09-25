import os

def create_terminal_button(name, filename, color_accent, icon_svg_path, text_x="54"):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 170 44" width="170" height="44">
  <defs>
    <linearGradient id="btnBg_{name}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#161b22" />
      <stop offset="50%" stop-color="#0e1217" />
      <stop offset="100%" stop-color="#0a0c10" />
    </linearGradient>
    <linearGradient id="border_{name}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{color_accent}" stop-opacity="0.9" />
      <stop offset="60%" stop-color="#30363d" stop-opacity="0.7" />
      <stop offset="100%" stop-color="{color_accent}" stop-opacity="0.3" />
    </linearGradient>
  </defs>

  <g>
    <!-- Button Card with Rounded Corners & Subtle Border -->
    <rect x="1.5" y="1.5" width="167" height="41" rx="9" fill="url(#btnBg_{name})" stroke="url(#border_{name})" stroke-width="1.5" />

    <!-- Terminal Command Chevron -->
    <text x="12" y="27" font-family="'Menlo', 'Fira Code', 'JetBrains Mono', monospace" font-size="13px" fill="{color_accent}" font-weight="700">❯</text>

    <!-- Icon -->
    <g transform="translate(26, 11) scale(0.92)" fill="{color_accent}">
      {icon_svg_path}
    </g>

    <!-- Button Text -->
    <text x="{text_x}" y="27" font-family="'Menlo', 'Fira Code', -apple-system, monospace" font-size="13px" font-weight="700" fill="#f0f6fc" letter-spacing="0.4px">{name}</text>
  </g>
</svg>"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated {filename}")

if __name__ == "__main__":
    email_path = '<path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>'
    linkedin_path = '<path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 8.76a1.69 1.69 0 1 0-.01-3.38 1.69 1.69 0 0 0 .01 3.38m1.39 9.74v-8.37H5.07v8.37h2.78z"/>'
    instagram_path = '<path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>'
    portfolio_path = '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>'

    create_terminal_button("Email", "email.svg", "#ff7b72", email_path, text_x="54")
    create_terminal_button("LinkedIn", "linkedin.svg", "#58a6ff", linkedin_path, text_x="54")
    create_terminal_button("Instagram", "instagram.svg", "#f0883e", instagram_path, text_x="54")
    create_terminal_button("Portfolio", "portfolio.svg", "#3fb950", portfolio_path, text_x="54")
