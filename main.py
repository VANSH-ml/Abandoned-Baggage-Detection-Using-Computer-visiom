import cv2
import time
import numpy as np
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
from collections import defaultdict
from config import ABANDONED_TIME, DISTANCE_THRESHOLD
from utils.draw_utils import draw_box_with_label
from utils.logic import calculate_distance
from playsound import playsound
import threading

# Load model and tracker
model = YOLO('weights/yolov8n.pt')
tracker = DeepSort(max_age=30)

bag_last_seen_with_person = defaultdict(lambda: time.time())
alerted_bags = set()
bag_owner_map = {}  # maps bag_id to last known person center
abandoned_bags = set()  # keep showing label if abandoned

cap = cv2.VideoCapture('videos/videoplayback (4).mp4')

# Sound alert
def play_alert():
    playsound('sounds/funny-alarm-317531.mp3')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    current_time = time.time()
    results = model(frame, verbose=False)[0]

    people = []
    bags = []

    for box in results.boxes.data.tolist():
        x1, y1, x2, y2, conf, cls = box
        cls = int(cls)
        if cls == 0:
            people.append([x1, y1, x2 - x1, y2 - y1])
        elif cls == 28:
            bags.append([x1, y1, x2 - x1, y2 - y1])

    detections = []
    for box in people:
        detections.append(([int(box[0]), int(box[1]), int(box[2]), int(box[3])], 0.99, 'person'))
    for box in bags:
        detections.append(([int(box[0]), int(box[1]), int(box[2]), int(box[3])], 0.99, 'suitcase'))

    tracks = tracker.update_tracks(detections, frame=frame)
    current_people = []

    for track in tracks:
        if not track.is_confirmed():
            continue
        if track.get_det_class() == 'person':
            l, t, r, b = map(int, track.to_ltrb())
            center = ((l + r) // 2, (t + b) // 2)
            current_people.append((track.track_id, center))

    for track in tracks:
        if not track.is_confirmed():
            continue

        track_id = track.track_id
        l, t, r, b = map(int, track.to_ltrb())
        cls = track.get_det_class()
        center = ((l + r) // 2, (t + b) // 2)

        if cls == 'suitcase':
            near_person = False
            min_distance = float('inf')
            closest_person_center = None

            for pid, pcenter in current_people:
                distance = calculate_distance(center, pcenter)
                if distance < DISTANCE_THRESHOLD and distance < min_distance:
                    near_person = True
                    min_distance = distance
                    closest_person_center = pcenter
                    bag_owner_map[track_id] = pcenter
                    bag_last_seen_with_person[track_id] = current_time

            time_alone = current_time - bag_last_seen_with_person[track_id]

            if not near_person and time_alone > ABANDONED_TIME:
                abandoned_bags.add(track_id)
                color = (0, 0, 255)
                label = f"ABANDONED\n{int(time_alone)} sec"
                cv2.circle(frame, center, 30, (0, 0, 255), 3)

                if track_id not in alerted_bags:
                    print(f"[ALERT] 🚨 Abandoned bag detected (ID {track_id}) at {time.strftime('%H:%M:%S')}")
                    threading.Thread(target=play_alert).start()
                    alerted_bags.add(track_id)

                if track_id in bag_owner_map:
                    cv2.line(frame, center, bag_owner_map[track_id], (0, 0, 255), 2)

            elif track_id in abandoned_bags:
                time_alone = current_time - bag_last_seen_with_person[track_id]
                color = (0, 0, 255)
                label = f"ABANDONED\n{int(time_alone)} sec"
                cv2.circle(frame, center, 30, (0, 0, 255), 3)
                if track_id in bag_owner_map:
                    cv2.line(frame, center, bag_owner_map[track_id], (0, 0, 255), 2)
            else:
                color = (0, 255, 255)
                label = f"Suitcase {track_id} ({int(time_alone)}s)"

        elif cls == 'person':
            color = (0, 255, 0)
            label = f"Person {track_id}"
        else:
            continue

        draw_box_with_label(frame, (l, t, r, b), label, color)

    cv2.imshow("Abandoned Baggage Detection", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
