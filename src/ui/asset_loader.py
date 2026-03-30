# src/ui/asset_loader.py

import base64
import os

ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")

def load_assets():
    """
    Loads all PNG assets from the assets directory and converts them to 
    Base64 strings for embedding in HTML/JS.
    """
    assets = {}
    
    # List of expected assets
    files = [
        "floor.png",
        "desk.png",
        "chair.png",
        "agent_idle.png",
        "agent_walk.png",
        "clerk.png"
    ]
    
    for filename in files:
        path = os.path.join(ASSET_DIR, filename)
        if os.path.exists(path):
            with open(path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
                # Remove .png extension for key
                key = filename.replace(".png", "")
                assets[key] = f"data:image/png;base64,{encoded_string}"
        else:
            print(f"Warning: Asset {filename} not found.")
            
    return assets
