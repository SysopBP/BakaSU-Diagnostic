#!/system/bin/sh
# BakaSU consolidated SusFS diagnostics: read-only, no module loading or configuration changes.
# Run from Termux as: sh tools/susfs-consolidated-diagnostic.sh
set -u
OUT="${1:-${HOME:-/data/local/tmp}/BakaSU_SusFS_Diagnostic_$(date +%Y%m%d_%H%M%S).txt}"
TEST="/data/local/tmp/susfs-visibility-test/hidden.txt"
PROBE="/data/local/tmp/kitsu-susfs-probe.txt"
case "$OUT" in
 "${HOME:-/nonexistent}"/BakaSU_SusFS_Diagnostic_*.txt|/sdcard/Download/BakaSU_SusFS_Diagnostic_*.txt|/storage/emulated/0/Download/BakaSU_SusFS_Diagnostic_*.txt) ;;
 *) echo "Output must be in Termux home or Downloads" >&2; exit 2;;
esac
umask 077
{
echo "BAKASU SUSFS CONSOLIDATED DIAGNOSTIC"
date
echo "=== DEVICE ==="
getprop ro.product.model
getprop ro.build.version.release
uname -r
echo "=== UNPRIVILEGED IDENTITY ==="
id
echo "=== UNPRIVILEGED VISIBILITY ==="
for f in /sys/module/susfs_guard_lkm "$TEST" "$PROBE"; do
 echo "--- $f ---"
 ls -ld "$f" 2>&1
 if [ -f "$f" ]; then
  # Avoid collecting file contents; report readability only.
  if [ -r "$f" ]; then echo "readable=yes"; else echo "readable=no"; fi
 fi
done
echo "=== ROOT READ-ONLY SNAPSHOT ==="
su -c '
echo "identity:"; id
echo "kernel:"; uname -r
M=/data/adb/modules/susfs_guard_lkm
P=/sys/module/susfs_guard_lkm/parameters
echo "module metadata:"; cat "$M/module.prop" 2>&1
echo "loader log:"; cat "$M/load.log" 2>&1
echo "module presence:"; ls -ld /sys/module/susfs_guard_lkm 2>&1
echo "path rules and counters:"; cat /proc/susfs_path 2>&1
echo "path probe:"; cat "$P/sus_path_probe" 2>&1
for n in hide_from_apps hide_modules hide_mounts prefilter expose_proc fail_layer mount_stat map_stat; do
 echo "--- parameter $n ---"; cat "$P/$n" 2>&1
done
echo "open redirect:"; cat /proc/susfs_open_redirect 2>&1
echo "kstat:"; if [ -r /proc/susfs_kstat ]; then head -80 /proc/susfs_kstat; else echo "unavailable"; fi
echo "probe file metadata:"; ls -l /data/local/tmp/susfs-visibility-test/hidden.txt /data/local/tmp/kitsu-susfs-probe.txt 2>&1
'
echo "=== END ==="
} > "$OUT" 2>&1
RC=$?
if [ -f "$OUT" ]; then echo "Diagnostic saved: $OUT"; else echo "Diagnostic could not be written: $OUT" >&2; exit 1; fi
exit "$RC"
