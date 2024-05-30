import imageio as iio
import numpy as np
import imgaug as ia
from imgaug import augmenters as iaa
import os


class WeatherSimulator:
    def __init__(self):
        self.seq = iaa.OneOf(
            [
                iaa.Fog(seed=0),
                iaa.Rain(drop_size=(0.09, 0.09), speed=(0.4, 0.9)),
                iaa.FastSnowyLandscape(
                    lightness_threshold=(100, 255), lightness_multiplier=(1.0, 4.0)
                ),
                iaa.MultiplyBrightness(mul=(0.5, 0.7)),
                iaa.MultiplyBrightness(mul=(1, 1.5)),
            ]
        )

        self.image_arrays = []
        self.filename_arrays = []

    def init_path(self, data_path):
        image_extensions = [".jpg", ".jpeg", ".png", ".bmp"]

        for root, dirs, files in os.walk(data_path):
            for file in files:
                if any(file.endswith(ext) for ext in image_extensions):
                    image_path = os.path.join(root, file)
                    base_name = os.path.splitext(file)[0]
                    ext_name = os.path.splitext(file)[1]
                    new_name = f"{base_name}_aug{ext_name}"
                    try:
                        image = iio.v3.imread(image_path)
                        self.filename_arrays.append(new_name)
                        self.image_arrays.append(image)
                    except Exception as e:
                        print(f"Error loading {image_path}: {e}")

    def apply_effect(self, data_path):
        """
        Apply effect to an image.
        :param data_path: Path to the input images.
        :return: The image after applying the effect.
        """
        self.init_path(data_path)

        images_aug = self.seq(images=self.image_arrays)

        i = 0
        for img in images_aug:
            iio.imwrite(f"{i}_{self.filename_arrays[i]}", img)

            i += 1


if __name__ == "__main__":
    weather_simulator = WeatherSimulator()
    weather_simulator.apply_effect("./data/images/")
