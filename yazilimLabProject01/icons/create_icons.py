"""
İkon oluşturma scripti
Pillow kütüphanesi kullanarak buton ikonları oluşturur
"""
try:
    from PIL import Image, ImageDraw
except ImportError as e:
    raise

import os

def create_play_icon(size=20):
    """Yeşil play ikonu oluşturur"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    points = [
        (size * 0.2, size * 0.2),
        (size * 0.2, size * 0.8),
        (size * 0.8, size * 0.5)
    ]
    
    draw.polygon(points, fill=(34, 197, 94, 255))
    return img

def create_stop_icon(size=20):
    """Kırmızı stop ikonu oluşturur"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    margin = size * 0.15
    box = [margin, margin, size - margin, size - margin]
    draw.rectangle(box, fill=(239, 68, 68, 255))
    return img

def create_reset_icon(size=20):
    """Sarı reset ikonu oluşturur"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    margin = size * 0.15
    box = [margin, margin, size - margin, size - margin]
    draw.ellipse(box, fill=(245, 158, 11, 255))
    return img

def create_speed_icon(size=20):
    """Mavi speed ikonu oluşturur"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    points1 = [
        (size * 0.6, size * 0.1),
        (size * 0.3, size * 0.4),
        (size * 0.5, size * 0.4),
        (size * 0.2, size * 0.7),
        (size * 0.8, size * 0.7),
        (size * 0.4, size * 0.9),
        (size * 0.7, size * 0.6),
        (size * 0.5, size * 0.6),
        (size * 0.8, size * 0.3)
    ]
    
    draw.polygon(points1, fill=(59, 130, 246, 255))
    return img

def create_theme_icon(size=20):
    """Tema ikonu oluşturur"""
    import math
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    sun_center = (size * 0.7, size * 0.3)
    sun_radius = size * 0.25
    sun_box = [
        sun_center[0] - sun_radius,
        sun_center[1] - sun_radius,
        sun_center[0] + sun_radius,
        sun_center[1] + sun_radius
    ]
    draw.ellipse(sun_box, fill=(255, 193, 7, 255))
    
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        x1 = sun_center[0] + math.cos(rad) * (sun_radius + 2)
        y1 = sun_center[1] + math.sin(rad) * (sun_radius + 2)
        x2 = sun_center[0] + math.cos(rad) * (sun_radius + 6)
        y2 = sun_center[1] + math.sin(rad) * (sun_radius + 6)
        draw.line([(x1, y1), (x2, y2)], fill=(255, 193, 7, 255), width=1)
    
    moon_center = (size * 0.3, size * 0.7)
    moon_radius = size * 0.25
    moon_box = [
        moon_center[0] - moon_radius,
        moon_center[1] - moon_radius,
        moon_center[0] + moon_radius,
        moon_center[1] + moon_radius
    ]
    draw.ellipse(moon_box, fill=(156, 163, 175, 255))
    
    inner_moon_center = (moon_center[0] + 3, moon_center[1] - 3)
    inner_moon_radius = moon_radius * 0.7
    inner_moon_box = [
        inner_moon_center[0] - inner_moon_radius,
        inner_moon_center[1] - inner_moon_radius,
        inner_moon_center[0] + inner_moon_radius,
        inner_moon_center[1] + inner_moon_radius
    ]
    draw.ellipse(inner_moon_box, fill=(0, 0, 0, 0))
    return img

def main():
    """Tüm ikonları oluşturur ve kaydeder"""
    icons_dir = "icons"
    
    if not os.path.exists(icons_dir):
        os.makedirs(icons_dir)
    
    icons = {
        'play.png': create_play_icon(),
        'stop.png': create_stop_icon(),
        'reset.png': create_reset_icon(),
        'speed.png': create_speed_icon(),
        'theme.png': create_theme_icon()
    }
    
    for filename, icon in icons.items():
        filepath = os.path.join(icons_dir, filename)
        icon.save(filepath, 'PNG')
        print(f"Oluşturuldu: {filepath}")

if __name__ == "__main__":
    main()