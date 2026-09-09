#!/usr/bin/env bash
set -euo pipefail
[[ $EUID != 0 ]] || { echo 'OrangeFox sync must run as foxbuild, not root.'; exit 1; }
cd /content/fox-work
if [[ ! -d sync/.git ]]; then
    git clone https://gitlab.com/OrangeFox/sync.git sync
fi
# Audited official helper (2026-08-14). Recovery repos resolve latest fox_14.1.
git -C sync fetch origin 14eca5f7ef82c9dacfe353db8b93329383c7293f
git -C sync checkout --detach 14eca5f7ef82c9dacfe353db8b93329383c7293f
cd sync
./orangefox_sync.sh --branch 14.1 --path /content/fox-work/fox_14.1
cd /content/fox-work/fox_14.1
repo manifest -r -o /content/fox-logs/pinned-manifest.xml
git -C bootable/recovery rev-parse HEAD > /content/fox-logs/recovery-commit.txt
git -C bootable/recovery log -1 --format=fuller > /content/fox-logs/recovery-commit-details.txt
