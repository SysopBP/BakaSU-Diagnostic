#!/system/bin/sh
# Read-only Samsung kernel compatibility capture. No insmod, writes to kernel or reboot.
set -u
OUT="${1:-/sdcard/Download/SusFS_Kernel_Compatibility.txt}"
TMP="${OUT}.tmp"
{
  echo "=== Device kernel ==="
  uname -a
  cat /proc/version
  echo "=== Build properties ==="
  for p in ro.product.model ro.build.fingerprint ro.bootimage.build.fingerprint ro.boot.slot_suffix; do
    printf '%s=' "$p"; getprop "$p"
  done
  echo "=== Kernel configuration (when exposed) ==="
  if [ -r /proc/config.gz ]; then
    gzip -dc /proc/config.gz 2>/dev/null | grep -E '^(CONFIG_MODVERSIONS|CONFIG_MODULES|CONFIG_MODULE_UNLOAD|CONFIG_MODULE_SIG|CONFIG_LTO_CLANG|CONFIG_KALLSYMS|CONFIG_KALLSYMS_ALL)='
  else
    echo '/proc/config.gz unavailable'
  fi
  echo "=== Build metadata ==="
  for f in /sys/kernel/notes /sys/module/kernel/notes/.note.gnu.build-id; do
    [ ! -r "$f" ] || ls -l "$f"
  done
  echo "=== Existing loaded module (read-only) ==="
  grep -E '^susfs_guard_lkm ' /proc/modules 2>/dev/null || true
  echo "=== Nearby kernel module vermagic (when accessible) ==="
  for d in /vendor/lib/modules /vendor_dlkm/lib/modules /system_dlkm/lib/modules; do
    [ ! -d "$d" ] || { echo "$d"; ls "$d"/*.ko 2>/dev/null | head -5; }
  done
  echo "=== Symbol CRC exposure ==="
  if [ -r /proc/kallsyms ]; then
    echo '/proc/kallsyms readable (not exporting symbols)'
  else
    echo '/proc/kallsyms unavailable'
  fi
} > "$TMP" 2>&1
mv "$TMP" "$OUT"
echo "Saved: $OUT"
