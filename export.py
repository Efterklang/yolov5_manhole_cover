from ultralytics import YOLO

# Load a model
model = YOLO("yolov8x.pt")  # load an official model
model = YOLO("weight/best.pt")  # load a custom trained model

# Export the model
model.export(format="onnx")
