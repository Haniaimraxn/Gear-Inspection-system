# ⚙️ Gear Inspection System: Real-Time Machine Vision HUD

An Automated Optical Inspection (AOI) tool designed to catch gear defects in real time before parts hit the assembly line. Powered by **OpenCV**, **NumPy**, and **FastAPI**, it combines computer vision with dynamic CAD vector overlays inside a 3-panel Heads-Up Display (HUD) for instant quality control.

---

## 🔬 How It Works (3-Panel Pipeline)

The workstation processes frames using a real-time **Input-Process-Output (IPO)** architecture designed for high-speed manufacturing environments:

* 📹 **Panel 1: Optical Sensor Feed (Input)** — Ingests raw monochromatic camera frames, tracks live performance (~25 FPS, ~4.0 ms latency), and centers the part with crosshairs and dynamic tracking brackets.
* 📐 **Panel 2: CAD Vector Topology (Process)** — Extracts gear contours and maps them into polar coordinates. It overlays a ±0.50 mm tolerance band, projects a 360° polar angle grid (30° steps), plots pitch vector spokes, and indexes each detected tooth tip ($T_1 \dots T_{18}$).
* 🎯 **Panel 3: AI Decision Gate (Output)** — Evaluates part geometry against nominal CAD specs, updates factory yield metrics (`Pass / Fail / Yield %`), isolates broken or missing teeth using angle-gap clustering, and flags defect locations with target callouts.

---

## 🛠️ Built With

* 🐍 **Python 3.10+** — Core runtime driving the pipeline.
* 👁️ **OpenCV** — Spatial transformations, contour extraction, distance mapping, and HUD rendering.
* 🧮 **NumPy** — Vectorized matrix operations, polar angle sorting, and fast Euclidean distance calculations.
* ⚡ **FastAPI & Uvicorn** — Asynchronous web server serving live video streams and telemetry endpoints.
* 📡 **Motion JPEG (MJPEG)** — Low-overhead byte streaming directly to web browsers (`/video_feed`).

---

## 💡 Why This Approach?

* ⚡ **Sub-5ms Edge Processing** — Uses deterministic spatial math instead of heavy neural networks, keeping latency under 5 ms for real-time conveyor belt integration.
* 📏 **True CAD Metric Alignment** — Converts pixel dimensions directly into real-world physical measurements (Pitch Diameter: 268.0 mm, Outer Diameter: 300.0 mm) to enforce ISO manufacturing standards.
* 🔀 **Flexible Deployment** — Run it as a standalone desktop window for operators or stream it over HTTP to factory SCADA dashboards and web browsers.

---

## 🚀 Getting Started

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
