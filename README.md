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

## Upstream and licensing

This work builds on the broader [KernelSU](https://github.com/tiann/KernelSU) and [DirtyFrag / DFRoot](https://github.com/diabl0w/DFRoot) ecosystems. Credit and license obligations for individual components remain governed by their respective source files and licenses. Preserve original copyright notices, license texts, modification notices, and applicable corresponding-source distribution when publishing modified binaries.

The FragX preview and this diagnostic repository are separate distribution points. Refer to the exact source revision and included license files for each artifact; do not assume that a release's source obligations are satisfied solely by linking to this repository.

## Status

Experimental Samsung diagnostic workspace. The public preview is linked above; development branches and pending pull requests should be reviewed independently before merging or releasing.
