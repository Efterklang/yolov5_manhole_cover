# filename cls confidence xmin ymin xmax ymax
from ultralytics import YOLO
import os
from json import loads


def predict_images(img_dir, model_path):

    model = YOLO(model_path)
    results = model(img_dir)

    model.predict(
        img_dir,
        iou=0.7,
        conf=0.75,
        augment=True,
        imgsz=640,
        device="0",
        max_det=10,
        agnostic_nms=True,
    )

    i = 1

    with open(str(model_path).split("/")[-1].replace(".", "") + ".txt", "w") as outfile:
        for res in results:
            file_name = res.path.split("/")[-1] 
            predictions = loads(res.tojson())
            for prediction in predictions:
                class_id = prediction["class"]
                confidence = prediction["confidence"]
                box = prediction["box"]
                x_min = int(box["x1"])
                y_min = int(box["y1"])
                x_max = int(box["x2"])
                y_max = int(box["y2"])
                outfile.write(
                f"{file_name} {class_id} {confidence} {x_min} {y_min} {x_max} {y_max}\n"
            )
            outfile.flush()
        i += 1


if __name__ == "__main__":
    predict_images("./temp", "./weight/best.pt")
