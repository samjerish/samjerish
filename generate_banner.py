import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def get_coding_font(size):
    fonts_to_try = [
        ('/System/Library/Fonts/Menlo.ttc', 1),  # Menlo Bold
        ('/System/Library/Fonts/SFNSMono.ttf', 0),
        ('/System/Library/Fonts/Monaco.ttf', 0),
        ('/System/Library/Fonts/Supplemental/Courier New Bold.ttf', 0)
    ]
    for path, idx in fonts_to_try:
        if os.path.exists(path):
            try:
                if idx > 0:
                    return ImageFont.truetype(path, size, index=idx)
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

def create_rich_dark_base(w, h, photo_path="github banner.png", scale=1.0):
    base = Image.new('RGBA', (w, h), (10, 12, 16, 255))

    # 1. Subtle dark grey & slate ambient aura
    ambient = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    amb_draw = ImageDraw.Draw(ambient)
    amb_draw.ellipse((int(w * 0.45), -int(h * 0.3), int(w * 1.15), int(h * 1.3)), fill=(30, 42, 58, 130))
    amb_draw.ellipse((-int(w * 0.1), -int(h * 0.3), int(w * 0.5), int(h * 0.9)), fill=(24, 30, 42, 150))
    ambient = ambient.filter(ImageFilter.GaussianBlur(int(45 * scale)))
    base = Image.alpha_composite(base, ambient)
    draw = ImageDraw.Draw(base)

    # 2. Subtle tech dot grid on background
    step = int(24 * scale)
    dot_r = max(1, int(1.5 * scale))
    grid_end_x = int(w * 0.65)
    for gx in range(int(55 * scale), grid_end_x, step):
        for gy in range(int(30 * scale), int(h - 30 * scale), step):
            draw.ellipse((gx, gy, gx + dot_r * 2, gy + dot_r * 2), fill=(40, 48, 62, 110))

    # 3. Headline in coding font
    font_code = get_coding_font(int(35 * scale))
    lines = [
        "creativity and technology",
        "to craft user-centric",
        "solutions"
    ]

    line_h = int(54 * scale)
    total_text_h = (len(lines) - 1) * line_h + int(35 * scale)
    start_y = (h - total_text_h) // 2
    text_x = int(55 * scale)

    for i, line in enumerate(lines):
        y = start_y + i * line_h
        draw.text((text_x, y), line, fill=(240, 246, 252, 255), font=font_code)

    # 4. Large photo on the right
    if os.path.exists(photo_path):
        photo = Image.open(photo_path).convert('RGBA')
        photo_h = int(335 * scale)
        aspect = photo.width / photo.height
        photo_w = int(photo_h * aspect)
        photo = photo.resize((photo_w, photo_h), Image.LANCZOS)

        px = w - photo_w - int(10 * scale)
        py = h - photo_h

        # Soft blurred ground shadow beneath photo
        shadow = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        s_draw = ImageDraw.Draw(shadow)
        s_draw.ellipse(
            (px + int(25 * scale), py + photo_h - int(50 * scale), px + photo_w - int(25 * scale), py + photo_h + int(15 * scale)),
            fill=(20, 30, 45, 120)
        )
        shadow = shadow.filter(ImageFilter.GaussianBlur(int(15 * scale)))
        base = Image.alpha_composite(base, shadow)

        base.paste(photo, (px, py), photo)

    # 5. Crisp subtle dark theme border
    draw = ImageDraw.Draw(base)
    border_r = int(14 * scale)
    border_w = max(1, int(1.5 * scale))
    draw.rounded_rectangle((1, 1, w - 2, h - 2), radius=border_r, outline=(48, 54, 61, 220), width=border_w)

    return base


def generate_banner_png(output_path="header_banner.png", photo_path="github banner.png"):
    w, h = 2000, 680
    banner = create_rich_dark_base(w, h, photo_path, scale=2.0)
    banner.save(output_path, 'PNG', optimize=True)
    print(f"Generated {output_path} successfully ({w}x{h})")


def generate_banner_gif(output_path="header_banner.gif", photo_path="github banner.png"):
    w, h = 1000, 340
    base = create_rich_dark_base(w, h, photo_path, scale=1.0)
    bg_blank = Image.new('RGBA', (w, h), (10, 12, 16, 255))

    # Opening wipe entrance (16 frames) + Sheen sweep (42 frames) + Pause (18 frames) = 76 frames (~4.5s)
    opening_frames = 16
    sheen_frames = 42
    pause_frames = 18
    total_frames = opening_frames + sheen_frames + pause_frames

    beam_width = 240
    tilt = 0.38

    frames = []
    for i in range(total_frames):
        if i < opening_frames:
            # Opening swipe entrance: reveals banner smoothly from left to right
            prog = i / float(opening_frames - 1)
            eased = 1 - (1 - prog) ** 3
            wipe_x = int(w * eased)

            mask = Image.new('L', (w, h), 0)
            m_draw = ImageDraw.Draw(mask)
            m_draw.rectangle((0, 0, wipe_x, h), fill=255)

            # Feather leading edge
            if wipe_x < w:
                for fx in range(max(0, wipe_x - 30), min(w, wipe_x + 10)):
                    ratio = (fx - (wipe_x - 30)) / 40.0
                    alpha = int(255 * (1 - ratio))
                    m_draw.line([(fx, 0), (fx, h)], fill=alpha)

            frame = Image.composite(base, bg_blank, mask)

            # Glowing leading beam
            if wipe_x < w:
                beam = Image.new('RGBA', (w, h), (0, 0, 0, 0))
                b_draw = ImageDraw.Draw(beam)
                b_draw.line([(wipe_x, 0), (wipe_x, h)], fill=(200, 220, 255, 230), width=6)
                beam = beam.filter(ImageFilter.GaussianBlur(4))
                frame = Image.alpha_composite(frame, beam)

        elif i < opening_frames + sheen_frames:
            # Sheen sweep across full banner
            sheen_i = i - opening_frames
            prog = sheen_i / float(sheen_frames - 1)
            center_x = -260 + prog * 1520

            frame = base.copy()
            sheen = Image.new('RGBA', (w, h), (0, 0, 0, 0))
            sheen_draw = ImageDraw.Draw(sheen)

            steps = 35
            for s in range(-steps, steps + 1):
                t = s / float(steps)
                offset = t * (beam_width / 2.0)
                dist = abs(t)
                alpha_wide = 40 * math.exp(-3.0 * (dist ** 2))
                alpha_core = 50 * math.exp(-12.0 * (dist ** 2))
                alpha = int(min(255, alpha_wide + alpha_core))

                if alpha > 0:
                    x_top = center_x + offset + (h * tilt) / 2.0
                    x_bot = center_x + offset - (h * tilt) / 2.0
                    sheen_draw.line([(x_top, 0), (x_bot, h)], fill=(255, 255, 255, alpha), width=4)

            frame = Image.alpha_composite(frame, sheen)
        else:
            frame = base.copy()

        frames.append(frame.convert('RGB'))

    palette_img = base.convert('RGB').quantize(colors=256)
    quantized_frames = [f.quantize(palette=palette_img) for f in frames]

    quantized_frames[0].save(output_path, save_all=True, append_images=quantized_frames[1:], duration=60, loop=0, optimize=True)
    print(f"Generated {output_path} successfully ({w}x{h}, {len(quantized_frames)} frames)")


def generate_banner_svg(output_path="header_banner.svg", photo_path="github banner.png"):
    import base64
    photo_b64 = ""
    if os.path.exists(photo_path):
        with open(photo_path, "rb") as f:
            photo_b64 = base64.b64encode(f.read()).decode("utf-8")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 340" width="1000" height="340">
  <defs>
    <!-- Background Gradients -->
    <linearGradient id="cardBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a0c10" />
      <stop offset="50%" stop-color="#0e1217" />
      <stop offset="100%" stop-color="#090b0e" />
    </linearGradient>

    <radialGradient id="ambientGlow" cx="75%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#283548" stop-opacity="0.4" />
      <stop offset="60%" stop-color="#161b22" stop-opacity="0.1" />
      <stop offset="100%" stop-color="#0a0c10" stop-opacity="0" />
    </radialGradient>

    <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#30363d" stop-opacity="0.9" />
      <stop offset="50%" stop-color="#58a6ff" stop-opacity="0.3" />
      <stop offset="100%" stop-color="#21262d" stop-opacity="0.8" />
    </linearGradient>

    <linearGradient id="beamGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0" />
      <stop offset="50%" stop-color="#58a6ff" stop-opacity="0.22" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0" />
    </linearGradient>

    <!-- Tech Dot Grid Pattern -->
    <pattern id="dotGrid" x="0" y="0" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="12" cy="12" r="1.2" fill="#30363d" opacity="0.45" />
    </pattern>
  </defs>

  <style>
    @keyframes smoothSlideInLeft {{
      0% {{
        opacity: 0;
        transform: translateX(-40px);
      }}
      100% {{
        opacity: 1;
        transform: translateX(0);
      }}
    }}

    @keyframes smoothSlideInRight {{
      0% {{
        opacity: 0;
        transform: translateX(45px);
      }}
      100% {{
        opacity: 1;
        transform: translateX(0);
      }}
    }}

    @keyframes lightSweep {{
      0% {{
        transform: translateX(-450px) skewX(-20deg);
        opacity: 0;
      }}
      20% {{
        opacity: 1;
      }}
      60% {{
        transform: translateX(1150px) skewX(-20deg);
        opacity: 0.8;
      }}
      80%, 100% {{
        transform: translateX(1150px) skewX(-20deg);
        opacity: 0;
      }}
    }}

    @keyframes cursorBlink {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0; }}
    }}

    .font-code {{
      font-family: 'Menlo', 'Fira Code', 'JetBrains Mono', 'SF Mono', Consolas, monospace;
      font-size: 34px;
      font-weight: 700;
      fill: #f0f6fc;
      letter-spacing: -0.3px;
    }}

    .line-1 {{
      animation: smoothSlideInLeft 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.1s both;
    }}
    .line-2 {{
      animation: smoothSlideInLeft 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.3s both;
    }}
    .line-3 {{
      animation: smoothSlideInLeft 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.5s both;
    }}

    .photo-reveal {{
      animation: smoothSlideInRight 0.95s cubic-bezier(0.16, 1, 0.3, 1) 0.15s both;
    }}

    .sweep-beam {{
      animation: lightSweep 4.5s ease-in-out infinite 0.9s;
    }}

    .blink-cursor {{
      fill: #58a6ff;
      animation: cursorBlink 0.9s infinite;
    }}
  </style>

  <!-- Base Card Background -->
  <rect x="1" y="1" width="998" height="338" rx="16" fill="url(#cardBg)" stroke="url(#borderGrad)" stroke-width="1.8" />

  <!-- Ambient Lighting Layer -->
  <rect x="1" y="1" width="998" height="338" rx="16" fill="url(#ambientGlow)" />

  <!-- Background Tech Dot Grid on Left Side -->
  <rect x="2" y="2" width="620" height="336" fill="url(#dotGrid)" />

  <!-- Coding Tagline -->
  <g transform="translate(60, 110)">
    <text class="font-code line-1" x="0" y="0">creativity and technology</text>
    <text class="font-code line-2" x="0" y="54">to craft user-centric</text>
    <text class="font-code line-3" x="0" y="108">solutions<tspan class="blink-cursor">_</tspan></text>
  </g>

  <!-- Large Photo with Smooth Slide-in from Right -->
  <g class="photo-reveal">
    <image href="data:image/png;base64,{photo_b64}" x="625" y="10" width="360" height="330" preserveAspectRatio="xMidYMid meet" />
  </g>

  <!-- Silky Light Sweep Beam Overlay -->
  <rect class="sweep-beam" x="0" y="0" width="280" height="340" fill="url(#beamGrad)" pointer-events="none" />

</svg>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated {output_path} successfully ({len(svg)} bytes)")


if __name__ == "__main__":
    generate_banner_png()
    generate_banner_gif()
    generate_banner_svg()
