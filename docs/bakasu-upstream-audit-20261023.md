# BakaSU upstream audit (66 commits)

Baseline: `239e1e8871b8fcd51a6e5b3002e0ba522fdd99fb`
Compared head: `39faf94a2d4a40d48093398bafcde649916edbc1`

This is a complete commit inventory, **not** an assertion that all commits are missing or safe to merge. The isolated CI branch tests four kernel commits; no runtime compatibility is established until device tests pass. Review Samsung, FragX, KitsuSU identity, signing, soft reboot and SusFS paths before promotion.

## Kernel / security (15)

- [`325265c534`](https://github.com/Baka-SU/BakaSU/commit/325265c53425648552560ef5c625aced6e15534d) — kernel: Add Android riscv64 support with LKM (https://github.com/tiann/KernelSU/pull/3750)
- [`f6513993fb`](https://github.com/Baka-SU/BakaSU/commit/f6513993fb6dde11457bb7bf183cb3868dbb069d) — kernel: synchronization for track_throne in pkg_observer
- [`c4bdcaae02`](https://github.com/Baka-SU/BakaSU/commit/c4bdcaae023f8318e85b0782cf534fca4bc8aa62) — kernel: don't path_put when 3.6- in dentry_open
- [`b0fa24df91`](https://github.com/Baka-SU/BakaSU/commit/b0fa24df91674e02e8fba29ad31ddff0174456ca) — kernel: escape to root when reading allowlist
- [`f397410c7d`](https://github.com/Baka-SU/BakaSU/commit/f397410c7da5f2b85e769b64992f8868cac990ba) — fix(kernel): Fix avtab removal length calculation and xperms update
- [`8770c7e324`](https://github.com/Baka-SU/BakaSU/commit/8770c7e324a22895703c4916b8a16520e0b81c79) — fix(kernel): Avoid repeatedly triggering service stage (https://github.com/tiann/KernelSU/pull/3800)
- [`9dbce02e51`](https://github.com/Baka-SU/BakaSU/commit/9dbce02e511ea6b6305a238b84e456f6a92e1d0b) — kernel, userspace: don't add repo name in full name by default and announce BAKASU instead of KSU_SUKISU in module scripts
- [`ba8cfa502e`](https://github.com/Baka-SU/BakaSU/commit/ba8cfa502ebe9d84c0fe79928f07b0738c5a2c55) — kernel: fix sidtab detection (https://github.com/tiann/KernelSU/pull/3873)
- [`8450dd287e`](https://github.com/Baka-SU/BakaSU/commit/8450dd287ef6ee25ca2b6b858b43c9354c73060c) — kernel: pkg_observer: defer track_throne to task_work (https://github.com/tiann/KernelSU/pull/3871)
- [`969de3d0ce`](https://github.com/Baka-SU/BakaSU/commit/969de3d0ce65d2d75e5a2f6c548d9e14817ef459) — fix(kernel): Keep original permission check sequence
- [`48fa4bb7ec`](https://github.com/Baka-SU/BakaSU/commit/48fa4bb7ec8bddb8ea932a8c9be0877f89a1fa73) — kernel: suspend susfs build
- [`fa12ffde82`](https://github.com/Baka-SU/BakaSU/commit/fa12ffde8244008e9afdb7ac0c1bb1bc1b06b95a) — kernel: fix time side-channel detection in selinux hide (https://github.com/tiann/KernelSU/pull/3877)
- [`648144087e`](https://github.com/Baka-SU/BakaSU/commit/648144087efd32f5fe68982e8cbf5efc1576038a) — kernel: don't process execve for su when ksud does not exist (#597)
- [`d7260ca1e5`](https://github.com/Baka-SU/BakaSU/commit/d7260ca1e5c128061122924d0d48754e361e135c) — kernel: check context_add_hash before operate sidtab when possible (#623)
- [`522081c5b1`](https://github.com/Baka-SU/BakaSU/commit/522081c5b1c58587c4c743242eecf445ccebed5d) — kernel: compat for 32bit userspace on 64bit kernel (#612)

## Manager / UI (22)

- [`f228776b25`](https://github.com/Baka-SU/BakaSU/commit/f228776b253b8eaa2d48bb1848c2d5947446ab98) — manager: bump the maven group across 1 directory with 7 updates (#440)
- [`94dd3c93c2`](https://github.com/Baka-SU/BakaSU/commit/94dd3c93c2053a84fd752df6eb85db99b7d70ab8) — manager: update translations from Weblate (#434)
- [`83850e8e93`](https://github.com/Baka-SU/BakaSU/commit/83850e8e93c5f7cfaec69cf03707f13e799df36a) — manager: update translations from Weblate (#444)
- [`72fe0d0c9d`](https://github.com/Baka-SU/BakaSU/commit/72fe0d0c9d2738f175eb296167ee061fcd3e0dbf) — manager: Update maven group in manager (#446)
- [`75de877b5d`](https://github.com/Baka-SU/BakaSU/commit/75de877b5d920609a7d920a92380779d9d0c01a8) — manager: fix hang in splashscreen and hang in webui start (#439)
- [`4c5c8cedaf`](https://github.com/Baka-SU/BakaSU/commit/4c5c8cedaf3cecf297f9b529362e529f506e6891) — manager: support xz compression modules
- [`55a531d026`](https://github.com/Baka-SU/BakaSU/commit/55a531d02641e7d47798c1bd2e6223d3df2603ff) — manager: cleanup
- [`bbcdc0d923`](https://github.com/Baka-SU/BakaSU/commit/bbcdc0d923ed66f0eab352545863cff767d5d906) — manager: replace HanziToPinyin with icu transliteration
- [`c2ef226653`](https://github.com/Baka-SU/BakaSU/commit/c2ef226653f07967d8276bd2f3dfd31a1bab35cb) — manager: don't offer kernel install in jailbreak mode
- [`157eaeeac0`](https://github.com/Baka-SU/BakaSU/commit/157eaeeac0f5f2cb8f99ec459bd26328fe2ba54d) — manager: don't mark prevent_background_refresh
- [`61e2ce8305`](https://github.com/Baka-SU/BakaSU/commit/61e2ce83055e015e97e1e0f5b303b060b6c6a01f) — manager: Update maven group in manager (#462)
- [`c8dc617dd7`](https://github.com/Baka-SU/BakaSU/commit/c8dc617dd7e19630bc5f39f678cd93de798559d2) — manager: refactor intent handling and introduce URL schema
- [`1bfed00f59`](https://github.com/Baka-SU/BakaSU/commit/1bfed00f597e65700d70fee0feb1d424fc21a2e5) — manager: fix normal webui can not open
- [`bede8a4d28`](https://github.com/Baka-SU/BakaSU/commit/bede8a4d28ef86526688de251ebf47ca0adc2b5d) — manager: update translations from Weblate (#457)
- [`c9246641b9`](https://github.com/Baka-SU/BakaSU/commit/c9246641b9eee8b9986050e8bf1832f88da880c2) — manager: update translations from Weblate (#599)
- [`373303c525`](https://github.com/Baka-SU/BakaSU/commit/373303c525d05c8b47801305f506ef9124dbd6e6) — manager: improve theme initialization and navigation behavior
- [`f6cb7e70c1`](https://github.com/Baka-SU/BakaSU/commit/f6cb7e70c10ebde149f3121ae68b945514fd0801) — manager: update translations from Weblate (#603)
- [`b2c595ddfa`](https://github.com/Baka-SU/BakaSU/commit/b2c595ddfa64b685e5a144ad37b7c95f912fb92a) — manager: update translations from Weblate (#619)
- [`896e8981e0`](https://github.com/Baka-SU/BakaSU/commit/896e8981e0ed76ec14d1dcb39ab793438b304886) — manager: fix monet and opt performance (#614)
- [`7c383cfeef`](https://github.com/Baka-SU/BakaSU/commit/7c383cfeef3a2ac450f2f1273dae74bd50356d31) — manager, ksud: refine flashing flow and simplify AnyKernel3 execution (#630)
- [`dac2d18640`](https://github.com/Baka-SU/BakaSU/commit/dac2d186406a0d2b0ce3c67cad5a1fa1adbf9f4d) — manager: support multiple module repositories, one-shot scripts and other minimal fixes (#600)
- [`39faf94a2d`](https://github.com/Baka-SU/BakaSU/commit/39faf94a2d4a40d48093398bafcde649916edbc1) — manager: update translations from Weblate (#629)

## Daemon / userspace (8)

- [`d7f199613d`](https://github.com/Baka-SU/BakaSU/commit/d7f199613d663755883f05c49d698f0e50fea637) — ksud: use waitsys to wait when soft reboot (https://github.com/tiann/KernelSU/pull/3754)
- [`6ce433809b`](https://github.com/Baka-SU/BakaSU/commit/6ce433809b345410152affdec3b61efe1fe3f928) — ksud: fix waitsys not avaliable in arm
- [`20756bfbc0`](https://github.com/Baka-SU/BakaSU/commit/20756bfbc08499f6daa91b562d7bd30075c531b0) — ksud: remove multithread analysing boot in slot_info
- [`fedfbb2d3e`](https://github.com/Baka-SU/BakaSU/commit/fedfbb2d3e9a74069baa20dca97a7608e8734465) — ksud: bail directly when boot image is empty or parse failed
- [`fa8311f632`](https://github.com/Baka-SU/BakaSU/commit/fa8311f632a215b5381ec644627c6198d1e8a13e) — ksud: fmt
- [`59c42e8828`](https://github.com/Baka-SU/BakaSU/commit/59c42e882835cf8a115b72b14c1c7805fe8b577d) — ksud: Update Rust crate libc to v0.2.190 (#453)
- [`9fc9b9c66c`](https://github.com/Baka-SU/BakaSU/commit/9fc9b9c66cadb8e5face8e1cfaf6ef74ae915dd8) — ksud: Scan APK comments up to the ZIP length limit (https://github.com/tiann/KernelSU/pull/3802)
- [`63268b9bd8`](https://github.com/Baka-SU/BakaSU/commit/63268b9bd879079311ad8d9e96c6ab93a8b42251) — ksud: Skip KMI detection for config-only patches(https://github.com/tiann/KernelSU/pull/3803)

## Build / dependencies (14)

- [`4644540826`](https://github.com/Baka-SU/BakaSU/commit/4644540826165c36263f797360ed7fdb22489fa3) — ci,ksubot: use self-host bot API
- [`5dd1864d70`](https://github.com/Baka-SU/BakaSU/commit/5dd1864d70ce416598920cd4cc7cd274b1dfebce) — ci: refine rust cache
- [`3b3c5496f5`](https://github.com/Baka-SU/BakaSU/commit/3b3c5496f58f878636fb564b732d7dc98d805b24) — build(deps): bump the crates group in /userspace/ksud with 10 updates (#441)
- [`e96a963629`](https://github.com/Baka-SU/BakaSU/commit/e96a96362945621c12289ddacbf0f8fb82e349e4) — ci: Configure Renovate (#443)
- [`bd142a3cab`](https://github.com/Baka-SU/BakaSU/commit/bd142a3cabbc6b4ec41fde4e7458b351629d40bd) — deps: Update Rust crate cc to v1.5.1 (#447)
- [`542f9061d6`](https://github.com/Baka-SU/BakaSU/commit/542f9061d6c0123eafdc2ade61db98e1ae3b2e1c) — ci: Do not build telegram-bot-api when in pr or workflow_call
- [`3a2745f78a`](https://github.com/Baka-SU/BakaSU/commit/3a2745f78ab68e61c02a0681463021952083ec8c) — chore: migrate Renovate config (#449)
- [`34210a4dec`](https://github.com/Baka-SU/BakaSU/commit/34210a4dec297cb48ce4bfa1c5ba50a2f7d22641) — ci: Do not ignore libcxx update
- [`0357c65f53`](https://github.com/Baka-SU/BakaSU/commit/0357c65f53f7682ba69d548d6612da557ffc766f) — deps: Update Rust crate cc to v1.6.0 (#454)
- [`5b76b884c7`](https://github.com/Baka-SU/BakaSU/commit/5b76b884c75f729a220bb317aa4a4fc78f0e0e9c) — deps: Update Rust crate in ksud (#602)
- [`9097b1a1c6`](https://github.com/Baka-SU/BakaSU/commit/9097b1a1c6c889756201bbc5713a84a9b23f7908) — deps: Update cargo group in ksud  (#615)
- [`f4435f007b`](https://github.com/Baka-SU/BakaSU/commit/f4435f007b16f61705089ff982e3f981a6017979) — deps: Update cargo group in ksud (#617)
- [`8748525c89`](https://github.com/Baka-SU/BakaSU/commit/8748525c89a649c6d4410024438747e0e320ae78) — renovate: ignore prettyplease
- [`2489b38582`](https://github.com/Baka-SU/BakaSU/commit/2489b38582a08fee7b586d05185da5e5d12c6a5c) — deps: Update Rust crate libc to v0.2.191 (#627)

## Other / documentation (7)

- [`6803643e19`](https://github.com/Baka-SU/BakaSU/commit/6803643e19e2e6e8287f96461aabb93bdd6c47fa) — fix(manager): Unexport magica receiver (https://github.com/tiann/KernelSU/pull/3747)
- [`eb9732ec86`](https://github.com/Baka-SU/BakaSU/commit/eb9732ec86dfa559aeaebc1946c032c6a19fcc01) — ksubot: split commit with `------`
- [`91157d2764`](https://github.com/Baka-SU/BakaSU/commit/91157d27645756049428d78896f5e499b8bd56db) — refactor(ksud): update waitsys and refactor logic (https://github.com/tiann/KernelSU/pull/3755)
- [`0e4698951b`](https://github.com/Baka-SU/BakaSU/commit/0e4698951b8e0e1cb997e46f2049c691869a4f45) — ksubot: fix commit msg
- [`80c0e190d0`](https://github.com/Baka-SU/BakaSU/commit/80c0e190d044d974be82b6f3355242e67acd8d9a) — feat(ksud): add timeout for boot stage scripts(https://github.com/tiann/KernelSU/pull/3797)
- [`97c102ba05`](https://github.com/Baka-SU/BakaSU/commit/97c102ba05ee2915390cacae6d11e1727d6ca350) — treewide: rename project (#461)
- [`e5423590be`](https://github.com/Baka-SU/BakaSU/commit/e5423590bec3e24daffa4e9555c9592071319c68) — Revert "manager: replace HanziToPinyin with icu transliteration"

