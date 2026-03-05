from __future__ import annotations
from typing import List, Dict, Any
from ultralytics import YOLO

def run_detection(image_path: str, model_path: str, conf: float = 0.25) -> List[Dict[str, Any]]:
    """
        Retorna: [{class, confidence, bbox:{x,y,w,h}}]
        bbox em pixels (xywh)
    """
    model = YOLO(model_path)
    results = model.predict(source=image_path, conf=conf, verbose=False)

    detections = []
    for r in results:
        names = r.names  # id -> label
        if r.boxes is None:
            continue

        for b in r.boxes:
            cls_id = int(b.cls[0].item())
            label = names[cls_id]
            conf_score = float(b.conf[0].item())
            # x1, y1, x2, y2 bbox
            x1, y1, x2, y2 = [float(v.item()) for v in b.xyxy[0]]
            detections.append({
                "class": label,
                "confidence": conf_score,
                "bbox": {
                    "x": x1,
                    "y": y1,
                    "w": max(0.0, x2 - x1),
                    "h": max(0.0, y2 - y1),
                }
            })
    return detections