# Meizu 21 OrangeFox — GitHub Actions

针对魅族 21 标准版 M2461/meizu21，原厂 Android 14 / Flyme 10.5.0.2G。不是魅族 21 Pro 镜像。

状态：GitHub 构建已启动，尚未生成镜像。第一轮环境准备发现构建账号工作目录权限问题，已修复并重试。设备树尚未通过实际编译与真机测试。Colab 的部分源码不会迁移到 GitHub，新任务需要重新同步。

## 使用

1. 将本目录全部内容（包括隐藏的 `.github` 目录）放到仓库根目录。
2. 打开 Actions → Meizu 21 OrangeFox → Run workflow。
3. 下载任务页面 Artifacts 中的日志。仅编译和镜像检查全部通过时提供 `meizu21-OrangeFox-UNTESTED-*`。
4. 产物保留 7 天，及时下载。此流程不创建公开 Release、不刷手机。

公开仓库会公开本目录内所有原厂提取组件；必须由所有者确认后再上传。当前包包括约 34 MB 原厂内核、厂商 HAL/库、固件、配置和证据记录，不含用户数据。私有仓库的 Actions 配额与硬件不同，本配置不承诺私有仓库足够运行，也不授权付费超额。

## 构建与资源策略

- `ubuntu-24.04` GitHub 托管 x64 临时机器，任务上限 350 分钟。
- 清理脚本只允许在 GitHub 托管机器执行，仅删除列明的无关预装 SDK；不对磁盘分区，不删除用户电脑内容。
- 沿用官方 fox_14.1 同步脚本固定提交；记录本次实际源码提交 manifest。
- 源码预检要求 85 GB 空闲、10 GiB RAM，这是最低检查而不是完成保证。低于条件会提前停止，不强行下载。
- 同步和编译每 15 秒检查磁盘，小于 8 GiB 时停止进程组，保留错误状态和日志。
- 内核复用、ccache 关闭；按 RAM/CPU 约束编译并行度。可用时启用约物理内存一半容量的 zram，不代表物理 RAM 增加。
- 不启用 ALLOW_MISSING_DEPENDENCIES；缺失依赖必须修复。
- 不自动迁移或删除 Colab 原有下载。

## 验证与限制

检查 header v4、kernel_size=0、legacy LZ4、100 MiB 容量、必要文件、FBE 参数、ELF 库名依赖、AVB 镜像自校验，输出 SHA256。AVB 自校验通过不代表厂商认可签名。

真实硬件的启动、触摸、震动、亮度、USB/ADB/MTP、解密、fastbootd、动态分区和重启路径均未验证。参见 DEVICE-NOTES.md，但其中 Colab 入口/历史进度不作为 GitHub 实时状态。

`evidence/colab-status.json` 为历史记录；不能用于判断当前 GitHub 任务是否运行或成功。

## 文件

- `.github/workflows/build.yml`：手动工作流，最小只读仓库权限，产物上传。
- `ci/prepare.sh`：临时机器清理、依赖安装、可选 zram。
- `ci/watch.py`：磁盘保护与错误码传递。
- `ci/verify.sh`：校验与打包测试候选镜像。
- `tools/`：从 Colab 适配包复用的实际同步/编译/检查脚本。
- `device/meizu/meizu21/`：标准版设备树与原厂组件。

原始固件不被修改。首次云端失败后优先读取日志，不能把资源预检、工作流语法通过当作 Recovery 构建成功。

## 同一机器内修复重试

同步完成后读取本公开仓库 main 最新提交的设备树和构建脚本，每次记录实际 SHA。编译失败时等待最多 20 分钟；维护者推送修复后自动继续，最多八次，不重新下载 Android 源码。整个任务仍受 350 分钟上限约束。最终使用的配置 SHA 可能不同于触发工作流的 SHA，产物中必须附带 device-tree-commit.txt 与 recovery-local.patch。当前旧任务不会自动获得后来添加的工作流步骤。
