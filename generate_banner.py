import os
from PIL import Image, ImageDraw, ImageFont

def generate_banner(output_path="header_banner.png", avatar_path="profile.png"):
    # 2x Retina resolution: 2000 x 680 (displays crisp at 1000 x 340)
    w, h = 2000, 680
    banner = Image.new('RGBA', (w, h), (252, 244, 250, 255))
    draw = ImageDraw.Draw(banner)

    # Fonts
    font_name = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 98)
    font_sub = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 48)
    font_watermark = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 380)

    # Faint decorative watermark 'S' in background
    draw.text((340, 130), 'S', fill=(244, 230, 242, 255), font=font_watermark)

    # Text placement
    text_x = 110
    name_y = 185
    draw.text((text_x, name_y), 'SAM JERISH D', fill=(30, 25, 48, 255), font=font_name)

    sub1_y = name_y + 145
    draw.text((text_x, sub1_y), 'AI & machine learning student, full-stack developer &', fill=(108, 98, 126, 255), font=font_sub)

    sub2_y = sub1_y + 70
    draw.text((text_x, sub2_y), 'robotics & computer vision enthusiast', fill=(108, 98, 126, 255), font=font_sub)

    # Right side: Circular portrait (2x)
    av_size = 500
    if os.path.exists(avatar_path):
        avatar = Image.open(avatar_path).convert('RGBA')
        avatar = avatar.resize((av_size, av_size), Image.LANCZOS)

        mask = Image.new('L', (av_size, av_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, av_size, av_size), fill=255)

        ring_size = av_size + 24
        av_x = w - ring_size - 110
        av_y = (h - ring_size) // 2

        # Subtle outer shadow and clean white ring
        draw.ellipse((av_x - 6, av_y - 2, av_x + ring_size + 6, av_y + ring_size + 10), fill=(232, 218, 230, 255))
        draw.ellipse((av_x, av_y, av_x + ring_size, av_y + ring_size), fill=(255, 255, 255, 255))

        banner.paste(avatar, (av_x + 12, av_y + 12), mask)

    banner.save(output_path, 'PNG', optimize=True)
    print(f"Generated {output_path} successfully ({w}x{h})")

if __name__ == "__main__":
    generate_banner()
