from glance.collectors import Collector


class MemInfo(Collector):
    pass


class _MemInfo_Linux(MemInfo):
    @classmethod
    def for_platform(self):
        return {'class': 'posix', 'os': 'Linux'}

    def _collect(self):
        with open('/proc/meminfo', 'r') as fp:
            data = [row.strip() for row in fp.read().strip().split("\n")]

        keys = {
            'MemTotal': 'mem_total',
            'MemFree': 'mem_free',
            'Buffers': 'buffers',
            'Cached': 'cached',
            'SwapCached': 'swap_cached',
            'Active': 'active',
            'Inactive': 'inactive',
            'Active(anon)': 'active_anon',
            'Inactive(anon)': 'inactive_anon',
            'Active(file)': 'active_file',
            'Inactive(file)': 'inactive_file',
            'Unevictable': 'unevictable',
            'Mlocked': 'mlocked',
            'SwapTotal': 'swap_total',
            'SwapFree': 'swap_free',
            'Dirty': 'dirty',
            'Writeback': 'writeback',
            'AnonPages': 'anon_pages',
            'Mapped': 'mapped',
            'Shmem': 'shmem',
            'Slab': 'slab',
            'SReclaimable': 'sreclaimable',
            'SUnreclaim': 'sunreclaim',
            'KernelStack': 'kernel_stack',
            'PageTables': 'page_tables',
            'NFS_Unstable': 'nfs_unstable',
            'Bounce': 'bounce',
            'WritebackTmp': 'writeback_tmp',
            'CommitLimit': 'commit_limit',
            'Committed_AS': 'committed_as',
            'VmallocTotal': 'vmalloc_total',
            'VmallocUsed': 'vmalloc_used',
            'VmallocChunk': 'vmalloc_chunk',
            'HardwareCorrupted': 'hardware_corrupted',
            'AnonHugePages': 'anon_huge_pages',
            'HugePages_Total': 'hugepages_total',
            'HugePages_Free': 'hugepages_free',
            'HugePages_Rsvd': 'hugepages_rsvd',
            'HugePages_Surp': 'hugepages_surp',
            'Hugepagesize': 'hugepagesize',
            'DirectMap4k': 'directmap_4k',
            'DirectMap2M': 'directmap_2m',
        }

        for row in data:
            row = row.split(':', 1)
            row += row.pop().strip().split(None, 1)
            if len(row) < 3:
                row.append(None)

            key = keys[row[0]]
            value = self.cast(row[1], int)
            if row[2]:
                value = self.cast(self.conv(value, 'datasize', row[2].upper(), 'B'), int)

            setattr(self, key, value)
