# BakaSU Diagnostic

Independent SysopBP diagnostic modifications of [Baka-SU/BakaSU](https://github.com/Baka-SU/BakaSU), using upstream v4.2.0-rc3 in the current workflow. This is not an official BakaSU release. Production KernelSU driver/ksud changes remain outside this diagnostic workspace.

The modified BakaSU distribution retains the upstream [GPLv3 license](LICENSE). Other upstream component/artwork licenses remain applicable and are preserved in the matching source archive. The diagnostic snippets are modifications to upstream manager code, not a claim of original authorship of BakaSU.

Each successful build artifact includes the repacked APK, a tracked-source archive containing the applied diagnostic changes, SOURCE-PROVENANCE.txt with the exact upstream commit and this workspace commit, upstream license files, and SHA256SUMS.txt. Generated signing keys and password files are excluded. Build-generated binaries are not substituted for their preferred source.

The source archive excludes untracked build outputs and signing material. Keep Cargo/Gradle lockfiles and use the recorded workflow/toolchain when reproducing. Compilation and archive creation do not prove device compatibility or authorize use of unrelated third-party assets.
