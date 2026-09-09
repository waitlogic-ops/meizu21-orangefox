# Meizu 21 R4：以 21 Pro 设备树为基准

用户明确要求完全参考 21 Pro 方案。本版撤销 R2/R3 自行设计的启动修改，以固定参考版本为基准；仍为尚未真机验证的 OrangeFox 候选。

参考：https://github.com/adontoo/device_meizu_m2481-TWRP/tree/c7cea8004036ca55bc3fce125080aa0ad7c28bac

## 原样采用

以下文件逐字复制，SHA256 记录于 `evidence/R4-reference-contract.json`：

- init.recovery.qcom.rc、init.recovery.usb.rc。
- KeyMint、Gatekeeper、QSEE、Secure Element、健康、启动控制、震动服务和 start_crypto_services 的 init 配置。
- start_crypto_services.sh：模块加载事件启动脚本；脚本启动 KeyMint 并等待进程状态。没有加入自定义属性门槛或解密跳过逻辑。
- system.prop、recovery.fstab、system/vendor/vendor-odm 的 ueventd 配置。

BoardConfig 以参考文件为底稿，保留其 APEX 禁用、加密选项、99.87.36/2099-12-31 版本属性、默认中文、亮度、120 帧配置、触摸映射、屏幕启动设置及工具选项。上述版本属性属于参考项目的兼容配置，不是实际 Android 版本或真实安全补丁水平。

删除自定义 predecrypt C++ 补丁、30 秒后跳过自动解密逻辑、屏幕编号与对应源码补丁。构建使用未添加这些补丁的 OrangeFox recovery 源码。

## 必须保留的机型和产品差异

| 差异 | 依据 |
|---|---|
| M2461/meizu21 名称、目录与原厂 Image | 成品面向标准版；不使用 Pro 的内核或设备标识 |
| 标准版原厂 HAL、依赖库和固件 | 服务方案来自 Pro，硬件二进制来自用户标准版固件；新增文件来源与哈希见 R4-stock-components.json |
| 标准版驱动模块列表、vendor_boot 模块加载 | 不加载 Pro 压感/NFC 专用模块 |
| 不采用 Pro 的 9663676416 super 容量和分组配置 | 缺少标准版相同容量的证据；recovery 使用设备动态分区元数据识别实际布局 |
| 不套用 thermal_zone47 CPU 温度节点 | 没有证据证明标准版该节点含义相同 |
| OrangeFox fox_14.1 源码、OrangeFox 构建变量 | 用户要 OrangeFox；参考项目使用 TWRP 16，二者不是同一个源码树；触摸映射通过 OrangeFox 对应变量启用 |
| TARGET_RECOVERY_DEVICE_DIRS、库复制规则 | 将标准版组件纳入 OrangeFox ramdisk；显式包含 debuggerd 两个依赖，修正此前漏库 |
| GitHub Actions 的固定依赖版本、资源监控和产物校验 | 保留可复现、适合免费运行器的现有编译基础设施；不改变手机启动流程 |

100 MiB、header v4、LZ4、不含内核的 recovery 结构与两机参考一致。fstab 本轮按参考原样使用，云端静态核验不能证明每条挂载在标准版真机上正常。

## 检查与交付门槛

本地检查参考文件哈希、服务可执行文件存在、原厂组件依赖和构建脚本。云编译后再次核对实际镜像内的原样文件、版本属性、APEX 禁用、无自定义启动补丁及 ELF 依赖；通过后才发布候选镜像。

镜像名称：`OrangeFox-meizu21-R4-PROSCHEME.img`。R4 没有屏幕阶段编号。启动、触摸、震动、解密和其他硬件功能仍未验证；照参考配置不等于已证明可用。助手不执行实体机命令，用户测试与回滚说明见 TESTING.md。
