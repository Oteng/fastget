from __future__ import unicode_literals
import requests
import os
import Downloader
import time

"""
This file is for downloading files from http
and writing then to disk
"""


class HTTP(Downloader):
    def __init__(self, file_info):
        self.start = None
        self.end = None
        self.file_info = file_info
        self.file = None
        self.cal_offset()
        self.downloaded_byte = 0

    def download(self):
        data_handle = requests.get(self.file_info.data_url)
        data = data_handle.raw

        before = time.time()
        while True:
            # get a block of data from the server
            data_block = data.read(self.buffer if self.buffer is not None else 1024)
            self.downloaded_byte += len(data_block)

            # break out of loop when download is done
            if len(data_block) == 0:
                self.file.close()
                break

            # open file just in time
            if self.file is None:
                try:
                    self.file = open(self.file_info.file_name, "wb")
                    assert self.file is not None
                    self.file.seek(self.start, os.SEEK_CUR)
                except (IOError, OSError) as err:
                    print err
                    # raise error again because we controller to know that the file was not opened
                    raise

            # start writing
            try:
                self.file.write(data_block)
            except (IOError, OSError) as err:
                print err
                self.file.close()
                # raise error again because we controller to know that the file was not opened
                raise

            # measure the time it took to download and write to disk
            after = time.time()
            self.set_buffer(after - before, len(data_block))
            before = after

    def cal_offset(self):
        _range = self.file_info.range.split("-")
        self.start = int(_range[0])
        self.end = int(_range[1])

