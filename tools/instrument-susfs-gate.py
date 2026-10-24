#!/usr/bin/env python3
"""Instrument only the pinned SusFS path eligibility gate (experimental build)."""
from pathlib import Path
p = Path("source/kernel/sus_path.c")
s = p.read_text()
needle = """static inline bool sus_path_gate_ok(struct inode *inode)
{
    if (!hide_from_apps)
        return true;
    if (!susfs_is_current_proc_umounted_app())
        return false;
    return current_uid().val != inode->i_uid.val;
}"""
assert s.count(needle) == 1, "Upstream gate changed; refuse to patch"
replacement = """/* Experimental read-only counters; no UIDs, inode IDs, or paths retained. */
static atomic64_t diag_gate_bypass = ATOMIC64_INIT(0);
static atomic64_t diag_gate_nonapp = ATOMIC64_INIT(0);
static atomic64_t diag_gate_owner = ATOMIC64_INIT(0);
static atomic64_t diag_gate_allow = ATOMIC64_INIT(0);

#define DIAG_COUNTER_PARAM(name) \\
static int diag_get_##name(char *buf, const struct kernel_param *kp) \\
{ return scnprintf(buf, PAGE_SIZE, "%lld\\n", (long long)atomic64_read(&diag_gate_##name)); } \\
static const struct kernel_param_ops diag_ops_##name = { .get = diag_get_##name }; \\
module_param_cb(diag_##name, &diag_ops_##name, NULL, 0444)

DIAG_COUNTER_PARAM(bypass);
DIAG_COUNTER_PARAM(nonapp);
DIAG_COUNTER_PARAM(owner);
DIAG_COUNTER_PARAM(allow);

static inline bool sus_path_gate_ok(struct inode *inode)
{
    if (!hide_from_apps) {
        atomic64_inc(&diag_gate_bypass);
        return true;
    }
    if (!susfs_is_current_proc_umounted_app()) {
        atomic64_inc(&diag_gate_nonapp);
        return false;
    }
    if (current_uid().val == inode->i_uid.val) {
        atomic64_inc(&diag_gate_owner);
        return false;
    }
    atomic64_inc(&diag_gate_allow);
    return true;
}"""
p.write_text(s.replace(needle, replacement))
print("Instrumented four path gate outcomes; gate decisions unchanged")
