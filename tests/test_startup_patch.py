from pathlib import Path
import tempfile,subprocess,shutil,sys
repo=Path(__file__).resolve().parents[1]
upstream=Path(sys.argv[1])
with tempfile.TemporaryDirectory() as d:
 root=Path(d); rec=root/'bootable/recovery'
 for n in ['partitionmanager.cpp','twrp.cpp','gui/gui.cpp','gui/gui.h']:
  p=rec/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(upstream/n,p)
 subprocess.run(['python3',str(repo/'ci/patch-source.py'),str(root)],check=True)
 subprocess.run(['python3',str(repo/'ci/patch-startup.py'),str(root)],check=True)
 before={str(p.relative_to(rec)):p.read_bytes() for p in rec.rglob('*') if p.is_file()}
 subprocess.run(['python3',str(repo/'ci/patch-startup.py'),str(root)],check=True)
 assert before=={str(p.relative_to(rec)):p.read_bytes() for p in rec.rglob('*') if p.is_file()}
 s=(rec/'partitionmanager.cpp').read_text()
 for x in ['partition-post-processing','apex-skipped','properties-begin','properties-ready','decrypt-begin','decrypt-returned','crypto-timeout']:
  assert x in s,x
 assert s.index('"decrypt-begin"') < s.index('\n\t\t\tDecrypt_Data();') < s.index('"decrypt-returned"')
 assert 'resources-begin' in (rec/'twrp.cpp').read_text()
 assert 'touch-begin' in (rec/'gui/gui.cpp').read_text()
 # A changed upstream anchor must fail instead of silently producing an incomplete patch.
 (rec/'gui/gui.cpp').write_text('unrelated source')
 assert subprocess.run(['python3',str(repo/'ci/patch-startup.py'),str(root)],capture_output=True).returncode != 0
print('Startup patch coverage, repeatability and drift rejection passed.')
