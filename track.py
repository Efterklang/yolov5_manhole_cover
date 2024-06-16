import cv2
from ultralytics import YOLO


class SpeedDetector:
    def __init__(
        self, video_path, model_path, tracker_path, focus, output_path, fps=30
    ):
        self.video_path = video_path
        self.model = YOLO(model_path)
        self.tracker_path = tracker_path
        self.output_path = output_path
        self.fps = fps
        self.focus = focus
        self.cap = cv2.VideoCapture(self.video_path)
        self.track_history = defaultdict(lambda: [])

    def capture_frames(self):

        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            # Read a frame from the video
            success, frame = cap.read()
            if success:
                # Run YOLOv9 tracking on the frame, persisting tracks between frames
                conf = 0.2
                iou = 0.5
                # Loop over each frame of the video and perform object detection and tracking
                for result in model.track(
                    frame,
                    persist=True,
                    conf=conf,
                    iou=iou,
                    show=False,
                    tracker="bytetrack.yaml",
                ):
                    names = result.names
                    classes = result.boxes.cls.tolist()
                    boxes = result.boxes.xywh.cpu()
                    track_ids = result.boxes.id.int().cpu().tolist()
                    for box, car_cls, track_id in zip(boxes, classes, track_ids):
                        if car_cls == "pedestrian":
                            alerter.alert_pedestrian()
                            break
                        x, y, w, h = box
                        car_type = names[int(car_cls)]
                        track = self.track_history[track_id]
                        track.append((float(x), float(y)))  # x, y center point
                        if len(track) > 30:  # retain 90 tracks for 90 frames
                            track.pop(0)
                            speed = get_speed(track, car_type, track_id)
                            self.detect_isDanger(speed)

    def get_pixel_height(self, box_height, car_type):
        actual_height = 1.5  # meter

        if car_type == "car":
            actual_height = 1.500
        elif car_type == "truck":
            actual_height = 3.496
        elif car_type == "bus":
            actual_height = 3.199
        elif car_type == "motorbike":
            actual_height = 1.199
        else:
            actual_height = 1.5  # TODO more types can be added
        # D = (F*W)/P
        meter_per_pixel = int((self.focus * actual_height) / (box_height - 2) / 1000)
        return meter_per_pixel

    def get_reletive_speed(self, car_type, track_id):
        speed = 0
        for tracker_id in detections.tracker_id:
            if len(self.track_history[tracker_id]) > self.fps:  # 每秒测定一次速度
                # calculate the speed
                track = self.track_history[track_id]
                coordinate_start = coordinates[tracker_id][-1]
                coordinate_end = coordinates[tracker_id][0]
                pixel_distance = abs(coordinate_start - coordinate_end)
                actual_distance = pixel_distance * self.get_pixel_height(
                    box_height, car_type
                )
                time = len(coordinates[tracker_id]) / video_info.fps
                speed = distance / time * 3.6
        return speed if speed > 0 else 0

    def detect_isDanger(self, speed):
        if speed < 5 or speed > 20:
            alerter.alert_speed()


class alerter:

    @staticmethod
    def alert_pedestrian(self):
        # call_api(type="pedestrian")
        pass

    def alert_speed(self):
        # call_api(type="speed")
        pass
