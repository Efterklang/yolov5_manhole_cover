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

    def list_to_string(self, input_list) -> str:
        count = str(len(input_list))
        if count == 0:  # 判断列表是否为空
            value_str = "-1"
        else:
            value_str = ",".join(str(i) for i in input_list)
        return count + "\n" + value_str

    def predictImg(self,img_path):
        img = cv2.imread(img_path)
        boxes, scores, class_ids = self.detector(img)
        print(f"{path.abspath(img_path)}\n{self.list_to_string(class_ids)}")

if __name__ == "__main__":
    predictor = ImagePredictor()
    # Test 
    # while True:
    #     img_path = input()
    #     try:
    #         predictor.predictImg(img_path)
    #     except Exception as e:
    #         print(f"Error: An error occurred while predicting the image: {e}")
    
    channel.basic_consume(
        auto_ack=True,
        queue="files",
        on_message_callback=lambda ch, method, properties, body: predictor.predictImg(
            body.decode()
        ),
    )
    channel.start_consuming()
