# BakaSU Diagnostic

Samsung-focused diagnostic and experimental build workspace for BakaSU-derived root-management work.

> **Experimental software.** This repository is a development and diagnostic workspace, not a guarantee of root support on any particular device, Android version, or security patch. Do not flash experimental images without a verified recovery path and a backup.

## Project relationship

- **BakaSU Diagnostic (this repository):** Samsung compatibility experiments, diagnostics, and build workflows. The original workspace targeted BakaSU 4.0.0.
- **KitsuSU:** A separately branded KernelSU-derived manager developed from this line of work, with Samsung-oriented integrations. Changes proposed in pull requests are not necessarily present on the default branch.
- **[FragX](https://github.com/SysopBP/FragX):** A separate DirtyFrag-derived application. The FragX preview release also presents the KitsuSU project; this does **not** mean FragX and KitsuSU share the same codebase or that either is compatible with every Samsung device.

**Current preview:** [FragX + KitsuSU — Samsung Preview 1](https://github.com/SysopBP/FragX/releases/tag/v0.1.0-preview.1)

## Development areas

- Samsung kernel compatibility investigation, including RKP, KDP, and DEFEX-related work
- Root manager, driver, and userspace integration diagnostics
- Build and packaging automation
- Experimental manager identity and branding work
- Source distribution and license compliance checks

The existence of a patch, workflow, or successful APK build does not prove a kernel exploit works or that a device is supported. Verify the exact branch, build artifact, kernel, firmware, and security patch before testing.

## Work in progress

Review outstanding changes before assuming they are merged into `main`:

- [PR #1 — source and GPL packaging](https://github.com/SysopBP/BakaSU-Diagnostic/pull/1)
- [PR #2 — Samsung compatibility and KitsuSU-related work](https://github.com/SysopBP/BakaSU-Diagnostic/pull/2)

Consult [Actions](https://github.com/SysopBP/BakaSU-Diagnostic/actions) for build results. A green CI run confirms only the checks performed by that workflow; it is not device-level validation.

## Building and testing

Inspect the relevant workflow under [`.github/workflows`](https://github.com/SysopBP/BakaSU-Diagnostic/tree/main/.github/workflows) and its source revision before using any artifact. Development or CI-signed APKs may not be update-compatible with separately signed releases. Do not distribute signing keys or credentials.

If reporting an issue, include the device model, Android and One UI versions, security patch date, kernel version, exact commit/build, and sanitized diagnostic output. **Never post private keys, tokens, device identifiers, or personal information.**

## Origins and credits

**KitsuSU began as a customized BakaSU-derived project; it is not an original replacement for the upstream root implementation.** The development lineage is:

[KernelSU](https://github.com/tiann/KernelSU) → [SukiSU Ultra](https://github.com/SukiSU-Ultra/SukiSU-Ultra) → [BakaSU (formerly ReSukiSU)](https://github.com/Baka-SU/BakaSU) → KitsuSU modifications in this workspace.

- **KernelSU / weishu and contributors:** original upstream kernel-assisted root project.
- **SukiSU Ultra and contributors:** intermediate downstream project credited by BakaSU.
- **BakaSU Development and contributors:** original BakaSU implementation and manager that KitsuSU was developed from.
- **OukaroMF:** original BakaSU artwork attribution; see BakaSU's asset-specific licensing documentation. Do not assume original artwork can be relicensed or reused as KitsuSU artwork.
- **diabl0w / DFRoot:** separately sourced Samsung-related compatibility work where actually incorporated; verify file-level provenance and applicable terms.
- **SysopBP and contributors/testers:** KitsuSU-specific branding, integration, diagnostic and Samsung-focused changes, subject to the actual commit history.

### Version and branding history

The original diagnostic workspace targeted **BakaSU 4.0.0**. Subsequent experimental work introduced the **KitsuSU** identity, manager changes and Samsung-specific integrations. A new name, icon, package identifier or driver label does not erase upstream copyright or change the underlying code's license.

### Licensing checklist

Upstream BakaSU documents **GPL-2.0-only for its kernel directory**, **GPL-3.0-or-later for most other code**, and separate licensing arrangements for specified artwork. See its [LICENSE](https://github.com/Baka-SU/BakaSU/blob/main/LICENSE) and [ASSETS_LICENSE.md](https://github.com/Baka-SU/BakaSU/blob/main/ASSETS_LICENSE.md). These are upstream statements, not a substitute for reviewing the exact KitsuSU source and bundled third-party components.

Before distributing modified APKs or kernel binaries, preserve applicable copyright and license notices, provide the corresponding source as required, identify changes, and include relevant license and asset notices with the distributed material. The pending [source-packaging PR](https://github.com/SysopBP/BakaSU-Diagnostic/pull/1) should be verified against the exact release artifact. **This README alone does not establish GPL compliance.**

## Upstream and licensing

This work builds on the broader [KernelSU](https://github.com/tiann/KernelSU) and [DirtyFrag / DFRoot](https://github.com/diabl0w/DFRoot) ecosystems. Credit and license obligations for individual components remain governed by their respective source files and licenses. Preserve original copyright notices, license texts, modification notices, and applicable corresponding-source distribution when publishing modified binaries.

The FragX preview and this diagnostic repository are separate distribution points. Refer to the exact source revision and included license files for each artifact; do not assume that a release's source obligations are satisfied solely by linking to this repository.

## Status

Experimental Samsung diagnostic workspace. The public preview is linked above; development branches and pending pull requests should be reviewed independently before merging or releasing.
