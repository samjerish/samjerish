import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_rich_base(w, h, avatar_path="github.png", scale=1.0):
    base = Image.new('RGBA', (w, h), (250, 245, 252, 255))

    # 1. Ambient atmospheric glow
    ambient = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    amb_draw = ImageDraw.Draw(ambient)
    # Right-side glow behind avatar
    amb_draw.ellipse((int(w * 0.58), -int(h * 0.2), int(w * 1.1), int(h * 1.2)), fill=(215, 205, 250, 160))
    # Top-left gentle coral/peach aura
    amb_draw.ellipse((-int(w * 0.1), -int(h * 0.3), int(w * 0.45), int(h * 0.9)), fill=(255, 225, 235, 140))
    # Soft blur
    ambient = ambient.filter(ImageFilter.GaussianBlur(int(45 * scale)))
    base = Image.alpha_composite(base, ambient)
    draw = ImageDraw.Draw(base)

    # 2. Subtle modern tech dot grid
    step = int(24 * scale)
    dot_r = max(1, int(1.5 * scale))
    grid_end_x = int(w * 0.62)
    for gx in range(int(60 * scale), grid_end_x, step):
        for gy in range(int(35 * scale), int(h - 35 * scale), step):
            draw.ellipse((gx, gy, gx + dot_r * 2, gy + dot_r * 2), fill=(222, 208, 235, 110))

    # 3. Floating Pill Badge
    pill_x = int(65 * scale)
    pill_y = int(42 * scale)
    pill_h = int(28 * scale)
    pill_w = int(260 * scale)
    draw.rounded_rectangle(
        (pill_x, pill_y, pill_x + pill_w, pill_y + pill_h),
        radius=int(14 * scale),
        fill=(255, 255, 255, 230),
        outline=(225, 210, 235, 255),
        width=max(1, int(1 * scale))
    )
    # Live status green dot
    dot_cx = pill_x + int(14 * scale)
    dot_cy = pill_y + int(14 * scale)
    dr = int(4 * scale)
    draw.ellipse((dot_cx - dr, dot_cy - dr, dot_cx + dr, dot_cy + dr), fill=(39, 201, 63, 255))

    font_badge = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', int(12 * scale))
    draw.text((pill_x + int(24 * scale), pill_y + int(6 * scale)), 'CREATIVE DEV & AI BUILDER', fill=(110, 80, 160, 255), font=font_badge)

    # 4. Big striking headline text
    font_headline = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', int(38 * scale))
    lines = [
        "Creativity and technology",
        "to craft user-centric",
        "solutions"
    ]
    start_y = int(88 * scale)
    line_h = int(48 * scale)
    text_x = int(65 * scale)

    for i, line in enumerate(lines):
        y = start_y + i * line_h
        draw.text((text_x, y), line, fill=(28, 22, 46, 255), font=font_headline)

    # 5. Interactive-style tech stack pills
    tags = ["AI / ML", "Computer Vision", "Robotics", "Full-Stack"]
    tag_font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', int(11 * scale))
    tag_x = text_x
    tag_y = start_y + len(lines) * line_h + int(14 * scale)
    for tag in tags:
        bbox = draw.textbbox((0, 0), tag, font=tag_font)
        tw = bbox[2] - bbox[0]
        pw = tw + int(18 * scale)
        ph = int(22 * scale)
        draw.rounded_rectangle((tag_x, tag_y, tag_x + pw, tag_y + ph), radius=int(6 * scale), fill=(240, 232, 246, 220), outline=(220, 205, 232, 200), width=1)
        draw.text((tag_x + int(9 * scale), tag_y + int(4 * scale)), tag, fill=(100, 80, 130, 255), font=tag_font)
        tag_x += pw + int(10 * scale)

    # 6. Right side: Clean photo without border lines
    av_size = int(260 * scale)
    if os.path.exists(avatar_path):
        avatar = Image.open(avatar_path).convert('RGBA')
        avatar = avatar.resize((av_size, av_size), Image.LANCZOS)

        av_x = w - av_size - int(50 * scale)
        av_y = (h - av_size) // 2

        # Soft atmospheric shadow behind avatar
        shadow = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        s_draw = ImageDraw.Draw(shadow)
        s_draw.rounded_rectangle(
            (av_x + int(4 * scale), av_y + int(8 * scale), av_x + av_size - int(4 * scale), av_y + av_size + int(8 * scale)),
            radius=int(18 * scale),
            fill=(150, 130, 180, 95)
        )
        shadow = shadow.filter(ImageFilter.GaussianBlur(int(14 * scale)))
        base = Image.alpha_composite(base, shadow)

        # Smooth rounded mask, NO border lines
        mask = Image.new('L', (av_size, av_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle((0, 0, av_size, av_size), radius=int(16 * scale), fill=255)

        base.paste(avatar, (av_x, av_y), mask)

    return base


def generate_banner_png(output_path="header_banner.png", avatar_path="github.png"):
    w, h = 2000, 680
    banner = create_rich_base(w, h, avatar_path, scale=2.0)
    banner.save(output_path, 'PNG', optimize=True)
    print(f"Generated {output_path} successfully ({w}x{h})")


def generate_banner_gif(output_path="header_banner.gif", avatar_path="github.png"):
    w, h = 1000, 340
    base = create_rich_base(w, h, avatar_path, scale=1.0)

    # Swipe animation:
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
                alpha_wide = 50 * math.exp(-3.0 * (dist ** 2))
                alpha_core = 60 * math.exp(-12.0 * (dist ** 2))
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
