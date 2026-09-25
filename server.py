import time
import cv2
import numpy as np
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse, JSONResponse
from generate_dataset import render_industrial_gear
from inspector import GearInspector

app = FastAPI(title="Industrial Automated Inspection System", version="2.0.0")
inspector = GearInspector()

def generate_mjpeg_stream():
    angle = 0
    toggle_counter = 0
    has_defect = False
    prev_time = time.time()
    
    while True:
        curr_time = time.time()
        elapsed = curr_time - prev_time
        prev_time = curr_time
        fps = 1.0 / elapsed if elapsed > 0 else 25.0
        latency_ms = elapsed * 1000.0

        toggle_counter += 1
        if toggle_counter >= 200:
            has_defect = not has_defect
            toggle_counter = 0

        frame = render_industrial_gear(angle_deg=angle, has_defect=has_defect)
        dashboard, _ = inspector.inspect(frame, fps=fps, latency_ms=latency_ms)

        _, encoded_img = cv2.imencode('.jpg', dashboard)
        frame_bytes = encoded_img.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        angle = (angle + 1) % 360
        time.sleep(0.03)

@app.get("/", response_class=HTMLResponse)
def live_terminal():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Industrial Automated Inspection Terminal</title>
        <style>
            body { background-color: #0a0e14; color: #00e5ff; font-family: monospace; text-align: center; margin: 0; padding: 20px; }
            h1 { color: #ffb700; margin-bottom: 5px; }
            p { color: #a0a0a0; margin-top: 0; }
            .container { display: inline-block; border: 2px solid #00e5ff; border-radius: 6px; box-shadow: 0 0 20px rgba(0, 229, 255, 0.25); padding: 10px; background: #10141b; }
            img { display: block; max-width: 100%; height: auto; }
        </style>
    </head>
    <body>
        <h1>INDUSTRIAL AUTOMATED INSPECTION HUD</h1>
        <p>Live Web Telemetry, CAD Topology & AI Decision Gate Feed</p>
        <div class="container">
            <img src="/video_feed" alt="Live Inspection Stream" />
        </div>
    </body>
    </html>
    """

@app.get("/video_feed")
def video_feed():
    return StreamingResponse(generate_mjpeg_stream(), media_type="multipart/x-mixed-replace;boundary=frame")

@app.get("/metrics")
def get_inspection_metrics():
    return JSONResponse({
        "total_inspected": inspector.total_count,
        "passed_parts": inspector.pass_count,
        "rejected_parts": inspector.fail_count,
        "yield_rate_percent": round((inspector.pass_count / inspector.total_count * 100.0), 2) if inspector.total_count > 0 else 100.0
    })