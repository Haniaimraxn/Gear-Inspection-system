#                              Industrial Automated Gear Inspection Workstation

An edge-compatible **Automated Optical Inspection (AOI)** machine vision system engineered for real-time non-destructive quality control (NDT) of mechanical transmission components. The platform features a 3-panel Heads-Up Display (HUD) executing concurrent photon capture, dynamic topological vector rendering, and real-time structural defect isolation.

---

##                                    Technical Overview & Capabilities

The system executes a real-time **Input-Process-Output (IPO)** spatial analysis pipeline designed to replace manual visual inspection in automated assembly lines:

* **Panel 1 — Optical Sensor Feed (Input)**: Ingests monochromatic camera streams, calculates frame rate ($\sim 25\text{ FPS}$) and loop execution latency ($\approx 4.0\text{ms}$), applies spatial center reticle crosshairs, and renders optical tracking bounding brackets.
* **Panel 2 — CAD Vector Topology (Process)**: Performs contour extraction and polar coordinate mapping. Constructs a shaded $\pm 0.50\text{mm}$ tolerance zone band, renders $360^\circ$ angular polar scales ($30^\circ$ intervals), establishes radial pitch vector spokes, and dynamically indexes all intact tooth centroids ($T_1 \dots T_{18}$).
* **Panel 3 — AI Decision Gate (Output)**: Evaluates structural integrity against nominal CAD parameters, calculates dynamic factory yield metrics (`Pass / Fail / Yield %`), isolates tooth fractures via automated angle-gap clustering, and displays target bounding overlays with spatial anomaly callouts.

---

##                                           Core Technology Stack

* **Language**: Python 3.10+
* **Image Processing & Computer Vision**: OpenCV (`cv2`) — Spatial geometry transformation, contour hierarchy extraction, Gaussian blurring, and dynamic distance transform rendering.
* **Matrix Computation & Linear Algebra**: NumPy — Vectorized coordinate transformation, polar angle matrix sorting, Euclidean radius mapping, and array clustering.
* **Asynchronous Web Engine**: FastAPI & Uvicorn — Low-latency HTTP server providing Asynchronous Server Gateway Interface (ASGI) routing for remote telemetry monitoring.
* **Video Protocol**: MJPEG (Motion JPEG) — Low-overhead video byte streaming over standard web endpoints (`/video_feed`).

---

## Main Perspective & Industry Scope

The engineering perspective of this system focuses on **Sub-Millimeter Quality Assurance Automation**:

1. **Deterministic Edge Processing**: Bypasses heavy neural network overhead by leveraging deterministic spatial analysis, achieving sub-5ms frame processing latency suitable for high-speed conveyor belts.
2. **CAD Blueprint Telemetry Alignment**: Converts raw pixel arrays into normalized engineering metrics (Pitch Diameter: $268.0\text{mm}$, Outer Diameter: $300.0\text{mm}$), validating manufacturing deviations directly against ISO standards.
3. **Dual Deployment Flexibility**: Operates natively as a localized workstation GUI (OpenCV GUI viewport) or as a web streaming terminal (FastAPI microservice) integrated into centralized SCADA or industrial IoT dashboards.

---

## Deployment & Execution Workstation

### 1. Install Environment Dependencies
```bash
pip install -r requirements.txt