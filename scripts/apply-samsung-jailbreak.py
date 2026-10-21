#!/usr/bin/env python3
"""Apply diabl0w Samsung compat integration to BakaSU v4.2.0-rc3.
Run from a clean upstream checkout after copying vendor/kernel/compat files.
All anchors are validated in memory before any source file is changed.
"""
import re
from pathlib import Path

changes = {}
def edit(name, old, new):
    p = Path('kernel') / name
    s = changes.get(p, p.read_text())
    if s.count(old) != 1:
        raise SystemExit(f'{p}: expected one anchor: {old[:80]!r}, got {s.count(old)}; use clean v4.2.0-rc3')
    changes[p] = s.replace(old, new, 1)

def include(name):
    p = Path('kernel') / name
    s = changes.get(p, p.read_text())
    if '#include "compat/jailbreak.h"' not in s:
        s, n = re.subn(r'(?m)^(#include[^\n]*\n)', r'\1#include "compat/jailbreak.h"\n', s, count=1)
        if n != 1:
            raise SystemExit(f'{p}: missing include')
        changes[p] = s

for name in ['jailbreak.h', 'jailbreak.c', 'defex.c', 'kdp.c', 'rkp.c']:
    if not (Path('kernel/compat') / name).is_file():
        raise SystemExit(f'Missing kernel/compat/{name}')
# Brand the version returned by the driver; keep version/commit identifiers intact.
edit('Kbuild', 'REPO_NAME := ReSukiSU\n', 'REPO_NAME := KitsuSU\n')
edit('Kbuild', 'kernelsu-objs += compat/kernel_compat.o\n',
     'kernelsu-objs += compat/kernel_compat.o\nkernelsu-objs += compat/jailbreak.o compat/defex.o compat/kdp.o compat/rkp.o\n')
include('core/init.c')
edit('core/init.c', '    ksu_init_symbol_resolver();\n', '    ksu_init_symbol_resolver();\n    init_jailbreak();\n')
# Keep KDP active until the final credential release has completed.
edit('core/init.c', '    put_cred(ksu_cred);\n}', '    ksu_put_cred(ksu_cred);\n    exit_jailbreak();\n}')
include('hook/arm64/patch_memory.c')
edit('hook/arm64/patch_memory.c',
     'int ksu_patch_text(void *dst, void *src, size_t len, int flags)\n{\n',
     'int ksu_patch_text(void *dst, void *src, size_t len, int flags)\n{\n    if (static_branch_unlikely(&ksu_rkp_key) && len == sizeof(void *))\n        return ksu_rkp_branch_patch(dst, src);\n\n')
f = 'feature/selinux_hide.c'
include(f)
edit(f, 'static write_op_fn orig_context_write, orig_access_write;\n',
     'static write_op_fn orig_context_write, orig_access_write;\nstatic write_op_fn callthru_context_write, callthru_access_write;\n')
for name in ['context', 'access']:
    edit(f, f'static ssize_t my_write_{name}(', f'static ssize_t __nocfi my_write_{name}(')
    edit(f, f'return orig_{name}_write(file, buf, size);', f'return callthru_{name}_write(file, buf, size);')
    edit(f, f'    orig_{name}_write = *{name}_write;\n',
         f'    orig_{name}_write = *{name}_write;\n    if (!static_branch_unlikely(&ksu_rkp_key))\n        callthru_{name}_write = orig_{name}_write;\n')
    anchor = f'    ret = ksu_patch_text({name}_write, &my, sizeof(my), KSU_PATCH_TEXT_FLUSH_DCACHE);\n'
    # Resolve stubs immediately after each patch, matching the upstream port.
    edit(f, anchor, anchor + f'    if (!ret && static_branch_unlikely(&ksu_rkp_key))\n        callthru_{name}_write = (write_op_fn)ksu_rkp_get_stub(orig_{name}_write);\n')
edit(f, 'extern setprocattr_fn ksu_orig_setprocattr;\n#endif\n',
     'extern setprocattr_fn ksu_orig_setprocattr;\n#endif\nstatic setprocattr_fn callthru_setprocattr;\n')
edit(f, 'return ((setprocattr_fn)selinux_setprocattr_hook.original)(name, value, size);',
     'return callthru_setprocattr(name, value, size);')
anchor = '    ret = ksu_lsm_hook(&selinux_setprocattr_hook);\n'
edit(f, anchor, anchor + '    if (!ret)\n        callthru_setprocattr = static_branch_unlikely(&ksu_rkp_key)\n            ? (setprocattr_fn)ksu_rkp_get_stub(selinux_setprocattr_hook.original)\n            : (setprocattr_fn)selinux_setprocattr_hook.original;\n')
edit(f, 'static int my_sel_open_handle_status(',
     'static sel_open_handle_status_fn callthru_sel_open_handle_status;\nstatic int __nocfi my_sel_open_handle_status(')
edit(f, 'int ret = orig_sel_open_handle_status(inode, filp);', 'int ret = callthru_sel_open_handle_status(inode, filp);')
anchor = '    int ret = ksu_patch_text(sel_open_handle_status_slot, &new_fn, sizeof(new_fn), KSU_PATCH_TEXT_FLUSH_DCACHE);\n'
edit(f, anchor, anchor + '    if (!ret)\n        callthru_sel_open_handle_status = static_branch_unlikely(&ksu_rkp_key)\n            ? (sel_open_handle_status_fn)ksu_rkp_get_stub(orig_sel_open_handle_status)\n            : orig_sel_open_handle_status;\n')
# Do not clear call-through pointers before hooks are restored.
for p in sorted(Path('kernel').rglob('*.c')):
    if p.parent == Path('kernel/compat'):
        continue
    s = changes.get(p, p.read_text())
    new = re.sub(r'\b(commit_creds|put_cred)\(', r'ksu_\1(', s)
    if new != s:
        changes[p] = new
        include(str(p.relative_to('kernel')))
# Credential wrappers can fail on KDP; preserve upstream error handling.
edit('policy/app_profile.c', '    ksu_commit_creds(cred);\n\n    disable_seccomp();',
     '    ret = ksu_commit_creds(cred);\n    if (ret)\n        goto out_abort_creds;\n\n    disable_seccomp();')
for p, s in changes.items():
    p.write_text(s)
    print(f'patched {p}')
print(f'Done: {len(changes)} files')
