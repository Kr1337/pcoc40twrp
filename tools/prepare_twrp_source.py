#!/usr/bin/env python3
"""Apply the POCO C40 TWRP branding and recovery-boot fixes to an Android source tree."""
from pathlib import Path
import re
import sys

if len(sys.argv) != 2:
    raise SystemExit(f"usage: {sys.argv[0]} ANDROID_SOURCE_ROOT")
root = Path(sys.argv[1]).resolve()
required = [
    root / "bootable/recovery/variables.h",
    root / "vendor/twrp/config/BoardConfigTWRP.mk",
    root / "bootable/recovery/gui/theme/common/portrait.xml",
]
if not all(path.is_file() for path in required):
    raise SystemExit("not a TWRP Android source root")

def replace_text(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    if new in text:
        return
    if old not in text:
        raise SystemExit(f"expected text missing from {path}: {old!r}")
    path.write_text(text.replace(old, new))

# TW_VERSION_STR joins main + '-' + TW_DEVICE_VERSION from this device tree.
p = root / "bootable/recovery/variables.h"
text = p.read_text()
text = re.sub(r'(#define TW_MAIN_VERSION_STR\s+)"(?:3\.7\.0_11|codex-frost-twrp_3\.7\.0)"', r'\1"codex"', text)
text = text.replace('#define TW_VERSION_STR TW_MAIN_VERSION_STR\n', '#define TW_VERSION_STR TW_MAIN_VERSION_STR TW_DEVICE_VERSION\n')
if '#define TW_MAIN_VERSION_STR       "codex"' not in text or '#define TW_VERSION_STR TW_MAIN_VERSION_STR TW_DEVICE_VERSION' not in text:
    raise SystemExit("could not set the requested recovery version")
p.write_text(text)

# Android 11 manifest adds a recovery fastboot cmdline that sends this board back to the bootloader.
p = root / "vendor/twrp/config/BoardConfigTWRP.mk"
text = p.read_text()
text, count = re.subn(
    r'\nifeq \(\$\(BOARD_USES_RECOVERY_AS_BOOT\),true\)\s*\n.*?twrpfastboot=1.*?\nendif\s*\nendif\s*',
    '\n', text, count=1, flags=re.S)
if count == 0 and 'twrpfastboot=1' in text:
    raise SystemExit(f"unrecognized twrpfastboot block in {p}")
p.write_text(text)

common = root / "bootable/recovery/gui/theme/common"
for p in [common / "portrait.xml", common / "landscape.xml", *sorted((common / "languages").glob("*.xml"))]:
    if p.is_file():
        text = p.read_text().replace("Team Win Recovery Project", "Anime FemBoy Recovery Project")
        p.write_text(text)

p = root / "bootable/recovery/gui/theme/portrait_hdpi/splash.xml"
text = p.read_text().replace("<author>TeamWin</author>", "<author>Anime FemBoy Recovery Project</author>")
text = re.sub(r'\n\s*<image name="splashteamwin" filename="splashteamwin" retainaspect="1"/>', '', text)
text = re.sub(r'\n\s*<image>\s*<image resource="splashteamwin"/>\s*<placement[^>]*/>\s*</image>', '', text)
text = text.replace("Recovery Project %tw_version%", "Anime FemBoy Recovery Project")
p.write_text(text)
print("Applied POCO C40 TWRP version, branding, and recovery boot fixes.")
