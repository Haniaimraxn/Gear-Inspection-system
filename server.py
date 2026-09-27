import os
import cv2
import numpy as np
import time
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from inspector import GearInspector

app = FastAPI(title="Industrial Gear Inspection Terminal")
inspector = GearInspector()

def generate_cad_gear_frame():
    """Generates a bright synthetic gear image so the screen is never black."""
    img = np.zeros((720, 640, 3), dtype=np.uint8)
    center = (320, 360)
    num_teeth = 18
    r_outer = 210
    r_inner = 150
    
    pts = []
    for i in range(num_teeth * 2):
        angle = i * (np.pi / num_teeth)
        r = r_outer if i % 2 == 0 else r_inner
        x = int(center[0] + r * np.cos(angle))
        y = int(center[1] + r * np.sin(angle))
        pts.append([x, y])
        
    pts = np.array(pts, np.int32).reshape((-1, 1, 2))
    cv2.fillPoly(img, [pts], (220, 220, 220))
    cv2.circle(img, center, r_inner - 20, (160, 160, 160), -1)
    cv2.circle(img, center, 60, (10, 10, 10), -1)
    return img

def get_hud_frame():
    # Resolve absolute directory path for Vercel serverless runtime
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(base_dir, "dataset")
    raw_frame = None

    if os.path.exists(dataset_dir):
        images = sorted([
            os.path.join(dataset_dir, f)
            for f in os.listdir(dataset_dir)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ])
        if images:
            idx = int(time.time() * 1.5) % len(images)
            raw_frame = cv2.imread(images[idx])

    # If dataset image fails to load, use synthetic CAD gear
    if raw_frame is None:
        raw_frame = generate_cad_gear_frame()

    try:
        hud_frame, _ = inspector.process_frame(raw_frame)
    except Exception:
        hud_frame = raw_frame

    _, buffer = cv2.imencode(".jpg", hud_frame)
    return buffer.tobytes()

@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Industrial Gear Inspection Terminal</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body { 
                background-color: #05070a; 
                color: #58a6ff; 
                font-family: monospace; 
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                padding: 10px; 
            }
            .hud-card {
                width: 100%;
                max-width: 1800px;
                background: #0d1117;
                border: 1px solid #30363d;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8);
            }
            img { 
                width: 100%; 
                height: auto; 
                display: block; 
            }
        </style>
    </head>
    <body>
        <div class="hud-card">
            <img id="stream" src="/snapshot" alt="Industrial Automated Inspection HUD Stream" />
        </div>

        <script>
            const img = document.getElementById('stream');
            setInterval(() => {
                img.src = '/snapshot?t=' + new Date().getTime();
            }, 250);
        </script>
    </body>
    </html>
    """

@app.get("/snapshot")
def snapshot():
    frame_bytes = get_hud_frame()
    return Response(content=frame_bytes, media_type="image/jpeg")

@app.get("/metrics")
def get_metrics():
    return inspector.get_telemetry()