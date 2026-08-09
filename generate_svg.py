import sys

def generate_svg():
    lines = [
        {"type": "cmd", "text": "cat about.txt"},
        {"type": "title", "text": "👋 SAM JERISH D"},
        {"type": "normal", "text": "AI &amp; Machine Learning Student • Full-Stack Developer"},
        {"type": "normal", "text": "Passionate about AI, Robotics, Computer Vision, and turning ideas"},
        {"type": "normal", "text": "into real-world solutions. 🚀"},
        {"type": "empty", "text": ""},
        {"type": "cmd", "text": "./show_skills.sh"},
        {"type": "list", "key": "Languages", "text": "Python, Java, JavaScript"},
        {"type": "list", "key": "Web      ", "text": "HTML, CSS, React"},
        {"type": "list", "key": "Database ", "text": "SQL"},
        {"type": "list", "key": "AI/ML    ", "text": "Artificial Intelligence, Machine Learning, Computer Vision"},
        {"type": "list", "key": "Dev      ", "text": "Full-Stack, Android, Intelligent Robotics"},
        {"type": "list", "key": "Tools    ", "text": "Git, GitHub, VS Code, Blender"},

        {"type": "cmd", "text": "cat contact.txt"},
        {"type": "normal", "text": "📧 samjerishd@gmail.com"},
        {"type": "normal", "text": "🔗 linkedin.com/in/samjerishd"},
        {"type": "normal", "text": "📸 instagram.com/samjerishd"},
        {"type": "empty", "text": ""},
        {"type": "prompt_only", "text": ""}
    ]

    svg_width = 850
    svg_height = 650
    line_height = 24
    start_y = 60
    start_x = 20

    css_delays = ""
    svg_text_elements = ""

    current_y = start_y
    delay = 0.5
    delay_step = 0.3

    for i, line in enumerate(lines):
        line_class = f"line delay-{i}"
        css_delays += f"      .delay-{i} {{ animation-delay: {delay:.1f}s; }}\n"

        if line["type"] == "empty":
            current_y += line_height
            continue

        svg_text_elements += f'    <text class="text {line_class}" y="{current_y}">\n'
        
        if line["type"] == "cmd":
            svg_text_elements += f'      <tspan class="prompt">sam@macbook:~$</tspan> <tspan class="cmd">{line["text"]}</tspan>\n'
            delay += 0.6
        elif line["type"] == "prompt_only":
            svg_text_elements += f'      <tspan class="prompt">sam@macbook:~$</tspan> <tspan class="cursor">█</tspan>\n'
        elif line["type"] == "title":
            svg_text_elements += f'      <tspan class="title">{line["text"]}</tspan>\n'
        elif line["type"] == "normal":
            svg_text_elements += f'      {line["text"]}\n'
        elif line["type"] == "list":
            # using xml:space="preserve" in the SVG so spaces are kept
            svg_text_elements += f'      [<tspan class="key">{line["key"]}</tspan>] {line["text"]}\n'
        elif line["type"] == "proj":
            svg_text_elements += f'      drwxr-xr-x 1 sam sam 1024 <tspan class="value">{line["name"]}</tspan> {line["desc"]}\n'

        svg_text_elements += '    </text>\n'
        
        current_y += line_height
        delay += delay_step

    svg_template = f"""<?xml version="1.0" encoding="utf-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
  <style>
    .text {{ font-family: 'Fira Code', 'Courier New', Courier, monospace; font-size: 15px; fill: #a9b7c6; white-space: pre; }}
    .prompt {{ fill: #98c379; font-weight: bold; }}
    .cmd {{ fill: #e5c07b; }}
    .title {{ fill: #61afef; font-weight: bold; font-size: 18px; }}
    .value {{ fill: #98c379; }}
    .key {{ fill: #e06c75; font-weight: bold; }}
    
    /* Typewriter cursor */
    .cursor {{
      fill: #a9b7c6;
      animation: blink 1s step-end infinite;
    }}
    @keyframes blink {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0; }}
    }}
    
    /* Line animations */
    .line {{
      opacity: 0;
      animation: appear 0.1s forwards;
    }}
    @keyframes appear {{
      to {{ opacity: 1; }}
    }}
    
{css_delays}
  </style>
  
  <!-- Window frame -->
  <rect x="0" y="0" width="{svg_width}" height="{svg_height}" rx="10" ry="10" fill="#1e1e1e" />
  <!-- Top bar -->
  <rect x="0" y="0" width="{svg_width}" height="35" fill="#2d2d2d" rx="10" ry="10" />
  <rect x="0" y="20" width="{svg_width}" height="15" fill="#2d2d2d" />
  
  <!-- Buttons -->
  <circle cx="20" cy="17" r="6" fill="#ff5f56" />
  <circle cx="40" cy="17" r="6" fill="#ffbd2e" />
  <circle cx="60" cy="17" r="6" fill="#27c93f" />
  
  <!-- Content -->
  <g transform="translate({start_x}, {start_y})">
{svg_text_elements}
  </g>
</svg>"""

    with open("terminal.svg", "w", encoding="utf-8") as f:
        f.write(svg_template)

if __name__ == "__main__":
    generate_svg()
