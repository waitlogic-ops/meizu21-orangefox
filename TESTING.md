# 魅族 21 OrangeFox 首次测试与回滚

R4 不显示阶段编号，启动与加密流程见 REFERENCE-R4.md。

本说明面向 Meizu 21 标准版 M2461/meizu21 的实验镜像。不是 Meizu 21 Pro。当前文档不代表已有镜像通过编译或真机测试；以随镜像交付的校验结果为准。

## 刷入前

- 确认镜像 SHA256 与 SHA256SUMS 一致，使用最终通过校验的构建，不要混用 R1、R2 或其他运行的镜像。本版 R4 是参考 21 Pro 的候选，静态校验通过仍不代表启动已修复。
- 核实手机仍为对应的 Android 14 / Flyme 10.5.0.2G 基线。其他 ROM 必须重新评估 HAL、内核和解密兼容性。
- 手机必须已解锁 bootloader。若未解锁，停在此处；解锁可能清除用户数据，本流程不执行解锁。
- 备份重要数据，并保存同基线的原厂 recovery.img。首次测试只修改确认过的当前 recovery 槽位。
- 不修改 boot、vendor_boot、init_boot、dtbo 或 vbmeta，不格式化 data/metadata。

在 fastboot 模式读取设备信息：

```sh
fastboot getvar product
fastboot getvar current-slot
fastboot getvar partition-size:recovery_a
fastboot getvar partition-size:recovery_b
fastboot getvar unlocked
```

如果变量不受支持，不能把空输出解释为已解锁或默认 A 槽。需要使用设备支持的方法进一步确认。预期 recovery 容量为 104857600 字节，即 0x6400000；机型、槽位或容量不符时停止。

## 首次刷入示例

仅当明确确认当前槽位为 a、设备和镜像匹配时：

```sh
fastboot flash recovery_a OrangeFox-meizu21-R4-PROSCHEME.img
fastboot reboot recovery
```

若当前槽位是 b，则只把刷入目标替换为 recovery_b。首次不要同时覆盖两个槽位。若 bootloader 不支持 reboot recovery，使用它支持的进入 Recovery 方法，不继续尝试随机分区命令。

该镜像不含内核，不使用 `fastboot boot` 加载。AVB 自校验成功不等于拥有原厂签名；如果启动验证拒绝镜像，先回滚并收集错误，不直接刷改 vbmeta。

## 测试顺序

1. 显示与交互：能进入界面，触摸位置准确，按键有效；屏幕关闭后能唤醒；亮度可调。
2. USB：ADB 可发现设备。MTP 使用支持 Android MTP 的电脑客户端测试；Mac 的 Finder 没显示设备并不能单独证明 MTP 失败。
3. 状态：检查时间/时区、电量/充电状态及 GUI 设置中的震动反馈。
4. 存储：先以只读方式检查系统分区。由机主在设备界面输入 PIN/密码测试 data 解密；失败时不格式化、不尝试删除锁屏数据。
5. 重启：分别验证重启 system、bootloader、recovery。测试 fastbootd 后，用 `fastboot getvar is-userspace` 确認其是否返回 yes，再返回 system。
6. 动态分区：核对逻辑分区可识别、可只读挂载。首次不以刷写 system/super 来测试，也不清除快照状态。

可以收集以下只读诊断：

```sh
adb devices
adb shell uname -a
adb shell cat /proc/modules
adb shell getprop init.svc.vendor.qseecomd
adb shell getprop vendor.sys.listeners.registered
adb shell getprop init.svc.vendor.keymint-qti
adb shell getprop init.svc.vendor.gatekeeper_default
adb shell getprop init.svc.vendor.qti.vibrator
adb pull /tmp/recovery.log
adb logcat -d > recovery-logcat.txt
```

日志可能包含设备标识或文件名，分享前检查并遮盖个人内容。不得把用户 PIN/密码写入命令或日志。

## 回滚

重新进入 bootloader fastboot，用同基线原厂镜像恢复本次实际修改的 recovery 槽位。例如只修改过 a：

```sh
fastboot flash recovery_a recovery.img
fastboot reboot
```

如果修改过 b，则恢复 recovery_b。不要为了回滚实验 Recovery 而刷整套固件或改变活动槽位。

本任务的原厂恢复镜像在用户 Mac 上：

```text
/Users/spoffish/Downloads/魅族 21/MEIZU21GLOBAL 国际版/FIRMWARE/recovery.img
```

执行回滚时明确指定该原厂镜像或其校验一致的副本，不要误用同名实验文件。若无法进入 fastboot，停止继续写入，按设备可用的原厂恢复途径处理。

## 未验证项

在得到真机记录前，启动、触摸、震动、亮度、按键、USB/ADB/MTP、data 解密、动态分区、fastbootd、重启和时间/电量都应标记为未验证。构建与静态检查只能证明镜像结构和部分依赖符合预期，不能证明上述硬件功能正常。
