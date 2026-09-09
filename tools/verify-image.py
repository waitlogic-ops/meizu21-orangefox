#!/usr/bin/env python3
"""Structural + ELF dependency checks; deliberately makes no hardware claim."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import struct
import subprocess
import tempfile

def cpio_entries(data):
    entries = {}
    pos = 0
    while pos + 110 <= len(data):
        h = data[pos:pos+110]
        if h[:6] not in (b'070701', b'070702'):
            raise ValueError('Invalid CPIO magic')
        v = [int(h[6+i*8:14+i*8], 16) for i in range(13)]
        mode, size, namesize = v[1], v[6], v[11]
        name = data[pos+110:pos+110+namesize-1].decode()
        pos = (pos+110+namesize+3) & ~3
        payload = data[pos:pos+size]
        if len(payload) != size:
            raise ValueError('Truncated CPIO entry')
        pos = (pos+size+3) & ~3
        if name == 'TRAILER!!!':
            return entries
        n = Path(name)
        if n.is_absolute() or '..' in n.parts:
            raise ValueError('Unsafe CPIO pathname')
        entries[str(n)] = (mode, payload)
    raise ValueError('Missing CPIO trailer')

def verify(path):
    b = Path(path).read_bytes()
    assert b[:8] == b'ANDROID!', 'Wrong boot magic'
    assert struct.unpack_from('<I', b, 40)[0] == 4, 'Header must be v4'
    k, r = struct.unpack_from('<2I', b, 8)
    assert k == 0, 'Dedicated recovery must NOT contain a kernel'
    assert 0 < r <= len(b)-4096, 'Invalid ramdisk range'
    assert len(b) <= 104857600, 'Recovery exceeds stock 100 MiB partition image'
    ramdisk = b[4096:4096+r]
    assert ramdisk[:4] == bytes.fromhex('02214c18'), 'Expected stock-compatible legacy LZ4'
    unpacked = subprocess.run(['lz4', '-d', '-c'], input=ramdisk,
                              capture_output=True, check=True).stdout
    entries = cpio_entries(unpacked)
    required = ['system/bin/recovery', 'system/etc/recovery.fstab',
                'init.recovery.qcom.rc',
                'vendor/bin/hw/android.hardware.security.keymint-service-qti',
                'vendor/bin/hw/vendor.qti.hardware.vibrator.service',
                'system/bin/hw/android.hardware.boot-service.qti.recovery']
    for name in required:
        assert name in entries, 'Missing ' + name
    fstab = entries['system/etc/recovery.fstab'][1].decode()
    assert 'v2+inlinecrypt_optimized+wrappedkey_v0' in fstab
    assert 'metadata_encryption=aes-256-xts:wrappedkey_v0' in fstab
    assert 'fileencryption=ice' not in fstab
    # A filename dependency audit cannot validate ABI symbols, dlopen or namespaces.
    sonames = {Path(n).name for n in entries}
    reader = shutil.which('llvm-readelf') or shutil.which('readelf')
    assert reader, 'Install binutils or llvm-readelf'
    missing = {}
    elf_count = 0
    with tempfile.TemporaryDirectory() as tmp:
        for n, (mode, payload) in entries.items():
            if payload[:4] != b'\x7fELF':
                continue
            elf_count += 1
            p = Path(tmp)/'elf'
            p.write_bytes(payload)
            output = subprocess.check_output([reader, '-d', str(p)], text=True)
            needs = re.findall(r'Shared library: \[(.*?)\]', output)
            absent = sorted(set(needs)-sonames)
            if absent:
                missing[n] = absent
    result = dict(image=str(path), sha256=hashlib.sha256(b).hexdigest(),
                  bytes=len(b), header=4, kernel_bytes=k, ramdisk_bytes=r,
                  cpio_entries=len(entries), checked_ELFs=elf_count,
                  missing_sonames=missing, hardware_verified=False)
    print(json.dumps(result, indent=2))
    assert not missing, 'Missing runtime libraries; do not mark this image ready for testing'
    return result

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('image')
    verify(p.parse_args().image)
