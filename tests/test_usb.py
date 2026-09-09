#!/usr/bin/env python3
"""Check device init MTP trigger gating and cleanup, without USB access."""
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'device/meizu/meizu21/recovery/root/init.recovery.usb.rc'
actions=[]
for line in p.read_text().splitlines():
    if line.startswith('on '): actions.append((line[3:].split(' && '),[]))
    elif line.startswith('    '): actions[-1][1].append(line.strip())
def commands(props):
    return [cmd for cond,body in actions if all(c.startswith('property:') and props.get(c[9:].split('=',1)[0])==c.split('=',1)[1] for c in cond) for cmd in body]
p={'sys.usb.config':'mtp,adb','sys.usb.configfs':'1','sys.usb.ffs.ready':'1','sys.usb.ffs.mtp.ready':'0'}
assert not any('/UDC' in c for c in commands(p))
p['sys.usb.ffs.mtp.ready']='1'
cmds=commands(p)
assert any('functions/ffs.mtp' in c and c.endswith('/f1') for c in cmds)
assert any('functions/ffs.adb' in c and c.endswith('/f2') for c in cmds)
assert any('/UDC' in c for c in cmds)
p['sys.usb.ffs.ready']='0'
assert not any('/UDC' in c for c in commands(p))
p['sys.usb.config']='none'
assert 'rm /config/usb_gadget/g1/configs/b.1/f2' in commands(p)
assert 'setprop sys.usb.ffs.mtp.ready 0' in commands(p)
for mode in ['adb','sideload','fastboot']:
    p['sys.usb.config']=mode
    assert not any('/UDC' in c for c in commands(p)), 'Must leave upstream modes to generic init'
print('MTP descriptor gating, cleanup and upstream mode separation passed.')
