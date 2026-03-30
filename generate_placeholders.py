# generate_placeholders.py
from PIL import Image, ImageDraw, ImageColor
import os
import math

ASSET_DIR = "src/ui/assets"
os.makedirs(ASSET_DIR, exist_ok=True)

def draw_isometric_cube(draw, x, y, width, height, depth, color_top, color_left, color_right):
    """
    Draws a pseudo-3D cube centered roughly at x, y.
    simple projection: 
    - Top face is a rhombus.
    - Front faces are rectangles/parallelograms.
    """
    # Half dimensions
    w = width / 2
    h = height # Z-height
    d = depth / 2
    
    # Top Face (Diamond)
    top_points = [
        (x, y - d),          # Top
        (x + w, y),          # Right
        (x, y + d),          # Bottom
        (x - w, y)           # Left
    ]
    draw.polygon(top_points, fill=color_top)
    
    # Right Face
    right_points = [
        (x + w, y),          # Top-Left (of face)
        (x + w, y + h),      # Bottom-Left
        (x, y + d + h),      # Bottom-Right
        (x, y + d)           # Top-Right
    ]
    draw.polygon(right_points, fill=color_right)
    
    # Left Face
    left_points = [
        (x - w, y),          # Top-Right
        (x, y + d),          # Top-Left
        (x, y + d + h),      # Bottom-Left
        (x - w, y + h)       # Bottom-Right
    ]
    draw.polygon(left_points, fill=color_left)

def create_3d_pawn(filename, color_hex, size=(64, 64)):
    """Draws a 3D-looking pawn/meeple."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    base_color = ImageColor.getrgb(color_hex)
    dark_color = tuple(max(0, c - 40) for c in base_color)
    light_color = tuple(min(255, c + 40) for c in base_color)
    
    cx, cy = size[0] // 2, size[1] // 2 + 10
    radius = 12
    height = 25
    
    # Body (Cylinder-ish)
    # Side
    draw.rectangle((cx - radius, cy - height, cx + radius, cy), fill=dark_color)
    # Bottom Ellipse
    draw.ellipse((cx - radius, cy - 6, cx + radius, cy + 6), fill=dark_color)
    # Top Ellipse (Face)
    draw.ellipse((cx - radius, cy - height - 6, cx + radius, cy - height + 6), fill=light_color, outline=dark_color, width=1)
    
    # Head (Sphere-ish)
    head_r = 10
    head_y = cy - height - 8
    draw.ellipse((cx - head_r, head_y - head_r, cx + head_r, head_y + head_r), fill="#f1c40f", outline="#f39c12")
    
    img.save(f"{ASSET_DIR}/{filename}")

def create_3d_desk(filename, size=(128, 80)):
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    cx, cy = size[0] // 2, size[1] // 2
    
    # Desk body
    draw_isometric_cube(draw, cx, cy, width=80, height=30, depth=30, 
                        color_top="#3498db", color_left="#2980b9", color_right="#1abc9c")
    
    img.save(f"{ASSET_DIR}/{filename}")

def create_3d_chair(filename, size=(64, 64)):
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    cx, cy = size[0] // 2, size[1] // 2
    
    # Seat
    draw_isometric_cube(draw, cx, cy, width=30, height=5, depth=30, 
                        color_top="#e67e22", color_left="#d35400", color_right="#cf6d17")
    # Backrest
    draw_isometric_cube(draw, cx - 10, cy - 15, width=5, height=25, depth=30, 
                        color_top="#e67e22", color_left="#d35400", color_right="#cf6d17")
    
    img.save(f"{ASSET_DIR}/{filename}")

def create_isometric_floor(filename, size=(64, 64)):
    img = Image.new("RGBA", size, (0,0,0,0))
    draw = ImageDraw.Draw(img)
    
    # Draw a rotated square (rhombus)
    # Top point
    p1 = (size[0]//2, 0)
    # Right
    p2 = (size[0], size[1]//2)
    # Bottom
    p3 = (size[0]//2, size[1])
    # Left
    p4 = (0, size[1]//2)
    
    draw.polygon([p1, p2, p3, p4], fill="#ecf0f1", outline="#bdc3c7")
    
    img.save(f"{ASSET_DIR}/{filename}")

# Generate 3D Assets
create_isometric_floor("floor.png")
create_3d_desk("desk.png")
create_3d_chair("chair.png")
create_3d_pawn("agent_idle.png", "#e74c3c")
create_3d_pawn("agent_walk.png", "#2ecc71")
create_3d_pawn("clerk.png", "#2c3e50")

print("3D Isometric assets generated.")
