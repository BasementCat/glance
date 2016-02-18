from glance.collectors import Collector

class Stats(Collector):
    pass


class _Stats_Linux(Stats):
    @classmethod
    def for_platform(self):
        return {'class': 'posix', 'os': 'Linux'}

    def _collect(self):
        with open('/proc/diskstats', 'r') as fp:
            data = [row.strip().split() for row in fp.read().strip().split("\n")]

        for row in data:
            stat = dict(zip(
                ['major_number', 'minor_number', 'device', 'reads_success', 'reads_merged',
                    'reads_sectors', 'reads_time_ms', 'writes_success', 'writes_merged',
                    'writes_sectors', 'writes_time_ms', 'iops_current', 'iops_time_ms'],
                row
            ))
            for k, v in stat.items():
                if k != 'device':
                    stat[k] = self.cast(v, int)

            setattr(self, stat['device'], stat)


class Mounts(Collector):
    pass


class _Mounts_Linux(Mounts):
    @classmethod
    def for_platform(self):
        return {'class': 'posix', 'os': 'Linux'}

    def _collect(self):
        with open('/proc/mounts', 'r') as fp:
            data = [row.strip().split() for row in fp.read().strip().split("\n")]

        for row in data:
            stat = dict(zip(
                ['device', 'mountpoint', 'filesystem', 'options', '_', '_'],
                row
            ))
            del stat['_']
            stat['options'] = stat['options'].split(',')

            setattr(self, stat['mountpoint'], stat)


class Swaps(Collector):
    pass


class _Swaps_Linux(Swaps):
    @classmethod
    def for_platform(self):
        return {'class': 'posix', 'os': 'Linux'}

    def _collect(self):
        with open('/proc/swaps', 'r') as fp:
            data = [row.strip().split() for row in fp.read().strip().split("\n")]
        del data[0]

        for row in data:
            stat = dict(zip(
                ['location', 'type', 'size', 'used', 'priority'],
                row
            ))
            for k, v in stat.items():
                if k in ('size', 'used', 'priority'):
                    stat[k] = self.cast(v, int)

            setattr(self, stat['location'], stat)
