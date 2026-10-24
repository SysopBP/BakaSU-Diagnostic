#!/usr/bin/env python3
"""Add read-only SusFS gate diagnostics to a pinned upstream checkout."""
from pathlib import Path

p = Path("kernel/sus_path.c")
s = p.read_text()
anchor = "static inline bool sus_path_gate_ok(struct inode *inode)\n{"
assert s.count(anchor) == 1, "unexpected upstream gate layout"
block = """/* Diagnostic-only counters; never alter the gate decision. */
static atomic64_t sus_diag_gate_calls = ATOMIC64_INIT(0);
static atomic64_t sus_diag_gate_bypass = ATOMIC64_INIT(0);
static atomic64_t sus_diag_gate_ineligible = ATOMIC64_INIT(0);
static atomic64_t sus_diag_gate_owner = ATOMIC64_INIT(0);
static atomic64_t sus_diag_gate_allowed = ATOMIC64_INIT(0);
static atomic64_t sus_diag_gate_low_uid = ATOMIC64_INIT(0);
static atomic64_t sus_diag_gate_umount_false = ATOMIC64_INIT(0);
static atomic64_t sus_diag_gate_umount_fallback = ATOMIC64_INIT(0);
static atomic64_t sus_diag_gate_umount_isolated = ATOMIC64_INIT(0);

static int sus_diag_gate_get(char *buf, const struct kernel_param *kp)
{
    return scnprintf(buf, PAGE_SIZE,
        "gate_calls=%lld bypass=%lld ineligible=%lld owner=%lld allowed=%lld low_uid=%lld umount_false=%lld fallback=%lld isolated=%lld gate_off=%d\\n",
        (long long)atomic64_read(&sus_diag_gate_calls),
        (long long)atomic64_read(&sus_diag_gate_bypass),
        (long long)atomic64_read(&sus_diag_gate_ineligible),
        (long long)atomic64_read(&sus_diag_gate_owner),
        (long long)atomic64_read(&sus_diag_gate_allowed),
        (long long)atomic64_read(&sus_diag_gate_low_uid),
        (long long)atomic64_read(&sus_diag_gate_umount_false),
        (long long)atomic64_read(&sus_diag_gate_umount_fallback),
        (long long)atomic64_read(&sus_diag_gate_umount_isolated),
        (int)READ_ONCE(susfs_ksu_umount_gate_off));
}
static const struct kernel_param_ops sus_diag_gate_ops = {
    .get = sus_diag_gate_get,
};
module_param_cb(sus_diag_gate, &sus_diag_gate_ops, NULL, 0400);

"""
s = s.replace(anchor, block + anchor, 1)
old = """static inline bool sus_path_gate_ok(struct inode *inode)
{
    if (!hide_from_apps)
        return true;
    if (!susfs_is_current_proc_umounted_app())
        return false;
    return current_uid().val != inode->i_uid.val;
}"""
new = """static inline bool sus_path_gate_ok(struct inode *inode)
{
    atomic64_inc(&sus_diag_gate_calls);
    if (!hide_from_apps) {
        atomic64_inc(&sus_diag_gate_bypass);
        return true;
    }
    if (!susfs_is_current_proc_umounted_app()) {
        atomic64_inc(&sus_diag_gate_ineligible);
        if (current_uid().val < 10000)
            atomic64_inc(&sus_diag_gate_low_uid);
        else
            atomic64_inc(&sus_diag_gate_umount_false);
        return false;
    }
    if (READ_ONCE(susfs_ksu_umount_gate_off))
        atomic64_inc(&sus_diag_gate_umount_fallback);
    else if (susfs_uid_is_isolated(current_uid().val))
        atomic64_inc(&sus_diag_gate_umount_isolated);
    if (current_uid().val == inode->i_uid.val) {
        atomic64_inc(&sus_diag_gate_owner);
        return false;
    }
    atomic64_inc(&sus_diag_gate_allowed);
    return true;
}"""
assert s.count(old) == 1, "unexpected gate body"
s = s.replace(old, new, 1)
p.write_text(s)
print("Applied read-only gate counters; original decisions preserved.")
