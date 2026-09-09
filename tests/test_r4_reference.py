from pathlib import Path
import hashlib,json,re
repo=Path(__file__).resolve().parents[1];d=repo/'device/meizu/meizu21'
c=json.loads((repo/'evidence/R4-reference-contract.json').read_text())
for rel,digest in c['exact_files'].items():
 assert hashlib.sha256((d/rel).read_bytes()).hexdigest()==digest,rel
board=(d/'BoardConfig.mk').read_text()
for token in ['PLATFORM_VERSION := 99.87.36','PLATFORM_SECURITY_PATCH := 2099-12-31','TW_EXCLUDE_APEX := true','TW_USE_MEIZU_TOUCH_MAPPING := true','TW_SCREEN_BLANK_ON_BOOT := true']:
 assert token in board,token
assert 'TW_USE_LEGACY_BATTERY_SERVICES' not in board
assert 'TW_SKIP_ADDITIONAL_FSTAB' not in board
for lib in ['libdebuggerd_client','libprocinfo']:
 assert lib in board
loop=(repo/'ci/build-loop.py').read_text()
assert 'patch-source.py' not in loop and 'patch-startup.py' not in loop
for f in (d/'recovery/root').rglob('*.rc'):
 assert 'meizu21.crypto.props_ready' not in f.read_text()
for f in (d/'recovery/root/vendor/etc/init').glob('*.rc'):
 for line in f.read_text().splitlines():
  parts=line.split()
  if parts and parts[0]=='service':
   assert len(parts)>=3
   executable=d/'recovery/root'/parts[2].lstrip('/')
   assert executable.is_file(),parts[2]
   assert executable.stat().st_mode & 0o111, 'Non-executable service: '+parts[2]
print('R4 reference: exact hashes, service executables, library inclusion and no custom startup hooks passed.')
