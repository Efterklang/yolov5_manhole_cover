# 递归清除__pycache__文件夹

import os
import shutil


def clean_pycache(path):
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if dir == "__pycache__":
                shutil.rmtree(os.path.join(root, dir))


clean_pycache(".")
