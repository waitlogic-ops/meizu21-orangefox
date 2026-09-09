$(call inherit-product, $(SRC_TARGET_DIR)/product/base.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit_only.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/virtual_ab_ota/compression_with_xor.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/emulated_storage.mk)
$(call inherit-product, vendor/twrp/config/common.mk)
$(call inherit-product, device/meizu/meizu21/device.mk)
PRODUCT_DEVICE := meizu21
PRODUCT_NAME := twrp_meizu21
PRODUCT_BRAND := meizu
PRODUCT_MODEL := MEIZU 21
PRODUCT_MANUFACTURER := meizu
