import os
import cv2
import numpy as np

os.makedirs("dataset/control", exist_ok=True)
os.makedirs("dataset/defective", exist_ok=True)

def render_industrial_gear(angle_deg=0, has_defect=False):
    width, height = 500, 500
    cx, cy = 250, 250
    
    # Industrial Matte Background (#0A0E14)
    img = np.full((height, width, 3), (20, 14, 10), dtype=np.uint8)
    
    # Precision Grid Overlay
    for x in range(0, width, 25):
        color = (35, 25, 18) if x % 100 == 0 else (25, 18, 12)
        cv2.line(img, (x, 0), (x, height), color, 1)
    for y in range(0, height, 25):
        color = (35, 25, 18) if y % 100 == 0 else (25, 18, 12)
        cv2.line(img, (0, y), (width, y), color, 1)

    num_teeth = 18
    r_outer, r_inner, r_bore = 150, 118, 48
    rad = np.radians(angle_deg)
    
    outer_pts = []
    for i in range(num_teeth * 2):
        a = i * (np.pi / num_teeth) + rad
        is_tooth = (i % 2 == 0)
        
        if has_defect and i in [8, 9]:
            r = r_inner - 6  # Fractured tooth condition
        else:
            r = r_outer if is_tooth else r_inner
            
        outer_pts.append((cx + r * np.cos(a), cy + r * np.sin(a)))

    gear_mask = np.zeros((height, width), dtype=np.uint8)
    pts_array = np.array(outer_pts, dtype=np.int32)
    cv2.fillPoly(gear_mask, [pts_array], 255)

    # Keyway Bore Geometry
    keyway_pts = []
    for i in range(36):
        a = i * (np.pi / 18)
        rk = r_bore + (12 if 0.25 <= a <= 0.55 else 0)
        keyway_pts.append((cx + rk * np.cos(a), cy + rk * np.sin(a)))
    
    cv2.fillPoly(gear_mask, [np.array(keyway_pts, dtype=np.int32)], 0)

    # Metallic Distance Surface Rendering
    dist = cv2.distanceTransform(gear_mask, cv2.DIST_L2, 5)
    cv2.normalize(dist, dist, 0, 255, cv2.NORM_MINMAX)
    metallic = cv2.convertScaleAbs(dist, alpha=0.65, beta=45)
    
    for r_ring in [68, 92, 110]:
        cv2.circle(metallic, (cx, cy), r_ring, 85, 2)

    gear_bgr = cv2.cvtColor(metallic, cv2.COLOR_GRAY2BGR)
    mask_3ch = gear_mask > 0
    img[mask_3ch] = gear_bgr[mask_3ch]

    return img

if __name__ == "__main__":
    print("Generating Industrial Synthetic Dataset...")
    for i in range(1, 11):
        cv2.imwrite(f"dataset/control/gear_{i}.png", render_industrial_gear(angle_deg=(i-1)*36, has_defect=False))
        cv2.imwrite(f"dataset/defective/gear_defective_{i}.png", render_industrial_gear(angle_deg=(i-1)*36, has_defect=True))
    print("Dataset Generation Complete.")