#!/usr/bin/env bash
set -eo pipefail
[[ $EUID != 0 ]] || { echo 'Run build as foxbuild.'; exit 1; }
cd /content/fox-work/fox_14.1
test -f .repo/manifest.xml
test -f device/meizu/meizu21/BoardConfig.mk
export FOX_BUILD_DEVICE=meizu21
export MEIZU_TOUCH_MAPPING="${MEIZU_TOUCH_MAPPING:-0}"
source device/meizu/meizu21/vendorsetup.sh
source build/envsetup.sh
source device/meizu/meizu21/vendorsetup.sh
lunch twrp_meizu21-ap2a-eng
# Small RAM runtimes get one compiler job. Do not fake missing dependencies.
ram_kib=$(awk '/MemTotal:/ {print $2}' /proc/meminfo)
jobs=$((ram_kib / 6291456))
(( jobs >= 1 )) || jobs=1
(( jobs <= 4 )) || jobs=4
cpu_count=$(nproc)
(( jobs <= cpu_count )) || jobs=$cpu_count
# Earlier attempts used the platform default /vendor -> /system/vendor.
# Remove only that generated symlink before retrying with a real vendor directory.
root_vendor=out/target/product/meizu21/root/vendor
if [[ -L "$root_vendor" ]]; then
    link_target=$(readlink "$root_vendor")
    case "$link_target" in
        /system/vendor|system/vendor) rm "$root_vendor"; mkdir -p "$root_vendor" ;;
        *) echo "Unexpected generated vendor symlink: $link_target"; exit 1 ;;
    esac
fi
export USE_CCACHE=0
mka -j"$jobs" adbd recoveryimage
