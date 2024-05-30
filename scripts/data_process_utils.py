import logging
import os
import shutil
from collections import defaultdict
import random


class DatasetRetriever:
    def __init__(self, img_dir, lbl_dir):
        self.img_dir = img_dir
        self.lbl_dir = lbl_dir

    def find_missing_txt_files(self, remove=False):
        i = 0
        for img_file in os.listdir(self.img_dir):
            if img_file.endswith(".jpg"):
                base_name = os.path.splitext(img_file)[0]
                txt_file = os.path.join(self.lbl_dir, base_name + ".txt")
                if not os.path.isfile(txt_file):
                    # 如果不存在，打印.jpg文件名
                    if remove:
                        os.remove(os.path.join(self.img_dir, img_file))
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


class DatasetProcessor:

    def __init__(self, img_dir, lbl_dir, map_dict):
        """
        init_args:
        img_dir: str, path to the image directory
        lbl_dir: str, path to the label directory
        map_dict: dict, mapping from old number to new number
        """
        self.img_dir = img_dir
        self.lbl_dir = lbl_dir
        self.map_dict = map_dict

    def mapping_labels(self):
        """
        This function is used to correct the number mapping in the label files.
        """
        for foldername, subfolders, filenames in os.walk(self.lbl_dir):
            for filename in filenames:
                if filename.endswith(".txt"):
                    file_path = os.path.join(foldername, filename)
                    print(f"Processing file: {file_path}")
                    self.write_change_number(file_path)

    def change_number(self, line):
        """
        mapping_labels() helper function
        """
        for idx, char in enumerate(line):
            if char in self.map_dict:
                return line[:idx] + self.map_dict[char] + line[idx + 1 :]
        return line

    def write_change_number(self, filename):
        """
        mapping_labels() helper function
        """
        with open(filename, "r") as rf:
            lines = rf.readlines()

        with open(filename, "w") as wf:
            for line in lines:
                wf.write(self.change_number(line))

    def rename_files(self, prefix):
        """
        This function is used to rename the files in the image and label directories.
        format: prefix{label}_{number}
        """
        label_count = {
            "0": 0,
            "1": 0,
            "2": 0,
            "3": 0,
            "4": 0,
            "5": 0,
            "6": 0,
            "background": 0,
        }
        for foldername, subfolders, filenames in os.walk(self.lbl_dir):
            for filename in filenames:
                label_path = os.path.join(foldername, filename)
                with open(label_path, "r") as f:
                    label = f.readline().split(" ")[0]
                    if label == "":
                        print(label_path)
                        new_filename = "{:s}background{:05d}".format(
                            prefix, label_count["background"]
                        )
                    else:
                        try:
                            new_filename = "{:s}{:s}_{:05d}".format(
                                prefix, label, label_count[label]
                            )
                        except KeyError:
                            print(f"Label not found: {label}")
                            continue
                img_file_path = os.path.join(
                    self.img_dir, filename.replace(".txt", ".jpg")
                )

                if os.path.exists(img_file_path):
                    shutil.move(
                        img_file_path,
                        os.path.join(self.img_dir, new_filename + ".jpg"),
                    )  # rename img file
                    shutil.move(
                        label_path, os.path.join(self.lbl_dir, new_filename + ".txt")
                    )  # rename label file
                    if label == "":
                        label_count["background"] += 1
                    else:
                        label_count[label] += 1
                else:
                    print(f"Image file not found: {img_file_path}")

        for k, v in label_count.items():
            print(f"Total number of {k} files: {v}")

    def process_data_with_labels(self, label_num, mode="remove"):
        i = 0
        if mode == "remove":
            for file in os.listdir(self.lbl_dir):
                if file.endswith(".txt"):
                    file_name = os.path.splitext(os.path.basename(file))[0]
                    self.remove_labels(file_name, label_num)
                    i += 1
            print("Total number of removed data: ", i)
        elif mode == "move":
            for file in os.listdir(self.lbl_dir):
                if file.endswith(".txt"):
                    file_name = os.path.splitext(os.path.basename(file))[0]
                    self.move_labels(file_name, label_num, "datasets/Japan/val/")
                    i += 1
            print("Total number of removed data: ", i)

    def move_labels(self, file_name, label_num, dest_dir):
        file_lbl_path = os.path.join(self.lbl_dir, file_name + ".txt")
        file_img_path = os.path.join(self.img_dir, file_name + ".jpg")
        dest_lbl_path = os.path.join(dest_dir + "/labels", file_name + ".txt")
        dest_img_path = os.path.join(dest_dir + "/images", file_name + ".jpg")
        # random move
        random_num = random.randint(0, 3)
        if random_num == 0:
            with open(file_lbl_path, "r") as f:
                for line in f:
                    words = line.split()
                    if words[0].isdigit and words[0] == label_num:
                        try:
                            shutil.move(file_lbl_path, dest_lbl_path)
                            shutil.move(file_img_path, dest_img_path)
                        except FileNotFoundError as e:
                            print(f"Error in removing files: {e}")

    def remove_labels(self, file_name, label_num):
        file_lbl_path = os.path.join(self.lbl_dir, file_name + ".txt")
        file_img_path = os.path.join(self.img_dir, file_name + ".jpg")

        with open(file_lbl_path, "r") as f:
            for line in f:
                words = line.split()
                if words[0].isdigit and words[0] == label_num:
                    try:
                        os.remove(file_lbl_path)
                        os.remove(file_img_path)
                    except FileNotFoundError as e:
                        print(f"Error in removing files: {e}")


class DatasetClassifier:
    def __init__(self, lbl_path, img_path, output_path):
        self.lbl_path = lbl_path
        self.img_path = img_path
        self.output_path = output_path

    def create_directories(self, file_type, have_test):
        """
        创建目录的辅助函数，减少重复代码
        """
        # 创建目录结构
        if file_type == "images":
            directory_structure = [
                "train/images",
                "val/images",
            ]
            if have_test:
                directory_structure.append("test/images")
        elif file_type == "labels":
            directory_structure = [
                "train/labels",
                "val/labels",
            ]
            if have_test:
                directory_structure.append("test/labels")
        else:
            raise ValueError("Invalid file type")
        for dirpath in directory_structure:
            dir_path = os.path.join(self.output_path, dirpath)  # 使用字符串进行join操作
            os.makedirs(dir_path, exist_ok=True)

    def _classify(self, input_path, file_type, have_test=False):
        """
        classify() helper function
        """
        self.create_directories(file_type=file_type, have_test=have_test)

        i, j, k = 0, 0, 0
        for root, dirs, files in os.walk(input_path):
            for file in files:
                tag = os.path.splitext(file)[0]
                # 从字符串tag中找到第一个数字字符，赋给变量num。如果tag中没有数字字符，num赋值为None。
                num = next((char for char in reversed(tag) if char.isdigit()), None)
                
                if num == "3":
                    destination = "val"
                    i += 1
                elif num == "9" and have_test:
                    destination = "test"
                    j += 1
                else:
                    destination = "train"
                    k += 1
                
                src_file = os.path.join(root, file)
                dest_file = os.path.join(self.output_path, destination, file_type, file)
                shutil.move(src_file, dest_file)

        print(f"{input_path} is classified")
        print("Total number of train files: ", k)
        print("Total number of val files: ", i)
        print("Total number of test files: ", j)

    def classify(self):
        self._classify(self.lbl_path, file_type="labels")
        self._classify(self.img_path, file_type="images")


if __name__ == "__main__":
    print("Starting...")
