#!/system/bin/sh
# SPDX-License-Identifier: GPL-2.0-only
[ "$KSU" = true ] || abort '- KernelSU-compatible manager required.'
[ "$ARCH" = arm64 ] || abort '- ARM64 only.'
case "$(uname -r)" in
  6.12.*-android16-*) ;;
  *) abort '- This preview supports Android 16 GKI 6.12 only.' ;;
esac
cd "$MODPATH" || abort '- Cannot access module files.'
sha256sum -c payload.sha256 || abort '- Payload checksum mismatch.'
# Do not replace the upstream package while its optional common early loader is installed.
HOOK=/data/adb/post-fs-data.d/00-susfs-guard-lkm.sh
[ ! -e "$HOOK" ] && [ ! -L "$HOOK" ] || abort '- Remove the existing upstream SusFS loader module first.'
set_perm_recursive "$MODPATH" 0 0 0755 0644
for script in load.sh post-fs-data.sh action.sh; do set_perm "$MODPATH/$script" 0 0 0755; done
set_perm "$MODPATH/bin/susfs_insmod" 0 0 0755
touch "$MODPATH/skip_mount"
ui_print '- KitsuSU SusFS Loader preview 1: Android 16 / 6.12'
ui_print '- Loader only. No hiding rules, partition writes, or automatic reboot.'
ui_print '- After root is restored, use KitsuSU Soft reboot to activate.'
ui_print '- Full reboot still loses temporary FragX root.'
ui_print '- Loading successfully does not verify Kstat or Open Redirect.'
