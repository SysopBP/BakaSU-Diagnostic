# Samsung S26 Ultra kernel-specific SusFS target (research only)

Device: SM-S948U1 (m3q), Android 17, firmware S948U1UEU4ZZHK_OYM4ZZHK
Running kernel: 6.12.69-android16-6-pe7f118b-abogkiS948USQU4ZZHK-4k
Build toolchain observed: Android clang 19.0.1, based on r536225
Observed configuration: CONFIG_MODULES=y, CONFIG_MODVERSIONS=y, CONFIG_MODULE_SIG=y
Current generic experiment: 6.12.76-4k — **not device compatible**.

Source acquisition:
- Samsung official release center: https://opensource.samsung.com/
- Search SM-S948U1 and SM-S948U; inspect the listed release firmware/version.
- Do not substitute another firmware's source without explicitly marking it approximate.
- Confirm kernel source, .config, Module.symvers, generated headers, compiler/build flags, and vendor ABI metadata before compiling.
- A Samsung release ZIP alone may not contain the exact generated Module.symvers for the shipping binary; verify, do not assume.
- If exact source or symbol CRCs cannot be obtained, stop at research; do not claim a loadable artifact.

Required gates before any device installation:
1. Four read-only diag_* parameters verified in modinfo.
2. Matching kernel release/vermagic and exported symbol CRCs.
3. Relevant signing/loader requirements verified; CONFIG_MODULE_SIG=y alone does not imply enforcement.
4. Separate, non-flashable artifact until validation; never force insmod or replace currently loaded SusFS.
5. Do not merge experimental changes into the known-good baseline.

Observed runtime: hide_from_apps=1, prefilter=Y; hide_list contains both test paths; untrusted Termux can stat and cat both. Root-run sus_path_probe reports gate_inode=0 and gate_any=0; these are not app-context results.
