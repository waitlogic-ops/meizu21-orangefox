#!/usr/bin/env python3
"""Keep disk headroom and preserve the command exit status; never delete sources."""
import os
import signal
import shutil
import subprocess
import sys
import time

root, minimum, sep, *command = sys.argv[1:]
assert sep == '--' and command
minimum = float(minimum) * 1024**3
if shutil.disk_usage(root).free < minimum:
    sys.exit('Insufficient free disk before starting command.')
proc = subprocess.Popen(command, start_new_session=True)

def stop():
    try:
        os.killpg(proc.pid, signal.SIGTERM)
        proc.wait(timeout=15)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        proc.wait()
    except ProcessLookupError:
        pass

try:
    tick = 0
    while proc.poll() is None:
        free = shutil.disk_usage(root).free
        if tick % 4 == 0:
            print(f'[resources] free disk: {free / 1024**3:.2f} GiB', flush=True)
            if os.path.exists('/proc/meminfo'):
                from pathlib import Path
                print(next(line for line in Path('/proc/meminfo').read_text().splitlines() if line.startswith('MemAvailable:')), flush=True)
        if free < minimum:
            print('Stopping: disk headroom fell below limit.', flush=True)
            stop()
            sys.exit(75)
        tick += 1
        time.sleep(15)
except BaseException:
    stop()
    raise
sys.exit(proc.returncode if proc.returncode >= 0 else 128 - proc.returncode)
