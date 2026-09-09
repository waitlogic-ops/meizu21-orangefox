from pathlib import Path
import tempfile,subprocess
repo=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as d:
 p=Path(d);code=r'''
#include <cstdio>
#include <ctime>
#include <unistd.h>
#include <cassert>
#include <string>
int fills=0,flips=0;std::string state;
int property_set(const char*,const char* v){state=v;return 0;}
int gr_fb_width(){return 1080;}int gr_fb_height(){return 2400;}
void gr_noclip(){}void gr_color(unsigned char,unsigned char,unsigned char,unsigned char){}
void gr_fill(int x,int y,int w,int h){assert(x>=0&&y>=0&&w>0&&h>0&&x+w<=1080&&y+h<=2400);++fills;}
void gr_flip(){++flips;}
'''+(repo/'ci/meizu21-stage.inc').read_text()+r'''
int main(){
gui_meizu21_stage(1,"before-graphics");assert(fills==0&&flips==0&&state=="01");
meizu21_stage_visible=true;
for(int i=0;i<100;++i)gui_meizu21_stage(i,"visible");
assert(flips==100&&fills>100);
gui_meizu21_stage_done();int old=fills;
gui_meizu21_stage(91,"after-startup");assert(fills==old&&flips==100);
}
'''
 (p/'test.cpp').write_text(code)
 subprocess.run(['c++','-std=c++17',str(p/'test.cpp'),'-o',str(p/'test')],check=True)
 subprocess.run([str(p/'test')],check=True,stdout=subprocess.DEVNULL)
print('Startup overlay: no drawing before graphics/after startup; digits 00–99 stay in bounds.')
