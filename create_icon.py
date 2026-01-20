#!/usr/bin/env python3
"""
Create Windows ICO icon for Sinistra Keys
kidD Icarus / kidDicarus Inc.

Creates a proper multi-size ICO file without external SVG dependencies.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Create icon.ico with k.I. branding"""
    
    # Colors
    BG_DARK = (10, 10, 10)
    CRIMSON = (139, 0, 0)
    CRIMSON_LIGHT = (178, 34, 34)
    GOLD = (218, 165, 32)
    GOLD_LIGHT = (255, 215, 0)
    
    # Create base image at 256x256
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Background circle with gradient effect
    # Outer glow
    draw.ellipse([4, 4, size-4, size-4], fill=CRIMSON_LIGHT)
    # Main circle
    draw.ellipse([8, 8, size-8, size-8], fill=BG_DARK)
    # Inner border
    draw.ellipse([12, 12, size-12, size-12], outline=CRIMSON, width=3)
    
    # Draw "k.I." text
    try:
        # Try to use Arial Black or Arial Bold
        for font_name in ['arialbd.ttf', 'ariblk.ttf', 'arial.ttf', 'calibrib.ttf']:
            try:
                font_large = ImageFont.truetype(font_name, 90)
                break
            except:
                continue
        else:
            font_large = ImageFont.load_default()
    except:
        font_large = ImageFont.load_default()
    
    # Draw gold "k.I." text centered
    text = "k.I."
    bbox = draw.textbbox((0, 0), text, font=font_large)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - 10
    
    # Text shadow
    draw.text((x+2, y+2), text, fill=(50, 50, 50), font=font_large)
    # Main text
    draw.text((x, y), text, fill=GOLD_LIGHT, font=font_large)
    
    # Draw small RTL arrow at bottom
    arrow_y = size - 50
    arrow_points = [
        (size//2 - 40, arrow_y),      # Arrow tip
        (size//2 - 20, arrow_y - 15),  # Top
        (size//2 - 20, arrow_y - 5),   # Top inner
        (size//2 + 40, arrow_y - 5),   # Right top
        (size//2 + 40, arrow_y + 5),   # Right bottom
        (size//2 - 20, arrow_y + 5),   # Bottom inner
        (size//2 - 20, arrow_y + 15),  # Bottom
    ]
    draw.polygon(arrow_points, fill=CRIMSON_LIGHT)
    
    # Create multiple sizes for ICO
    sizes = [16, 24, 32, 48, 64, 128, 256]
    images = []
    
    for s in sizes:
        resized = img.resize((s, s), Image.Resampling.LANCZOS)
        images.append(resized)
    
    # Save as ICO
    ico_path = 'icon.ico'
    images[0].save(
        ico_path, 
        format='ICO',
        sizes=[(s, s) for s in sizes],
        append_images=images[1:]
    )
    
    print(f"Created {ico_path} ({os.path.getsize(ico_path)} bytes)")
    print(f"Sizes: {sizes}")
    return True


if __name__ == '__main__':
    try:
        create_icon()
        print("SUCCESS!")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
