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

def create_rich_dark_base(w, h, photo_path="photo_nobg_dark.png", scale=1.0):
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


def generate_banner_png(output_path="header_banner.png", photo_path="photo_nobg_dark.png"):
    w, h = 2000, 680
    banner = create_rich_dark_base(w, h, photo_path, scale=2.0)
    banner.save(output_path, 'PNG', optimize=True)
    print(f"Generated {output_path} successfully ({w}x{h})")


def generate_banner_gif(output_path="header_banner.gif", photo_path="photo_nobg_dark.png"):
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


if __name__ == "__main__":
    generate_banner_png()
    generate_banner_gif()
