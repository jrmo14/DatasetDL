from bs4 import BeautifulSoup
import requests
import json
import os
from urllib.request import Request, urlopen


class Downloader:
    def __init__(self, search_terms: str, download_dir: str, img_count: int = 100):
        """

        :param search_terms: A list of terms or single term to search for
        :param download_dir: Where to put the files
        :param img_count: How many images to download
        """
        self.download_dir = download_dir
        self.img_count = img_count
        self.paths = []
        self.searches = []
        if type(search_terms) == str:
            self.searches.append(f"https://google.com/search?q={search_terms.replace(' ', '+')}&source=lnms&tbm=isch")
        if type(search_terms) == list:
            for term in search_terms:
                if type(term) == str:
                    self.searches.append(f"https://google.com/search?q={term.replace(' ', '+')}&source=lnms&tbm=isch")
        self.request_header = {'User-Agent':
                                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        if not os.path.exists(download_dir):
            print(f"Making folder: {download_dir}")
            os.mkdir(download_dir)

    def download(self):
        for term in self.searches:
            download_count = self.download_term(term)
            print(f"Downloaded {download_count} imgs")

    def download_term(self, term: str) -> int:
        """
        This function actually does the searching, downloading and image saving
        :param term: The term to search for
        :return: The number of images successfully downloaded
        """
        soup = BeautifulSoup(requests.get(term, headers=self.request_header).text, 'html.parser')
        imgs = [(json.loads(j.text)["ou"], json.loads(j.text)["ity"]) for j in
                soup.find_all("div", {"class": "rg_meta"})]
        download_count = 0
        for i, (img_url, img_type) in enumerate(imgs[:self.img_count]):
            print(f"Trying to download image {i} from {img_url}")
            try:
                raw_img = urlopen(Request(img_url, headers=self.request_header)).read()
                if len(img_type) == 0:
                    print(f"FORCING JPG for {i}")
                    img_type = 'jpg'
                with open(os.path.join(self.download_dir, f"img_{i}.{img_type}"), "wb") as file:
                    file.write(raw_img)
                download_count += 1
            except Exception as ex:
                print(f"Couldn't download {img_url}")
                print(ex)
        return download_count


if __name__ == "__main__":
    downloader = Downloader("apple", "data", img_count=5)
    downloader.download()
