from pathlib import Path
import tempfile,subprocess,os,shutil
src=Path(__file__).resolve().parent
for script in src.glob('*.sh'): subprocess.run(['sh','-n',str(script)],check=True)
with tempfile.TemporaryDirectory() as temp:
 root=Path(temp); mod=root/'module';shutil.copytree(src,mod)
 fake=root/'commands';fake.mkdir(); proc=root/'proc';proc.mkdir();sys=root/'sys/module';sys.mkdir(parents=True)
 for name,text in {
 'id':'echo 0',
 'getprop':'echo "${TEST_SAFE:-0}"',
 'uname':'case "$1" in -r) echo "${TEST_KERNEL:-6.12.69-android16-6-test}";; -m) echo aarch64;; esac',
 'sha256sum':'exit 0',
 'dmesg':'echo test-log'
 }.items():
  p=fake/name;p.write_text('#!/bin/sh\n'+text+'\n');p.chmod(0o755)
 script=(src/'load.sh').read_text().replace('/sys/module',str(sys)).replace('/proc/susfs',str(proc/'susfs'))
 (mod/'load.sh').write_text(script)
 (mod/'bin').mkdir(exist_ok=True)
 loader=mod/'bin/susfs_insmod'
 loader.write_text('#!/bin/sh\necho call >> "'+str(root/'calls')+'"\n[ "${TEST_FAIL:-0}" = 0 ] || exit 7\nmkdir -p "'+str(sys/'susfs_guard_lkm')+'"\n')
 loader.chmod(0o755)
 env=dict(os.environ,PATH=str(fake)+':'+os.environ['PATH'])
 def run(**kw):return subprocess.run(['sh',str(mod/'load.sh')],env=env|kw,capture_output=True).returncode
 def calls(): return len((root/'calls').read_text().splitlines()) if (root/'calls').exists() else 0
 assert run(TEST_SAFE='1')==0 and calls()==0
 (mod/'disable').touch();assert run()==0 and calls()==0;(mod/'disable').unlink()
 assert run(TEST_KERNEL='6.6.1-android15-test')==1 and calls()==0
 assert run(TEST_FAIL='1')==1 and calls()==1 and (mod/'load-failed').exists()
 failed_log=(mod/'load.log').read_bytes()
 assert run()==1 and calls()==1 and (mod/'load.log').read_bytes()==failed_log # retry latch preserves evidence
 (mod/'load-failed').unlink()
 assert run()==0 and calls()==2 and not (mod/'load-failed').exists()
 success_log=(mod/'load.log').read_bytes()
 assert run()==0 and calls()==2 and (mod/'load.log').read_bytes()==success_log # duplicate guard preserves evidence
 assert (mod/'load.log.previous').read_bytes()==failed_log
 (mod/'load.lock').mkdir();assert run()==1 and calls()==2
 print('PASS: shell syntax, safe mode, disabled module, kernel mismatch, failed load, failure latch, successful load, duplicate guard, concurrent-load lock')
