# SPDX-License-Identifier: Apache-2.0
# Experimental bring-up for the supplied Flyme 10.5.0.2G firmware only.
DEVICE_PATH := device/meizu/meizu21
TARGET_ARCH := arm64
TARGET_ARCH_VARIANT := armv8-a
TARGET_CPU_ABI := arm64-v8a
TARGET_CPU_VARIANT := generic
TARGET_CPU_VARIANT_RUNTIME := cortex-a76
TARGET_NO_BOOTLOADER := true
TARGET_BOOTLOADER_BOARD_NAME := pineapple
TARGET_BOARD_PLATFORM := pineapple

BOARD_BOOT_HEADER_VERSION := 4
BOARD_KERNEL_PAGESIZE := 4096
BOARD_KERNEL_IMAGE_NAME := Image
TARGET_PREBUILT_KERNEL := $(DEVICE_PATH)/prebuilt/Image
BOARD_EXCLUDE_KERNEL_FROM_RECOVERY_IMAGE := true
BOARD_RECOVERYIMAGE_PARTITION_SIZE := 104857600
BOARD_MKBOOTIMG_ARGS += --header_version 4 --pagesize 4096
BOARD_RAMDISK_USE_LZ4 := true
# Stock recovery is kernel-free. Do not place DTB or vendor ramdisk here.
BOARD_AVB_ENABLE := true
# Public AOSP development key, never represented as an OEM signature.
# Keep the stock recovery rollback value (1); do not advance it to a date.
BOARD_AVB_RECOVERY_KEY_PATH := external/avb/test/data/testkey_rsa4096.pem
BOARD_AVB_RECOVERY_ALGORITHM := SHA256_RSA4096
BOARD_AVB_RECOVERY_ROLLBACK_INDEX := 1
BOARD_AVB_RECOVERY_ROLLBACK_INDEX_LOCATION := 1

AB_OTA_UPDATER := true
AB_OTA_PARTITIONS := boot dtbo init_boot odm recovery system_dlkm vbmeta vendor vendor_boot vendor_dlkm
# Do not guess super size/group geometry from the sum of extracted images.
BOARD_USES_METADATA_PARTITION := true
BOARD_USERDATAIMAGE_FILE_SYSTEM_TYPE := f2fs
TARGET_USERIMAGES_USE_F2FS := true
TARGET_USERIMAGES_USE_EXT4 := true
TARGET_USES_MKE2FS := true
BOARD_HAS_LARGE_FILESYSTEM := true
BOARD_HAS_NO_REAL_SDCARD := true
TARGET_RECOVERY_FSTAB := $(DEVICE_PATH)/recovery.fstab
TARGET_RECOVERY_DEVICE_DIRS += $(DEVICE_PATH)
TARGET_RECOVERY_PIXEL_FORMAT := "RGBX_8888"
TW_THEME := portrait_hdpi
TW_DEFAULT_LANGUAGE := en
TW_EXTRA_LANGUAGES := true
TW_BRIGHTNESS_PATH := "/sys/class/backlight/panel0-backlight/brightness"
# All parsed stock panel DTBOs specify 4095; stock init sets brightness to 2047.
TW_MAX_BRIGHTNESS := 4095
TW_DEFAULT_BRIGHTNESS := 1024
TW_FRAMERATE := 60
TW_INCLUDE_CRYPTO := true
TW_INCLUDE_CRYPTO_FBE := true
TW_INCLUDE_FBE_METADATA_DECRYPT := true
TW_USE_FSCRYPT_POLICY := 2
BOARD_USES_QCOM_FBE_DECRYPTION := true
TW_SUPPORT_INPUT_AIDL_HAPTICS := true
TW_INCLUDE_FASTBOOTD := true
TW_INCLUDE_RESETPROP := true
TW_INCLUDE_LIBRESETPROP := true
TW_INCLUDE_LPTOOLS := true
TW_INCLUDE_LPDUMP := true
TW_SKIP_ADDITIONAL_FSTAB := true
TW_ENABLE_FS_COMPRESSION := true
RECOVERY_SDCARD_ON_DATA := true
TARGET_USES_LOGD := true
TWRP_INCLUDE_LOGCAT := true
TW_DEVICE_VERSION := meizu21-Flyme10.5.0.2G-experimental
# Prebuilt ELF files are in recovery/root. Their closure is audited separately.
BUILD_BROKEN_ELF_PREBUILT_PRODUCT_COPY_FILES := true
BUILD_BROKEN_PLUGIN_VALIDATION := soong-libaosprecovery_defaults soong-libguitwrp_defaults soong-libminuitwrp_defaults soong-vold_defaults

# Libraries used by stock HALs copied into the recovery ramdisk.
TARGET_RECOVERY_DEVICE_MODULES += libbase libbinder_ndk libc++ libc libcrypto libcutils libdl libdmabufheap libgatekeeper libhardware libhidlbase libion liblog libm libutils libxml2 libz android.hardware.boot@1.1
RECOVERY_LIBRARY_SOURCE_FILES += $(foreach lib,$(TARGET_RECOVERY_DEVICE_MODULES),$(TARGET_OUT_SHARED_LIBRARIES)/$(lib).so)
