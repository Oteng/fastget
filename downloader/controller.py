from __future__ import unicode_literals
import requests


class Controller:
    def __init__(self, file_info):
        self.file_info = file_info
        self.data_header = None
        self.set_data_header()
        self.num_threads = 4

    def set_data_header(self):
        self.data_header = requests.head(self.file_info["url"], headers=self.file_info["http_headers"]).headers


    def create_threads(self):
        file_size = int(self.data_header["Content-Length"])
        segment_size = file_size / self.num_threads
        tmp = segment_size * (self.num_threads - 1)
        last_segment_size = file_size - tmp
