import xml.etree.ElementTree as ET
import os
from PIL import Image

label = {
    'good': 0,
    'broke': 1,
    'lose': 2,
    'uncovered': 3,
    'circle': 4
}

def parse_xml(xml_file)->str:
    tree = ET.parse(xml_file)
    root = tree.getroot()

    filename = root.find('filename').text
    img = Image.open('./datasets/images/train/' + filename)
    width, height = img.size

    info = []

    for obj in root.findall('object'):
        
        object_class = label[obj.find('name').text]
        
        bndbox = obj.find('bndbox')
        
        xmin = bndbox.find('xmin').text
        ymin = bndbox.find('ymin').text
        xmax = bndbox.find('xmax').text
        ymax = bndbox.find('ymax').text

        x_center = (int(xmin) + int(xmax)) / 2 / width
        y_center = (int(ymin) + int(ymax)) / 2 / height
        bnd_height = (int(ymax) - int(ymin)) / height
        bnd_width = (int(xmax) - int(xmin)) / width
        
        info.append(f"{object_class} {(int(xmin) + int(xmax)) / 2 / width} {y_center} {bnd_width} {bnd_height}")

    return info


def genTxt(path,output)->None:
    for root, dirs, files in os.walk(path):
        for file in files:
            f = file.split('.')[0] # remove the extension
            infos = parse_xml(os.path.join(root, file))
            with open(output + '/' +  f + '.txt', 'w') as f:
                for info in infos:
                    f.write(info + '\n')

if __name__ == '__main__':
    print('Start parsing xmls...')
    path = 'datasets/train_xmls'
    output = 'datasets/labels/train'
    genTxt(path,output)
