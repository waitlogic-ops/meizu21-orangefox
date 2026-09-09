# Meizu 21 OrangeFox revision 2

This revision addresses two confirmed configuration/code defects; it does not establish the cause of the reported splash hang, and has not been tested on a phone.

- After 30 seconds without both KeyMint and Gatekeeper processes running, skip startup automatic decryption and log the failure. Preserve encrypted state. A running process does not prove Binder readiness, and this does not bound a later blocking HAL RPC.
- Supply FunctionFS/configfs MTP and MTP+ADB actions, wait for MTP and ADB descriptors, and remove the extra gadget links when leaving that mode. Keep upstream ADB/sideload/fastbootd handling. Exclude the legacy USB init override.

## References

User-supplied recovery14.img: SHA256 6871c9f3678315955638e45dbd290131841c025543ea45e0e6f1381f79d4e048. Its properties identify m2461/API34, build 2025-08-10. Header v4, no kernel, legacy LZ4 ramdisk, 100 MiB. No binaries copied from this image.

https://github.com/adontoo/device_meizu_m2481-TWRP/tree/c7cea8004036ca55bc3fce125080aa0ad7c28bac

Both reference configurations use ffs.mtp plus ffs.adb. The Pro's crypto script waits up to 30 seconds for process startup, but does not itself protect our C++ automatic-decryption call. Its TWRP16 settings and device-specific drivers are not Meizu21 OrangeFox14 compatibility evidence.

The old m2461 image does contain its AAC config through /odm/etc -> /vendor/odm/etc. Missing config is therefore not an established explanation for the reported absence of vibration. Keep the stock-derived vibrator service, dependencies, configuration and firmware already present in this project's ramdisk.

## Validation

`python3 tests/test_predecrypt.py` compiles and executes the patched startup block with simulated init properties. It checks timeout skips decryption, immediate readiness and delayed readiness. The old hook failed the timeout assertion before the fix.

Image verification requires the compiled timeout log marker and configfs MTP configuration, in addition to partition format, FBE flags, required files and ELF dependency checks. These checks cannot validate actual touch, haptics, display, decryption, USB enumeration or successful boot.

## Working m2461 reference follow-up

The user confirmed the old image enters its UI and can access internal files. Its QSEE, KeyMint, Gatekeeper and selected QSEE dependency binaries match the supplied stock components byte-for-byte. Unlike the prior OrangeFox image, stock and recovery14 ueventd grant system access to Qualcomm DMA heaps. The KeyMint service in our tree runs as system, as in stock. Restore stock qcom heap, qce and ion node permissions; the QSEE library explicitly references qcom,qseecom and qcom,qseecom-ta. This closes a static permissions gap, but remains unproven as the splash failure's cause.

The vibrator startup also restores stock system ownership and mode 0600 on /sys/class/qcom-haptics/primitive_duration after module loading. The AAC device node already grants system access. This is a stock-alignment correction, not proof of working haptics.
