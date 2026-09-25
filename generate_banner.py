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

    # Opening horizon flare + shutter unfold (22 frames) + Sheen sweep (38 frames) + Pause (14 frames) = 74 frames (~3.7s)
    opening_frames = 22
    sheen_frames = 38
    pause_frames = 14
    total_frames = opening_frames + sheen_frames + pause_frames

    beam_width = 240
    tilt = 0.38

    frames = []
    for i in range(total_frames):
        if i < opening_frames:
            prog = i / float(opening_frames - 1)
            # 1. Horizon split opening
            if prog < 0.35:
                # Laser ignition phase
                laser_prog = prog / 0.35
                laser_w = int(w * (1 - (1 - laser_prog) ** 2))
                frame = bg_blank.copy()
                laser = Image.new('RGBA', (w, h), (0, 0, 0, 0))
                l_draw = ImageDraw.Draw(laser)
                lx_start = (w - laser_w) // 2
                lx_end = (w + laser_w) // 2
                l_draw.line([(lx_start, h // 2), (lx_end, h // 2)], fill=(88, 166, 255, 240), width=6)
                l_draw.line([(lx_start, h // 2), (lx_end, h // 2)], fill=(255, 255, 255, 255), width=2)
                # Star flare center
                flare_r = int(50 * math.sin(laser_prog * math.pi))
                if flare_r > 0:
                    l_draw.ellipse((w // 2 - flare_r, h // 2 - flare_r // 3, w // 2 + flare_r, h // 2 + flare_r // 3), fill=(255, 255, 255, 200))
                laser = laser.filter(ImageFilter.GaussianBlur(3))
                frame = Image.alpha_composite(frame, laser)
            else:
                # Vertical shutter unfold phase
                unfold_prog = (prog - 0.35) / 0.65
                eased_y = 1 - (1 - unfold_prog) ** 3
                reveal_h = max(2, int(h * eased_y))
                y_top = (h - reveal_h) // 2
                y_bot = y_top + reveal_h

                mask = Image.new('L', (w, h), 0)
                m_draw = ImageDraw.Draw(mask)
                m_draw.rounded_rectangle((0, y_top, w, y_bot), radius=14, fill=255)
                frame = Image.composite(base, bg_blank, mask)

                # Horizon glowing border edges during expansion
                if unfold_prog < 0.9:
                    edge = Image.new('RGBA', (w, h), (0, 0, 0, 0))
                    e_draw = ImageDraw.Draw(edge)
                    e_draw.line([(0, y_top), (w, y_top)], fill=(88, 166, 255, int(200 * (1 - unfold_prog))), width=3)
                    e_draw.line([(0, y_bot), (w, y_bot)], fill=(88, 166, 255, int(200 * (1 - unfold_prog))), width=3)
                    edge = edge.filter(ImageFilter.GaussianBlur(2))
                    frame = Image.alpha_composite(frame, edge)

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

    quantized_frames[0].save(output_path, save_all=True, append_images=quantized_frames[1:], duration=50, loop=0, optimize=True)
    print(f"Generated {output_path} successfully ({w}x{h}, {len(quantized_frames)} frames)")


def generate_banner_svg(output_path="header_banner.svg", photo_path="github banner.png"):
    import base64
    photo_b64 = ""
    if os.path.exists(photo_path):
        with open(photo_path, "rb") as f:
            photo_b64 = base64.b64encode(f.read()).decode("utf-8")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1000 340" width="1000" height="340">
  <defs>
    <!-- Background Gradients -->
    <linearGradient id="cardBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a0c10" />
      <stop offset="50%" stop-color="#0e1217" />
      <stop offset="100%" stop-color="#090b0e" />
    </linearGradient>

    <radialGradient id="ambientGlow" cx="78%" cy="50%" r="65%">
      <stop offset="0%" stop-color="#283548" stop-opacity="0.55" />
      <stop offset="55%" stop-color="#161b22" stop-opacity="0.18" />
      <stop offset="100%" stop-color="#0a0c10" stop-opacity="0" />
    </radialGradient>

    <radialGradient id="centerIgniteGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#58a6ff" stop-opacity="0.9" />
      <stop offset="30%" stop-color="#388bfd" stop-opacity="0.5" />
      <stop offset="70%" stop-color="#1f6feb" stop-opacity="0.15" />
      <stop offset="100%" stop-color="#0d1117" stop-opacity="0" />
    </radialGradient>

    <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#30363d" stop-opacity="0.95" />
      <stop offset="50%" stop-color="#58a6ff" stop-opacity="0.45" />
      <stop offset="100%" stop-color="#21262d" stop-opacity="0.85" />
    </linearGradient>

    <linearGradient id="horizonBeam" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#58a6ff" stop-opacity="0" />
      <stop offset="25%" stop-color="#58a6ff" stop-opacity="0.3" />
      <stop offset="50%" stop-color="#ffffff" stop-opacity="0.95" />
      <stop offset="75%" stop-color="#58a6ff" stop-opacity="0.3" />
      <stop offset="100%" stop-color="#58a6ff" stop-opacity="0" />
    </linearGradient>

    <linearGradient id="sheenGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0" />
      <stop offset="50%" stop-color="#58a6ff" stop-opacity="0.25" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0" />
    </linearGradient>

    <!-- Tech Dot Grid Pattern -->
    <pattern id="dotGrid" x="0" y="0" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="12" cy="12" r="1.2" fill="#30363d" opacity="0.45" />
    </pattern>

    <!-- Smooth Horizon Expansion Clip -->
    <clipPath id="horizonShutterClip">
      <rect class="shutter-rect" x="0" y="0" width="1000" height="340" rx="16" />
    </clipPath>
  </defs>

  <style>
    /* 1. Card Horizon Shutter Unfold */
    @keyframes horizonUnfold {{
      0% {{
        transform: scaleY(0.02) scaleX(0.4);
        opacity: 0;
      }}
      20% {{
        transform: scaleY(0.04) scaleX(1);
        opacity: 0.95;
      }}
      100% {{
        transform: scaleY(1) scaleX(1);
        opacity: 1;
      }}
    }}

    /* 2. Horizon Flare Beam Pulse & Disperse */
    @keyframes horizonLaser {{
      0% {{
        transform: scaleX(0);
        opacity: 0;
      }}
      25% {{
        transform: scaleX(1);
        opacity: 1;
      }}
      60% {{
        transform: scaleX(1.05);
        opacity: 0.8;
      }}
      100% {{
        transform: scaleX(1.1);
        opacity: 0;
      }}
    }}

    /* 3. Star Flare Ignite Pulse */
    @keyframes starFlare {{
      0% {{
        transform: scale(0);
        opacity: 0;
      }}
      25% {{
        transform: scale(1.4);
        opacity: 1;
      }}
      60% {{
        transform: scale(0.8);
        opacity: 0.4;
      }}
      100% {{
        transform: scale(0);
        opacity: 0;
      }}
    }}

    /* 4. Text Line Cinematic Rise */
    @keyframes textCinematicRise {{
      0% {{
        opacity: 0;
        transform: translateY(30px) scale(0.96);
      }}
      100% {{
        opacity: 1;
        transform: translateY(0) scale(1);
      }}
    }}

    /* 5. Portrait Cinematic Drift In */
    @keyframes photoCinematicDrift {{
      0% {{
        opacity: 0;
        transform: translateX(40px) scale(0.95);
      }}
      100% {{
        opacity: 1;
        transform: translateX(0) scale(1);
      }}
    }}

    /* 6. Looping Ethereal Light Sheen */
    @keyframes etherealSheenLoop {{
      0%, 25% {{
        transform: translateX(-450px) skewX(-22deg);
        opacity: 0;
      }}
      38% {{
        opacity: 0.9;
      }}
      68% {{
        transform: translateX(1150px) skewX(-22deg);
        opacity: 0.7;
      }}
      78%, 100% {{
        transform: translateX(1150px) skewX(-22deg);
        opacity: 0;
      }}
    }}

    @keyframes cursorBlink {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0; }}
    }}

    .shutter-rect {{
      transform-origin: center center;
      animation: horizonUnfold 1.35s cubic-bezier(0.16, 1, 0.3, 1) both;
    }}

    .laser-beam {{
      transform-origin: center center;
      animation: horizonLaser 1.1s cubic-bezier(0.16, 1, 0.3, 1) both;
    }}

    .star-flare {{
      transform-origin: center center;
      animation: starFlare 0.9s cubic-bezier(0.16, 1, 0.3, 1) both;
    }}

    .font-code {{
      font-family: 'Menlo', 'Fira Code', 'JetBrains Mono', 'SF Mono', Consolas, monospace;
      font-size: 34px;
      font-weight: 700;
      fill: #f0f6fc;
      letter-spacing: -0.3px;
    }}

    .line-1 {{
      animation: textCinematicRise 0.95s cubic-bezier(0.16, 1, 0.3, 1) 0.35s both;
    }}
    .line-2 {{
      animation: textCinematicRise 0.95s cubic-bezier(0.16, 1, 0.3, 1) 0.5s both;
    }}
    .line-3 {{
      animation: textCinematicRise 0.95s cubic-bezier(0.16, 1, 0.3, 1) 0.65s both;
    }}

    .photo-reveal {{
      animation: photoCinematicDrift 1.1s cubic-bezier(0.16, 1, 0.3, 1) 0.4s both;
    }}

    .sheen-beam {{
      animation: etherealSheenLoop 5.5s ease-in-out infinite 1.8s;
    }}

    .blink-cursor {{
      fill: #58a6ff;
      animation: cursorBlink 0.9s infinite;
    }}
  </style>

  <!-- Card Body with Horizon Unfold Reveal -->
  <g clip-path="url(#horizonShutterClip)">
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

    <!-- Large Photo with Smooth Cinematic Drift from Right -->
    <g class="photo-reveal">
      <image xlink:href="data:image/png;base64,{photo_b64}" href="data:image/png;base64,{photo_b64}" x="625" y="10" width="360" height="330" preserveAspectRatio="xMidYMid meet" />
    </g>

    <!-- Looping Silky Light Sheen Beam Overlay -->
    <rect class="sheen-beam" x="0" y="0" width="280" height="340" fill="url(#sheenGrad)" pointer-events="none" />
  </g>

  <!-- Opening Horizon Laser Beam Effect -->
  <g class="laser-beam" pointer-events="none">
    <rect x="0" y="167" width="1000" height="6" fill="url(#horizonBeam)" />
    <rect x="0" y="168" width="1000" height="3" fill="#ffffff" opacity="0.9" />
  </g>

  <!-- Opening Central Star Flare Pulse -->
  <g class="star-flare" transform="translate(500, 170)" pointer-events="none">
    <circle cx="0" cy="0" r="90" fill="url(#centerIgniteGlow)" />
    <ellipse cx="0" cy="0" rx="180" ry="4" fill="#ffffff" opacity="0.8" />
    <ellipse cx="0" cy="0" rx="4" ry="70" fill="#58a6ff" opacity="0.7" />
  </g>

  <!-- Outer Static Border to keep card boundary crisp -->
  <rect x="1" y="1" width="998" height="338" rx="16" fill="none" stroke="url(#borderGrad)" stroke-width="1.8" />

</svg>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated {output_path} successfully ({len(svg)} bytes)")


if __name__ == "__main__":
    generate_banner_png()
    generate_banner_gif()
    generate_banner_svg()
