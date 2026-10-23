// SPDX-License-Identifier: AGPL-3.0-only
// KitsuSU LKM adapter. The upstream configuration backend is deliberately not invoked.
const command = '/system/bin/sh /data/adb/modules/susfs_guard_lkm/status.sh';
let sequence = 0;
export function runProbe(bridge = globalThis.ksu) {
  return new Promise((resolve, reject) => {
    if (!bridge || typeof bridge.exec !== 'function') {
      reject(new Error('Open this page using KitsuSU’s module WebUI button.'));
      return;
    }
    const callback = `kitsu_status_${++sequence}`;
    const timer = setTimeout(() => {
      delete globalThis[callback];
      reject(new Error('Status check timed out. Try Refresh.'));
    }, 20000);
    globalThis[callback] = (code, stdout, stderr) => {
      clearTimeout(timer);
      delete globalThis[callback];
      if (Number(code) === 0) resolve(String(stdout || ''));
      else reject(new Error(String(stderr || `Status check failed (exit ${code}).`)));
    };
    try { bridge.exec(command, '{}', callback); }
    catch (error) {
      clearTimeout(timer);
      delete globalThis[callback];
      reject(error);
    }
  });
}

export function sections(text) {
  const result = {};
  let key = '';
  for (const line of text.split('\n')) {
    const match = /^=== (.+) ===$/.exec(line);
    if (match) { key = match[1]; result[key] = ''; }
    else if (key) result[key] += line + '\n';
  }
  return result;
}

export function interfaceLabel(text = '') {
  return text.startsWith('Interface present;') ? 'Interface present · unverified'
    : text.startsWith('Interface unavailable;') ? 'Interface unavailable' : 'Not verified';
}

if (typeof document !== 'undefined') {
  const refresh = document.getElementById('refresh');
  const report = document.getElementById('report');
  const message = document.getElementById('message');
  const copy = document.getElementById('copy');
  const badge = (id, value) => { document.querySelector(`#${id} span`).textContent = value; };
  async function update() {
    refresh.disabled = true;
    copy.disabled = true;
    report.textContent = '';
    message.textContent = 'Checking…';
    for (const id of ['status_sus_path', 'status_sus_kstat', 'status_open_redirect']) badge(id, 'Checking…');
    try {
      const text = await runProbe();
      const data = sections(text);
      report.textContent = text;
      document.getElementById('kernel').textContent = (data.KERNEL || 'Unknown').trim();
      message.textContent = (data.MODULE || '').trim() === 'present'
        ? 'LKM loaded. Interface presence does not verify feature behavior.' : 'LKM not detected.';
      badge('status_sus_path', interfaceLabel(data.susfs_path));
      badge('status_sus_kstat', interfaceLabel(data.susfs_kstat));
      badge('status_open_redirect', interfaceLabel(data.susfs_open_redirect));
      copy.disabled = false;
    } catch (error) {
      message.textContent = error.message;
      for (const id of ['status_sus_path', 'status_sus_kstat', 'status_open_redirect']) badge(id, 'Not verified');
    } finally { refresh.disabled = false; }
  }
  refresh.addEventListener('click', update);
  copy.addEventListener('click', async () => {
    try {
      if (typeof globalThis.ksu?.clipboard === 'function') globalThis.ksu.clipboard(report.textContent);
      else await navigator.clipboard.writeText(report.textContent);
      message.textContent = 'Report copied. You can paste it into chat.';
    } catch { message.textContent = 'Copy unavailable. The report remains visible below.'; }
  });
  update();
}
