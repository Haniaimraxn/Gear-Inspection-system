import os
import cv2
import numpy as np
import time
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from inspector import GearInspector

app = FastAPI(title="Industrial Gear Inspection Terminal")
inspector = GearInspector()

def get_hud_frame():
    dataset_dir = "dataset"
    raw_frame = None

    if os.path.exists(dataset_dir):
        images = sorted([
            os.path.join(dataset_dir, f)
            for f in os.listdir(dataset_dir)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ])
        if images:
            # Cycle through dataset frames smoothly based on timestamp
            idx = int(time.time() * 1.5) % len(images)
            raw_frame = cv2.imread(images[idx])

    # Fallback if dataset folder is empty
    if raw_frame is None:
        raw_frame = np.zeros((720, 1280, 3), dtype=np.uint8)

    # Process frame through 3-panel HUD inspector pipeline
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
                font-family: 'Segoe UI', Tahoma, monospace; 
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