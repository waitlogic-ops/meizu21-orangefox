# 适配审计与尚待验证项

目前没有真机日志。原厂依据见 evidence，不能把参考 21 Pro 的硬件行为当作标准版事实。

## 已依据源码核对

- fox_14.1 支持独立 A/B recovery、AIDL boot control、AIDL haptics 和 Meizu 触摸映射开关。
- 触摸映射开关仅值为 1 时生效；目前保持关闭，需 getevent/显示坐标证据决定。
- 原厂 recovery 模块列表含 goodix_ts.ko、haptic_aac.ko、qcom-hv-haptics.ko、qti_battery_charger.ko。
- 源码可从 vendor_boot 的 /lib/modules 加载模块，但需要显式启用对应选项；现已显式启用原厂 vendor_boot 模块加载后备路径，尚待真机确认。
- 原厂 qseecomd 二进制含 vendor.sys.listeners.registered 属性名。

## 构建后必须处理/验证

- 检查原厂模块是否实际加载；若缺失，在设备树中启用按原厂清单的模块加载，不能采用 Pro 的全部模块列表。
- 检查 qseecomd 访问 ssd 分区的时序。参考项目等待节点再启动，Gatekeeper 等待 listeners.registered；现已按此顺序修改，尚待真机确认。
- KeyMint 启动前应使用已安装系统的版本和安全补丁属性。参考 TWRP 16 的 prepdecrypt 逻辑不能直接假定存在于 OrangeFox 14.1，已增加 Meizu 专用源码补丁，在 Decrypt_Data 前读取已安装系统属性并发出就绪信号；读取失败回退到已提供的原厂 Android 14/2023-10-05 基线并记录日志。其他 ROM 不保证兼容。
- 确认运行时 vendor/odm 挂载不会遮蔽 Recovery 内的 HAL/库，并检查动态加载依赖、VINTF 和 namespace。
- 验证 data metadata encryption/FBE、fastbootd、亮度、电池、触摸、震动、MTP 与重启路径。

上述不是完成项。编译产物只能标记为待真机验证候选。
