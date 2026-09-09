from pathlib import Path
import re
p=Path(__file__).resolve().parents[1]/'device/meizu/meizu21'
assert 'TW_EXCLUDE_APEX := true' in (p/'BoardConfig.mk').read_text()
assert 'vendor.gatekeeper.disable_spu=true' in (p/'device.mk').read_text()
s=(p/'recovery/root/init.recovery.meizu21-services.rc').read_text()
for name in ['vendor.keymint-qti','vendor.gatekeeper_default']:
 block=re.search(r'^service '+re.escape(name)+r' .*?(?=^service |\Z)',s,re.M|re.S).group()
 assert '\n    user root\n' in block
 assert '\n    class early_hal\n' in block
 assert '/vendor/lib64:/vendor/lib64/hw:/system/lib64:/sbin' in block
s=(p/'recovery/root/init.recovery.qcom.rc').read_text()
assert 'on property:vendor.sys.listeners.registered=true\n    start vendor.gatekeeper_default' in s
assert 'on property:meizu21.crypto.props_ready=1\n    start vendor.keymint-qti' in s
print('R3 service identities and independent startup gates passed.')
