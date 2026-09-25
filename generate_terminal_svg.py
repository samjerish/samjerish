import html

def escape_xml(s):
    return html.escape(str(s), quote=True)

def generate_terminal_svg(output_path="terminal.svg"):
    lines = [
        {"type": "cmd", "prompt": "samjerish@quantum-core:~$", "cmd": "whoami --bio"},
        {"type": "title", "text": "SAM JERISH D"},
        {"type": "badge", "text": "AI & Machine Learning Student  •  Full-Stack Developer"},
        {"type": "quote", "text": "Creativity and technology to craft user-centric solutions."},
        {"type": "empty"},

        {"type": "cmd", "prompt": "samjerish@quantum-core:~$", "cmd": "neofetch --developer"},
        {"type": "spec", "key": "OS", "val": "macOS Sonoma (Darwin arm64)"},
        {"type": "spec", "key": "Host", "val": "AI, Vision & Robotics Workstation"},
        {"type": "spec", "key": "Focus", "val": "Artificial Intelligence, Deep Learning & Robotics"},
        {"type": "spec", "key": "Robotics", "val": "Intelligent Navigation, Obstacle Avoidance & Perception"},
        {"type": "spec", "key": "Stack", "val": "Python, PyTorch, OpenCV, React, Node.js, C++, TypeScript"},
        {"type": "spec", "key": "Status", "val": "Developing real-world autonomous systems & scalable apps 🚀"},
        {"type": "empty"},

        {"type": "cmd", "prompt": "samjerish@quantum-core:~$", "cmd": "git status --contributions"},
        {"type": "git_branch", "text": "On branch main -> Ahead of 'origin/main' with continuous commits"},
        {"type": "git_success", "text": "✔ 100% committed to engineering impactful software"},
        {"type": "empty"},

        {"type": "prompt_cursor", "prompt": "samjerish@quantum-core:~$"}
    ]

    svg_width = 880
    svg_height = 540
    start_x = 28
    start_y = 74
    line_height = 24

    svg_content = []
    current_y = start_y
    anim_index = 1
    css_rules = []

    for item in lines:
        item_type = item["type"]

        if item_type == "empty":
            current_y += 14
            continue

        delay = round(0.12 + anim_index * 0.1, 2)
        css_rules.append(f'.anim-{anim_index} {{ animation: fadeInUp 0.45s cubic-bezier(0.16, 1, 0.3, 1) {delay}s both; }}')

        if item_type == "cmd":
            prompt = escape_xml(item["prompt"])
            cmd = escape_xml(item["cmd"])
            svg_content.append(
                f'<g class="anim-{anim_index}"><text class="font-mono" x="{start_x}" y="{current_y}">'
                f'<tspan fill="#3fb950" font-weight="700">{prompt}</tspan> '
                f'<tspan fill="#58a6ff" font-weight="600">{cmd}</tspan>'
                f'</text></g>'
            )

        elif item_type == "title":
            text = escape_xml(item["text"])
            svg_content.append(
                f'<g class="anim-{anim_index}"><text class="font-mono" x="{start_x}" y="{current_y}">'
                f'<tspan fill="#d2a8ff" font-size="18px" font-weight="800">⚡ {text}</tspan>'
                f'</text></g>'
            )

        elif item_type == "badge":
            text = escape_xml(item["text"])
            svg_content.append(
                f'<g class="anim-{anim_index}"><text class="font-mono" x="{start_x}" y="{current_y}">'
                f'<tspan fill="#79c0ff" font-weight="600">❯ {text}</tspan>'
                f'</text></g>'
            )

        elif item_type == "quote":
            text = escape_xml(item["text"])
            svg_content.append(
                f'<g class="anim-{anim_index}"><text class="font-mono" x="{start_x}" y="{current_y}">'
                f'<tspan fill="#8b949e" font-style="italic">  &quot;{text}&quot;</tspan>'
                f'</text></g>'
            )

        elif item_type == "spec":
            key = escape_xml(item["key"])
            val = escape_xml(item["val"])
            svg_content.append(
                f'<g class="anim-{anim_index}"><text class="font-mono" x="{start_x}" y="{current_y}">'
                f'<tspan fill="#ff7b72" font-weight="700">  [{key}]</tspan>'
                f'<tspan fill="#c9d1d9"> : </tspan>'
                f'<tspan fill="#f0883e">{val}</tspan>'
                f'</text></g>'
            )

        elif item_type == "git_branch":
            text = escape_xml(item["text"])
            svg_content.append(
                f'<g class="anim-{anim_index}"><text class="font-mono" x="{start_x}" y="{current_y}">'
                f'<tspan fill="#e3b341">  ⎇ {text}</tspan>'
                f'</text></g>'
            )

        elif item_type == "git_success":
            text = escape_xml(item["text"])
            svg_content.append(
                f'<g class="anim-{anim_index}"><text class="font-mono" x="{start_x}" y="{current_y}">'
                f'<tspan fill="#3fb950" font-weight="600">  {text}</tspan>'
                f'</text></g>'
            )

        elif item_type == "prompt_cursor":
            prompt = escape_xml(item["prompt"])
            svg_content.append(
                f'<g class="anim-{anim_index}"><text class="font-mono" x="{start_x}" y="{current_y}">'
                f'<tspan fill="#3fb950" font-weight="700">{prompt}</tspan> '
                f'<tspan class="cursor">█</tspan>'
                f'</text></g>'
            )

        anim_index += 1
        current_y += line_height

    css_rules_str = "\n    ".join(css_rules)
    svg_content_str = "\n    ".join(svg_content)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
  <defs>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#161b22" />
      <stop offset="100%" stop-color="#21262d" />
    </linearGradient>
    <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#30363d" />
      <stop offset="50%" stop-color="#58a6ff" stop-opacity="0.6" />
      <stop offset="100%" stop-color="#30363d" />
    </linearGradient>
  </defs>

  <style>
    .font-mono {{
      font-family: 'Fira Code', 'JetBrains Mono', 'SF Mono', Consolas, Monaco, monospace;
      font-size: 14.5px;
      letter-spacing: -0.2px;
    }}
    @keyframes fadeInUp {{
      0% {{ opacity: 0; transform: translateY(6px); }}
      100% {{ opacity: 1; transform: translateY(0); }}
    }}
    {css_rules_str}
    .cursor {{
      fill: #58a6ff;
      animation: blink 0.9s infinite;
    }}
    @keyframes blink {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0; }}
    }}
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
    print(f"Generated {output_path} successfully ({len(svg)} bytes) - 100% valid XML")

if __name__ == "__main__":
    generate_terminal_svg()
