import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import sys
import os
from pathlib import Path


class Labeler:
    def __init__(self, img_directory, classes, dataset_dir=""):
        """

        :param img_directory:  The directory containing the images to label
        :type str
        :param classes: The classes to label the images with
        :type list
        :param dataset_dir: (Optional) The directory to move the images to, containing folders for each class
        :type str
        """
        self.img_directory = img_directory
        self.dataset_dir = dataset_dir
        self.classes = classes
        print(f"Classes are {self.classes}")
        if not os.path.exists(img_directory):
            raise Exception("Invalid img_directory")
        img_types = ["*.jpg", "*.png"]
        # Get the paths of all of the images in the img_directory that have an extension in img_types
        self.images = [img for img_ in [Path(img_directory).rglob(t) for t in img_types] for img in img_]
        self.labels = {}
        self.img_idx = 0
        self.label_idx = None

    def label(self):
        for image in self.images:
            fig, ax = plt.subplots()
            fig.canvas.mpl_connect('key_press_event', self.press_handler)
            print(f"Opening {image}")
            img = mpimg.imread(str(image))
            ax.imshow(img)
            # This only supports 10 classes for now
            label_opts = ", ".join([f"{i}: {label}" for i, label in enumerate(self.classes)])
            plt.title(label_opts)
            plt.show()
        plt.close(fig)
        self.write_labels()

    def write_labels(self):
        print("writing labels")
        if not self.dataset_dir == "":
            self.move_files()
        label_dir = self.dataset_dir if not self.dataset_dir == "" else self.img_directory
        with open(os.path.join(label_dir, "labels.txt"), "w") as label_file:
            for label in self.labels.keys():
                for file in self.labels[label]:
                    label_file.write(f"{file}: {label}\n")
        print("Labels written")

    def move_files(self):
        if not os.path.exists(self.dataset_dir):
            os.mkdir(self.dataset_dir)
        for c in self.labels.keys():
            if not os.path.exists(os.path.join(self.dataset_dir, c)):
                os.mkdir(os.path.join(self.dataset_dir, c))
            for i, file in enumerate(self.labels[c]):
                filename = file.split('/')[-1]
                dest = os.path.join(self.dataset_dir, c, filename)
                self.labels[c][i] = dest
                print(f"Moving {file} to {dest}")
                os.rename(file, dest)

    def press_handler(self, event):
        self.label_idx = int(event.key)
        img_label = self.classes[self.label_idx]
        print(f"You labeled {self.images[self.img_idx]} as {img_label}")
        plt.close()
        if img_label not in self.labels:
            self.labels[img_label] = []
        self.labels[img_label].append(str(self.images[self.img_idx]))
        sys.stdout.flush()
        self.img_idx += 1


if __name__ == "__main__":
    labeler = Labeler("./data", ["apple", "not apple"], dataset_dir="def_not_data")
    labeler.label()
