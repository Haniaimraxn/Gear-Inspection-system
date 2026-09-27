⚙️ Industrial Automated Gear Inspection Workstation 🔍
An edge-compatible Automated Optical Inspection (AOI) system engineered for real-time, non-destructive quality control (NDT) of mechanical transmission components. The platform provides a 3-panel Heads-Up Display (HUD) that handles concurrent photon capture, dynamic topological vector rendering, and real-time structural defect isolation. 🛠️

📊 Technical Overview & Capabilities
The system executes a real-time Input-Process-Output (IPO) spatial analysis pipeline, built to replace manual visual inspection on high-speed automated assembly lines:

📸 Panel 1 — Optical Sensor Feed (Input): Ingests raw monochromatic video streams, tracks frame rates (∼25 FPS) and loop latency (≈4.0ms), applies spatial center reticle crosshairs, and projects optical tracking bounding brackets.

📐 Panel 2 — CAD Vector Topology (Process): Performs contour extraction and polar coordinate mapping. It constructs a shaded ±0.50mm tolerance band, projects a 360 
∘
  polar scale at 30 
∘
  increments, maps radial pitch vector spokes, and dynamically indexes intact tooth centroids (T 
1
​
 …T 
18
​
 ).

🤖 Panel 3 — AI Decision Gate (Output): Evaluates structural integrity against nominal CAD specifications, calculates real-time factory yield metrics (Pass / Fail / Yield %), isolates tooth fractures via automated angle-gap clustering, and highlights spatial anomalies with targeted bounding overlays.

💻 Core Technology Stack
🐍 Language: Python 3.10+

👁️ Computer Vision: OpenCV (cv2) — Spatial geometry transformation, contour hierarchy extraction, Gaussian smoothing, and dynamic distance transform rendering.

🔢 Matrix Computation: NumPy — Vectorized coordinate transforms, polar angle matrix sorting, Euclidean radius mapping, and spatial array clustering.

⚡ Web Engine & Microservice: FastAPI & Uvicorn — Low-latency ASGI server providing asynchronous HTTP endpoints for remote telemetry monitoring.

📡 Streaming Protocol: Motion JPEG (MJPEG) — Lightweight byte streaming over dedicated web endpoints (/video_feed).

🏭 Engineering Focus & Industrial Scope
Designed specifically for Sub-Millimeter Quality Assurance Automation:

⚡ Deterministic Edge Processing: Uses algorithmic spatial analysis instead of heavy neural network models, keeping frame processing latency under 5ms for seamless integration with high-speed conveyors.

📏 CAD Telemetry Alignment: Translates raw pixel data into normalized engineering metrics (Pitch Diameter: 268.0mm, Outer Diameter: 300.0mm) to validate manufacturing tolerances directly against ISO standards.

🌐 Flexible Deployment: Operates as a local desktop GUI (OpenCV viewport) or streams over the web via FastAPI for integration into centralized SCADA and Industrial IoT (IIoT) dashboards.

🚀 Setup & Execution
1. Install Dependencies 📦
Bash
pip install -r requirements.txt