# filename cls confidence xmin ymin xmax ymax
from ultralytics import YOLO
import os
from json import loads


def predict_images(image_path):

    model = YOLO("./weight/best.pt")
    res = model(image_path)

    model.predict(
        image_path,
        iou=0.7,
        conf=0.75,
        imgsz=640,
        device="0",
        max_det=10,
    )

    return loads(res[0].tojson())


def process_directory(image_dir):
    # Get all jpg images in the directory
    image_files = [
        f for f in os.listdir(image_dir) if f.endswith(".jpg") or f.endswith(".png")
    ]

    with open("output.txt", "w") as outfile:
        for image_file in image_files:
            image_path = os.path.join(image_dir, image_file)

            predictions = predict_images(image_path)

            for prediction in predictions:
                class_id = prediction["class"]
                confidence = prediction["confidence"]
                box = prediction["box"]
                x_min = box["x1"]
                y_min = box["y1"]
                x_max = box["x2"]
                y_max = box["y2"]

                outfile.write(
                    f"{image_file} {class_id} {confidence} {x_min} {y_min} {x_max} {y_max}\n"
                )


if __name__ == "__main__":
    process_directory("./datasets/manholecover/test/")
