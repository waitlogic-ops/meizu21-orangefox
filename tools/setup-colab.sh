#!/usr/bin/env bash
set -euo pipefail
[[ $(uname -m) == x86_64 && $(uname -s) == Linux ]]
[[ $EUID == 0 ]] || { echo 'Run this setup cell as Colab root.'; exit 1; }
kit_tools=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
python3 "$kit_tools/preflight.py"
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y git curl ca-certificates python3 python3-pip \
    build-essential bc bison flex gperf ccache zip unzip rsync \
    libc6-dev-i386 lib32z1-dev lib32ncurses-dev libssl-dev libxml2-utils \
    xsltproc zlib1g-dev liblz4-tool lzop libncurses-dev squashfs-tools \
    pngcrush schedtool imagemagick libelf-dev openjdk-17-jdk \
    cpio file binutils jq
id foxbuild >/dev/null 2>&1 || useradd -m -s /bin/bash foxbuild
install -d -o foxbuild -g foxbuild /content/fox-work /content/fox-logs
curl --fail --location --retry 3 https://storage.googleapis.com/git-repo-downloads/repo -o /usr/local/bin/repo
chmod 0755 /usr/local/bin/repo
cd /content
runuser -u foxbuild -- git config --global user.name 'Local recovery build'
runuser -u foxbuild -- git config --global user.email 'recovery-build@localhost'
runuser -u foxbuild -- git config --global color.ui false
