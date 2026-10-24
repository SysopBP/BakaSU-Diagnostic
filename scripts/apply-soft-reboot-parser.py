#!/usr/bin/env python3
"""Retain Samsung service tracking when the upstream waitsys helper cannot start."""
from pathlib import Path
from shutil import copyfile

path = Path('userspace/ksud/src/android/soft_reboot.rs')
source = path.read_text()
replacements = [
    ('    info!("emulating soft_reboot!");\n', '    info!("waiting for Samsung bootchecker before soft reboot");\n    samsung_bootchecker::wait_for_safe_boot().map_err(anyhow::Error::msg)?;\n    info!("emulating soft_reboot!");\n'),
    ('const WAITSYS_FD_ENV:', 'mod samsung_services;\nmod samsung_bootchecker;\n\nconst WAITSYS_FD_ENV:'),
    ('    info!("stop");\n', '''    // Keep the phone-tested Samsung parser if waitsys cannot initialize.
    let fallback_services = if !wait_after_stop {
        match samsung_services::collect_system_server_services() {
            Ok(services) => Some(services),
            Err(error) => {
                warn!("Samsung fallback could not collect services: {error:#}");
                None
            }
        }
    } else {
        None
    };

    info!("stop");
'''),
    ('    info!("post-fs-data");\n', '''    if let Some(services) = fallback_services {
        samsung_services::wait_for_system_server_services(&services);
    }

    info!("post-fs-data");
'''),
]
for old, new in replacements:
    if source.count(old) != 1:
        raise SystemExit(f'Unexpected upstream soft-reboot anchor: {old!r}')
    source = source.replace(old, new, 1)
destination = path.parent / 'soft_reboot/samsung_services.rs'
destination.parent.mkdir(parents=True, exist_ok=True)
copyfile(Path(__file__).resolve().parents[1] / 'vendor/userspace/samsung_services.rs', destination)
bootchecker = path.parent / 'soft_reboot/samsung_bootchecker.rs'
copyfile(Path(__file__).resolve().parents[1] / 'vendor/userspace/samsung_bootchecker.rs', bootchecker)
path.write_text(source)
print('Preserved Samsung service tracking fallback alongside upstream waitsys')
