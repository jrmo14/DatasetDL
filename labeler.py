#!/usr/bin/env python3
import cv2
import sys
import os
from pathlib import Path
import argparse
import shutil


class Labeler:
    def __init__(self, img_dir, classes, output_dir):
        """

              :param img_dir:  The directory containing the images to label
              :type str
              :param classes: The classes to label the images with
              :type list
              :param output_dir: (Optional) The directory to move the images to, containing folders for each class
              :type str
              """
        self.img_directory = img_dir
        self.dataset_dir = output_dir
        self.classes = classes
        print(f"Classes are {self.classes}")
        if not os.path.exists(self.img_directory):
            raise Exception("Invalid img_directory")
        img_types = ["*.jpg", "*.png"]
        # Get the paths of all of the images in the img_directory that have an extension in img_types
        self.image_paths = [img for img_ in [Path(self.img_directory).rglob(t) for t in img_types] for img in img_]
        self.labels = {}
        self.img_idx = 0
        self.label_idx = None

    def label(self):
        label_opts = {}
        for i, label in enumerate(self.classes):
            label_opts[i + 1] = label
            folder_path = os.path.join(self.dataset_dir, label)
            try:
                os.mkdir(folder_path)
            except FileExistsError:
                pass
        valid_keys = [str(i + 1) for i in range(len(self.classes))]
        valid_keys.append('d')
        for image_path in self.image_paths:
            img = cv2.imread(str(image_path))
            cv2.imshow(str(label_opts), img)
            key = chr(cv2.waitKey(0))
            while key not in valid_keys:
                print(f"Press a valid key: {label_opts}, d")
                key = chr(cv2.waitKey(0))
            if key == 'd':
                print(f"You dropped {image_path.name}")
                continue
            key = int(key)
            file_name = image_path.name
            print(f"You labeled {image_path.name} as {label_opts[key]}")
            destination = os.path.join(self.dataset_dir, label_opts[key], file_name)

            print(f"Move {image_path} to {destination}")
            shutil.copyfile(str(image_path), destination)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script for labeling recognition data")
    parser.add_argument('--input_dir', '-i', default='./data')
    parser.add_argument('--output_dir', '-o', default='./labeled_data')
    parser.add_argument('--labels', '-l', nargs='+', help='<REQUIRED> The labels for data', required=True)
    args = parser.parse_args()

    labeler = Labeler(args.input_dir, args.labels, args.output_dir)
    labeler.label()
