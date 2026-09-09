#!/usr/bin/env bash
if [[ "${FOX_BUILD_DEVICE:-}" == "meizu21" ]]; then
    export FOX_AB_DEVICE=1
    export FOX_VIRTUAL_AB_DEVICE=1
    export OF_AB_DEVICE_WITH_RECOVERY_PARTITION=1
    export OF_USE_AIDL_BOOT_CONTROL=1
    export OF_NO_REFLASH_CURRENT_ORANGEFOX=1
    export FOX_MAINTAINER="local-meizu21-bringup"
    export FOX_VARIANT="R4-ProScheme"
    export FOX_USE_MEIZU_TOUCH_MAPPING=1
fi
