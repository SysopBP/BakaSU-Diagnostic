#!/system/bin/sh
# SPDX-License-Identifier: GPL-2.0-only
# KitsuSU Samsung preview wrapper, SysopBP, 2026-10-23.
MODDIR=${0%/*}
umask 077
[ "$(id -u)" = 0 ] || { echo 'Root required'; exit 1; }
[ ! -f "$MODDIR/disable" ] && [ ! -f "$MODDIR/remove" ] || exit 0
[ "$(getprop persist.sys.safemode)" != 1 ] || exit 0
[ "$(getprop ro.sys.safemode)" != 1 ] || exit 0
# A leftover lock after a killed loader deliberately blocks automatic retries.
mkdir "$MODDIR/load.lock" 2>/dev/null || { echo 'Loader locked; inspect load.log before retrying'; exit 1; }
trap 'rmdir "$MODDIR/load.lock" 2>/dev/null' EXIT
exec >"$MODDIR/load.log" 2>&1
status() {
  echo "$1"
  sed -i "s#^description=.*#description=$1#" "$MODDIR/module.prop"
}
echo "KitsuSU SusFS preview loader: $(date)"
if [ -d /sys/module/susfs_guard_lkm ] || [ -e /proc/susfs_path ]; then
  status 'SusFS already present; skipped duplicate load. Feature status is separate.'
  exit 0
fi
if [ -f "$MODDIR/load-failed" ]; then
  status 'Previous load failed; automatic retries paused. Inspect load.log.previous.'
  exit 1
fi
REL=$(uname -r)
case "$REL" in
  6.12.*-android16-*) ;;
  *) status 'Unsupported kernel; this preview requires Android 16 GKI 6.12.'; exit 1 ;;
esac
[ "$(uname -m)" = aarch64 ] || { status 'Unsupported CPU architecture.'; exit 1; }
cd "$MODDIR" || exit 1
sha256sum -c payload.sha256 || { status 'Payload checksum failed; no module loaded.'; exit 1; }
# Latch before entering the loader: a crash or interrupted load must not loop.
touch "$MODDIR/load-failed" || exit 1
./bin/susfs_insmod ./lib/susfs_guard_lkm-android16-6.12.ko expose_proc=1
RC=$?
echo "susfs_insmod exit=$RC"
if [ "$RC" = 0 ] && [ -d /sys/module/susfs_guard_lkm ]; then
  rm -f "$MODDIR/load-failed"
  status 'SusFS loaded; individual features still require runtime checks.'
else
  status 'SusFS load failed; automatic retries paused. Inspect load.log.'
fi
echo '=== Runtime interfaces ==='
ls -l /proc/susfs* 2>/dev/null
for NODE in /proc/susfs_path /proc/susfs_kstat /proc/susfs_open_redirect; do
  if [ -r "$NODE" ]; then echo "=== $NODE ==="; cat "$NODE"; fi
done
echo '=== Recent SusFS kernel messages ==='
dmesg | grep -iE 'susfs|kstat:|or_entry:|opath' | tail -100
if [ -f "$MODDIR/load-failed" ]; then
  cp "$MODDIR/load.log" "$MODDIR/load.log.previous"
  exit 1
fi
exit 0
