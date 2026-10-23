#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-only
"""Package preview 2 using the verified preview 1 kernel payload and built WebUI."""
import argparse
import hashlib
from pathlib import Path
import subprocess
import zipfile
from webui.prepare import COMMIT

ROOT = Path(__file__).resolve().parent
SEED = ROOT.parents[1] / 'releases/experimental/KitsuSU-SusFS-Loader-6.12-preview1.zip'
SEED_SHA = '24a12afcc050e56fabc52e97a191d4f2580970cfb530d711d80c2df7307250b8'

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--webroot', type=Path, required=True)
    ap.add_argument('--upstream', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    if hashlib.sha256(SEED.read_bytes()).hexdigest() != SEED_SHA:
        raise SystemExit('Preview 1 seed checksum mismatch')
    head = subprocess.check_output(['git', '-C', str(args.upstream), 'rev-parse', 'HEAD'], text=True).strip()
    if head != COMMIT or not (args.webroot / 'index.html').is_file():
        raise SystemExit('Missing WebUI build or incorrect upstream revision')
    with zipfile.ZipFile(SEED) as z:
        files = {name: z.read(name) for name in z.namelist()}
    for name in ('action.sh', 'status.sh', 'load.sh', 'customize.sh'):
        files[name] = (ROOT / name).read_bytes()
    prop = files['module.prop'].decode().replace('preview.1', 'preview.2').replace('2026102301', '2026102302')
    files['module.prop'] = prop.replace('Loader only; no rules.', 'WebUI diagnostics; no rules.').encode()
    for p in sorted(args.webroot.rglob('*')):
        if p.is_file(): files['webroot/' + p.relative_to(args.webroot).as_posix()] = p.read_bytes()
    files['licenses/WebUI-AGPL-3.0.txt'] = (args.upstream / 'LICENSE').read_bytes()
    files['source/sidex15-webui.tar'] = subprocess.check_output(['git', '-C', str(args.upstream), 'archive', COMMIT])
    for p in sorted((ROOT / 'webui').glob('*')):
        if p.is_file(): files['source/webui-adapter/' + p.name] = p.read_bytes()
    for name in ('pack_webui.py', 'customize.sh', 'action.sh', 'load.sh', 'status.sh'):
        files['source/kitsu-loader/' + name] = (ROOT / name).read_bytes()
    files['WEBUI-NOTICES.txt'] = (f'WebUI adapted from sidex15/susfs4ksu-module, webui commit {COMMIT}.\n'
        'https://github.com/sidex15/susfs4ksu-module/tree/' + COMMIT + '\n'
        'Upstream WebUI and adaptations: AGPL-3.0; included under licenses/.\n'
        'LKM and loader retain their separate GPL-2.0 license.\n'
        'Modified by SysopBP for KitsuSU: status-only LKM backend; configuration controls omitted.\n'
        'Full upstream source and adaptation scripts are in source/.\n').encode()
    files['README.md'] = (b'# KitsuSU SusFS Loader preview 2\n\n'
        b'Open the module WebUI button in KitsuSU for read-only runtime status, logs and Copy report.\n'
        b'Action now reads status only. Opening either screen never loads or configures SusFS.\n'
        b'Install through Modules; the manager stages updates until the next supported soft reboot.\n'
        b'No root recovery, reboot, feature configuration or kernel-hook repair is performed by the UI.\n'
        b'Interface presence is not functional verification. Missing interfaces have no diagnosed cause yet.\n'
        b'Kstat/Open Redirect rules remain unconfigured. See WEBUI-NOTICES.txt for upstream credits.\n\n'
        b'## Original loader documentation\n\n' + files['README.md'])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.out, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o100755 if name.endswith('.sh') or name == 'bin/susfs_insmod' else 0o100644) << 16
            z.writestr(info, data)
    print(hashlib.sha256(args.out.read_bytes()).hexdigest(), args.out)

if __name__ == '__main__': main()
