import os
import hashlib
from collections import defaultdict


class FileProcessor:
    """
    dir1: 第一个目录(datasets1/train/images)
    dir2: 第二个目录(datasets2/train/images)
    base_dir: 要删除的文件所在的目录(datasets2/dog/train/),同时删除img和label文件
    """

    def __init__(self, dir1, dir2, base_dir, block_size=65536):
        self.block_size = block_size
        self.dir1 = dir1
        self.dir2 = dir2
        self.base_dir = base_dir
        self.file_dict1 = None
        self.file_dict2 = None

    def calculate_hash(self, file_path):
        """
        Calculate the hash of a file
        """
        hash_algo = hashlib.sha256()
        with open(file_path, "rb") as f:
            while True:
                data = f.read(self.block_size)
                if not data:
                    break
                hash_algo.update(data)
        return hash_algo.hexdigest()

    def gen_hash_dict(self, directory):
        """
            Generate a dictionary of file hashes
        """
        file_dict = defaultdict(list)
        for foldername, subfolders, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(foldername, filename)
                file_hash = self.calculate_hash(filepath)
                file_dict[file_hash].append(filepath)
        return file_dict

    def remove_duplicates(self):
        if not self.file_dict1:
            self.file_dict1 = self.find_duplicates(self.dir1)
        if not self.file_dict2:
            self.file_dict2 = self.find_duplicates(self.dir2)

        duplicate_count = 0

        for file_hash, filepaths in self.file_dict1.items():
            if file_hash in self.file_dict2:
                duplicate_count += 1
                name = "".join(self.file_dict2[file_hash]).split("\\")[1].split(".")[0]
                txt_path = os.path.join(self.base_dir, "labels", name + ".txt")
                img_path = os.path.join(self.base_dir, "images", name + ".jpg")
                os.remove(img_path)
                os.remove(txt_path)

        print(f"Total number of removed duplicate files in {base}: {duplicate_count}")


if __name__ == "__main__":
    base = "datasets2/dog/train/"
    processor = FileProcessor("datasets1/train/images", "datasets2/train/images", base)
    processor.remove_duplicates()