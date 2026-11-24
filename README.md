# TWRP device tree for POCO C40 (`frost`)

Device tree for building TWRP 3.7.x on the Android 11 recovery source tree. The target device is the POCO C40 (codename `frost`, JLQ JR510). This repository contains the device tree; it does not contain the Android/TWRP source checkout or a flashable image.

## Build

Place this repository at `device/xiaomi/frost` in a TWRP 11.0 source checkout, then run:

```bash
export ALLOW_MISSING_DEPENDENCIES=true
source build/envsetup.sh
lunch twrp_frost-eng
mka bootimage -j"$(nproc --all)"
```

The output is `out/target/product/frost/boot.img`. This device has no dedicated recovery partition; recovery is packaged as a boot image. Confirm the image and partition layout for your firmware before flashing.

## Device and current status

- POCO C40, codename `frost`; Android 11; JLQ JR510
- A/B slots; boot and vendor_boot partitions
- `/data` uses F2FS and file based encryption; metadata encryption keys are under `/metadata/vold/metadata_encryption`
- The fstab retains the FBE and key directory parameters needed for encrypted data handling.
- Russian is the default interface language and additional TWRP languages are enabled.

A local build completed, but this tree has not yet been validated on the phone. In particular, mounting/decrypting `/data`, storage capacity reporting, and the boot flow still need on-device verification. Treat images built from this tree as experimental.

## Flashing

Only flash an image built for this device and firmware. Make a backup of the stock boot image first. Since there is no recovery partition, recovery images use the boot partition; flashing the wrong boot image can prevent Android from starting.
