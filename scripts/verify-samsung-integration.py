#!/usr/bin/env python3
"""Fail CI if source adaptation drops the Samsung ABI, identity, or reboot fallback."""
import argparse
from pathlib import Path
import struct

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source', type=Path, required=True)
root = parser.parse_args().source

checks = {
    'kernel/Kbuild': ['REPO_NAME := KitsuSU', 'compat/jailbreak.o compat/defex.o compat/kdp.o compat/rkp.o'],
    'kernel/core/init.c': ['init_jailbreak();', 'exit_jailbreak();'],
    'kernel/hook/arm64/patch_memory.c': ['return ksu_rkp_branch_patch(dst, src);'],
    'kernel/feature/selinux_hide.c': [
        'callthru_context_write(file, buf, size)',
        'callthru_access_write(file, buf, size)',
        'return callthru_setprocattr(name, value, size);',
        'callthru_sel_open_handle_status(inode, filp)',
        'ksu_rkp_get_stub(orig_context_write)',
        'ksu_rkp_get_stub(orig_access_write)',
        'context_add_hash(orig_policydb, &orig_context)',
    ],
    'manager/app/build.gradle.kts': ['namespace = "app.kitsusu.manager"', '"SAMSUNG_BUILD", "true"'],
    'manager/build.gradle.kts': ['extra["defaultManagerPackageName"] = "app.kitsusu.manager"'],
    'userspace/ksud/src/android/soft_reboot.rs': [
        'mod samsung_services;', 'Waitsys::spawn()',
        'samsung_services::collect_system_server_services()',
        'samsung_services::wait_for_system_server_services(&services);',
    ],
    'userspace/ksud/src/android/soft_reboot/samsung_services.rs': [r'^\d+\s+', 'Duration::from_secs(5)'],
    'userspace/ksud/build.rs': ['KSU_PACKAGE_NAME=app.kitsusu.manager'],
    'userspace/ksud/src/android/cli.rs': ['String::from("app.kitsusu.manager")'],
}
for filename, anchors in checks.items():
    content = (root / filename).read_text()
    for anchor in anchors:
        if anchor not in content:
            raise SystemExit(f'{filename}: missing required integration anchor {anchor!r}')

helper = (root / 'userspace/ksud/bin/aarch64/waitsys').read_bytes()
if len(helper) < 64 or helper[:6] != b'\x7fELF\x02\x01' or struct.unpack_from('<H', helper, 18)[0] != 183:
    raise SystemExit('waitsys must be a nonempty little-endian AArch64 ELF64 executable')
if not (root / 'manager/app/src/main/java/app/kitsusu/manager/ui/screen/main/KitsuRecoveryControls.kt').is_file():
    raise SystemExit('KitsuSU recovery UI missing after namespace migration')
print('Samsung source integration gates passed')
