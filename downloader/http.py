from __future__ import unicode_literals
import requests
import os
from download import Downloader
import time



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
        # TODO: check status code and report reason for aborting download to controller
        data_handle = requests.get(self.file_info["data_url"], headers=self.file_info["header"], stream=True)
        data = data_handle.raw

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
