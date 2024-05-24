import cv2
from os import path
from inference import YOLOv8
# import zmq
import os

# context = zmq.Context()
# socket = context.socket(zmq.REP)
# socket.bind("tcp://*:20050")


class ImagePredictor:
    def __init__(
        self, model_path="./weights/fc924.onnx", conf_thres=0.2, iou_thres=0.3
    ):
        self.detector = YOLOv8(model_path, conf_thres=conf_thres, iou_thres=iou_thres)
        self.db_index_map_class = {
            0: 0,  # 0  good
            1: 1,  # 1  broke
            2: 2,  # 2  lose
            3: 3,  # 3  uncovered
            4: 4,  # 4  circle
        }

    def list_to_string(self, input_list) -> str:
        value_list = [
            self.db_index_map_class[value]
            for value in input_list
            if self.db_index_map_class[value] != -1
        ]
        count = str(len(value_list))
        value_str = ",".join(str(i) for i in value_list) if count != "0" else "-1"
        return count + "\n" + value_str

    def predictImg(self, img_path):
        img = cv2.imread(img_path)
        boxes, scores, class_ids = self.detector(img)
        print(f"{path.abspath(img_path)}\n{self.list_to_string(class_ids)}")
        return f"{path.abspath(img_path)}\n{self.list_to_string(class_ids)}"


if __name__ == "__main__":
    predictor = ImagePredictor()
    while True:
        path = input()
        try:
            predictor.predictImg(path)
        except Exception as e:
            print(f"Error: An error occurred while predicting the image: {e}")
#     predictor = ImagePredictor()
#     while True:
#         # Wait for next request from client
#         message = socket.recv()
#         message = message.decode("utf-8")
#         print(f"Received request: {message}")
#         # 如果定义了环境变量就拼接根目录/upload,否则拼接/home/nbb/Documents/JiShe4C/upload
#         filePath = ""
#         if "DOCKER_FLAG" in os.environ:
#             filePath = "/upload/" + message
#         else:
#             filePath = "/home/nbb/Documents/JiShe4C/upload/" + message
#         rel = predictor.predictImg(filePath)
#         #  Send reply back to client
#         socket.send_string(rel)
