import xml.etree.ElementTree as ET
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


if __name__ == "__main__":
    path = "../datasets/xml"
    output = "../datasets/labels"
    parser = XMLParser(path, output)
    parser.genTxt()
