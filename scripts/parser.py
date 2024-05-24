import xml.etree.ElementTree as ET
import csv
import os
import logging
from PIL import Image

label = {
    # TODO 'class_name': class_id
    "class_1": 0,
    "class_2": 1,
    "class_3": 2,
}


class XMLParser:
    def __init__(self, path, output):
        self.path = path
        self.output = output

    def parse_xml(self, xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        filename = root.find("filename").text
        img = Image.open("../datasets/images/" + filename)
        width, height = img.size

        info = []

        for obj in root.findall("object"):
            object_class = label[obj.find("name").text]
            bndbox = obj.find("bndbox")
            xmin = bndbox.find("xmin").text
            ymin = bndbox.find("ymin").text
            xmax = bndbox.find("xmax").text
            ymax = bndbox.find("ymax").text

            x_center = (int(xmin) + int(xmax)) / 2 / width
            y_center = (int(ymin) + int(ymax)) / 2 / height
            bnd_height = (int(ymax) - int(ymin)) / height
            bnd_width = (int(xmax) - int(xmin)) / width

            info.append(
                f"{object_class} {(int(xmin) + int(xmax)) / 2 / width} {y_center} {bnd_width} {bnd_height}"
            )

        return info

    def genTxt(self):
        """
        Generate txt files from xml files
        """
        for root, dirs, files in os.walk(self.path):
            for file in files:
                f = file.split(".")[0]  # remove the extension
                infos = self.parse_xml(os.path.join(root, file))
                with open(self.output + "/" + f + ".txt", "w") as f:
                    for info in infos:
                        f.write(info + "\n")


class CSVparser:
    """
    * Parse csv files to yolo format
    * from
    * xmin,ymin,xmax,ymax,Frame,class,Preview URL
    * to
    * class_id x_center y_center width height
    """

    def __init__(self, csv_path,img_path, output_path,map_dict = {
        "Car": 0,
        "Truck":1,
        "Pedestrian":2
    }):
        self.csv_path = csv_path
        self.img_path = img_path
        self.output_path = output_path
        self.map_dict = map_dict

    def parse_csv(self):
        with open(self.csv_path, "r") as csv_file:
            print("Parsing csv file... {csv_path}")
            reader = csv.reader(csv_file)
            next(reader)  # skip the header
            for row in reader:
                xmin, ymin, xmax, ymax, file_name, label, _ = row
                # get image width and height
                img = Image.open(f"{self.img_path}/{file_name}")
                base_name = file_name.split(".")[0]
                with open(f"{self.output_path}/{base_name}.txt", "a") as txt_file:
                    width, height = img.size
                    x_center = (int(xmin) + int(xmax)) / 2 / width
                    y_center = (int(ymin) + int(ymax)) / 2 / height
                    bnd_height = (int(ymax) - int(ymin)) / height
                    bnd_width = (int(xmax) - int(xmin)) / width
                    class_id = self.map_dict[label]
                    str = f"{class_id} {(int(xmin) + int(xmax)) / 2 / width} {y_center} {bnd_width} {bnd_height}\n"
                    txt_file.write(str)

if __name__ == "__main__":
    parser = CSVparser(
        "../datasets/object-detection-crowdai/labels_crowdai.csv",
        "../datasets/object-detection-crowdai/images",
        "../datasets/object-detection-crowdai/labels"
    )
    parser.parse_csv()
