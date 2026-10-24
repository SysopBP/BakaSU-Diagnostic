# SusFS gate/hook diagnostics — preserved baseline

Baseline: successful GitHub Actions run 40033249093, commit f8229fb7b1e05ffa0781d4cb3128920274b06994.
Source: inforcqb/susfs4ksu-lkm pinned to 8ab4500ffc3f13ec6ded79d7ab13e2e8147a1879.
Do not change existing build source pins, packaging, provenance rewriting, or tablet soft-reboot service parser.

## Reproduced S26 Ultra observations
- Module live, hide_from_apps=1, prefilter=Y, no_extra=0.
- /proc/susfs_path add/del works; rule matches exact inode pointer (ptr_equal=1).
- Unprivileged Termux (UID 10612, untrusted_app_27) can stat and read registered hidden.txt.
- ENOENT counters remain zero, and gate_inode=0 / gate_any=0 when probed from root.
- sys_call_table patching previously reported -EFAULT; /proc/susfs_kstat absent.
- Removing test rule restores file mode 0644.

## Next implementation (no behavior changes)
1. Add read-only, root-only kernel parameter exposing symbol resolution status of ksu_uid_should_umount.
2. Add read-only counters for LSM callback invocations, candidate rule matches, and eligible/denied decisions. No raw kernel addresses or app secrets in report.
3. Do not invoke the resolved KernelSU function for an arbitrary UID via sysfs: evaluate eligibility only in the current caller context, or expose aggregate counters from real callbacks.
4. Preserve hide_from_apps semantics, syscall patching, module load order, and module ZIP structure.
5. Compile all 8 KMI modules and validate ZIP provenance and parser tests.
6. Test on device before merging; no module reload while KernelSU function pointers may be live.

## Diagnostic interpretation
A root-run sus_path_probe reports the root caller's gate and cannot prove unprivileged app eligibility. UID >= 10000 alone does not establish KernelSU's should-umount policy when the symbol is resolved.
