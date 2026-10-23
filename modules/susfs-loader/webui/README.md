# KitsuSU LKM WebUI preview

Adapts the status-page markup from sidex15/susfs4ksu-module, `webui` commit
`b2d5e037b2370d5ae13a15eab0d7d1c29cbe80b0` (AGPL-3.0).
The upstream license and full source are included in the module ZIP alongside
these adaptations. The separately packaged kernel payload retains GPL-2.0.

This is a status-only integration, not a full port of upstream configuration.
Its fixed probe reads runtime interfaces and saved logs. It never invokes
`ksu_susfs`, upstream config scripts, network updates, loading or unloading.
Presence is labeled unverified; missing interfaces do not diagnose hook failure.
All report text is inserted with textContent.

Build from the repository root:

```sh
git clone https://github.com/sidex15/susfs4ksu-module upstream-webui
git -C upstream-webui checkout b2d5e037b2370d5ae13a15eab0d7d1c29cbe80b0
python3 modules/susfs-loader/webui/prepare.py --upstream upstream-webui --out webui-build
cd webui-build
npm ci --ignore-scripts --no-audit --no-fund
npm run build
cd ..
python3 modules/susfs-loader/pack_webui.py --webroot webui-build/dist --upstream upstream-webui --out rebuilt/KitsuSU-SusFS-Loader-6.12-preview2.zip
```

Phone validation still required: install the ZIP, apply the staged update using
the supported soft-reboot path, open the module WebUI, Refresh, and Copy report.
Confirm original load diagnostics survive Action and WebUI refreshes.
