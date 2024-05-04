import logging
import os
import shutil
from collections import defaultdict
import random


class DatasetRetriever:
    def __init__(self, img_dir, lbl_dir):
        self.img_dir = img_dir
        self.lbl_dir = lbl_dir

    def find_missing_txt_files(self):
        i = 0
        for img_file in os.listdir(self.img_dir):
            if img_file.endswith(".jpg"):
                base_name = os.path.splitext(img_file)[0]
                txt_file = os.path.join(self.lbl_dir, base_name + ".txt")
                if not os.path.isfile(txt_file):
                    # 如果不存在，打印.jpg文件名
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

    logger = logging.getLogger(__name__)

    def __init__(
        self,
        img_dir,
        lbl_dir,
        map_dict={"0": "5", "5": "5"},
    ):
        self.map_dict = map_dict
        self.img_dir = img_dir
        self.lbl_dir = lbl_dir

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
                    )
                    shutil.move(
                        label_path, os.path.join(self.lbl_dir, new_filename + ".txt")
                    )
                    if label == "":
                        label_count["background"] += 1
                    else:
                        label_count[label] += 1
                else:
                    print(f"Image file not found: {img_file_path}")

        for k, v in label_count.items():
            print(f"Total number of {k} files: {v}")

    def classify(self):
        """
        This function is used to classify the dataset into train, val, and test sets.
        """
        logger.info("Classifying the dataset(image) into train, val, and test sets.")
        classify_with_arguments(self.img_dir)
        logger.info("Classifying the dataset(label) into train, val, and test sets.")
        classify_with_arguments(self.lbl_dir)

    def classify_with_arguments(self, input):
        """
        classify() helper function
        """
        os.makedirs(input + "/train", exist_ok=True)
        os.makedirs(input + "/val", exist_ok=True)
        os.makedirs(input + "/test", exist_ok=True)
        i, j, k = 0, 0, 0
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

if __name__ == "__main__":
    img_dir = "datasets/Japan/train/images"
    lbl_dir = "datasets/Japan/train/labels"
    processor = DatasetProcessor(img_dir, lbl_dir)
    # DatasetRetriever(img_dir,lbl_2dir).find_missing_txt_files()
    # processor.mapping_labels()
    # processor.rename_files("pothole0")
