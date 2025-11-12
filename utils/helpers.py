import json
import cv2

def save_class_indices(class_indices, path):
    with open(path, 'w') as f:
        json.dump(class_indices, f)
    print(f"Class mapping saved at {path}")

def draw_detections(image, detections, output_path="output.jpg"):
    for det in detections:
        x1, y1, x2, y2 = det["box"]
        label = f"{det['class']} ({det['confidence']:.2f})"
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imwrite(output_path, image)
    print(f"Detections drawn and saved to {output_path}")



