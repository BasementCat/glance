from glance.collectors import Collector

class CPUInfo(Collector):
    is_continuous = False


class _CPUInfo_Linux(CPUInfo):
    @classmethod
    def for_platform(self):
        return {'class': 'posix', 'os': 'Linux'}

    def _collect(self):
        with open('/proc/cpuinfo', 'r') as fp:
            data = [section.strip().split("\n") for section in fp.read().strip().split("\n\n")]

        self.threads = len(data)
        data = {k.strip(): v.strip() for k, v in [row.split(':', 1) for row in data[0]]}
        self.vendor = data.get('vendor_id', None)
        self.family_id = self.cast(data.get('cpu family', None), int)
        self.model_id = self.cast(data.get('model', None), int)
        self.model_name = data.get('model name')
        self.stepping = self.cast(data.get('stepping', None), int)
        self.speed_mhz = self.cast(data.get('cpu MHz', None), float)
        self.cache_size_bytes = None
        _cache_size = data.get('cache size', None)
        if _cache_size:
            _cache_size = _cache_size.split(' ', 1)
            self.cache_size_bytes = int(self.conv(_cache_size[0], 'datasize', _cache_size[1], 'B'))
        self.cpus = int(self.threads / self.cast(data.get('siblings'), int))
        self.cores = self.cast(data.get('cpu cores'), int)
        self.has_fpu = True if data.get('fpu') == 'yes' else False
        self.has_fpu_exception = True if data.get('fpu_exception') == 'yes' else False
        self.flags = data.get('flags', '').split(' ')
        self.bogomips = self.cast(data.get('bogomips'), float)


class Load(Collector):
    pass


class _Load_Linux(Load):
    @classmethod
    def for_platform(self):
        return {'class': 'posix', 'os': 'Linux'}

    def _collect(self):
        with open('/proc/loadavg', 'r') as fp:
            data = [row.strip().split() for row in fp.read().strip().split("\n")]

        for row in data:
            stat = dict(zip(
                ['load_1m', 'load_5m', 'load_15m', 'tasks', 'pid'],
                row
            ))

            for k in ['load_1m', 'load_5m', 'load_15m']:
                stat[k] = self.cast(stat[k], float)
            stat['active_tasks'], stat['total_tasks'] = [self.cast(v, int) for v in stat['tasks'].split('/')]
            stat['active_tasks_adjusted'] = stat['active_tasks'] - 1

            del stat['tasks']
            del stat['pid']

            for k, v in stat.items():
                setattr(self, k, v)
