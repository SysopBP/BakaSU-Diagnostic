# KitsuSU Preview 2

Experimental Samsung preview with the reviewed BakaSU upstream snapshot, Samsung compatibility adaptations, recovery controls, build-fingerprint display, and refreshed SusFS runtime reporting.

## Samsung startup and reboot

Includes the Samsung bootchecker preflight from d59d7b3: before emulated soft reboot, wait up to 90 seconds for bootchecker and boot animation to stop and both boot-completion properties to report ready. Refuse when crash recovery is pending, the service contract is unrecognized, reads fail, or the wait expires. Stock bootchecker and recovery properties are unchanged.

After installing or replacing the manager, use a full reboot before re-establishing FragX root. The maintainer reported that soft reboot immediately after manager installation left apps unable to load. Full reboot can remove temporary FragX root; follow the existing FragX root-establishment procedure.

## Downloads and signing

The manager APK, matching daemon and eight bundled KitsuSU KMI drivers are built together with the permanent KitsuSU signing identity. CI verifies the final APK certificate and embedded daemon. Corresponding modified source and SHA-256 checksums accompany the build. The manager retains the experimental debug variant.

SusFS is an optional, separate experimental module from [run 40059969066](https://github.com/SysopBP/BakaSU-Diagnostic/actions/runs/40059969066). It is not rebuilt or bundled by this release branch.

## Verification and limitations

On the maintainer's S26 Ultra (SM-S948U1), kernel 6.12.69-android16-6-pee899be-abogkiS948USQU4BZID-4k:
- Root returned UID 0 in the KernelSU domain.
- The optional SusFS module loaded, resolving all 113 undefined symbols.
- Ordinary Termux access to the SusFS module directory returned ENOENT while root could access it.
- The ordinary probe file remained readable because the KitsuSU eligibility gate exempted root-authorized Termux; counters showed umount_false increasing and allowed remaining zero. This is not proof that file hiding is broken or verified for eligible apps.
- Ordinary file hiding for apps without root authorization remains unverified. Kstat and redirect functionality are not certified by module load success.
- A startup app_process linker crash referencing libnativeloader.so was captured; its cause and relationship to this candidate remain unconfirmed.

Reported FragX/KitsuSU device results and firmware limits are documented in preview-2-signing.md. Tablet soft reboot remains separately unverified. No additional device tests were requested for this preview wrap-up.
