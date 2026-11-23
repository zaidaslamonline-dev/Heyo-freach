# Blender first-scene prototype

This is a **Roblox-inspired 3D recreation**, not footage from Roblox Studio.

## What it renders
A 4-second vertical establishing scene for the supplied Hindi story: the bright gods' world, the red slave world, the dividing wall, Peter and Leo with golden wings, and Rose with a mechanical arm.

## Run locally
Install Blender 4.x and FFmpeg, then:
```bash
OUTPUT_DIR=render blender -b -t 4 --python scripts/blender/first_scene.py
ffmpeg -y -framerate 12 -i render/frame_%04d.png -c:v libx264 -pix_fmt yuv420p -crf 20 render/first_scene.mp4
```

The GitHub Actions workflow renders the same script and uploads the MP4, PNG frames, and .blend project as an artifact. This is a style/technical approval checkpoint, not the complete story video.
