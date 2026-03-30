import cv2
import numpy as np
from collections import defaultdict
from ultralytics import YOLO

class VideoQueueAnalyzer:
    def __init__(self, model_path="yolov8n.pt"):
        # Load the YOLO model (nano version for speed on CPU)
        self.model = YOLO(model_path)
        
        # Track history for heuristic analysis
        self.track_history = defaultdict(lambda: [])
        self.service_person_id = None
        self.frame_count = 0
        
    def process_frame(self, frame):
        self.frame_count += 1
        
        # Resize for faster processing if necessary
        # frame = cv2.resize(frame, (640, 480))
        annotated_frame = frame.copy()
        
        # Run YOLO tracking, classes=0 (person only)
        # persist=True enables DeepSORT tracking integration
        results = self.model.track(frame, persist=True, classes=[0], conf=0.3, verbose=False)
        
        boxes_data = results[0].boxes
        
        waiting_count = 0
        total_count = 0
        
        if boxes_data is not None and boxes_data.id is not None:
            boxes = boxes_data.xyxy.cpu().numpy()
            ids = boxes_data.id.int().cpu().tolist()
            total_count = len(ids)
            
            centers = []
            for box in boxes:
                center_x = (box[0] + box[2]) / 2.0
                center_y = (box[1] + box[3]) / 2.0
                centers.append((center_x, center_y))
            
            # Update history
            for track_id, center in zip(ids, centers):
                self.track_history[track_id].append(center)
                # Keep only recent history to avoid memory issues and adapt
                if len(self.track_history[track_id]) > 60:
                    self.track_history[track_id].pop(0)

            # Heuristic: Every 30 frames, attempt to identify the "Service Person"
            # It's the person whose variance in position is the lowest (standing still behind a counter)
            if self.frame_count % 30 == 0 or self.service_person_id is None:
                min_variance = float('inf')
                candidate = None
                
                for track_id, history in self.track_history.items():
                    # We evaluate anyone who has been tracked for at least a few frames
                    if len(history) >= 15:
                        history_np = np.array(history)
                        variance = np.var(history_np[:,0]) + np.var(history_np[:,1])
                        
                        if variance < min_variance:
                            min_variance = variance
                            candidate = track_id
                
                # Threshold to ensure they are actually reasonably still
                if candidate is not None and min_variance < 800:
                    self.service_person_id = candidate

            # Draw boxes logic
            for box, track_id, center in zip(boxes, ids, centers):
                x1, y1, x2, y2 = map(int, box)
                
                # Define line thickness and font scaling relative to frame size
                height, width, _ = frame.shape
                thickness = max(1, int(width * 0.003))
                font_scale = max(0.4, width * 0.0008)
                
                if track_id == self.service_person_id:
                    # Service Person is Green
                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), thickness)
                    cv2.putText(annotated_frame, "Service Person", (x1, max(y1-10, 0)), 
                                cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 255, 0), max(1, thickness-1))
                else:
                    # Queue/Waiting individuals are Blue
                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (255, 0, 0), thickness)
                    cv2.putText(annotated_frame, f"Waiting Customer", (x1, max(y1-10, 0)), 
                                cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 0, 0), max(1, thickness-1))
                    waiting_count += 1
            
        return annotated_frame, waiting_count, total_count
