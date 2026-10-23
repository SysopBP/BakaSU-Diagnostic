#!/system/bin/sh
# SPDX-License-Identifier: GPL-2.0-only
# Fixed read-only probe shared by Action and WebUI. Never loads or configures SusFS.
MODDIR=${0%/*}
[ "$(id -u)" = 0 ] || { echo 'Root required'; exit 1; }
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
MESSAGES=$(dmesg 2>&1)
RC=$?
if [ "$RC" != 0 ]; then
  printf 'Kernel log unavailable (exit %s):\n%s\n' "$RC" "$MESSAGES"
else
  MATCHES=$(printf '%s\n' "$MESSAGES" | grep -iE 'susfs|kstat:|or_entry:|opath|patch_memory' | tail -100)
  if [ -n "$MATCHES" ]; then printf '%s\n' "$MATCHES"; else echo 'No matching kernel messages remain.'; fi
fi
exit 0
