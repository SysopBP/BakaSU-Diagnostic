# Samsung upstream integration — 23 October 2026

Development branch: `test/bakasu-upstream-sync-20261023`. No main merge or release is authorized.
The phone-tested source pin remains `239e1e8871b8fcd51a6e5b3002e0ba522fdd99fb`.
The Samsung vendor port, manager identity/artwork/recovery controls and existing
tablet service-list parser patch are reapplied after the upstream patch queue.

## Implemented source integration

`scripts/apply-upstream-series.py` applies the ordered, checked-in patches in
`patches/bakasu` to a clean baseline. Kernel, daemon and manager jobs all use the
same queue; conflicts fail closed. Original authors and commit messages are
retained in the patch files. These are source integrations, not device verification.

| Upstream commit | Integrated change |
| --- | --- |
| ba8cfa502e | SID table detection |
| 969de3d0ce | Permission check order |
| 648144087e | Check daemon presence before manual su exec handling |
| f397410c7d | SELinux avtab lengths and extended permission updates |
| 20756bfbc0 | Sequential boot-slot metadata enumeration |
| fedfbb2d3e | Explicit boot-image parse failure |
| f6513993fb + 8450dd287e | Synchronous manager tracking deferred outside normal fsnotify callback locks |
| b0fa24df91 | Temporarily override credentials when loading allowlist, restoring on every exit |
| 9fc9b9c66c | Bound APK ZIP-comment scan by bytes scanned |
| 6803643e19 | Make boot-completed receiver private |
| 75de877b5d | Splash/WebUI startup repair, excluding generated baseline profiles |

The slot-info change reads metadata only; it does not repair or replace SusFS.
SusFS build/package jobs are skipped on this integration branch, while their
existing implementation and separate repair branches remain intact.

## Failure resolved and remaining work

Run `40062821818` failed before kernel compilation on all eight KMIs. Its blind
cherry-pick of `d7260ca1e5` conflicts with the baseline SELinux implementation and
compatibility Makefile. It depends on the later SELinux context-conversion rewrite.
The new queue removes that unbuildable transplant; this does not claim the hash
handling fix itself is integrated. Port it with `fa12ffde82` and audit Samsung RKP
call-through anchors before enabling it.

The waitsys bundle (`d7f199613d`, `91157d2764`, `6ce433809b`), service-stage UAPI
change, script timeouts, package rename, flashing changes and optional module
repository features remain separate follow-up work. Retaining the existing soft
reboot path avoids silently replacing the phone-tested implementation.

Local validation: clean-baseline queue application, Samsung kernel patch anchors,
manager package migration, soft-reboot parser anchor and artwork verification pass.
The build environment lacks Cargo/Android/DDK tooling locally; GitHub Actions runs
the host Rust parser tests and eight driver builds, then daemon/APK builds and
embedded-daemon/signature/package checks. A passing build is not a device test.

Device acceptance still requires FragX root establishment, allowlist persistence,
normal and repeated soft reboot, manager authorization, recovery controls, module
WebUI startup and Samsung compatibility testing on S26 Ultra and Tab 11 separately.
Keep the known-working installation available until those tests pass.
