from glance.collectors import Collector

from glance.collectors.cpu import CPUInfo

class LoadedModules(Collector):
    pass


class _LoadedModules_Linux_3x(LoadedModules):
    @classmethod
    def for_platform(self):
        return {'class': 'posix', 'os': 'Linux', 'release': '3'}

    def _collect(self):
        with open('/proc/modules', 'r') as fp:
            data = [row.strip().split() for row in fp.read().strip().split("\n")]

        for row in data:
            if len(row) == 6:
                row.append(None)

            mod = dict(zip(
                ['name', 'size', 'use_count', 'dependencies', 'state', 'address', 'flags'],
                row
            ))
            mod['size'] = self.cast(mod['size'], int)
            mod['use_count'] = self.cast(mod['use_count'], int)
            mod['dependencies'] = [] if mod['dependencies'] == '-' else mod['dependencies'].split(',')
            mod['address'] = self.cast(mod['address'], int, 16)
            mod['flags'] = [] if mod['flags'] is None else list(iter(mod['flags'].lstrip('(').rstrip(')')))

            setattr(self, mod['name'], mod)


class Uptime(Collector):
    pass


class _Uptime_Linux(Uptime):
    def __init__(self, cpuinfo=None, threads=None, *args, **kwargs):
        super(_Uptime_Linux, self).__init__(*args, **kwargs)
        if threads:
            self.threads = threads
        elif not cpuinfo:
            cpuinfo = CPUInfo()
        self.threads = cpuinfo.threads

    @classmethod
    def for_platform(self):
        return {'class': 'posix', 'os': 'Linux'}

    def _collect(self):
        with open('/proc/uptime') as fp:
            self.uptime, self.idle_sum = fp.readline().strip().split()

        self.uptime = self.cast(self.uptime, float)
        self.idle_sum = self.cast(self.idle_sum, float)
        self.idle = self.idle_sum / float(self.threads)
