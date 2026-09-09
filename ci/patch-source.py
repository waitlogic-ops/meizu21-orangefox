#!/usr/bin/env python3
"""Apply the reviewed Meizu-only pre-decryption hook; reject upstream drift."""
from pathlib import Path
import sys
root = Path(sys.argv[1])
p = root / 'bootable/recovery/partitionmanager.cpp'
s = p.read_text()
marker = '// MEIZU21_PREDECRYPT:'
anchor = '\t\tDataManager::SetValue(TW_IS_ENCRYPTED, 1);'
if marker not in s:
    if s.count(anchor) != 1:
        raise SystemExit('Recovery source changed: expected exactly one pre-decryption anchor.')
    code = Path(__file__).with_name('meizu21-predecrypt.inc').read_text()
    p.write_text(s.replace(anchor, code + anchor))
print('Meizu21 pre-decryption hook installed.')
