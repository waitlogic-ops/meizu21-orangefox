#!/usr/bin/env bash
# Read-only collection on the Mac after booting the experimental recovery.
set -euo pipefail
out="${1:-meizu21-test-logs}"
mkdir -p "$out"
adb get-state
adb shell getprop > "$out/getprop.txt"
adb shell 'cat /proc/mounts; cat /proc/modules; cat /proc/partitions' > "$out/storage-modules.txt"
adb shell 'getevent -lp' > "$out/input-capabilities.txt"
adb shell 'cat /sys/class/backlight/panel0-backlight/max_brightness; cat /sys/class/backlight/panel0-backlight/brightness' > "$out/backlight.txt"
adb shell 'for d in /sys/class/power_supply/*; do echo "$d"; cat "$d/uevent"; done' > "$out/power.txt"
adb shell 'ls -l /dev/aac_richtap_dev /sys/class/leds/vibrator*; service list' > "$out/services.txt"
adb shell dmesg > "$out/dmesg.txt" || true
adb logcat -d -b all > "$out/logcat.txt" || true
adb pull /tmp/recovery.log "$out/recovery.log" || true
echo "Saved locally to $out. Review logs for personal information before sharing."
