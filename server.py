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
    """Generates an 18-tooth gear image that matches inspector.py contour expectations."""
    img = np.zeros((720, 640, 3), dtype=np.uint8)
    center = (320, 360)
    num_teeth = 18
    r_outer = 210
    r_inner = 150
    
    # Outer tooth profile
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
    cv2.circle(img, center, 60, (10, 10, 10), -1)  # Center bore
    return img

def get_hud_frame():
    dataset_dir = "dataset"
    raw_frame = None

    if os.path.exists(dataset_dir):
        images = [
            os.path.join(dataset_dir, f)
            for f in os.listdir(dataset_dir)
            if f.endswith((".png", ".jpg"))
        ]
        if images:
            idx = int(time.time() * 2) % len(images)
            raw_frame = cv2.imread(images[idx])

    if raw_frame is None:
        raw_frame = generate_cad_gear_frame()

    # Pass frame through inspector to build the 3-panel side-by-side composite frame
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
    <html>
    <head>
        <title>Industrial Gear Inspection Terminal</title>
        <style>
            * { box-sizing: border-box; }
            body { 
                background-color: #05070a; 
                color: #58a6ff; 
                font-family: 'Segoe UI', Tahoma, monospace; 
                text-align: center; 
                margin: 0; 
                padding: 15px; 
            }
            h1 { color: #58a6ff; margin-bottom: 5px; font-size: 22px; }
            p { color: #8b949e; margin-bottom: 15px; font-size: 13px; }
            .hud-container {
                width: 100%;
                max-width: 1600px;
                margin: 0 auto;
                border: 1px solid #30363d;
                border-radius: 6px;
                overflow: hidden;
                box-shadow: 0 8px 24px rgba(0,0,0,0.6);
            }
            img { 
                width: 100%; 
                height: auto; 
                display: block; 
            }
        </style>
    </head>
    <body>
        <h1>⚙️ Industrial Gear Inspection System (AOI)</h1>
        <p>Real-Time SCADA Web Terminal • 3-Panel Inspection HUD</p>
        <div class="hud-container">
            <img id="stream" src="/snapshot" alt="3-Panel Gear Inspection HUD Stream" />
        </div>

        <script>
            const img = document.getElementById('stream');
            setInterval(() => {
                img.src = '/snapshot?t=' + new Date().getTime();
            }, 300);
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