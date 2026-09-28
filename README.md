# ⚙️ Industrial Automated Gear Inspection Workstation 🔍

An edge-compatible **Automated Optical Inspection (AOI)** platform engineered for real-time, non-destructive quality control (**NDT**) of high-precision mechanical transmission components. The system features a **3-panel Heads-Up Display (HUD)** designed to handle concurrent photon capture, dynamic topological vector rendering, and real-time structural defect isolation on fast-moving assembly lines.

---

## 📌 Project Title
**Industrial Automated Gear Inspection Workstation**

---

## 📝 Description (What does it do?)

The **Industrial Automated Gear Inspection Workstation** is an edge-compatible Automated Optical Inspection (AOI) platform engineered for real-time, non-destructive quality control (NDT) of mechanical transmission components. The platform provides a 3-panel Heads-Up Display (HUD) that handles concurrent photon capture, dynamic topological vector rendering, and real-time structural defect isolation.

The system executes a real-time **Input-Process-Output (IPO)** spatial analysis pipeline, built to replace manual visual inspection on high-speed automated assembly lines:
* 📷 **Panel 1 — Optical Sensor Feed (Input):** Ingests raw monochromatic video streams, tracks frame rates (~25 FPS) and loop latency (≈4.0ms), applies spatial center reticle crosshairs, and projects optical tracking bounding brackets.
* 📐 **Panel 2 — CAD Vector Topology (Process):** Performs contour extraction and polar coordinate mapping. It constructs a shaded ±0.50mm tolerance band, projects a 360° polar scale at 30° increments, maps radial pitch vector spokes, and dynamically indexes intact tooth centroids ($T_1 \dots T_{18}$).
* 🤖 **Panel 3 — AI Decision Gate (Output):** Evaluates structural integrity against nominal CAD specifications, calculates real-time factory yield metrics (Pass / Fail / Yield %), isolates tooth fractures via automated angle-gap clustering, and highlights spatial anomalies with targeted bounding overlays.

---

## 🚀 How to Run (Commands to start the project)

Follow these steps to set up the environment and start the inspection system on your local machine or cloud server:

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/Haniaimraxn/Gear-Inspection-system.git](https://github.com/Haniaimraxn/Gear-Inspection-system.git)
   cd Gear-Inspection-system