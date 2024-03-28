from PIL import Image
import os


def process_img(dir_path, output_path):
    for i in range(32, 36):
        file_name = f"well4_{i:04}.jpg"
        path = os.path.join(dir_path, file_name)
        if os.path.isfile(path):
            img = Image.open(path)
            img_rotated = img.rotate(90)
            img_horizontal = img.transpose(Image.FLIP_LEFT_RIGHT)
            img_vertical = img.transpose(Image.FLIP_TOP_BOTTOM)
            center_x = img.size[0] // 2
            center_y = img.size[1] // 2
            crop_size = min(img.size[0], img.size[1]) // 3
            img_cropped = img.crop(
                (
                    center_x - crop_size,
                    center_y - crop_size,
                    center_x + crop_size,
                    center_y + crop_size,
                )
            )

            img_rotated.save(output_path + f"well4_{i:04}_rotated.jpg")
            img_horizontal.save(output_path + f"well4_{i:04}_horizontal.jpg")
            img_vertical.save(output_path + f"well4_{i:04}_vertical.jpg")
            img_cropped.save(output_path + f"well4_{i:04}_cropped.jpg")


if __name__ == "__main__":
    process_img("./dataset/train/", "./dataset/train/Augmentation/circle/")
