import os
import cv2
import numpy as np
import time
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from inspector import GearInspector

app = FastAPI(title="Industrial Gear Inspection Terminal")
inspector = GearInspector()

def get_fallback_frame():
    """Generates a synthetic gear frame in memory if dataset is missing."""
    frame = np.zeros((720, 1280, 3), dtype=np.uint8)
    cv2.circle(frame, (640, 360), 200, (200, 200, 200), -1)
    for i in range(18):
        angle = i * (2 * np.pi / 18)
        cx = int(640 + 220 * np.cos(angle))
        cy = int(360 + 220 * np.sin(angle))
        cv2.circle(frame, (cx, cy), 25, (200, 200, 200), -1)
    return frame

def get_single_frame():
    dataset_dir = "dataset"
    images = []
    
    if os.path.exists(dataset_dir):
        images = [
            os.path.join(dataset_dir, f)
            for f in os.listdir(dataset_dir)
            if f.endswith((".png", ".jpg"))
        ]

    if images:
        # Cycle through dataset images based on current timestamp
        idx = int(time.time() * 2) % len(images)
        raw_frame = cv2.imread(images[idx])
    else:
        raw_frame = get_fallback_frame()

    if raw_frame is None:
        raw_frame = get_fallback_frame()

    hud_frame, _ = inspector.process_frame(raw_frame)
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
            // Refresh frame every 200ms to simulate live video on serverless
            const img = document.getElementById('stream');
            setInterval(() => {
                img.src = '/snapshot?t=' + new Date().getTime();
            }, 200);
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