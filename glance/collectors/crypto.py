from glance.collectors import Collector

class Crypto(Collector):
    is_continuous = False


class _Crypto_Linux(Crypto):
    @classmethod
    def for_platform(self):
        return {'class': 'posix', 'os': 'Linux'}

    def _collect(self):
        with open('/proc/crypto', 'r') as fp:
            data = [section.strip().split("\n") for section in fp.read().strip().split("\n\n")]

        keys = {
            'name': 'name',
            'driver': 'driver',
            'module': 'module',
            'priority': 'priority',
            'refcnt': 'refcnt',
            'selftest': 'selftest',
            'type': 'type',
        }

        ints = ['priority', 'refcnt', 'seedsize', 'blocksize', 'digestsize']

        for section in data:
            section = {k.strip(): v.strip() for k, v in [row.split(':', 1) for row in section]}
            out_section = {}
            for in_key, out_key in keys.items():
                out_section[out_key] = section.get(in_key)
            for k, v in section.items():
                if k not in keys.values():
                    out_section[k] = v
            for k, v in out_section.items():
                if k in ints:
                    out_section[k] = self.cast(v, int)
            setattr(self, out_section['name'], out_section)
