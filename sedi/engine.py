import os
import re
import multiprocessing
from json import loads
from threading import Thread
from abc import abstractmethod
from typing import List, Tuple

import requests
from requests import Response
from tqdm import tqdm

from sedi.config import USER_AGENT, BAIDU_URL, SOGOU_URL, T360_URL


class SearchEngine:
    def __init__(self, keyword: str, save_path: str):
        self.keyword = keyword
        self.save_path = save_path
        # Create a directory
        if not os.path.exists(save_path):
            os.mkdir(save_path)

        self.url = ''
        self.name = ''
        self.headers = {'User-Agent': USER_AGENT}

        self.img_list = []
        self.total = 0
        self.current = 0
        self.offset = 0
        self.p_bar = tqdm(desc='Searching')
        self.session = requests.Session()

    @abstractmethod
    def extract_image_list(self, response: Response) -> List[Tuple[str, str]]:
        pass

    def request_image_list(self):
        while True:
            url = self.url.format(keyword=self.keyword, current=self.current, offset=self.offset)
            response = self.session.get(url, headers=self.headers, timeout=5)

            data = self.extract_image_list(response)

            if not data:
                break

            self.img_list.extend(data)

            self.current += self.offset
            self.p_bar.update(len(data))

        self.p_bar.close()
        self.total = len(self.img_list)

    def download_image(self, url: str, filepath: str):
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
        self.p_bar = tqdm(desc=f'[{self.name}] Downloading', total=self.total)

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


class Baidu(SearchEngine):
    def __init__(self, keyword: str, save_path: str):
        super().__init__(keyword, save_path)
        self.url = BAIDU_URL
        self.name = 'baidu'
        self.offset = 60

    def extract_image_list(self, response: Response) -> List[Tuple[str, str]]:
        img_names = re.findall('"fromPageTitleEnc":"(.*?)"', response.text)
        img_urls = re.findall('"thumbURL":"(.*?)"', response.text)

        return list(zip(img_names, img_urls))


class Sogou(SearchEngine):
    def __init__(self, keyword: str, save_path: str):
        super().__init__(keyword, save_path)
        self.url = SOGOU_URL
        self.name = 'sogou'
        self.offset = 100

    def extract_image_list(self, response: Response) -> List[Tuple[str, str]]:
        data = loads(response.text)['data']
        return [(item['title'], item['picUrl']) for item in data['items']] if data else []


class T360(SearchEngine):
    def __init__(self, keyword: str, save_path: str):
        super().__init__(keyword, save_path)
        self.url = T360_URL
        self.name = '360'
        self.offset = 100

    def extract_image_list(self, response: Response) -> List[Tuple[str, str]]:
        data = loads(response.text)['list']
        return [(item['title'], item['thumb']) for item in data]
