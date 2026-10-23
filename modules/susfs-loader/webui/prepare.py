#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
"""Adapt pinned sidex15 WebUI status markup; do not ship its incompatible controls."""
import argparse
from pathlib import Path
import re
import shutil
import subprocess

COMMIT = 'b2d5e037b2370d5ae13a15eab0d7d1c29cbe80b0'
ROOT = Path(__file__).resolve().parent

def prepare(source, out):
    head = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    if head != COMMIT:
        raise SystemExit('Unexpected upstream WebUI revision')
    if out.exists():
        raise SystemExit('Output directory must not exist')
    shutil.copytree(source, out, ignore=shutil.ignore_patterns('.git', 'node_modules', 'dist'))
    page = (source / 'status.html').read_text()
    page = re.sub(r'<script\b[^>]*>.*?</script>', '', page, flags=re.S)
    page = re.sub(r' data-i18n="[^"]*"', '', page)
    page = page.replace('<title>Document</title>', '<title>KitsuSU SusFS</title>')
    page = page.replace('</head>', '<script type="module" src="./index.js"></script></head>')
    page = page.replace('Kernel Features Status', 'Runtime interfaces')
    # Keep only the three interfaces our fixed probe actually inspects.
    rows = re.compile(r'<div class="flex justify-between items-center py-2 px-2">.*?</div>\s*</div>', re.S)
    keep = {'status_sus_path', 'status_sus_kstat', 'status_open_redirect'}
    count = 0
    def row(match):
        nonlocal count
        text = match.group(0)
        if any(f'id="{key}"' in text for key in keep):
            count += 1
            return text.replace('Unknown', 'Not verified').replace(' Support', '')
        return ''
    page = rows.sub(row, page)
    if count != 3:
        raise SystemExit('Upstream status markup changed')
    page = re.sub(r'<a href="index.html".*?</a>', '', page, flags=re.S)
    intro = '''<header class="px-4 pt-5 text-white"><h1 class="text-2xl">KitsuSU SusFS</h1>
<p>Samsung LKM preview · status and diagnostics</p><p id="kernel" class="break-all text-sm"></p>
<p id="message" role="status" aria-live="polite">Opening status…</p>
<button id="refresh" class="btn btn-outline mt-3">Refresh</button>
<button id="copy" class="btn btn-outline mt-3" disabled>Copy report</button>
<p class="mt-3 text-sm">Configuration controls need an LKM backend adapter and are not included in this preview.</p></header>'''
    page = page.replace('<section class=', intro + '<section class=', 1)
    report = '''<section class="px-4 text-white"><h2 class="text-lg">Diagnostics and saved load logs</h2>
<pre id="report" class="text-xs whitespace-pre-wrap break-all"></pre>
<p class="py-4 text-sm">Adapted from sidex15/susfs4ksu-module WebUI (AGPL-3.0).
Source and license are included in this module ZIP under source/ and licenses/.</p></section>'''
    page = page.replace('</main>', report + '</main>')
    page = page.replace('</head>', '<style>body{background:#181a19;color:#eee;font-family:system-ui,sans-serif} .badge{height:auto;white-space:normal;text-align:right;max-width:55%} section{padding-top:1rem!important} .stats{width:calc(100% - 2rem)} pre{user-select:text} button{color:#eee!important} #message{margin-top:1rem}</style></head>')
    (out / 'index.html').write_text(page)
    shutil.copyfile(ROOT / 'index.js', out / 'index.js')
    # Build only this adapted entry; no upstream configuration or update entry point.
    (out / 'vite.config.js').write_text("import {defineConfig} from 'vite';\nexport default defineConfig({base:'./',build:{rollupOptions:{input:'index.html'}}});\n")

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--upstream', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    prepare(args.upstream.resolve(), args.out.resolve())
