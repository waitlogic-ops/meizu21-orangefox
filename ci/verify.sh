#!/usr/bin/env bash
set -euo pipefail
src=/content/fox-work/fox_14.1
img="$src/out/target/product/meizu21/recovery.img"
[[ -s "$img" ]]
python3 tools/verify-image.py "$img" | tee /content/fox-logs/image-check.json
python3 "$src/external/avb/avbtool.py" info_image --image "$img" | tee /content/fox-logs/avb-info.txt
python3 "$src/external/avb/avbtool.py" verify_image --image "$img" | tee /content/fox-logs/avb-verify.txt
sudo mkdir -p /content/fox-artifacts
sudo chown "$(id -u):$(id -g)" /content/fox-artifacts
cp "$img" /content/fox-artifacts/OrangeFox-meizu21-UNTESTED.img
cp DEVICE-NOTES.md TESTING.md REPAIR-R2.md /content/fox-artifacts/
cp /content/fox-logs/pinned-manifest.xml /content/fox-artifacts/
cp /content/fox-logs/device-tree-commit.txt /content/fox-artifacts/
cp /content/fox-logs/recovery-local.patch /content/fox-artifacts/
tar -czf /content/fox-artifacts/device-tree.tar.gz device/meizu/meizu21 ci
printf '%s\n' 'Experimental Meizu 21/M2461 image. Hardware and FBE decryption NOT verified. Not for Meizu 21 Pro. Development AVB verification is not OEM authorization.' > /content/fox-artifacts/UNTESTED.txt
(cd /content/fox-artifacts && sha256sum OrangeFox-meizu21-UNTESTED.img > SHA256SUMS)
