import os
import hashlib
from collections import defaultdict

# =================================================================================
# * calculate_hash 函数用于计算文件的哈希值                                            *
# * find_duplicates 函数用于生成给的目录下的 dict;                                     *
# * key为hash;value为file_path                                                     *
# * remove_duplicates 函数用于删除重复图片及其txt标注文件(根据sha256值判断是否重复)         *
# * args: directory1: 第一个目录(datasets1/dog/train/images)                        *
# *       base: 要删除的文件所在的目录(datasets2/dog/train/)                          *
# * example:                                                                      *
# * remove_duplicates("datasets1/dog/train/images", "datasets2/dog/train/")       *
# =================================================================================

class FileProcessor:
    def __init__(self, block_size=65536):
        self.block_size = block_size
        self.file_dict1 = None
        self.file_dict2 = None

    def calculate_hash(self, file_path):
        hash_algo = hashlib.sha256()
        with open(file_path, "rb") as f:
            while True:
                data = f.read(self.block_size)
                if not data:
                    break
                hash_algo.update(data)
        return hash_algo.hexdigest()

    def find_duplicates(self, directory):
        file_dict = defaultdict(list)
        for foldername, subfolders, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(foldername, filename)
                file_hash = self.calculate_hash(filepath)
                file_dict[file_hash].append(filepath)
        return file_dict

    def remove_duplicates(self, directory1, base):
        if not self.file_dict1:
            self.file_dict1 = self.find_duplicates(directory1)
        if not self.file_dict2:
            self.file_dict2 = self.find_duplicates(os.path.join(base, "images"))
        
        duplicate_count = 0
        for file_hash, filepaths in self.file_dict1.items():
            if file_hash in self.file_dict2:
                duplicate_count += 1
                name = "".join(self.file_dict2[file_hash]).split("\\")[1].split(".")[0]
                txt_path = os.path.join(base, "labels", name + ".txt")
                img_path = os.path.join(base, "images", name + ".jpg")
                os.remove(img_path)
                os.remove(txt_path)

        print(f"Total number of removed duplicate files in {base}: {duplicate_count}")


if __name__ == "__main__":
    processor = FileProcessor()
    processor.remove_duplicates("datasets1/dog/train/images", "datasets2/dog/train/")
