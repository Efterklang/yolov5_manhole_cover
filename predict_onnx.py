import cv2
from os import path
from inference import YOLOv8

class ImagePredictor:
    def __init__(self, model_path="./weights/fc924.onnx", conf_thres=0.2, iou_thres=0.3):
        self.detector = YOLOv8(model_path, conf_thres=conf_thres, iou_thres=iou_thres)

    def list_to_string(self, input_list) -> str:
        count = str(len(input_list))
        if count == 0:  # 判断列表是否为空
            value_str = "-1"
        else:
            value_str = ",".join(str(i) for i in input_list)
        return count + "\n" + value_str

    def predictImg(self, img_path):
        img = cv2.imread(img_path)
        boxes, scores, class_ids = self.detector(img)
        print(f"{path.abspath(img_path)}\n{self.list_to_string(class_ids)}")


if __name__ == "__main__":
    predictor = ImagePredictor()
    # Test
    while True:
        img_path = input()
        try:
            predictor.predictImg(img_path)
        except Exception as e:
            print(f"Error: An error occurred while predicting the image: {e}")
