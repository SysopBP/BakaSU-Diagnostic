#!/system/bin/sh
# SPDX-License-Identifier: GPL-2.0-only
# Fixed read-only probe shared by Action and WebUI. Never loads or configures SusFS.
MODDIR=${0%/*}
[ "$(id -u)" = 0 ] || { echo 'Root required'; exit 1; }
echo 'For the graphical UI, return to Modules and tap the SusFS module card or its WebUI button.'
section() { printf '\n=== %s ===\n' "$1"; }
section KERNEL
uname -r
section MODULE
if [ -d /sys/module/susfs_guard_lkm ]; then echo present; else echo absent; fi
for NODE in susfs_path susfs_kstat susfs_open_redirect; do
  section "$NODE"
  if [ -e "/proc/$NODE" ]; then
    echo 'Interface present; functionality not verified.'
    cat "/proc/$NODE" 2>&1
  else
    echo 'Interface unavailable; cause not established.'
  fi
done
for NAME in load.log load.log.previous; do
  section "$NAME"
  if [ -f "$MODDIR/$NAME" ]; then tail -c 65536 "$MODDIR/$NAME"; else echo 'No saved log.'; fi
done
section 'HOOK MESSAGES'
# Android may resolve printf to an external executable. Never pass a complete
# kernel ring buffer as an argument: it can exceed the per-argument limit.
LOG=$(mktemp "${TMPDIR:-/data/local/tmp}/kitsu-susfs-status.XXXXXX") || exit 1
trap 'rm -f "$LOG"' EXIT
dmesg >"$LOG" 2>&1
RC=$?
if [ "$RC" != 0 ]; then
  printf 'Kernel log unavailable (exit %s):\n' "$RC"
  tail -c 65536 "$LOG"
else
  # Filter a file, then bound the report sent through the WebUI bridge.
  grep -iE 'susfs|kstat:|or_entry:|opath|patch_memory' "$LOG" | tail -100 | tail -c 65536
  if ! grep -qiE 'susfs|kstat:|or_entry:|opath|patch_memory' "$LOG"; then
    echo 'No matching kernel messages remain.'
  fi
fi
exit 0
