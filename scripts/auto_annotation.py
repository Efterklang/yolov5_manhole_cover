from ultralytics import YOLO
import os
import logging


def auto_annotation(
    img_dir, output_path, model_path="./weight/best.pt", confidence=0.75
):

    model = YOLO(model_path)
    res = model(img_dir)

    model.predict(
        img_dir,
        iou=0.7,
        conf=confidence,
        imgsz=640,
        device="0",
        max_det=5,
    )
    cnt = 0
    for r in res:
        cnt += 1
        if os.name == "nt":
            file_name = res.path.split("\\")[-1]
        else:
            file_name = res.path.split("/")[-1]

        r.save_txt(os.path.join(output_path, file_name.rsplit(".", 1)[0] + ".txt"))
        logger.info(f"Processed {cnt} images")

    logger.info("\033[92m[DONE]\033[0m labels were located at:" + output_path)


def traverse_dir(
    img_dir_path, output_path, model_path="./weight/best.pt", confidence=0.75
):
    os.makedirs(output_path, exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger = logging.getLogger(__name__)
    logger.info("\033[93m[INFO]\033[0m Start auto annotation")
    auto_annotation(
        img_dir=img_dir_path,
        output_path=output_path,
        model_path="../weight/best.pt",
        confidence=0.75,
    )
    auto_annotation(entry.path, output_path, model_path, confidence)


if __name__ == "__main__":
    traverse_dir("./test/images", "./test/labels")
