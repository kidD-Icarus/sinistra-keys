#!/usr/bin/env python3
"""
Convert SVG icon to Windows ICO format
by kidD Icarus / kidDicarus Inc.
"""

import os
import sys

def convert_svg_to_ico():
    """Convert icon.svg to icon.ico using multiple fallback methods"""
    
    svg_path = "icon.svg"
    ico_path = "icon.ico"
    png_path = "icon.png"
    
    if not os.path.exists(svg_path):
        print(f"ERROR: {svg_path} not found!")
        return False
    
    # Method 1: Try cairosvg + Pillow
    try:
        import cairosvg
        from PIL import Image
        import io
        
        print("Using cairosvg + Pillow...")
        
        # Convert SVG to PNG at multiple sizes
        sizes = [16, 32, 48, 64, 128, 256]
        images = []
        
        for size in sizes:
            png_data = cairosvg.svg2png(url=svg_path, output_width=size, output_height=size)
            img = Image.open(io.BytesIO(png_data))
            img = img.convert('RGBA')
            images.append(img)
        
        # Save as ICO with multiple sizes
        images[0].save(ico_path, format='ICO', sizes=[(s, s) for s in sizes], append_images=images[1:])
        print(f"SUCCESS: Created {ico_path}")
        return True
        
    except ImportError:
        print("cairosvg not available, trying alternative...")
    except Exception as e:
        print(f"cairosvg method failed: {e}")
    
    # Method 2: Try Pillow with existing PNG
    try:
        from PIL import Image
        
        if os.path.exists(png_path):
            print(f"Using existing {png_path}...")
            img = Image.open(png_path)
        else:
            # Create a simple fallback icon
            print("Creating fallback icon...")
            img = Image.new('RGBA', (256, 256), (10, 10, 10, 255))
            
            # Draw a simple k.I. text placeholder
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(img)
            
            # Draw crimson circle
            draw.ellipse([10, 10, 246, 246], fill=(139, 0, 0, 255), outline=(178, 34, 34, 255), width=4)
            
            # Draw text
            try:
                font = ImageFont.truetype("arial.ttf", 80)
            except:
                font = ImageFont.load_default()
            
            draw.text((128, 128), "k.I.", fill=(218, 165, 32, 255), font=font, anchor="mm")
        
        # Convert to ICO
        img = img.convert('RGBA')
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        
        images = []
        for size in sizes:
            resized = img.resize(size, Image.Resampling.LANCZOS)
            images.append(resized)
        
        images[0].save(ico_path, format='ICO', sizes=sizes, append_images=images[1:])
        print(f"SUCCESS: Created {ico_path}")
        return True
        
    except ImportError:
        print("ERROR: Pillow not installed. Run: pip install pillow")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False


if __name__ == '__main__':
    success = convert_svg_to_ico()
    sys.exit(0 if success else 1)
