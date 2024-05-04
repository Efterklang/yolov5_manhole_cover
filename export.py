from ultralytics import YOLO

model = YOLO("./weights/best.pt")  # load a custom trained model

# Export the model
model.export(format="onnx")
