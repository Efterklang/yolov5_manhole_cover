# from ultralytics import YOLO

from ultralytics import YOLO
import json
import os


def parseJson(json_str, confidence) -> list:
    """
    Parses a JSON string and extracts the 'class' values from each object.
    Args:
        json_str (str): The JSON string to parse.
    Returns:

        list: A list of 'class' values extracted from the JSON objects.
    """
    map_class = {
        0: 1,  # 0  broke
        1: 2,  # 1  lose
        2: 3,  # 2  uncovered
        3: 6,  # 3  crack
        4: 7,  # 4  potholes
        5: 8,  # 5  模糊
    }
    json_data = json.loads(json_str)
    value_list = []
    for obj in json_data:
        original_value = obj.get("class", None)
        class_value = map_class[original_value]
        if class_value is not None and obj.get("confidence", 0) > confidence:
            value_list.append(class_value)
    return value_list


def list_to_string(input_list) -> str:
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


def predictImg(image_path, model_path="./weight/js.pt", device_arg="0", conf_arg=0.3):

    # 加载图片
    model = YOLO(model_path, "./weight/yolov8x.pt")
    res = model(image_path)

    model.predict(
        image_path,
        iou=0.7,
        conf=conf_arg,
        imgsz=640,
        device=device_arg,  # default:None; Options: 'cpu', '0', '0,1,2,3', ...
        max_det=5,
        augment=True,
        # visualize=True,
        save=True,
        show_labels=True,
        show_boxes=True,
        show_conf=True,
    )

    value_list = []
    r = res[0]
    from os.path import basename

    list_string = list_to_string(parseJson(r.tojson(), conf_arg))
    file_name = basename(r.path)
    print(file_name + "\n" + list_string)


if __name__ == "__main__":
    # import argparse
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--path", type=str, help="path to img")
    # parser.add_argument(
    #     "--model", type=str, default="./weight/best.pt", help="path to model"
    # )
    # args = parser.parse_args()
    # predictImg(args.path, args.model)
    # Example usage: python predict.py --path ./data/images/1.jpg
    # from sys import argv

    # path = argv[1]
    # predictImg(path)
    while True:
        path = input("输入图片路径：")
        if path == "exit":
            break
        predictImg(path)
