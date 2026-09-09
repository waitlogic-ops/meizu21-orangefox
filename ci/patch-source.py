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
    call = '\t\tDecrypt_Data();'
    if s.count(call) != 1:
        raise SystemExit('Recovery source changed: expected one startup decryption call.')
    guarded = '\t\tif (meizu21_crypto_services_running) {\n\t\t\tDecrypt_Data();\n\t\t} else {\n\t\t\tLOGERR("Meizu21: crypto services not running after 30s; skipping automatic decryption\\n");\n\t\t} '
    s = s.replace(call, guarded)
    p.write_text(s.replace(anchor, code + anchor))
print('Meizu21 pre-decryption hook installed.')
