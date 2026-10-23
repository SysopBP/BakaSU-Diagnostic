#!/usr/bin/env python3
"""Run the actual patched Rust parser in a small host-side Cargo test harness."""
from pathlib import Path
import argparse
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--source', type=Path, required=True)
args = parser.parse_args()
source = (args.source / 'userspace/ksud/src/android/soft_reboot.rs').read_text()
start = source.index('fn parse_service_list(')
end = source.index('fn parse_service_pid(', start)
tests = (Path(__file__).resolve().parents[1] / 'tests/service-list-parser.rs').read_text()
with tempfile.TemporaryDirectory(prefix='service-parser-test-') as directory:
    root = Path(directory)
    (root / 'src').mkdir()
    (root / 'Cargo.toml').write_text('[package]\nname="service-parser-regression"\nversion="0.1.0"\nedition="2021"\n[dependencies]\nanyhow="1"\nregex-lite="0.1"\n')
    (root / 'src/lib.rs').write_text('use anyhow::{Context, Result, ensure};\nuse regex_lite::Regex;\n' + source[start:end] + tests)
    subprocess.run(['cargo', 'test', '--manifest-path', str(root / 'Cargo.toml')], check=True)
