import os
import cv2
import numpy as np
import time
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from inspector import GearInspector

app = FastAPI(title="Industrial Gear Inspection Terminal")
inspector = GearInspector()

def generate_synthetic_gear():
    """Renders a valid 18-tooth gear shape in memory for serverless deploys."""
    img = np.zeros((720, 1280, 3), dtype=np.uint8)
    center = (640, 360)
    num_teeth = 18
    r_outer = 220
    r_inner = 170
    
    pts = []
    for i in range(num_teeth * 2):
        angle = i * (2 * np.pi / (num_teeth * 2))
        r = r_outer if i % 2 == 0 else r_inner
        x = int(center[0] + r * np.cos(angle))
        y = int(center[1] + r * np.sin(angle))
        pts.append([x, y])
        
    pts = np.array(pts, np.int32).reshape((-1, 1, 2))
    cv2.fillPoly(img, [pts], (180, 180, 180))
    cv2.circle(img, center, 70, (0, 0, 0), -1)  # Center bore
    return img

def get_single_frame():
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
        raw_frame = generate_synthetic_gear()

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
            body { background-color: #0d1117; color: #58a6ff; font-family: monospace; text-align: center; margin: 0; padding: 20px; }
            h1 { color: #58a6ff; margin-bottom: 5px; }
            p { color: #8b949e; margin-bottom: 20px; }
            img { border: 2px solid #30363d; border-radius: 8px; max-width: 95%; height: auto; }
        </style>
    </head>
    <body>
        <h1>⚙️ Industrial Gear Inspection System (AOI)</h1>
        <p>Live Telemetry & SCADA Stream Endpoint</p>
        <img id="stream" src="/snapshot" alt="Live Inspection HUD Stream" />

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
    frame_bytes = get_single_frame()
    return Response(content=frame_bytes, media_type="image/jpeg")

@app.get("/metrics")
def get_metrics():
    return inspector.get_telemetry()