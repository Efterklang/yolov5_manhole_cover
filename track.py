from ultralytics import YOLO

model = YOLO('path/to/best.pt')


res = model.track(
    source='path/to/video.mp4',  # can be a filename, RTSP or YouTube link
    show=True,  # show results
    tracker="bytetrack.yaml",
    conf=0.3,
)