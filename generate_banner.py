import os
import math
from PIL import Image, ImageDraw, ImageFont

def generate_banner_png(output_path="header_banner.png", avatar_path="github.png"):
    # 2x Retina resolution: 2000 x 680 (displays crisp at 1000 x 340)
    w, h = 2000, 680
    banner = Image.new('RGBA', (w, h), (252, 244, 250, 255))
    draw = ImageDraw.Draw(banner)

    # Fonts
    font_name = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 98)
    font_sub = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 48)
    font_watermark = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 380)

    # Faint decorative watermark 'SAM' in background
    draw.text((160, 116), 'SAM', fill=(240, 222, 238, 255), font=font_watermark)

    # Text placement
    text_x = 120
    name_y = 185
    draw.text((text_x, name_y), 'SAM JERISH D', fill=(30, 25, 48, 255), font=font_name)

    sub1_y = name_y + 145
    draw.text((text_x, sub1_y), 'AI & machine learning student, full-stack developer &', fill=(108, 98, 126, 255), font=font_sub)

    sub2_y = sub1_y + 70
    draw.text((text_x, sub2_y), 'robotics & computer vision enthusiast', fill=(108, 98, 126, 255), font=font_sub)

    # Right side: PNG portrait card (2x)
    av_size = 480
    if os.path.exists(avatar_path):
        avatar = Image.open(avatar_path).convert('RGBA')
        avatar = avatar.resize((av_size, av_size), Image.LANCZOS)

        radius = 32
        mask = Image.new('L', (av_size, av_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle((0, 0, av_size, av_size), radius=radius, fill=255)

        pad = 12
        card_w = av_size + 2 * pad
        card_h = av_size + 2 * pad
        av_x = w - card_w - 90
        av_y = (h - card_h) // 2

        # Subtle outer shadow and clean white card frame
        draw.rounded_rectangle((av_x - 6, av_y - 2, av_x + card_w + 6, av_y + card_h + 10), radius=radius + pad, fill=(232, 218, 230, 255))
        draw.rounded_rectangle((av_x, av_y, av_x + card_w, av_y + card_h), radius=radius + pad, fill=(255, 255, 255, 255))

        banner.paste(avatar, (av_x + pad, av_y + pad), mask)

    banner.save(output_path, 'PNG', optimize=True)
    print(f"Generated {output_path} successfully ({w}x{h})")


def generate_banner_gif(output_path="header_banner.gif", avatar_path="github.png"):
    w, h = 1000, 340
    base = Image.new('RGBA', (w, h), (252, 244, 250, 255))
    draw_base = ImageDraw.Draw(base)

    font_name = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 48)
    font_sub = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 24)
    font_watermark = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 190)

    # Faint watermark 'SAM' in background
    draw_base.text((80, 58), 'SAM', fill=(240, 222, 238, 255), font=font_watermark)

    # Text placement
    text_x = 60
    name_y = 92
    draw_base.text((text_x, name_y), 'SAM JERISH D', fill=(30, 25, 48, 255), font=font_name)

    sub1_y = name_y + 72
    draw_base.text((text_x, sub1_y), 'AI & machine learning student, full-stack developer &', fill=(108, 98, 126, 255), font=font_sub)

    sub2_y = sub1_y + 35
    draw_base.text((text_x, sub2_y), 'robotics & computer vision enthusiast', fill=(108, 98, 126, 255), font=font_sub)

    # Right side: PNG portrait card
    av_size = 240
    if os.path.exists(avatar_path):
        avatar = Image.open(avatar_path).convert('RGBA')
        avatar = avatar.resize((av_size, av_size), Image.LANCZOS)

        radius = 16
        mask = Image.new('L', (av_size, av_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle((0, 0, av_size, av_size), radius=radius, fill=255)

        pad = 6
        card_w = av_size + 2 * pad
        card_h = av_size + 2 * pad
        av_x = w - card_w - 45
        av_y = (h - card_h) // 2

        # Outer soft shadow & white frame
        draw_base.rounded_rectangle((av_x - 3, av_y - 1, av_x + card_w + 3, av_y + card_h + 5), radius=radius + pad, fill=(232, 218, 230, 255))
        draw_base.rounded_rectangle((av_x, av_y, av_x + card_w, av_y + card_h), radius=radius + pad, fill=(255, 255, 255, 255))
        base.paste(avatar, (av_x + pad, av_y + pad), mask)

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
