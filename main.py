from downloader import Downloader
from labeler import Labeler

if __name__ == "__main__":
    downloader = Downloader("apple", "data", img_count=5)
    downloader.download()
    labeler = Labeler("./data", ["apple", "not apple"], dataset_dir="def_not_data")
    labeler.label()
