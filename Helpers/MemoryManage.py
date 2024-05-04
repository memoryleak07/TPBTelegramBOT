import os


class memoryManage:
    total = ""
    used = ""
    free = ""
    error_message = "`Memory error`"

    def __init__(self, path):
        try:
            st = os.statvfs(path)
            self.total = round((st.f_frsize * st.f_blocks) / (1024 ** 3), 2)
            self.free = round((st.f_frsize * st.f_bavail) / (1024 ** 3), 2)
            self.used = round(self.total - self.free, 2)
        except:
            self.total = self.free = self.used = self.error_message
