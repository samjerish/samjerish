import os

def generate_terminal_svg(output_path="terminal.svg"):
    # Lines of terminal output
    lines = [
        {"type": "cmd", "prompt": "samjerish@quantum-core:~$", "cmd": "whoami --bio"},
        {"type": "title", "text": "SAM JERISH D"},
        {"type": "badge", "text": "AI & Machine Learning Student  •  Full-Stack Developer"},
        {"type": "quote", "text": "Passionate about AI, Robotics, Computer Vision, and turning into real-world solutions."},
        {"type": "empty"},

        {"type": "cmd", "prompt": "samjerish@quantum-core:~$", "cmd": "neofetch --developer"},
        {"type": "spec", "key": "OS", "val": "macOS Sonoma (Darwin arm64)"},
        {"type": "spec", "key": "Host", "val": "AI & Robotics Workstation"},
        {"type": "spec", "key": "Focus", "val": "Artificial Intelligence, Deep Learning & Vision"},
        {"type": "spec", "key": "Robotics", "val": "Autonomous Navigation, Simulation & Control"},
        {"type": "spec", "key": "Stack", "val": "Python, C++, PyTorch, OpenCV, React, Node.js"},
        {"type": "spec", "key": "Status", "val": "Building intelligent systems & scalable architectures 🚀"},
        {"type": "empty"},

        {"type": "cmd", "prompt": "samjerish@quantum-core:~$", "cmd": "git status --contributions"},
        {"type": "git_branch", "text": "On branch main -> Ahead of 'origin/main' by commits across AI, Vision & Web"},
        {"type": "git_success", "text": "✔ 100% committed to engineering impactful software"},
        {"type": "empty"},

        {"type": "prompt_cursor", "prompt": "samjerish@quantum-core:~$"}
    ]

    svg_width = 880
    svg_height = 540
    start_x = 28
    start_y = 72
    line_height = 24

    css_keyframes = """
    @keyframes blink {
      0%, 100% { opacity: 1; }
      50% { opacity: 0; }
    }
    @keyframes lineFadeIn {
      from { opacity: 0; transform: translateY(4px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .cursor {
      fill: #58a6ff;
      animation: blink 0.9s infinite;
    }
    .line {
      opacity: 0;
      animation: lineFadeIn 0.3s ease forwards;
    }
    """

    css_delays = ""
    svg_content = []

    current_y = start_y
    delay = 0.2
    step = 0.16

    for i, item in enumerate(lines):
        item_type = item["type"]
        line_class = f"line line-{i}"
        css_delays += f"    .line-{i} {{ animation-delay: {delay:.2f}s; }}\n"

        if item_type == "empty":
            current_y += 14
            delay += 0.08
            continue

        if item_type == "cmd":
            svg_content.append(
                f'<text class="font-mono {line_class}" x="{start_x}" y="{current_y}">'
                f'<tspan fill="#3fb950" font-weight="700">{item["prompt"]}</tspan> '
                f'<tspan fill="#58a6ff" font-weight="600">{item["cmd"]}</tspan>'
                f'</text>'
            )
            delay += 0.35

        elif item_type == "title":
            svg_content.append(
                f'<text class="font-mono {line_class}" x="{start_x}" y="{current_y}">'
                f'<tspan fill="#d2a8ff" font-size="18px" font-weight="800">⚡ {item["text"]}</tspan>'
                f'</text>'
            )
            delay += step

        elif item_type == "badge":
            svg_content.append(
                f'<text class="font-mono {line_class}" x="{start_x}" y="{current_y}">'
                f'<tspan fill="#79c0ff" font-weight="600">❯ {item["text"]}</tspan>'
                f'</text>'
            )
            delay += step

        elif item_type == "quote":
            svg_content.append(
                f'<text class="font-mono {line_class}" x="{start_x}" y="{current_y}">'
                f'<tspan fill="#8b949e" font-style="italic">  "{item["text"]}"</tspan>'
                f'</text>'
            )
            delay += step

        elif item_type == "spec":
            svg_content.append(
                f'<text class="font-mono {line_class}" x="{start_x}" y="{current_y}">'
                f'<tspan fill="#ff7b72" font-weight="700">  [{item["key"]}]</tspan>'
                f'<tspan fill="#c9d1d9"> : </tspan>'
                f'<tspan fill="#f0883e">{item["val"]}</tspan>'
                f'</text>'
            )
            delay += step

        elif item_type == "git_branch":
            svg_content.append(
                f'<text class="font-mono {line_class}" x="{start_x}" y="{current_y}">'
                f'<tspan fill="#e3b341">  ⎇ {item["text"]}</tspan>'
                f'</text>'
            )
            delay += step

        elif item_type == "git_success":
            svg_content.append(
                f'<text class="font-mono {line_class}" x="{start_x}" y="{current_y}">'
                f'<tspan fill="#3fb950" font-weight="600">  {item["text"]}</tspan>'
                f'</text>'
            )
            delay += step

        elif item_type == "prompt_cursor":
            svg_content.append(
                f'<text class="font-mono {line_class}" x="{start_x}" y="{current_y}">'
                f'<tspan fill="#3fb950" font-weight="700">{item["prompt"]}</tspan> '
                f'<tspan class="cursor">█</tspan>'
                f'</text>'
            )

        current_y += line_height

    svg_content_str = "\n    ".join(svg_content)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
  <defs>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#161b22" />
      <stop offset="100%" stop-color="#21262d" />
    </linearGradient>
    <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#30363d" />
      <stop offset="50%" stop-color="#58a6ff" stop-opacity="0.4" />
      <stop offset="100%" stop-color="#30363d" />
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <style>
    .font-mono {{
      font-family: 'Fira Code', 'JetBrains Mono', 'SF Mono', Consolas, Monaco, monospace;
      font-size: 14.5px;
      letter-spacing: -0.2px;
    }}
    {css_keyframes}
    {css_delays}
  </style>

  <!-- Terminal Window Shadow & Base Card -->
  <rect x="2" y="2" width="{svg_width - 4}" height="{svg_height - 4}" rx="14" fill="#0d1117" stroke="url(#borderGrad)" stroke-width="1.8" />

  <!-- Window Header Bar -->
  <rect x="2" y="2" width="{svg_width - 4}" height="42" rx="14" fill="url(#headerGrad)" />
  <rect x="2" y="32" width="{svg_width - 4}" height="12" fill="#161b22" />
  <line x1="2" y1="44" x2="{svg_width - 2}" y2="44" stroke="#30363d" stroke-width="1" />

  <!-- macOS Window Controls (Traffic Lights) -->
  <circle cx="24" cy="22" r="6.5" fill="#ff5f56" />
  <circle cx="44" cy="22" r="6.5" fill="#ffbd2e" />
  <circle cx="64" cy="22" r="6.5" fill="#27c93f" />

  <!-- Terminal Title -->
  <g transform="translate({svg_width / 2}, 26)">
    <text text-anchor="middle" font-family="'Fira Code', 'JetBrains Mono', monospace" font-size="12px" fill="#8b949e" font-weight="600">
      ⚡ samjerish@macbook: ~ (zsh) — 88x24
    </text>
  </g>

  <!-- Terminal Body Content -->
  <g>
    {svg_content_str}
  </g>
</svg>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated {output_path} successfully ({len(svg)} bytes)")

if __name__ == "__main__":
    generate_terminal_svg()
