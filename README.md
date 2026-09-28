# :gear: Industrial Automated Gear Inspection Workstation :search:

An edge-compatible **Automated Optical Inspection (AOI)** platform engineered for real-time, non-destructive quality control (**NDT**) of high-precision mechanical transmission components. The system features a **3-panel Heads-Up Display (HUD)** designed to handle concurrent photon capture, dynamic topological vector rendering, and real-time structural defect isolation on fast-moving assembly lines.

---

## :tools: System Architecture & Capabilities :bar_chart:

The workstation runs a low-latency **Input-Process-Output (IPO)** spatial analysis pipeline, serving as a high-speed computer vision alternative to manual inspection:

### :camera: Panel 1 — Optical Sensor Feed (Input) :incoming_envelope:
* :movie_camera: **Raw Stream Ingestion:** Captures monochromatic video streams at standard frame rates (~25 FPS) with minimal loop latency (≈4.0ms).
* :target: **Spatial Target Alignment:** Overlays a spatial center reticle crosshair to maintain consistent physical gear centering.
* :package: **Dynamic Bounding:** Projects real-time optical tracking brackets around detected gear geometries.

### :triangular_ruler: Panel 2 — CAD Vector Topology (Processing) :cpu:
* :mag: **Contour Extraction:** Performs edge detection and extracts vector contours for precise polar coordinate mapping.
* :straight_ruler: **Tolerance Mapping:** Constructs a shaded **±0.50mm nominal tolerance band** overlaid on the gear silhouette.
* :arrows_counterclockwise: **Polar Scale Projection:** Renders a **360° polar reference ring** indexed at **30° increments**.
* :gear: **Feature Indexing:** Maps radial pitch vector spokes and dynamically identifies intact tooth centroids ($T_1 \dots T_{18}$).

### :robot: Panel 3 — AI Decision Gate (Output) :white_check_mark:
* :chart_with_upwards_trend: **Quality Assurance Validation:** Evaluates structural geometry directly against factory **nominal CAD specifications**.
* :bar_chart: **Live Telemetry Tracking:** Computes real-time production yield stats (**Pass Count / Fail Count / Yield %**).
* :warning: **Anomaly Detection:** Isolates missing or damaged teeth via **angle-gap spatial clustering**.
* :label: **Visual Defect Marking:** Instantly highlights surface micro-fractures and structural deviations using targeted bounding overlays.

---

## :desktop_computer: Core Technology Stack :snake:

* :snake: **Python 3.10+:** Core runtime environment for system logic and data transformation.
* :eye: **OpenCV (`cv2`):** Handles image processing, dynamic spatial transformations, contour hierarchies, Gaussian blur filters, and distance transform algorithms.
* :hash: **NumPy:** Powers vector coordinate math, polar angle matrix operations, Euclidean distance mapping, and spatial array indexing.
* :zap: **FastAPI & Uvicorn:** High-performance asynchronous ASGI Web Framework enabling real-time remote telemetry microservices.
* :satellite: **MJPEG Streaming:** Delivers video frames via lightweight byte streams across dedicated HTTP endpoints (`/video_feed`).

---

## :factory: Engineering Focus & Industrial Scope :briefcase:

* :zap: **Deterministic Edge Analytics:** Relies on deterministic mathematical and geometric algorithms rather than heavy deep-learning neural models. Keeps frame latency below 5ms for seamless conveyor integration.
* :straight_ruler: **ISO Standard Metric Translation:** Converts raw pixel data into physical units (**Pitch Diameter: 268.0mm**, **Outer Diameter: 300.0mm**) for immediate validation against engineering tolerances.
* :globe_with_meridians: **Flexible Production Deployment:** Functions as a local OpenCV GUI desktop viewport or streams telemetry to centralized **SCADA** and **IIoT** dashboards.

---

## :rocket: Quickstart & Setup :box:

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
   cd your-repo-name