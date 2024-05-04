from ultralytics import YOLO
from multiprocessing import Process, Queue
from os.path import basename, isfile
from json import loads
from sys import argv

class ImagePredictor:
    def __init__(self, model_path="./weights/js.pt", device_arg="0", confidence=0.35):
        self.model = YOLO(model_path)
        self.device_arg = device_arg
        self.confidence = confidence

    def parseJson(self, json_str) -> list:
        """
        Parses a JSON string and extracts the 'class' values from each object.
        Args:
            json_str (str): The JSON string to parse.
        Returns:

            list: A list of 'class' values extracted from the JSON objects.
        """
        map_class = {
            0: -1,  # 0  good
            1: 1,  # 1  broke
            2: 2,  # 2  lose
            3: 3,  # 3  uncovered
            4: -1,  # 4  cracks
            5: 4,  # 5  pothole
            6: 5,  # 6  faded lane line
            7: 6,  # 7  accident
        }
        json_data = loads(json_str)
        value_list = []
        for obj in json_data:
            original_value = obj.get("class", None)
            class_value = map_class[original_value]
            if class_value is not None and obj.get("confidence", 0) > self.confidence and class_value != -1:
                value_list.append(class_value)
        return value_list

    def list_to_string(self, input_list) -> str:
        """
        Converts a list of values to a string representation.
        Args:
            input_list (list): The list of values to be converted.
        Returns:
            str: count\n + The string representation of the input list.
        """
        count = str(len(input_list))
        if not input_list:  # 判断列表是否为空
            value_str = "-1"
        else:
            value_str = ",".join(str(i) for i in input_list)
        return count + "\n" + value_str

    def predictImg(self, image_path):
        res = self.model(image_path)
        self.model.predict(
            image_path,
            conf=self.confidence,
            device=self.device_arg,
            iou=0.7,
            imgsz=640,
            max_det=5,
            save=True,
            show_labels=True,
            show_boxes=True,
            show_conf=True,
        )
        value_list = []
        r = res[0]
        json_data = self.parseJson(r.tojson())
        list_string = self.list_to_string(json_data)
        file_name = basename(r.path)
        print(file_name + "\n" + list_string)


if __name__ == "__main__":
    predictor = ImagePredictor()
    while True:
        path = input()
        if not isfile(path):
            print(f"Error: {path} does not exist or is not a file.")
            continue
        try:
            predictor.predictImg(path)
        except Exception as e:
            print(f"Error: An error occurred while predicting the image: {e}")
