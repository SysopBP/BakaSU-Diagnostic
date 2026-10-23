#!/system/bin/sh
# SPDX-License-Identifier: GPL-2.0-only
MODDIR=${0%/*}
# Read status or load if absent. A failed-load latch is never cleared automatically.
/system/bin/sh "$MODDIR/load.sh"
cat "$MODDIR/load.log"
