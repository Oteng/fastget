from __future__ import unicode_literals


class Downloader:
    def __init__(self):
        self.buffer = None

    def set_buffer(self, elapsed_time=None, bytes=None):
        new_min = max(bytes / 2.0, 1.0)
        new_max = min(max(bytes * 2.0, 1.0), 4194304)  # Do not surpass 4 MB
        if elapsed_time < 0.001:
            self.buffer = int(new_max)
        rate = bytes / elapsed_time
        if rate > new_max:
            self.buffer = int(new_max)
        if rate < new_min:
            self.buffer = int(new_min)
        self.buffer = int(rate)

    @staticmethod
    def change_header():
        raise NotImplementedError()