import cv2
from os import path
from inference import YOLOv8
import pika 

credentials = pika.PlainCredentials(username="root", password="")
connection = pika.BlockingConnection(
    pika.ConnectionParameters("", credentials=credentials)
)
channel = connection.channel()
channel.queue_declare("files")
channel.queue_declare("rels")

class ImagePredictor:
    def __init__(self, model_path="./models/js.onnx",conf_thres = 0.2,iou_thres =0.3):
        self.detector = YOLOv8(model_path, conf_thres=conf_thres, iou_thres=iou_thres)
        self.db_index_map_class = {
                0: -1,  # 0  good
                1: 1,  # 1  broke
                2: 2,  # 2  lose
                3: 3,  # 3  uncovered
                4: -1,  # 4  cracks
                5: 4,  # 5  pothole
                6: 5,  # 6  faded lane line
                7: 6,  # 7  accident
        }

    def list_to_string(self, input_list) -> str:
        value_list = [self.db_index_map_class[value] for value in input_list if self.db_index_map_class[value] != -1]
        count = str(len(value_list))
        value_str = ",".join(str(i) for i in value_list) if count != "0" else "-1"
        return count + "\n" + value_str

    def predictImg(self,img_path):
        img = cv2.imread(img_path)
        boxes, scores, class_ids = self.detector(img)
        print(f"{path.abspath(img_path)}\n{self.list_to_string(class_ids)}")

if __name__ == "__main__":
    predictor = ImagePredictor()
    
    channel.basic_consume(
        auto_ack=True,
        queue="files",
        on_message_callback=lambda ch, method, properties, body: predictor.predictImg(
            body.decode()
        ),
    )
    channel.start_consuming()
