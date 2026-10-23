#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-only
"""Reproduce the Samsung preview ZIP with unchanged, checksum-pinned upstream binaries."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parent
TAG = 'v2.3.0-r18.4'
COMMIT = '8b65f13f3eff4e9d530c92a92dde6133b0700ae7'
REPO = 'https://github.com/inforcqb/susfs4ksu-lkm'
ASSET = f'susfs_guard_lkm-module-{TAG}-arm64.zip'
RELEASE_SHA = '7288d43d2965957c1fa95f91b8e58387a6d15a16003b75d0c0dcaaac26529888'
PAYLOADS = {
    'bin/susfs_insmod': '16a722d2158ff629e9e3d6d056e8333f15971410965ce5894216ed80dbfa44a4',
    'lib/susfs_guard_lkm-android16-6.12.ko': '49e06572a503d64d40ee562fd2929b21efeba65fd430a9cc2f9c30c09f9646c9',
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--upstream-zip', type=Path)
    ap.add_argument('--upstream-source', type=Path)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        archive = args.upstream_zip
        if archive is None:
            archive = tmp / ASSET
            with urllib.request.urlopen(f'{REPO}/releases/download/{TAG}/{ASSET}', timeout=90) as r:
                archive.write_bytes(r.read())
        if digest(archive) != RELEASE_SHA:
            raise SystemExit('Upstream release ZIP checksum mismatch')
        source = args.upstream_source
        if source is None:
            source = tmp / 'upstream'
            subprocess.run(['git', 'clone', '--depth', '1', '--branch', TAG, REPO + '.git', str(source)], check=True)
        revision = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
        if revision != COMMIT:
            raise SystemExit('Upstream source revision mismatch')
        stage = tmp / 'stage'
        stage.mkdir()
        for name in ('load.sh', 'post-fs-data.sh', 'action.sh', 'customize.sh', 'module.prop',
                     'payload.sha256', 'skip_mount', 'provenance.json'):
            shutil.copyfile(ROOT / name, stage / name)
        shutil.copyfile(ROOT / 'PACKAGE-README.md', stage / 'README.md')
        with zipfile.ZipFile(archive) as z:
            for name in (*PAYLOADS, 'LICENSE'):
                p = stage / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(z.read(name))
                if name in PAYLOADS and digest(p) != PAYLOADS[name]:
                    raise SystemExit(f'Binary checksum mismatch: {name}')
        (stage / 'source').mkdir()
        subprocess.run(['git', '-C', str(source), 'archive', '--format=tar.gz', '--prefix=susfs4ksu-lkm/',
                        '--output=' + str(stage / 'source' / f'susfs4ksu-lkm-{TAG}.tar.gz'), COMMIT], check=True)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(args.out, 'w', zipfile.ZIP_DEFLATED) as z:
            for p in sorted(stage.rglob('*')):
                if not p.is_file():
                    continue
                info = zipfile.ZipInfo(p.relative_to(stage).as_posix())
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = (0o100755 if p.suffix == '.sh' or p.name == 'susfs_insmod' else 0o100644) << 16
                z.writestr(info, p.read_bytes())
        with zipfile.ZipFile(args.out) as z:
            if z.testzip() is not None:
                raise SystemExit('ZIP integrity failure')
        print(digest(args.out) + '  ' + str(args.out))


if __name__ == '__main__':
    main()
