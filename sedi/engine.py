import os
import re
import multiprocessing
from threading import Thread

import requests
from tqdm import tqdm

from .config import BAIDU_URL, USER_AGENT


class Baidu:
    def __init__(self, keyword, save_path):
        self.keyword = keyword
        self.save_path = save_path
        # Create a directory
        if not os.path.exists(save_path):
            os.mkdir(save_path)

        self.url = BAIDU_URL
        self.headers = {'User-Agent': USER_AGENT}

        self.img_list = []
        self.total = 2000
        self.offset = 0
        self.p_bar = tqdm(desc='searching', total=self.total)
        self.session = requests.Session()

    def request_image_list(self):
        while True:
            url = self.url.format(self.keyword, self.keyword, self.offset)
            response = self.session.get(url, headers=self.headers, timeout=5)

            img_names = re.findall('"fromPageTitleEnc":"(.*?)"', response.text)
            img_urls = re.findall('"thumbURL":"(.*?)"', response.text)

            if not img_urls:
                break

            # data = response.json()['data'][:-1]
            data = zip(img_names, img_urls)
            self.img_list.extend(data)

            self.offset += 30
            self.p_bar.update(30)

        self.p_bar.update(self.total - self.p_bar.n)
        self.p_bar.close()
        self.total = len(self.img_list)

    def download_image(self, url, filepath):
        try:
            response = self.session.get(url, headers=self.headers, timeout=3)

            with open(filepath, 'wb') as fp:
                fp.write(response.content)
        except requests.exceptions.ConnectTimeout:
            pass
        except OSError:
            pass

    def batch_download(self):
        while self.img_list:
            img_name, img_url = self.img_list.pop()
            # File naming rules
            img_name = re.sub(r'[\\/:*"<>|?]', '', img_name[:255])
            filepath = os.path.join(self.save_path, f'{img_name}.jpg')
            # Avoid repeated downloads
            if not os.path.exists(filepath):
                self.download_image(img_url, filepath)

            self.p_bar.update(1)

    def multithreading_download(self):
        self.p_bar = tqdm(desc='downloading', total=self.total)

        threads = []
        for _ in range(multiprocessing.cpu_count()):
            thread = Thread(target=self.batch_download)
            thread.start()
            threads.append(thread)
        [thread.join() for thread in threads]

        self.p_bar.close()

    def begin(self):
        self.request_image_list()
        self.multithreading_download()
