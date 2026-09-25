import os
import cv2
import numpy as np
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from inspector import GearInspector

app = FastAPI(title="Industrial Gear Inspection Terminal")

inspector = GearInspector()

def get_fallback_frame():
    """Generates a synthetic gear frame in memory if local dataset is missing on serverless deploys."""
    frame = np.zeros((720, 1280, 3), dtype=np.uint8)
    cv2.circle(frame, (640, 360), 200, (200, 200, 200), -1)
    for i in range(18):
        angle = i * (2 * np.pi / 18)
        cx = int(640 + 220 * np.cos(angle))
        cy = int(360 + 220 * np.sin(angle))
        cv2.circle(frame, (cx, cy), 25, (200, 200, 200), -1)
    return frame

def generate_frames():
    dataset_dir = "dataset"
    images = []
    
    if os.path.exists(dataset_dir):
        images = [
            os.path.join(dataset_dir, f)
            for f in os.listdir(dataset_dir)
            if f.endswith((".png", ".jpg"))
        ]

    idx = 0
    while True:
        if images:
            raw_frame = cv2.imread(images[idx % len(images)])
            idx += 1
        else:
            raw_frame = get_fallback_frame()

        if raw_frame is None:
            raw_frame = get_fallback_frame()

        hud_frame, _ = inspector.process_frame(raw_frame)
        _, buffer = cv2.imencode(".jpg", hud_frame)
        frame_bytes = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
        )

@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Industrial Gear Inspection Terminal</title>
        <style>
            body { background-color: #0d1117; color: #58a6ff; font-family: monospace; text-align: center; margin: 0; padding: 20px; }
            h1 { color: #58a6ff; }
            img { border: 2px solid #30363d; border-radius: 8px; max-width: 95%; height: auto; }
        </style>
    </head>
    <body>
        <h1>⚙️ Industrial Gear Inspection System (AOI)</h1>
        <p>Live Telemetry & SCADA Stream Endpoint</p>
        <img src="/video_feed" alt="Live Inspection HUD Stream" />
    </body>
    </html>
    """

@app.get("/video_feed")
def video_feed():
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

@app.get("/metrics")
def get_metrics():
    return inspector.get_telemetry()