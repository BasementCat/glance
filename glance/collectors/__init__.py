import os
import platform
import time

class Collector(object):
    is_continuous = True

    def __new__(cls, *args, **kwargs):
        impl = cls.find_for_platform()
        return object.__new__(impl, *args, **kwargs)

    def __init__(self, collect_now=None):
        self._initial_vars = vars(self).keys()
        if collect_now is None:
            collect_now = not self.is_continuous
        if collect_now:
            self.collect()

    @classmethod
    def for_platform(self):
        raise NotImplementedError("A subclass must return a dict containing one or more of the keys: class, os, release")

    @classmethod
    def is_supported(self):
        return True

    @classmethod
    def find_for_platform(self):
        for cls in self.__subclasses__():
            require = {'class': None, 'os': None, 'release': None}
            require.update(cls.for_platform())
            if require['class'] is not None and require['class'] != os.name:
                continue
            if require['os'] is not None and require['os'] != platform.system():
                continue
            if require['release'] is not None and not platform.release().startswith(require['release']):
                continue

            if cls.is_supported():
                return cls
            else:
                raise NotImplementedError("Collector {} is implemented but not supported on this system but declined to provide a reason")
        raise NotImplementedError("Collector {} is not implemented for {}/{}/{}".format(self.__name__, os.name, platform.system(), platform.release()))

    @staticmethod
    def cast(val, type_, *args, **kwargs):
        return type_(val, *args, **kwargs) if val is not None else None

    @staticmethod
    def conv(val, measurement, from_unit, to_unit):
        if val is None:
            return None

        convs = {
            'datasize': {
                'EB': 1024 ** 6,
                'PB': 1024 ** 5,
                'TB': 1024 ** 4,
                'GB': 1024 ** 3,
                'MB': 1024 ** 2,
                'KB': 1024,
                'B': 1,
            }
        }

        if measurement not in convs:
            raise ValueError("Invalid measurement: " + measurement)
        if from_unit not in convs[measurement]:
            raise ValueError("Invalid from_unit: " + from_unit)
        if to_unit not in convs[measurement]:
            raise ValueError("Invalid to_unit: " + to_unit)

        return (float(val) * convs[measurement][from_unit]) * convs[measurement][to_unit]

    def collect(self):
        started_at = time.time()
        self._collect()
        self._timing = time.time() - started_at
        return self

    def _collect(self):
        raise NotImplementedError("Subclasses must implement _collect()")

    def export(self):
        return {k: v for k, v in vars(self).items() if k not in self._initial_vars and k != '_initial_vars'}
