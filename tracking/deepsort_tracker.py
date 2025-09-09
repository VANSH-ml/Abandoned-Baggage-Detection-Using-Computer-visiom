from deep_sort_realtime.deepsort_tracker import DeepSort

class DeepSortTracker:
    def __init__(self, max_age=30, n_init=3, nms_max_overlap=1.0):
        """
        Wrapper for DeepSort object tracker.

        Args:
            max_age (int): Number of frames to keep 'lost' tracks alive.
            n_init (int): Minimum detections before track is confirmed.
            nms_max_overlap (float): IOU threshold for suppression.
        """
        self.tracker = DeepSort(
            max_age=max_age,
            n_init=n_init,
            nms_max_overlap=nms_max_overlap
        )

    def update(self, detections, frame):
        """
        Updates tracks based on current frame's detections.

        Args:
            detections (List[Tuple(bbox, confidence, class_label)]):
                bbox: [x, y, w, h]
                confidence: float
                class_label: str

            frame (np.array): Current frame from video/camera.

        Returns:
            List of tracked objects with:
            - track_id
            - class_label
            - bbox: left, top, right, bottom
        """
        active_tracks = []
        tracks = self.tracker.update_tracks(detections, frame=frame)

        for track in tracks:
            if not track.is_confirmed():
                continue

            track_id = track.track_id
            class_label = track.get_det_class()
            l, t, r, b = map(int, track.to_ltrb())

            active_tracks.append({
                "id": track_id,
                "label": class_label,
                "bbox": (l, t, r, b),
                "center": ((l + r) // 2, (t + b) // 2)
            })

        return active_tracks
