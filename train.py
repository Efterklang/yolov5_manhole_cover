from ultralytics import YOLO
from ultralytics import settings


settings.update({"datasets_dir": "./datasets", "weights_dir": "./weight"})
print(settings)
model = YOLO('yolov8-MobileNetV3.yaml')
model.load("./weight/yolov8x.pt")
results = model.train(
    data="jtdatasets.yaml",
    epochs=3,
    patience=100,
    imgsz=640,
    batch=-1,
    save=True,
    device="cpu",
    plots=True,
    cache=True,
    verbose=True,
    # Augmentation
    degrees=90,
    shear=10,
    perspective=0.001,
    flipud=0.5,
    mixup=0.5,
    copy_paste=0.5,
)
