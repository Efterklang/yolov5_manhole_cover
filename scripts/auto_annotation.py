from ultralytics import YOLO
import os
import logging

from ultralytics import YOLO
import os
import logging

class AutoAnnotator:
    def __init__(self, model_path="./weights/best.pt", confidence=0.75, imgsz=640, device="0", max_det=5, iou=0.7):
        self.model = YOLO(model_path)
        self.confidence = confidence
        self.imgsz = imgsz
        self.device = device
        self.max_det = max_det
        self.iou = iou
        logging.basicConfig(level=logging.INFO, format="%(message)s")
        self.logger = logging.getLogger(__name__)

    def annotate_image(self, img_path, output_path):
        res = self.model(img_path)
        self.model.predict(img_path, self.iou, self.confidence, self.imgsz, self.device, self.max_det)
        if os.name == "nt":
            file_name = res.path.split("\\")[-1]
        else:
            file_name = res.path.split("/")[-1]
        res.save_txt(os.path.join(output_path, file_name.rsplit(".", 1)[0] + ".txt"))

    def annotate_directory(self, img_dir_path, output_path):
        os.makedirs(output_path, exist_ok=True)
        self.logger.info("\033[93m[INFO]\033[0m Start auto annotation")
        cnt = 0
        for entry in os.scandir(img_dir_path):
            if entry.is_file():
                self.annotate_image(entry.path, output_path)
                cnt += 1
                self.logger.info(f"Processed {cnt} images")
        self.logger.info("\033[92m[DONE]\033[0m labels were located at:" + output_path)


if __name__ == "__main__":
    annotator = AutoAnnotator(model_path="./weights/best.pt", confidence=0.75)
    annotator.annotate_directory("./datasets/images", "./datasets/labels")
