#!/usr/bin/env python3
"""Published source-space floor; live monitoring enforces remaining space."""
import json
import os
import platform
import shutil
from pathlib import Path

def check(root='/content'):
    root = Path(root)
    free = shutil.disk_usage(root).free / 2**30
    mem = int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines()
                   if x.startswith('MemTotal:'))) / 2**20
    result = dict(architecture=platform.machine(), disk_free_GiB=round(free, 1),
                  RAM_GiB=round(mem, 1), CPUs=os.cpu_count(),
                  minimum_disk_GB=85, minimum_RAM_GiB=10,
                  recommended='110-150 GiB free disk, 24 GiB RAM; GPU is not used')
    print(json.dumps(result, indent=2))
    errors = []
    if platform.system() != 'Linux' or platform.machine() != 'x86_64':
        errors.append('Requires x86_64 Linux.')
    if free * 2**30 < 85 * 10**9:
        errors.append('Less than 85 GB free: below the published fox_14.1 source-space floor.')
    if mem < 10:
        errors.append('Less than 10 GiB RAM: compilation is unlikely to finish reliably.')
    if errors:
        raise RuntimeError('\n'.join(errors))
    return result

if __name__ == '__main__':
    check()
