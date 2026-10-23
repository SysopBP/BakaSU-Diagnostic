# KitsuSU SusFS Loader — Samsung preview 1

Target: ARM64 Android 16 GKI 6.12 kernel (`6.12.*-android16-*`), including the tested SM-S948U1 kernel. This is a loader preview, not a new SusFS driver or a general Samsung compatibility claim.

## Installation and activation

1. Restore working FragX/KitsuSU root first.
2. In KitsuSU Modules, install this ZIP. Installation does not load the kernel module immediately.
3. Use the working KitsuSU **Soft reboot** procedure to process module startup stages. A full reboot loses temporary FragX root; this module cannot restore root itself.
4. Open SusFS Configuration and inspect Status / Runtime availability. If SusFS was manually loaded already, the loader skips it.
5. Root check: `su -c 'cat /data/adb/modules/susfs_guard_lkm/load.log'`.

The manager module Action button also invokes the guarded loader in the current rooted session. It never clears a prior failure latch or forces a reload. If another loader module is installed, remove that module first. This package uses the upstream module ID to avoid running two independent loaders.

## Behavior and limitations

- Runs at module post-fs-data; KitsuSU's pinned soft-reboot implementation calls that stage.
- Does not install a common early script, write boot partitions, change SELinux mode, add hiding rules, or reboot automatically.
- Checks disable/remove and Android safe-mode properties, kernel family, ARM64, payload SHA-256, existing SusFS, and a concurrent-load lock.
- A failed or interrupted loader pauses later automatic attempts. A killed process can leave load.lock behind; inspect logs before manually removing that lock.
- Kernel-module loading still carries the same kernel-crash risk as the manual load. This wrapper has been tested in a mocked shell environment, not installed on a phone by the authoring session.
- Uses unchanged upstream v2.3.0-r18.4 binaries. SUS Path passed the earlier device test, but Kstat/open-entry hook writes failed on the tested kernel. This package does not fix those failures, and successful loading does not mean every feature works.
- Full reboot unloads the LKM; loading resumes only after root and the supported module startup stages run again.
- Existing manager configuration is not cleared by installation. The loader itself submits no hiding rules.

## Disable/remove and failure recovery

Disable or remove through KitsuSU Modules. This stops future module loads; it does not unload an LKM already in the running kernel. A full reboot clears the loaded LKM and temporary root.

After an ordinary load failure, inspect `load.log` and `load.log.previous`. Do not repeatedly retry unchanged failing payloads. If the cause is understood and corrected, remove only `load-failed` in this module's directory before a deliberate retry. The wrapper never bypasses the duplicate-load check.

## Provenance, licensing, and credits

SusFS LKM/loader: inforcqb, https://github.com/inforcqb/susfs4ksu-lkm/tree/v2.3.0-r18.4
Upstream origins credited by that project: simonpunk/susfs4ksu and SukiSU-Ultra (memory patching, LSM hooks, symbol resolver). See included upstream source and LICENSE.

Wrapper adaptation: SysopBP, 2026-10-23. GPL-2.0-only. Source for this wrapper is the shell scripts in this ZIP. Corresponding upstream source is bundled as `source/susfs4ksu-lkm-v2.3.0-r18.4.tar.gz`. Binary checksums are in payload.sha256. Upstream release ZIP SHA-256: 7288d43d2965957c1fa95f91b8e58387a6d15a16003b75d0c0dcaaac26529888.
