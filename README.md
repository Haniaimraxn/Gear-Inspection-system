# ⚙️ Industrial Automated Gear Inspection Workstation 🔍

An edge-compatible **Automated Optical Inspection (AOI)** platform engineered for real-time, non-destructive quality control (**NDT**) of high-precision mechanical transmission components. The system features a **3-panel Heads-Up Display (HUD)** designed to handle concurrent photon capture, dynamic topological vector rendering, and real-time structural defect isolation on fast-moving assembly lines.

---

## 🏷️ System Identifier
**Edge-AI Industrial Transmission Quality Assurance Platform**

---

## 📝 Description (What does it do)

The **Industrial Automated Gear Inspection Workstation** is a low-latency computer vision solution designed to replace manual quality checks on automated assembly lines. 

By executing a real-time **Input-Process-Output (IPO)** spatial analysis pipeline directly at the edge, the system ingests raw video feeds, extracts precision CAD vector topologies, and calculates real-time factory yield metrics—isolating tooth fractures and surface defects instantly with under 5ms frame latency.

---

## 🛠️ System Architecture & Capabilities 📊

The workstation runs a low-latency spatial analysis pipeline across three core processing HUD panels:

### 📷 Panel 1 — Optical Sensor Feed (Input) 📨
* 🎥 **Raw Stream Ingestion:** Captures monochromatic video streams at standard frame rates (~25 FPS) with minimal loop latency (≈4.0ms).
* 🎯 **Spatial Target Alignment:** Overlays a spatial center reticle crosshair to maintain consistent physical gear centering.
* 📦 **Dynamic Bounding:** Projects real-time optical tracking brackets around detected gear geometries.

### 📐 Panel 2 — CAD Vector Topology (Processing) 🖥️
* 🔍 **Contour Extraction:** Performs edge detection and extracts vector contours for precise polar coordinate mapping.
* 📏 **Tolerance Mapping:** Constructs a shaded **±0.50mm nominal tolerance band** overlaid on the gear silhouette.
* 🔄 **Polar Scale Projection:** Renders a **360° polar reference ring** indexed at **30° increments**.
* ⚙️ **Feature Indexing:** Maps radial pitch vector spokes and dynamically identifies intact tooth centroids ($T_1 \dots T_{18}$).

### 🤖 Panel 3 — AI Decision Gate (Output) ✅
* 📈 **Quality Assurance Validation:** Evaluates structural geometry directly against factory **nominal CAD specifications**.
* 📊 **Live Telemetry Tracking:** Computes real-time production yield stats (**Pass Count / Fail Count / Yield %**).
* ⚠️ **Anomaly Detection:** Isolates missing or damaged teeth via **angle-gap spatial clustering**.
* 🏷️ **Visual Defect Marking:** Instantly highlights surface micro-fractures and structural deviations using targeted bounding overlays.

---

## 💻 Core Technology Stack 🐍

* 🐍 **Python 3.10+:** Core runtime environment for system logic and data transformation.
* 👁️ **OpenCV (`cv2`):** Handles image processing, dynamic spatial transformations, contour hierarchies, Gaussian blur filters, and distance transform algorithms.
* 🔢 **NumPy:** Powers vector coordinate math, polar angle matrix operations, Euclidean distance mapping, and spatial array indexing.
* ⚡ **FastAPI & Uvicorn:** High-performance asynchronous ASGI Web Framework enabling real-time remote telemetry microservices.
* 📡 **MJPEG Streaming:** Delivers video frames via lightweight byte streams across dedicated HTTP endpoints (`/video_feed`).

---

## 🏭 Engineering Focus & Industrial Scope 💼

* ⚡ **Deterministic Edge Analytics:** Relies on deterministic mathematical and geometric algorithms rather than heavy deep-learning neural models. Keeps frame latency below 5ms for seamless conveyor integration.
* 📏 **ISO Standard Metric Translation:** Converts raw pixel data into physical units (**Pitch Diameter: 268.0mm**, **Outer Diameter: 300.0mm**) for immediate validation against engineering tolerances.
* 🌐 **Flexible Production Deployment:** Functions as a local OpenCV GUI desktop viewport or streams telemetry to centralized **SCADA** and **IIoT** dashboards.

---

## 🚀 How to Run 📦

Follow these commands to install dependencies and start the inspection server locally or on Replit:

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/Haniaimraxn/Gear-Inspection-system.git](https://github.com/Haniaimraxn/Gear-Inspection-system.git)
   cd Gear-Inspection-system