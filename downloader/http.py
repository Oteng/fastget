from __future__ import unicode_literals

import os
import time

import requests

from download import Downloader
from utils import (
    get_next_user_agent,
)


class HTTP(Downloader):
    """
    this class represent a single instance of the downloading of a file.
    multiple instances of this class running multiple threads that is how it works
    It does this by downloading a particular segment of a file specified by the content-range
    header
    """

    def __init__(self, file_info):
        Downloader.__init__(self)
        self.start = None
        self.end = None
        self.file_info = file_info
        self.file = None
        self.cal_offset()
        self.downloaded_byte = 0

    def download(self):
        # TODO: signal controller of status and errors if donwload has to exist
        retrys = 5
        data = None
        while retrys > 0:
            # try to get a connection to the server
            data_handle = requests.get(self.file_info["data_url"], headers=self.file_info["header"], stream=True)
            # check status code

            # this status code should be seen since controller will check if resum is posisble
            if data_handle.status_code == 416:
                raise Exception("Resume not possible" + data_handle.status_code)

            # unexpected error
            if data_handle.status_code < 500 or data_handle.status_code >= 600:
                raise Exception("Unexpected error" + data_handle.status_code)

            if data_handle.status_code >= 500 or data_handle.status_code < 600:
                # the server has a problem or it is trying to refuse our connection
                # pretend to be a new user and try again (find a way to change ip for ip tracking servers)
                self.file_info["header"] = self.file_info["header"]["User-Agent"] = get_next_user_agent()
                retrys -= 1
                continue

            data = data_handle.raw
            break

        before = time.time()
        while True:
            # get a block of data from the server
            data_block = data.read(self.buffer if self.buffer is not None else min((self.end - self.start), 1024))
            self.downloaded_byte += len(data_block)
            print self.buffer
            # break out of loop when download is done
            if len(data_block) == 0:
                self.file.close()
                break

            # open file just in time
            if self.file is None:
                try:
                    self.file = open(self.file_info["file_name"], "wb")
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
        _range = self.file_info["range"].split("-")
        self.start = int(_range[0])
        self.end = int(_range[1])
