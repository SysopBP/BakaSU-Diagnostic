#!/usr/bin/env python3
"""Apply the reviewed integration queue to the exact phone-tested baseline."""
import argparse
from pathlib import Path
import subprocess

BASE = '239e1e8871b8fcd51a6e5b3002e0ba522fdd99fb'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source', type=Path, required=True)
args = parser.parse_args()
source = args.source.resolve()
queue = Path(__file__).resolve().parents[1] / 'patches/bakasu'

def git(*args):
    return subprocess.check_output(['git', '-C', str(source), *args], text=True).strip()

if git('rev-parse', 'HEAD') != BASE:
    raise SystemExit('Integration requires the pinned baseline, not a moving upstream head')
if git('status', '--porcelain', '--untracked-files=no'):
    raise SystemExit('Integration requires a clean tracked working tree')
patches = sorted(queue.glob('*.patch'))
if len(patches) != 12:
    raise SystemExit(f'Expected 12 reviewed patches, found {len(patches)}')
# Check each patch against its predecessors; abort rather than resolving silently.
for patch in patches:
    git('apply', '--check', str(patch))
    git('apply', str(patch))
    print('Applied', patch.name)
