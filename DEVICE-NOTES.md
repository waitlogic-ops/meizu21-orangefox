> R4 已切换为 21 Pro 参考方案。以下为原始设备取证与早期适配记录；当前启动、加密、USB 和服务配置以 REFERENCE-R4.md 及实际设备树为准。

# 魅族 21 OrangeFox / Colab 实验性适配包

状态：设备树已准备，尚未通过完整源码编译，未在真机运行。此目录不包含新生成的 recovery 镜像。原厂文件未改动。

## 设备与方案

| 项目 | 从本地固件确认的值 |
|---|---|
| 设备 | meizu21，M2461，MEIZU 21 |
| 平台 | Qualcomm pineapple（骁龙 8 Gen 3 / SM8650 平台）|
| 系统 | Android 14 / API 34，Flyme 10.5.0.2G |
| 首发 API | 34 |
| 指纹 | meizu/meizu_21/meizu21:14/UKQ1.230917.001/1724151849:user/release-keys |
| 内核 | 6.1.25-android14-11，原厂 ARM64 Image |
| 启动结构 | boot v4 仅内核；init_boot v4 通用 ramdisk；vendor_boot v4 驱动 ramdisk、DTB、bootconfig；独立 recovery v4 无内核 |
| 分区 | A/B + Virtual A/B 压缩快照；system/vendor 等为动态逻辑分区 |
| recovery 镜像容量 | 原厂文件 104857600 字节（100 MiB），真机分区大小还需 fastboot 核实 |
| 文件系统 | 系统 EROFS；data 与 metadata 为 F2FS |
| 加密 | FBE v2 + inlinecrypt_optimized + wrappedkey_v0；metadata encryption 为 aes-256-xts:wrappedkey_v0 |

原厂 recovery.fstab 仍写旧式 `fileencryption=ice`，适配使用 vendor_boot 的实际启动 fstab。原件、哈希、模块与源代码版本记录在 evidence。

选择独立 recovery 路线：复用设备已有的 boot 内核、vendor_boot 驱动/DTB、dtbo、init_boot。构建目录中的 prebuilt/Image 来自原厂 boot，仅满足构建依赖；`BOARD_EXCLUDE_KERNEL_FROM_RECOVERY_IMAGE` 保证不嵌入 recovery。不构建或更换内核，不生成 super，不猜测 super 分区大小，不将 vendor ramdisk 合并进 recovery。

OrangeFox 官方同步脚本在核实时标记 R12.0，支持 12.1、14.1；本机首发 API 34，采用 fox_14.1。该构建分支仍被同步脚本标记为实验性。官方 wiki 部分页面仍标记 R11.3，版本以源码及实际产物内的标识为准。每次 Colab 同步保存精确 manifest，避免把构建分支号误当发布版本。

## Colab 操作

1. 在 Chrome 已登录的 Colab 上传旁边的 `Meizu21-OrangeFox-Colab.ipynb`。
2. 使用 Python 3 CPU 运行时。GPU 不加速 Android 编译。首个单元检查 x86_64、磁盘和内存。
3. 官方给出的 14.1 空间要求为至少 85 GB（约 79.2 GiB）；110–150 GiB 是包含编译产物的保守建议，不是硬门槛。内存最低 10 GiB、建议 24 GiB。脚本每 15 秒监测磁盘，空闲低于 8 GiB 时停止并保留源码及日志。实际需求由同步与编译结果决定。
4. 第二个单元上传 `Meizu21-OrangeFox-kit.zip`，它仅含适配所需文件，无需上传整个固件。
5. 顺序运行环境安装、官方源码同步、构建、检查和下载。编译使用普通用户 foxbuild；日志实时输出并保存在 `/content/fox-logs`。
6. 源码在 `/content/fox-work/fox_14.1`；镜像预期在 `out/target/product/meizu21/recovery.img`。下载单元只在编译和结构/依赖检查成功后标注成功。
7. 若 Colab 报配额、磁盘不足、OOM 或会话中断，保留日志；当前会话还在时可以重复执行相应步骤。运行时被删除后需重新上传、同步。Google Drive 扩容不能增加运行时磁盘；不会自动购买套餐或规避会话限制。

## 已实现的适配与验证边界

| 功能 | 配置/依据 | 当前验证状态 |
|---|---|---|
| 内核、DTB、DTBO、驱动 | 保留原厂启动链；vendor ramdisk 包含 Goodix、mz_gesture_ts、haptic_aac 等模块 | 已静态核实，启动加载未验证 |
| 触摸、按键 | 使用现有输入事件与原厂模块 | 未验证；首次不启用 Meizu 坐标缩放，确认异常后才启用 notebook 的 MEIZU_TOUCH_MAPPING |
| 震动 | 原厂 AIDL vibrator 服务、AAC 配置与依赖库 | 静态依赖已收集，接口/校准/SELinux/运行时尚未验证 |
| 亮度 | 原厂 panel0-backlight 节点；默认 1024，DTBO 给出的上限 4095 | 真实 max_brightness、灭屏/唤醒未验证 |
| USB/ADB/MTP | 原厂 a600000.dwc3 peripheral 设置 + 默认 TWRP configfs USB | 未验证 |
| 分区挂载/FBE | 原厂 vendor fstab 加密参数、metadata、KeyMint/Gatekeeper/QSEE 服务 | 未验证，不能保证 PIN/密码解密 |
| 动态分区/fastbootd | A/B、动态分区、快照支持和 fastbootd | 未编译/未验证；未猜测 super 几何 |
| 电量/时间 | 上游标准 health/RTC 读取和原厂内核 | 未验证；暂不启用未经核实的 RTC 偏移补丁 |
| 重启/槽位 | 原厂 Qualcomm AIDL boot control，UI reboot targets | 未验证，首次不切换槽位 |

原厂 recovery 的 AVB 为 SHA256_RSA4096，回滚索引 1，主 vbmeta 以索引位置 1 链接 recovery。测试构建使用公开 AOSP 开发密钥，保持索引 1，不是厂商签名；不会默认修改设备 vbmeta。

实验性服务使用 recovery SELinux 域，未完成适配后的最小权限策略。库名闭包不等于 ABI、链接器 namespace、TEE 固件及 SELinux 全部兼容。源码编译失败或产物检查失败都必须继续修正，不能将该包描述为已成功移植。

## 首次真机测试与回滚

以下是产物编译/检查成功后的操作方案，目前不要刷入任何本目录文件。设备必须已解锁，且实际运行的 boot/vendor_boot/init_boot/dtbo/vendor 基线与本次固件一致。若当前手机已经升级 Flyme/Android，需要先重新提取当前版本；不要把老版本 boot 等刷上去凑基线。

先保存照片和应用数据，并准备与手机当前版本一致的原厂 recovery。包中记录的旧版 recovery 哈希是 `c1ed5ccd6d575ed9e3f991b5f2ee4219108afa62c8e22f0b0b976ea2a2378f3d`。恢复 recovery 不会恢复已经被格式化或破坏的用户数据。

在 bootloader fastboot 中只读检查：

```sh
fastboot getvar product
fastboot getvar current-slot
fastboot getvar has-slot:recovery
fastboot getvar partition-size:recovery_a
fastboot getvar partition-size:recovery_b
fastboot getvar unlocked
fastboot getvar is-userspace
```

只有结果确认机型、已解锁、独立 recovery_a/recovery_b、容量足够、处于 bootloader fastboot 后，才能刷当前槽。先保留另一槽 recovery，记录 current-slot，勿猜测 `recovery_ab` 伪分区名。

例如当前槽确认为 a，才使用：

```sh
fastboot flash recovery_a recovery.img
fastboot reboot recovery
```

若为 b，将命令中的 recovery_a 改为 recovery_b。不要对本机使用 `fastboot boot recovery.img`：此镜像没有内核。不要为测试而刷 boot、vendor_boot、init_boot、dtbo、vbmeta，也不要默认关闭 AVB。若引导拒绝镜像，收集错误后再判断，不能保证所有魅族引导程序都接受这种未由厂商签名的 recovery。

进入 UI 后先检查画面、四角触摸、音量/电源键、低亮度、震动、ADB、MTP、时间和电量。不要格式化 Data。能进入 UI 并不代表解密成功；用现有 PIN/密码测试并确认 `/data/media/0` 可读、文件内容正常。解密失败时记录日志，禁止反复格式化试错。

运行 `tools/collect-device.sh` 收集日志。确认挂载、fastbootd 能枚举、返回 recovery、返回 system、再次返回 bootloader。首次仅运行查询，避免擦除/调整动态分区或切换槽位。快照合并进行中时不要进行分区写入测试。

若黑屏、触摸无法恢复或无法正常启动：通过手机可用的实体键方式回 bootloader，向刚才测试的同一个 recovery 槽刷回与当前系统相匹配的原厂镜像，再重启。以槽 a 为例：

```sh
fastboot flash recovery_a /path/to/current-stock/recovery.img
fastboot reboot
```

如果无法进入 bootloader，普通 fastboot 回滚不可用；本方案不承诺 EDL 救砖能力。

## 来源

- [OrangeFox 官方编译指南](https://wiki.orangefox.tech/dev/building)
- [OrangeFox 官方同步脚本](https://gitlab.com/OrangeFox/sync)
- [OrangeFox 14.1 recovery 源码](https://gitlab.com/OrangeFox/bootable/Recovery/-/tree/fox_14.1)
- [OrangeFox 构建变量](https://wiki.orangefox.tech/dev/build_vars)
- [AOSP vendor boot 结构](https://source.android.com/docs/core/architecture/partitions/vendor-boot-partitions)
- [Google Colab 资源与运行时说明](https://research.google.com/colaboratory/faq.html)

设备配置为本次适配草稿；固件二进制仍属各自权利人，只用于用户设备的兼容研究。原厂 fstab 许可证文本保留在 evidence，公开分发前须核实对应许可和 OrangeFox 源码提供义务。
