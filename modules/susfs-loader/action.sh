#!/system/bin/sh
# SPDX-License-Identifier: GPL-2.0-only
MODDIR=${0%/*}
# Action is read-only. Loading is confined to the existing boot-stage loader.
/system/bin/sh "$MODDIR/status.sh"
