#!/usr/bin/env python3
"""Instrument reviewed startup boundaries; no partition or decryption policy changes."""
from pathlib import Path
import sys
root=Path(sys.argv[1])/'bootable/recovery'
names=['partitionmanager.cpp','twrp.cpp','gui/gui.cpp','gui/gui.h']
s={n:(root/n).read_text() for n in names}
marker='MEIZU21_STARTUP_DIAGNOSTICS'
if any(marker in v for v in s.values()):
    if not all(marker in v for v in s.values()):
        raise SystemExit('Incomplete prior startup patch; restore reviewed files first.')
    print('Startup stage patch already installed.')
    raise SystemExit(0)
def replace(n,old,new):
    if s[n].count(old)!=1:raise SystemExit(f'Startup source drift: {n}: {old[:80]!r}')
    s[n]=s[n].replace(old,new)
def stage(code,name):return f'gui_meizu21_stage({code}, "{name}");'
for n in names:s[n]='// '+marker+'\n'+s[n]
s['gui/gui.cpp'] = '#include <cutils/properties.h>\n' + s['gui/gui.cpp']
replace('gui/gui.h','int gui_init();','void gui_meizu21_stage(int stage, const char* name);\nvoid gui_meizu21_stage_done(void);\nint gui_init();')
replace('gui/gui.cpp','extern "C" int gui_init(void)',Path(__file__).with_name('meizu21-stage.inc').read_text()+'extern "C" int gui_init(void)')
replace('gui/gui.cpp','\tev_init();\n\treturn 0;', '\tmeizu21_stage_visible = true;\n\t'+stage(10,'touch-begin')+'\n\tev_init();\n\t'+stage(11,'touch-returned')+'\n\treturn 0;')
replace('twrp.cpp','\tif (!PartitionManager.Process_Fstab(fstab_filename, 1, !startup.Get_Fastboot_Mode())) {','\t'+stage(1,'fstab-begin')+'\n\tif (!PartitionManager.Process_Fstab(fstab_filename, 1, !startup.Get_Fastboot_Mode())) {')
replace('twrp.cpp','\tgui_init();','\t'+stage(2,'graphics-begin')+'\n\tgui_init();')
replace('twrp.cpp','\tgui_loadResources();','\t'+stage(90,'resources-begin')+'\n\tgui_loadResources();\n\t'+stage(91,'resources-returned')+'\n\tgui_meizu21_stage_done();')
n='partitionmanager.cpp'
replace(n,'void TWPartitionManager::Setup_Fstab_Partitions(bool Display_Error) {','void TWPartitionManager::Setup_Fstab_Partitions(bool Display_Error) {\n\t\t'+stage(20,'partition-post-processing'))
replace(n,'\t\tUnlock_Block_Partitions();','\t\t'+stage(21,'unlock-blocks-begin')+'\n\t\tUnlock_Block_Partitions();\n\t\t'+stage(22,'unlock-blocks-returned'))
replace(n,'\t\t//Setup Apex before decryption','\t\t'+stage(30,'system-vendor-mount-begin')+'\n\t\t//Setup Apex before decryption')
replace(n,'\t\t\t\tLOGINFO("Apex is disabled in this build\\n");','\t\t\t\t'+stage(31,'apex-skipped')+'\n\t\t\t\tLOGINFO("Apex is disabled in this build\\n");')
replace(n,'\t\t\t\ttwrpApex apex;','\t\t\t\t'+stage(32,'apex-begin')+'\n\t\t\t\ttwrpApex apex;')
replace(n,'\t\t\t\tTWFunc::check_and_run_script("/sbin/resyncapex.sh", "apex");','\t\t\t\tTWFunc::check_and_run_script("/sbin/resyncapex.sh", "apex");\n\t\t\t\t'+stage(33,'apex-returned'))
replace(n,'\t#ifndef USE_VENDOR_LIBS\n\t\tif (ven)','\t\t'+stage(40,'system-vendor-unmount-begin')+'\n\t#ifndef USE_VENDOR_LIBS\n\t\tif (ven)')
replace(n,'\t\tif (!datamedia && !settings_partition','\t\t'+stage(41,'settings-storage-begin')+'\n\t\tif (!datamedia && !settings_partition')
replace(n,'\t\tconst char* os_props[]','\t\t'+stage(50,'properties-begin')+'\n\t\tconst char* os_props[]')
replace(n,'\t\tandroid::base::SetProperty("meizu21.crypto.props_ready", "1");','\t\tandroid::base::SetProperty("meizu21.crypto.props_ready", "1");\n\t\t'+stage(51,'properties-ready'))
replace(n,'\t\tbool meizu21_crypto_services_running = false;','\t\t'+stage(60,'crypto-service-wait')+'\n\t\tbool meizu21_crypto_services_running = false;')
replace(n,'\t\t\tDecrypt_Data();','\t\t\t'+stage(70,'decrypt-begin')+'\n\t\t\tDecrypt_Data();\n\t\t\t'+stage(71,'decrypt-returned'))
replace(n,'\t\t\tLOGERR("Meizu21: crypto services not running after 30s; skipping automatic decryption\\n");','\t\t\t'+stage(61,'crypto-timeout')+'\n\t\t\tLOGERR("Meizu21: crypto services not running after 30s; skipping automatic decryption\\n");')
replace(n,'\t\tUpdate_System_Details();\n\t\tif (Get_Super_Status())','\t\t'+stage(80,'system-details-begin')+'\n\t\tUpdate_System_Details();\n\t\tif (Get_Super_Status())')
replace(n,'\t\tUnMount_Main_Partitions();\n\t#ifdef AB_OTA_UPDATER','\t\tUnMount_Main_Partitions();\n\t\t'+stage(81,'partition-setup-returning')+'\n\t#ifdef AB_OTA_UPDATER')
for n,v in s.items():(root/n).write_text(v)
print('Startup stage patch installed.')
