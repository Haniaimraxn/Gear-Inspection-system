import sys
import cv2
import uvicorn
import time
from generate_dataset import render_industrial_gear
from inspector import GearInspector

def run_desktop_gui():
    inspector = GearInspector()
    print("=====================================================")
    print("  AI AUTOMATION - QUALITY INSPECTION WORKSTATION")
    print("=====================================================")
    print("Running OpenCV Desktop View. Press 'q' to exit.\n")

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

        cv2.imshow("Industrial Automated Inspection HUD - AI Workstation", dashboard)

        angle = (angle + 1) % 360

        if cv2.waitKey(40) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--server":
        print("Starting FastAPI Industrial Inspection Web Server on http://localhost:8000...")
        uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
    else:
        run_desktop_gui()