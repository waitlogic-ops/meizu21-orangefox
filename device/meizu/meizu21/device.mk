LOCAL_PATH := device/meizu/meizu21
PRODUCT_SHIPPING_API_LEVEL := 34
BOARD_SHIPPING_API_LEVEL := 34
PRODUCT_TARGET_VNDK_VERSION := 34
PRODUCT_USE_DYNAMIC_PARTITIONS := true
PRODUCT_SOONG_NAMESPACES += $(LOCAL_PATH)
PRODUCT_PACKAGES += fastbootd android.hardware.fastboot@1.0-impl-mock \
    lpflash lpmake lpunpack \
    libbase libbinder_ndk libc++ libc libcrypto libcutils libdl \
    libdmabufheap libgatekeeper libhardware libhidlbase libion liblog libm \
    libutils libxml2 android.hardware.boot@1.1 libz
PRODUCT_PROPERTY_OVERRIDES += persist.sys.fuse.passthrough.enable=true
