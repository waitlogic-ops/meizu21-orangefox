#!/usr/bin/env bash
set -euo pipefail
[[ ${GITHUB_ACTIONS:-} == true && ${RUNNER_ENVIRONMENT:-} == github-hosted && $(uname -m) == x86_64 ]] || {
  echo 'This cleanup only supports disposable GitHub-hosted x64 runners.'; exit 1;
}
sudo mkdir -p /content/fox-logs
sudo chown "$(id -u):$(id -g)" /content/fox-logs
exec > >(tee /content/fox-logs/prepare.log) 2>&1
df -h
free -h
# Explicit unrelated preinstalled SDKs; no source-tree deletion or disk repartitioning.
sudo rm -rf /usr/share/dotnet /usr/local/lib/android /opt/ghc /usr/local/.ghcup \
  /opt/hostedtoolcache/CodeQL /usr/local/share/powershell /usr/share/swift \
  /usr/local/share/chromium /opt/google/chrome /opt/microsoft/msedge \
  /usr/local/share/boost /usr/local/share/vcpkg /opt/az /usr/local/aws-cli \
  /usr/share/miniconda /usr/share/kotlinc /usr/local/graalvm \
  /opt/hostedtoolcache/go /opt/hostedtoolcache/Ruby /opt/hostedtoolcache/PyPy \
  /home/runner/.rustup /home/runner/.cargo /home/runner/.ghcup
sudo apt-get clean
sudo mkdir -p /content/fox-kit
sudo cp -a device tools evidence /content/fox-kit/
sudo bash /content/fox-kit/tools/setup-colab.sh
# The runner also needs write access for tee and final diagnostic collection.
sudo chmod 0777 /content/fox-logs
# Optional compressed RAM swap. Failure does not pretend extra RAM is available.
if sudo modprobe zram && [[ -b /dev/zram0 ]] && ! swapon --show=NAME --noheadings | grep -qx /dev/zram0; then
  if [[ $(cat /sys/block/zram0/disksize) == 0 ]]; then
    mem_bytes=$(awk '/MemTotal:/ {printf "%.0f", $2 * 1024 / 2}' /proc/meminfo)
    if echo "$mem_bytes" | sudo tee /sys/block/zram0/disksize >/dev/null; then
      sudo mkswap /dev/zram0 && sudo swapon -p 100 /dev/zram0 || echo 'zram unavailable; continuing with physical RAM.'
    fi
  fi
fi
free -h
df -h /content
git rev-parse HEAD > /content/fox-logs/device-tree-commit.txt
