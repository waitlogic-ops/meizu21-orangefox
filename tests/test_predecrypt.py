#!/usr/bin/env python3
"""Run the patched startup block with simulated init properties; no device access."""
import subprocess, tempfile
from pathlib import Path
repo = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    p = root/'bootable/recovery/partitionmanager.cpp'
    p.parent.mkdir(parents=True)
    p.write_text('\t\tDataManager::SetValue(TW_IS_ENCRYPTED, 1);\n\t\tDecrypt_Data();\n')
    subprocess.run(['python3',str(repo/'ci/patch-source.py'),str(root)],check=True)
    block=p.read_text()
    pre=r'''
#include <string>
#include <cassert>
int ticks=0, decrypts=0, ready_at=0, PartitionManager=0;
#define LOGERR(...) ((void)0)
#define LOGINFO(...) ((void)0)
#define TW_IS_ENCRYPTED 1
void usleep(int) { ++ticks; }
void Decrypt_Data() { ++decrypts; }
namespace DataManager { void SetValue(int,int) {} }
namespace TWFunc {
std::string System_Property_Get(const char*) { return "14"; }
std::string Partition_Property_Get(const char*,int,const char*,const char*) { return "2023-10-05"; }
void Property_Override(const char*,std::string) {}
}
namespace android { namespace base {
bool SetProperty(const char*,const char*) { return true; }
std::string GetProperty(const char*,const char*) { return ticks>=ready_at ? "running" : "stopped"; }
}}
void setup() {
'''
    post='''
}
int main() {
ready_at=301; setup(); assert(ticks==300); assert(decrypts==0);
ticks=0; ready_at=0; setup(); assert(ticks==0); assert(decrypts==1);
ticks=0; ready_at=17; setup(); assert(ticks==17); assert(decrypts==2);
}
'''
    cpp=root/'test.cpp'; cpp.write_text(pre+block+post)
    subprocess.run(['c++','-std=c++17',str(cpp),'-o',str(root/'test')],check=True)
    subprocess.run([str(root/'test')],check=True)
print('Startup timeout and ready-path regression tests passed.')
