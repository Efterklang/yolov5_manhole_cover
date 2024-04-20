# | 类比编号 | 分类                  | 场景业务特点                                                           |
# | -------- | --------------------- | ---------------------------------------------------------------------- |
# | 0        | 井盖完好（good）      | 井盖及井圈都无破损并且完好盖在井上                                     |
# | 1        | 井盖破损（broke）     | 井盖外观出现裂缝、缺口、破洞等                                         |
# | 2        | 井盖缺失（lose）      | 井盖丢失，井口暴露                                                     |
# | 3        | 井盖未盖（uncovered） | 井盖发生倾斜、翘起、偏离井口没有覆盖完全，致使无法与井座严密闭合的情况 |
# | 4        | 井圈问题（circle）    | 井圈存在破损而井盖完好                                                 |
import os

# =================================================================================
# * mapping_labels 函数用于更正标签文件中的数字映射关系                                  *
# * mapping_labels 接受参数为txt文件所在的目录                                         *
# * change_number 与 write_change_number函数为 mapping_labels的辅助函数               *
# =================================================================================

def mapping_labels(directory):
    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(".txt"):
                file_path = os.path.join(foldername, filename)
                print(f"Processing file: {file_path}")
                write_change_number(file_path)

def change_number(line):
    map_dict = {"0": "1", "1": "4", "2": "0", "3": "2", "4": "3"}
    for idx, char in enumerate(line):
        if char in map_dict:
            return line[:idx] + map_dict[char] + line[idx + 1 :]
    return line


def write_change_number(filename):
    with open(filename, "r") as rf:
        lines = rf.readlines()

    with open(filename, "w") as wf:
        for line in lines:
            wf.write(change_number(line))


# =================================================================================
# * raname_files 函数用于对文件进行规范命名                                            *
# * args: directory_img: 图片文件所在的目录                                           *
# *       directory_lbl: 标签文件所在的目录                                           *
# =================================================================================


def rename_files(directory_img, directory_lbl):
    label_count = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0}
    for foldername, subfolders, filenames in os.walk(directory_lbl):
        for filename in filenames:
            label_path = os.path.join(foldername, filename)
            with open(label_path, "r") as f:
                label = f.readline().split(" ")[0]
                if label == "":
                    print(label_path)
                new_filename = "z2well{:s}_{:05d}".format(label, label_count[label])

            file_path_img = os.path.join(
                directory_img, filename.replace(".txt", ".jpg")
            )

            if os.path.exists(file_path_img):
                shutil.move(
                    file_path_img,
                    os.path.join(directory_img, new_filename + ".jpg"),
                )
                shutil.move(
                    label_path, os.path.join(directory_lbl, new_filename + ".txt")
                )
                label_count[label] += 1
            else:
                print(f"Image file not found: {file_path_img}")

    for k, v in label_count.items():
        print(f"Total number of {k} files: {v}")


import shutil


# =================================================================================
# * classify 函数用于将文件按照一定的比例分为训练集、验证集和测试集(8:1:1)                  *
# * args: input: 数据集所在的目录                                                    *
# * Examples: datasets/manholecover/images/xxx.jpg,xxx.jpg                        *
# *   执行classify("./datasets/manholecover/images/")即可完成对图像集的划分            *
# =================================================================================


def classify(input):
    os.makedirs(input + "/train", exist_ok=True)
    os.makedirs(input + "/val", exist_ok=True)
    os.makedirs(input + "/test", exist_ok=True)
    i, j, k = 0,0,0
    for root, dirs, files in os.walk(input):
        for file in files:
            tag = file.split(".")[0][::-1]
            for char in tag:
                if char.isdigit():
                    last_number = char
                    break
            if last_number == "3":
                shutil.move(
                    os.path.join(root, file), os.path.join(input + "/val", file)
                )
                i += 1
            elif last_number == "9":
                shutil.move(
                    os.path.join(root, file), os.path.join(input + "/test", file)
                )
                j += 1
            else:
                shutil.move(
                    os.path.join(root, file), os.path.join(input + "/train", file)
                )
                k += 1
    print("Total number of train files: ", k)
    print("Total number of val files: ", i)
    print("Total number of test files: ", j)


# =================================================================================
# * find_missing_txt_files 函数用于查找在给定的目录中没有对应.txt文件的.jpg文件            *
# * arguments: img_dir: .jpg文件的目录                                              *
# *            lbl_dir: .txt文件的目录                                              *
# =================================================================================


def find_missing_txt_files(img_dir, lbl_dir):
    i = 0
    for img_file in os.listdir(img_dir):
        if img_file.endswith(".jpg"):
            base_name = os.path.splitext(img_file)[0]
            txt_file = os.path.join(lbl_dir, base_name + ".txt")
            if not os.path.isfile(txt_file):
                # 如果不存在，打印.jpg文件名
                print(base_name)
                i += 1
    print("Total number of missing files: ", i)


def compare_number_in_file_and_filename(inputpath):

    for foldername, subfolders, filenames in os.walk(inputpath):
        for filename in filenames:
            file_path_txt = os.path.join(foldername, filename)
            with open(file_path_txt, "r") as f:
                label = f.readline().split(" ")[0]
                # print(label)
                file_tag = filename.split("_")[0][-1]
                if label != file_tag:
                    print(file_path_txt)



import os
import shutil
from collections import defaultdict

class DatasetProcessor:
    def __init__(self, map_dict={"0": "1", "1": "4", "2": "0", "3": "2", "4": "3"}):
        self.map_dict = map_dict

    def mapping_labels(self, directory):
        for foldername, subfolders, filenames in os.walk(directory):
            for filename in filenames:
                if filename.endswith(".txt"):
                    file_path = os.path.join(foldername, filename)
                    print(f"Processing file: {file_path}")
                    self.write_change_number(file_path)

    def change_number(self, line):
        for idx, char in enumerate(line):
            if char in self.map_dict:
                return line[:idx] + self.map_dict[char] + line[idx + 1 :]
        return line

    def write_change_number(self, filename):
        with open(filename, "r") as rf:
            lines = rf.readlines()

        with open(filename, "w") as wf:
            for line in lines:
                wf.write(self.change_number(line))

    def rename_files(self, directory_img, directory_lbl):
        label_count = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0}
        for foldername, subfolders, filenames in os.walk(directory_lbl):
            for filename in filenames:
                label_path = os.path.join(foldername, filename)
                with open(label_path, "r") as f:
                    label = f.readline().split(" ")[0]
                    if label == "":
                        print(label_path)
                    new_filename = "z2well{:s}_{:05d}".format(label, label_count[label])

                file_path_img = os.path.join(
                    directory_img, filename.replace(".txt", ".jpg")
                )

                if os.path.exists(file_path_img):
                    shutil.move(
                        file_path_img,
                        os.path.join(directory_img, new_filename + ".jpg"),
                    )
                    shutil.move(
                        label_path, os.path.join(directory_lbl, new_filename + ".txt")
                    )
                    label_count[label] += 1
                else:
                    print(f"Image file not found: {file_path_img}")

        for k, v in label_count.items():
            print(f"Total number of {k} files: {v}")

    def classify(self, input):
        os.makedirs(input + "/train", exist_ok=True)
        os.makedirs(input + "/val", exist_ok=True)
        os.makedirs(input + "/test", exist_ok=True)
        i, j, k = 0,0,0
        for root, dirs, files in os.walk(input):
            for file in files:
                tag = file.split(".")[0][::-1]
                for char in tag:
                    if char.isdigit():
                        last_number = char
                        break
                if last_number == "3":
                    shutil.move(
                        os.path.join(root, file), os.path.join(input + "/val", file)
                    )
                    i += 1
                elif last_number == "9":
                    shutil.move(
                        os.path.join(root, file), os.path.join(input + "/test", file)
                    )
                    j += 1
                else:
                    shutil.move(
                        os.path.join(root, file), os.path.join(input + "/train", file)
                    )
                    k += 1
        print("Total number of train files: ", k)
        print("Total number of val files: ", i)
        print("Total number of test files: ", j)

    def find_missing_txt_files(self, img_dir, lbl_dir):
        i = 0
        for img_file in os.listdir(img_dir):
            if img_file.endswith(".jpg"):
                base_name = os.path.splitext(img_file)[0]
                txt_file = os.path.join(lbl_dir, base_name + ".txt")
                if not os.path.isfile(txt_file):
                    # 如果不存在，打印.jpg文件名
                    print(base_name)
                    i += 1
        print("Total number of missing files: ", i)

    def compare_number_in_file_and_filename(self, inputpath):
        for foldername, subfolders, filenames in os.walk(inputpath):
            for filename in filenames:
                file_path_txt = os.path.join(foldername, filename)
                with open(file_path_txt, "r") as f:
                    label = f.readline().split(" ")[0]
                    # print(label)
                    file_tag = filename.split("_")[0][-1]
                    if label != file_tag:
                        print(file_path_txt)



if __name__ == "__main__":
    processor = DatasetProcessor()
    # processor.mapping_labels("../dog/labels")
    # processor.rename_files("../dog/images", "../dog/labels")
    # processor.classify("./datasets/manholecover/images/")
    # processor.find_missing_txt_files("./img_dir", "./lbl_dir")
    # processor.compare_number_in_file_and_filename("./inputpath")
    # processor.remove_duplicates("./datasets1/dog/train/images", "./datasets2/dog/train/")
