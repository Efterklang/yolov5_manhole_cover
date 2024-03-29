from ultralytics import YOLO
import os
import logging


def auto_annotation(
    image_path, output_path, model_path="./weight/best.pt", confidence=0.75
):

    model = YOLO(model_path)
    res = model(image_path)

    model.predict(
        image_path,
        iou=0.7,
        conf=confidence,
        imgsz=640,
        device="0",
        max_det=5,
    )

    r = res[0]
    r.save_txt(
        os.path.join(output_path, os.path.basename(image_path).replace(".jpg", ".txt"))
    )


def traverse_dir(
    img_dir_path, output_path, model_path="./weight/best.pt", confidence=0.75
):
    os.makedirs(output_path, exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger = logging.getLogger(__name__)
    logger.info("\033[93m[INFO]\033[0m Start auto annotation")
    cnt = 0
    for entry in os.scandir(img_dir_path):
        if entry.is_file() and entry.name.endswith(".jpg"):
            auto_annotation(entry.path, output_path, model_path, confidence)
            cnt += 1
            logger.info(f"Processed {cnt} images")
    logger.info("\033[92m[DONE]\033[0m labels were located at:" + output_path)


if __name__ == "__main__":
    traverse_dir("./test/images", "./test/labels")
