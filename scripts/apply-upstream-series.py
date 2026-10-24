#!/usr/bin/env python3
"""Verify the complete, immutable 66-commit snapshot before Samsung adaptation.

The previous 12-patch queue remains in patches/bakasu as integration history.
It must not be applied again: all twelve fixes are already in this source pin.
"""
import argparse
from pathlib import Path
import subprocess

BASE = '239e1e8871b8fcd51a6e5b3002e0ba522fdd99fb'
HEAD = '39faf94a2d4a40d48093398bafcde649916edbc1'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source', type=Path, required=True)
args = parser.parse_args()
source = args.source.resolve()

def git(*args):
    return subprocess.check_output(['git', '-C', str(source), *args], text=True).strip()

if git('rev-parse', 'HEAD') != HEAD:
    raise SystemExit('Integration requires the exact reviewed upstream snapshot')
if git('status', '--porcelain', '--untracked-files=no'):
    raise SystemExit('Integration requires a clean tracked working tree')
if git('rev-list', '--count', f'{BASE}..{HEAD}') != '66':
    raise SystemExit('Reviewed upstream inventory no longer matches 66 commits')
subprocess.run(['git', '-C', str(source), 'merge-base', '--is-ancestor', BASE, HEAD], check=True)
print('Verified complete reviewed upstream snapshot (66 commits); no duplicate patch application')
