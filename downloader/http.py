from __future__ import unicode_literals
from __future__ import with_statement
import requests
import os
import Downloader

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
        self.file_name = file_info.file_name
        self.cal_offset()
        self.downloaded_byte = 0

    def download(self):
        data_handle = requests.get(self.file_info.data_url)
        data = data_handle.raw
        while True:
            # get a block of data from the server
            data_block = data.read(self.get_buffer())
            self.downloaded_byte += len(data_block)

            # break out of loop when download is done
            if len(data_block) == 0:
                self.file.close()
                break

            # open file just in time
            if self.file is None:
                try:
                    self.file = open(self.file_name, "wb")
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

    def cal_offset(self):
        _range = self.file_info.range.split("-")
        self.start = _range[0]
        self.end = _range[1]

    def get_buffer(self):
        raise NotImplementedError("get return the right buffer")
