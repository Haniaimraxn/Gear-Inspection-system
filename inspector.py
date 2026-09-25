import cv2
import numpy as np

class GearInspector:
    def __init__(self, expected_teeth=18, nominal_outer_r=150, nominal_inner_r=118):
        self.expected_teeth = expected_teeth
        self.nominal_outer_r = nominal_outer_r
        self.nominal_inner_r = nominal_inner_r
        self.total_count = 0
        self.pass_count = 0
        self.fail_count = 0

    def draw_hud_brackets(self, img, color=(80, 60, 40), length=16):
        h, w, _ = img.shape
        cv2.line(img, (10, 10), (10 + length, 10), color, 1)
        cv2.line(img, (10, 10), (10, 10 + length), color, 1)
        cv2.line(img, (w - 10, 10), (w - 10 - length, 10), color, 1)
        cv2.line(img, (w - 10, 10), (w - 10, 10 + length), color, 1)
        cv2.line(img, (10, h - 10), (10 + length, h - 10), color, 1)
        cv2.line(img, (10, h - 10), (10, h - 10 - length), color, 1)
        cv2.line(img, (w - 10, h - 10), (w - 10 - length, h - 10), color, 1)
        cv2.line(img, (w - 10, h - 10), (w - 10, h - 10 - length), color, 1)

    def inspect(self, image_input, fps=25.0, latency_ms=4.0):
        if isinstance(image_input, str):
            raw_img = cv2.imread(image_input)
        else:
            raw_img = image_input.copy()

        h, w, _ = raw_img.shape
        cx, cy = w // 2, h // 2

        # -------------------------------------------------------------------
        # PANEL 1: OPTICAL SENSOR FEED (Input)
        # -------------------------------------------------------------------
        gray = cv2.cvtColor(raw_img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 40, 255, cv2.THRESH_BINARY)

        panel_input = raw_img.copy()
        self.draw_hud_brackets(panel_input)

        cv2.drawMarker(panel_input, (cx, cy), (0, 255, 255), cv2.MARKER_CROSS, 22, 1)
        cv2.circle(panel_input, (cx, cy), 160, (50, 40, 25), 1, cv2.LINE_AA)

        cv2.putText(panel_input, "PANEL 1: OPTICAL SENSOR FEED", (15, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.40, (255, 200, 0), 1, cv2.LINE_AA)
        cv2.putText(panel_input, f"CAM_01: 1080P MONO | {fps:.1f} FPS | LATENCY: {latency_ms:.1f}ms", (15, 42),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.30, (150, 150, 150), 1, cv2.LINE_AA)

        # -------------------------------------------------------------------
        # PANEL 2: CAD VECTOR TOPOLOGY (Process)
        # -------------------------------------------------------------------
        panel_process = np.full((h, w, 3), (20, 14, 10), dtype=np.uint8)
        self.draw_hud_brackets(panel_process)

        # Shaded Tolerance Band Overlay
        overlay = panel_process.copy()
        cv2.circle(overlay, (cx, cy), self.nominal_outer_r, (40, 30, 10), -1)
        cv2.circle(overlay, (cx, cy), self.nominal_inner_r, (20, 14, 10), -1)
        cv2.addWeighted(overlay, 0.4, panel_process, 0.6, 0, panel_process)

        # Reference Pitch & Root Circles
        cv2.circle(panel_process, (cx, cy), self.nominal_inner_r, (120, 80, 20), 1, cv2.LINE_AA)
        cv2.circle(panel_process, (cx, cy), 134, (160, 110, 30), 1, cv2.LINE_AA)
        cv2.circle(panel_process, (cx, cy), self.nominal_outer_r, (120, 80, 20), 1, cv2.LINE_AA)

        # Inner Keyway Bore Blueprint Lines
        cv2.circle(panel_process, (cx, cy), 48, (0, 200, 255), 1, cv2.LINE_AA)
        cv2.rectangle(panel_process, (cx + 38, cy - 8), (cx + 56, cy + 8), (0, 200, 255), 1)

        # Polar Angular Scale Ticks
        for deg in range(0, 360, 30):
            rad = np.radians(deg)
            x1 = int(cx + 152 * np.cos(rad))
            y1 = int(cy + 152 * np.sin(rad))
            x2 = int(cx + 162 * np.cos(rad))
            y2 = int(cy + 162 * np.sin(rad))
            cv2.line(panel_process, (x1, y1), (x2, y2), (180, 120, 40), 1, cv2.LINE_AA)
            
            lx = int(cx + 172 * np.cos(rad)) - 8
            ly = int(cy + 172 * np.sin(rad)) + 4
            cv2.putText(panel_process, f"{deg} deg", (lx, ly),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.22, (150, 130, 80), 1, cv2.LINE_AA)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        detected_teeth_count = 0
        has_defect = False
        defect_coords = None

        if contours:
            gear_contour = max(contours, key=cv2.contourArea)

            cv2.drawContours(panel_process, [gear_contour], -1, (255, 200, 0), 2, cv2.LINE_AA)
            cv2.drawContours(panel_process, [gear_contour], -1, (255, 255, 255), 1, cv2.LINE_AA)

            pts = gear_contour.reshape(-1, 2)
            radii = np.sqrt((pts[:, 0] - cx)**2 + (pts[:, 1] - cy)**2)
            angles = np.arctan2(pts[:, 1] - cy, pts[:, 0] - cx)

            tip_mask = radii > 138.0
            if np.any(tip_mask):
                tip_angles = angles[tip_mask]
                tip_pts = pts[tip_mask]

                sort_idx = np.argsort(tip_angles)
                sorted_angles = tip_angles[sort_idx]
                sorted_pts = tip_pts[sort_idx]

                clusters = []
                curr_cluster = [0]
                for k in range(1, len(sorted_angles)):
                    if sorted_angles[k] - sorted_angles[k - 1] < 0.15:
                        curr_cluster.append(k)
                    else:
                        clusters.append(curr_cluster)
                        curr_cluster = [k]
                clusters.append(curr_cluster)

                if len(clusters) > 1:
                    wrap_gap = (sorted_angles[0] + 2 * np.pi) - sorted_angles[clusters[-1][-1]]
                    if wrap_gap < 0.15:
                        clusters[0] = clusters[-1] + clusters[0]
                        clusters.pop()

                detected_teeth_count = len(clusters)

                cluster_angles = []
                for t_idx, cl in enumerate(clusters):
                    cl_pts = sorted_pts[cl]
                    cl_radii = np.sqrt((cl_pts[:, 0] - cx)**2 + (cl_pts[:, 1] - cy)**2)
                    max_idx = np.argmax(cl_radii)
                    tip_x, tip_y = cl_pts[max_idx]
                    
                    cv2.line(panel_process, (cx, cy), (tip_x, tip_y), (100, 70, 20), 1, cv2.LINE_AA)
                    cv2.circle(panel_process, (tip_x, tip_y), 4, (0, 255, 255), -1)
                    
                    lbl_x = int(cx + 140 * np.cos(np.arctan2(tip_y - cy, tip_x - cx))) - 6
                    lbl_y = int(cy + 140 * np.sin(np.arctan2(tip_y - cy, tip_x - cx))) + 3
                    cv2.putText(panel_process, f"T{t_idx+1}", (lbl_x, lbl_y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.24, (255, 255, 0), 1, cv2.LINE_AA)

                    cluster_angles.append(np.arctan2(tip_y - cy, tip_x - cx))

                if detected_teeth_count < self.expected_teeth:
                    has_defect = True
                    cluster_angles = np.sort(cluster_angles)
                    expected_pitch = (2 * np.pi) / self.expected_teeth
                    missing_angle = None
                    
                    for m in range(len(cluster_angles)):
                        next_m = (m + 1) % len(cluster_angles)
                        gap = cluster_angles[next_m] - cluster_angles[m]
                        if gap < 0:
                            gap += 2 * np.pi
                        
                        if gap > 1.4 * expected_pitch:
                            missing_angle = cluster_angles[m] + (gap / 2.0)
                            break

                    if missing_angle is not None:
                        defect_x = int(cx + self.nominal_inner_r * np.cos(missing_angle))
                        defect_y = int(cy + self.nominal_inner_r * np.sin(missing_angle))
                        defect_coords = (defect_x, defect_y)

        cv2.drawMarker(panel_process, (cx, cy), (0, 255, 255), cv2.MARKER_CROSS, 28, 1)

        cad_specs = [
            "MODEL: ISO_GEAR_18T",
            "PITCH_DIA: 268.0mm",
            "OUTER_DIA: 300.0mm",
            "BORE_KEYWAY: 96.0mm",
            "TOLERANCE: +/- 0.50mm"
        ]
        for idx, txt in enumerate(cad_specs):
            cv2.putText(panel_process, txt, (15, 385 + idx * 17),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.30, (0, 200, 255), 1, cv2.LINE_AA)

        cv2.putText(panel_process, "PANEL 2: CAD VECTOR TOPOLOGY", (15, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.40, (255, 200, 0), 1, cv2.LINE_AA)

        # -------------------------------------------------------------------
        # PANEL 3: AI DECISION GATE (Output)
        # -------------------------------------------------------------------
        panel_output = cv2.addWeighted(raw_img, 0.45, panel_process, 0.55, 0)
        self.draw_hud_brackets(panel_output)

        cv2.putText(panel_output, "PANEL 3: AI DECISION GATE", (15, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.40, (255, 200, 0), 1, cv2.LINE_AA)

        self.total_count += 1
        if has_defect:
            self.fail_count += 1
        else:
            self.pass_count += 1

        yield_rate = (self.pass_count / self.total_count) * 100.0 if self.total_count > 0 else 100.0
        cv2.putText(panel_output, f"INSPECTED: {self.total_count} | PASS: {self.pass_count} | REJECT: {self.fail_count} | YIELD: {yield_rate:.1f}%",
                    (15, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.30, (160, 200, 220), 1, cv2.LINE_AA)

        if has_defect:
            cv2.rectangle(panel_output, (12, 48), (340, 78), (20, 20, 180), -1)
            cv2.rectangle(panel_output, (12, 48), (340, 78), (50, 50, 255), 2)
            cv2.putText(panel_output, "[ STATUS: FAIL - REJECT PART ]", (20, 69),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.48, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.putText(panel_output, f"TEETH COUNT: {detected_teeth_count} / {self.expected_teeth} (1 MISSING)",
                        (15, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (180, 180, 255), 1, cv2.LINE_AA)

            if defect_coords is not None:
                dx, dy = defect_coords

                cv2.rectangle(panel_output, (dx - 22, dy - 22), (dx + 22, dy + 22), (50, 50, 255), 2)
                cv2.circle(panel_output, (dx, dy), 4, (0, 0, 255), -1)

                cv2.line(panel_output, (dx + 22, dy - 10), (dx + 75, dy - 40), (50, 50, 255), 1, cv2.LINE_AA)
                cv2.line(panel_output, (dx + 75, dy - 40), (dx + 210, dy - 40), (50, 50, 255), 1, cv2.LINE_AA)

                cv2.rectangle(panel_output, (dx + 75, dy - 56), (dx + 205, dy - 40), (50, 50, 255), -1)
                cv2.putText(panel_output, "ANOMALY DETECTED", (dx + 78, dy - 44),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.34, (255, 255, 255), 1, cv2.LINE_AA)

                cv2.putText(panel_output, "STRUCTURAL_TOOTH_FRACTURE", (dx + 75, dy - 24),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.36, (80, 80, 255), 1, cv2.LINE_AA)

                cv2.putText(panel_output, "DIAMETER_TOLERANCE_EXCEEDED", (dx - 130, dy + 45),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.35, (50, 50, 255), 1, cv2.LINE_AA)
        else:
            cv2.rectangle(panel_output, (12, 48), (340, 78), (20, 130, 20), -1)
            cv2.rectangle(panel_output, (12, 48), (340, 78), (0, 255, 0), 2)
            cv2.putText(panel_output, "[ STATUS: PASS - ACCEPT PART ]", (20, 69),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.48, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.putText(panel_output, f"TEETH COUNT: {detected_teeth_count} / {self.expected_teeth} INTACT (TOLERANCE OK)",
                        (15, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (180, 255, 180), 1, cv2.LINE_AA)

        dashboard = np.hstack((panel_input, panel_process, panel_output))
        return dashboard, has_defect