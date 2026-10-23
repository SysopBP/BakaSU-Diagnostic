#!/usr/bin/env python3
"""Correct the pinned upstream service-list parser without changing reboot policy."""
from pathlib import Path

path = Path('userspace/ksud/src/android/soft_reboot.rs')
source = path.read_text()
old = r'^\d\s+([^\s:]+):\s+\[[^\]]*\]$'
new = r'^\d+\s+([^\s:]+):\s+\[[^\]]*\]$'
if source.count(old) != 1:
    raise SystemExit('Expected exactly one single-digit service-list pattern; review upstream source')
path.write_text(source.replace(old, new, 1))
print('Patched service-list indices to accept multiple digits')
