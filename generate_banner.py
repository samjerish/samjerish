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

def create_rich_base(w, h, photo_path="photo_nobg_clean.png", scale=1.0):
    base = Image.new('RGBA', (w, h), (250, 245, 252, 255))

    # 1. Atmospheric ambient glow
    ambient = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    amb_draw = ImageDraw.Draw(ambient)
    amb_draw.ellipse((int(w * 0.45), -int(h * 0.3), int(w * 1.15), int(h * 1.3)), fill=(225, 215, 255, 175))
    amb_draw.ellipse((-int(w * 0.1), -int(h * 0.3), int(w * 0.45), int(h * 0.9)), fill=(255, 230, 242, 140))
    ambient = ambient.filter(ImageFilter.GaussianBlur(int(45 * scale)))
    base = Image.alpha_composite(base, ambient)
    draw = ImageDraw.Draw(base)

    # 2. Headline in coding font
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
        draw.text((text_x, y), line, fill=(28, 22, 45, 255), font=font_code)

    # 3. Big photo with background removed on the right
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
            (px + int(30 * scale), py + photo_h - int(50 * scale), px + photo_w - int(30 * scale), py + photo_h + int(15 * scale)),
            fill=(135, 115, 175, 100)
        )
        shadow = shadow.filter(ImageFilter.GaussianBlur(int(16 * scale)))
        base = Image.alpha_composite(base, shadow)

        base.paste(photo, (px, py), photo)

    return base


def generate_banner_png(output_path="header_banner.png", photo_path="photo_nobg_clean.png"):
    w, h = 2000, 680
    banner = create_rich_base(w, h, photo_path, scale=2.0)
    banner.save(output_path, 'PNG', optimize=True)
    print(f"Generated {output_path} successfully ({w}x{h})")


def generate_banner_gif(output_path="header_banner.gif", photo_path="photo_nobg_clean.png"):
    w, h = 1000, 340
    base = create_rich_base(w, h, photo_path, scale=1.0)

    # Sheen sweep animation:
    swipe_frames = 52
    pause_frames = 24
    total_frames = swipe_frames + pause_frames

    beam_width = 240
    tilt = 0.38

    frames = []
    for i in range(total_frames):
        frame = base.copy()
        if i < swipe_frames:
            progress = i / float(swipe_frames - 1)
            center_x = -260 + progress * 1520

            sheen = Image.new('RGBA', (w, h), (0, 0, 0, 0))
            sheen_draw = ImageDraw.Draw(sheen)

            steps = 35
            for s in range(-steps, steps + 1):
                t = s / float(steps)
                offset = t * (beam_width / 2.0)
                dist = abs(t)
                alpha_wide = 45 * math.exp(-3.0 * (dist ** 2))
                alpha_core = 55 * math.exp(-12.0 * (dist ** 2))
                alpha = int(min(255, alpha_wide + alpha_core))

                if alpha > 0:
                    x_top = center_x + offset + (h * tilt) / 2.0
                    x_bot = center_x + offset - (h * tilt) / 2.0
                    sheen_draw.line([(x_top, 0), (x_bot, h)], fill=(255, 255, 255, alpha), width=4)

            frame = Image.alpha_composite(frame, sheen)

        frames.append(frame.convert('RGB'))

    palette_img = base.convert('RGB').quantize(colors=256)
    quantized_frames = [f.quantize(palette=palette_img) for f in frames]

    quantized_frames[0].save(output_path, save_all=True, append_images=quantized_frames[1:], duration=60, loop=0, optimize=True)
    print(f"Generated {output_path} successfully ({w}x{h}, {len(quantized_frames)} frames)")


if __name__ == "__main__":
    generate_banner_png()
    generate_banner_gif()
