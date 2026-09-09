#!/usr/bin/env python3
"""Build public main snapshots; preserve source/out while awaiting a reviewed fix."""
import os
from pathlib import Path
import shutil
import subprocess
import time

if os.geteuid() == 0:
    raise SystemExit('Run as foxbuild, not root.')
source = Path('/content/fox-work/fox_14.1')
config = Path('/content/fox-work/build-config')
logs = Path('/content/fox-logs')
url = 'https://github.com/waitlogic-ops/meizu21-orangefox.git'

def run(*args, cwd=None, check=True):
    return subprocess.run(args, cwd=cwd, check=check)

def read(*args, cwd=None):
    return subprocess.check_output(args, cwd=cwd, text=True).strip()

if not config.exists():
    run('git', 'clone', '--depth=1', url, str(config), cwd=source.parent)
for attempt in range(1, 9):
    run('git', 'fetch', '--depth=1', 'origin', 'main', cwd=config)
    run('git', 'checkout', '--detach', 'FETCH_HEAD', cwd=config)
    sha = read('git', 'rev-parse', 'HEAD', cwd=config)
    (logs / 'device-tree-commit.txt').write_text(sha + '\n')
    print(f'BUILD_ATTEMPT={attempt} DEVICE_TREE_COMMIT={sha}', flush=True)
    device = source / 'device/meizu/meizu21'
    if device.exists():
        # This exact directory was created by this workflow from this repository.
        shutil.rmtree(device)
    device.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(config / 'device/meizu/meizu21', device)
    # Restore upstream files that older R2/R3 iterations patched. R4 adds no hooks.
    recovery = source / 'bootable/recovery'
    for name in ('partitionmanager.cpp', 'twrp.cpp', 'gui/gui.cpp', 'gui/gui.h'):
        original = subprocess.check_output(['git', 'show', 'HEAD:' + name], cwd=recovery)
        (recovery / name).write_bytes(original)
    diff = read('git', 'diff', cwd=recovery)
    (logs / 'recovery-local.patch').write_text(diff + '\n')
    result = run('bash', str(config / 'tools/build.sh'), cwd=source, check=False)
    if result.returncode == 0:
        image = source / 'out/target/product/meizu21/recovery.img'
        result = run('python3', str(config / 'tools/verify-image.py'), str(image), cwd=source, check=False)
    if result.returncode == 0:
        print('BUILD_SUCCESS: exact device-tree commit recorded above.', flush=True)
        raise SystemExit(0)
    print(f'BUILD_FAILED={result.returncode}; keeping source/out for up to 20 minutes awaiting a new main commit.', flush=True)
    deadline = time.monotonic() + 1200
    while time.monotonic() < deadline:
        time.sleep(30)
        try:
            head = read('git', 'ls-remote', 'origin', 'refs/heads/main', cwd=config).split()[0]
        except (subprocess.CalledProcessError, IndexError):
            continue
        if head != sha:
            print(f'New correction found: {head}; retrying without source resync.', flush=True)
            break
    else:
        raise SystemExit(result.returncode)
raise SystemExit('Eight build attempts exhausted; inspect logs.')
