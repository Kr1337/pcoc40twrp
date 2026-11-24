# TWRP device tree for POCO C40 (`frost`)

Device tree for building TWRP 3.7.x on the Android 11 recovery source tree. The target is POCO C40 (`frost`, JLQ JR510), firmware V13.0.26.0.RGFMIXM.

## Build from source

Place this repository at `device/xiaomi/frost` in a TWRP 11.0 source checkout. Apply the version/branding and recovery-boot fixes, then build:

```bash
python3 device/xiaomi/frost/tools/prepare_twrp_source.py "$PWD"
export ALLOW_MISSING_DEPENDENCIES=true
source build/envsetup.sh
lunch twrp_frost-eng
mka bootimage -j4
```

The output is `out/target/product/frost/boot.img`. The tree's prebuilt kernel is the POCO C40 v35 reference kernel. This device has no dedicated recovery partition; recovery is packaged as a boot image.

The requested recovery version string is `codex-frost-twrp_3.7.0`; the interface header and splash text are `Anime FemBoy Recovery Project`.

## `/data` and recovery services

`/data` is F2FS with file based encryption and metadata encryption. The metadata key files are stored at `/metadata/vold/metadata_encryption`. The recovery fstab contains the stock FBE/key directory options.

A recovery log pulled from the phone showed that `/metadata` mounted, but `/data` did not: TWRP reported `Unable to decrypt metadata encryption`, then the F2FS driver reported an invalid superblock when it tried the still-encrypted userdata block. The running v35 ramdisk did not include `/vendor` or import the POCO Microtrust/Keymaster services. This tree now packages those vendor files and imports the recovery init services so they can be tested.

The hardware validation is still in progress. Do not treat FBE decryption or storage reporting as fixed until the phone reports nonzero `/data` capacity and successfully mounts the filesystem. Do not format `/data` as a troubleshooting step; that erases user data.

## Device

- POCO C40, codename `frost`, model 220333QPG
- Android 11, JLQ JR510
- A/B slots, `boot` and `vendor_boot` are each 96 MiB
- Dynamic `system`, `system_ext`, `product`, and `vendor` partitions
- No dedicated recovery partition

## Flashing

Use only an image built for this device and firmware. Keep a verified stock `boot.img` available before flashing. For initial tests, change only one boot slot and preserve the other slot as a fallback.
