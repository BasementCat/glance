from glance.collectors import Collector

class FilesystemList(Collector):
    is_continuous = False


class _FilesystemList_Linux(FilesystemList):
    @classmethod
    def for_platform(self):
        return {'class': 'posix', 'os': 'Linux'}

    def _collect(self):
        with open('/proc/filesystems', 'r') as fp:
            data = [row.strip().split() for row in fp.read().strip().split("\n")]

        self.virtual = []
        self.block = []
        self.other = []

        for row in data:
            if len(row) == 1:
                self.block += row
            elif row[0] == 'nodev':
                self.virtual.append(row[1])
            else:
                self.other.append(row)
