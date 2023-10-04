import psutil


class memoryManage:
    total = 0
    used = 0
    free = 0

    def __init__(self, path):
        hdd = psutil.disk_usage(path)
        self.total = str(round(hdd.total / (2**30), 2))
        self.used = str(round(hdd.used / (2**30), 2))
        self.free = str(round(hdd.free / (2**30), 2))
