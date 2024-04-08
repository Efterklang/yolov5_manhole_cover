from ultralytics import YOLO

# Load a model
model = YOLO("/root/teamshare/weights/zhlast.pt")

# Customize validation settings
validation_results = model.val(
    data="./datasets.yaml", imgsz=640, conf=0.25, iou=0.6, device="0"
)
