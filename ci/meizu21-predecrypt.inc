		// MEIZU21_PREDECRYPT: prepare OS properties before constructing the stock HAL.
		// Values read from mounted partitions take priority over the supplied stock baseline.
		const char* os_props[] = {"ro.build.version.release", "ro.build.version.security_patch"};
		const char* stock_props[] = {"14", "2023-10-05"};
		for (int i = 0; i < 2; ++i) {
			std::string value = TWFunc::System_Property_Get(os_props[i]);
			if (value.empty()) {
				value = stock_props[i];
				LOGERR("Meizu21: could not read %s; using supplied stock baseline %s\n", os_props[i], value.c_str());
			}
			TWFunc::Property_Override(os_props[i], value);
		}
		std::string vendor_spl = TWFunc::Partition_Property_Get("ro.vendor.build.security_patch", PartitionManager, "/vendor", "build.prop");
		if (vendor_spl.empty()) vendor_spl = "2023-10-05";
		TWFunc::Property_Override("ro.vendor.build.security_patch", vendor_spl);
		android::base::SetProperty("meizu21.crypto.props_ready", "1");
		// Gatekeeper waits for QSEE; KeyMint starts independently after props_ready.
		bool meizu21_crypto_services_running = false;
		for (int i = 0; i < 300; ++i) {
			if (android::base::GetProperty("init.svc.vendor.keymint-qti", "") == "running" &&
			    android::base::GetProperty("init.svc.vendor.gatekeeper_default", "") == "running") {
				meizu21_crypto_services_running = true;
				break;
			}
			usleep(100000);
		}
