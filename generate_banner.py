import os
import math
from PIL import Image, ImageDraw, ImageFont

def generate_banner_png(output_path="header_banner.png", avatar_path="github.png"):
    # 2x Retina resolution: 2000 x 680 (displays crisp at 1000 x 340)
    w, h = 2000, 680
    banner = Image.new('RGBA', (w, h), (252, 244, 250, 255))
    draw = ImageDraw.Draw(banner)

    # Big modern bold font
    font_big = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 86)

    lines = [
        "Creativity and technology",
        "to craft user-centric",
        "solutions"
    ]

    line_height = 112
    total_text_h = (len(lines) - 1) * line_height + 86
    start_y = (h - total_text_h) // 2
    text_x = 130

    for i, line in enumerate(lines):
        y = start_y + i * line_height
        draw.text((text_x, y), line, fill=(28, 24, 44, 255), font=font_big)

    # Right side: PNG portrait without any border lines
    av_size = 520
    if os.path.exists(avatar_path):
        avatar = Image.open(avatar_path).convert('RGBA')
        avatar = avatar.resize((av_size, av_size), Image.LANCZOS)

        radius = 32
        mask = Image.new('L', (av_size, av_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle((0, 0, av_size, av_size), radius=radius, fill=255)

        av_x = w - av_size - 100
        av_y = (h - av_size) // 2

        banner.paste(avatar, (av_x, av_y), mask)

    banner.save(output_path, 'PNG', optimize=True)
    print(f"Generated {output_path} successfully ({w}x{h})")


def generate_banner_gif(output_path="header_banner.gif", avatar_path="github.png"):
    w, h = 1000, 340
    base = Image.new('RGBA', (w, h), (252, 244, 250, 255))
    draw_base = ImageDraw.Draw(base)

    font_big = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 43)

    lines = [
        "Creativity and technology",
        "to craft user-centric",
        "solutions"
    ]

    line_height = 56
    total_text_h = (len(lines) - 1) * line_height + 43
    start_y = (h - total_text_h) // 2
    text_x = 65

    for i, line in enumerate(lines):
        y = start_y + i * line_height
        draw_base.text((text_x, y), line, fill=(28, 24, 44, 255), font=font_big)

    # Right side: PNG portrait without any border lines
    av_size = 260
    if os.path.exists(avatar_path):
        avatar = Image.open(avatar_path).convert('RGBA')
        avatar = avatar.resize((av_size, av_size), Image.LANCZOS)

        radius = 16
        mask = Image.new('L', (av_size, av_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle((0, 0, av_size, av_size), radius=radius, fill=255)

        av_x = w - av_size - 50
        av_y = (h - av_size) // 2

        base.paste(avatar, (av_x, av_y), mask)

    # Swipe animation:
    # 52 frames swipe (~3.1s) + 24 frames calm pause (~1.4s) = 76 frames total at 60ms (~4.5s loop)
    swipe_frames = 52
    pause_frames = 24
    total_frames = swipe_frames + pause_frames

    beam_width = 240
    tilt = 0.38  # angle tilt

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
                alpha_wide = 55 * math.exp(-3.0 * (dist ** 2))
                alpha_core = 65 * math.exp(-12.0 * (dist ** 2))
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
