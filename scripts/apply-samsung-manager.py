#!/usr/bin/env python3
"""Brand and relocate the pinned Samsung manager, preserving driver signature checks."""
from pathlib import Path

changes = {}
def edit(name, old, new):
    p = Path(name)
    text = changes.get(p, p.read_text())
    if text.count(old) != 1:
        raise SystemExit(f'{p}: expected exactly one anchor {old!r}')
    changes[p] = text.replace(old, new, 1)

edit('manager/build.gradle.kts',
     'extra["defaultManagerAppName"] = if (extra["isPrBuild"] == true) "ReSukiSU PR" else "ReSukiSU"',
     'extra["defaultManagerAppName"] = "KitsuSU"')
app = 'manager/app/build.gradle.kts'
edit(app, 'buildConfigField("boolean", "IS_PR_BUILD", isPrBuild.toString())',
     'buildConfigField("boolean", "IS_PR_BUILD", isPrBuild.toString())\n        // Samsung artifacts must not offer incompatible upstream manager updates.\n        buildConfigField("boolean", "SAMSUNG_BUILD", "true")')
edit(app, '"ReSukiSU_${managerVersionName}_${managerVersionCode}"',
     '"KitsuSU_${managerVersionName}_${managerVersionCode}"')
home = 'manager/app/src/main/java/com/resukisu/resukisu/ui/screen/main/HomePage.kt'
edit(home, 'import androidx.compose.material3.LargeFlexibleTopAppBar',
     'import androidx.compose.material3.TopAppBar')
edit(home, '    LargeFlexibleTopAppBar(', '    TopAppBar(')
# A custom wallpaper should continue behind the compact header even without blur.
# Patch only HomePage's two app-bar color branches; preserve solid default themes.
home_source = Path(home).read_text()
color_anchor = 'if (themeConfig.isEnableBlur)\n                    Color.Transparent'
if home_source.count(color_anchor) != 2:
    raise SystemExit(f'{home}: expected two app-bar color branches')
changes[Path(home)] = changes[Path(home)].replace(
    color_anchor,
    'if (themeConfig.isEnableBlur || themeConfig.customBackgroundUri != null)\n                    Color.Transparent',
)
edit(home, 'if (!uiState.systemStatus.isOfficialSignature) {',
     'if (!uiState.systemStatus.isOfficialSignature &&\n                        !(BuildConfig.SAMSUNG_BUILD && uiState.systemStatus.isManager)) {')
# Keep the phone-tested debug configuration; omit its persistent home warning.
edit(home, 'if (BuildConfig.DEBUG) {',
     'if (BuildConfig.DEBUG && !BuildConfig.SAMSUNG_BUILD) {')
usecase = 'manager/app/src/main/java/com/resukisu/resukisu/domain/usecase/CheckManagerUpdateUseCase.kt'
edit(usecase, 'import com.resukisu.resukisu.data.update.ManagerUpdateRepository',
     'import com.resukisu.resukisu.BuildConfig\nimport com.resukisu.resukisu.data.update.ManagerUpdateRepository')
edit(usecase, '        when (channel) {',
     '        if (BuildConfig.SAMSUNG_BUILD) null else when (channel) {')
# Product-facing branding; native version metadata and credits stay intact.
base = 'manager/app/src/main/java/com/resukisu/resukisu/'
edit(base + 'data/logging/BugreportDataSource.kt',
     'pw.println("ReSukiSU: $ksuKernelFull")',
     'pw.println("KitsuSU driver: $ksuKernelFull")')
edit(base + 'di/AppModules.kt',
     '"ReSukiSU/${BuildConfig.VERSION_CODE}"',
     '"KitsuSU/${BuildConfig.VERSION_CODE}"')
edit(base + 'ui/screen/about/About.kt',
     'https://github.com/ReSukiSU/ReSukiSU',
     'https://github.com/SysopBP/BakaSU-Diagnostic/tree/feat/samsung-jailbreak')
edit(base + 'ui/screen/about/About.kt',
     'https://t.me/ReSukiSU',
     'https://github.com/SysopBP/BakaSU-Diagnostic/issues')
edit(base + 'ui/screen/main/ModulePage.kt',
     'R.drawable.ic_launcher_foreground',
     'R.drawable.kitsu_fox')
for path, text in changes.items():
    path.write_text(text)
    print(f'patched {path}')

# Original KitsuSU fox artwork, shared by both launcher choices.
from shutil import copyfile
asset_dir = Path(__file__).resolve().parent.parent / 'vendor/manager'
res = Path('manager/app/src/main/res')
for asset in ('kitsu_fox.png', 'kitsu_fox_mono.png'):
    target = res / 'drawable' / asset
    copyfile(asset_dir / asset, target)
icon = """<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@android:color/black" />
    <foreground android:drawable="@drawable/kitsu_fox" />
    <monochrome android:drawable="@drawable/kitsu_fox_mono" />
</adaptive-icon>
"""
for name in ('ic_launcher', 'ic_launcher_round', 'ic_launcher_alt', 'ic_launcher_alt_round'):
    (res / 'mipmap' / (name + '.xml')).write_text(icon)

# Modified by SysopBP on 2026-10-21: ship only the replacement fox artwork.
# The inherited anime launcher artwork has separate redistribution restrictions.
# Remove unused drawable variants from both the APK resources and source bundle.
for name in ('ic_launcher_foreground.xml', 'ic_launcher_foreground_alt.xml',
             'ic_launcher_monochrome.xml', 'ic_launcher_monochrome_alt.xml'):
    (res / 'drawable' / name).unlink(missing_ok=True)
copyfile(asset_dir / 'kitsu_fox.png', Path('manager/app/src/main/ic_launcher-playstore.png'))

# Source archives are distributions too: remove inherited documentation artwork,
# while retaining licensing texts, authorship credits and the technical docs.
for docs in (Path('docs'), Path('docs/zh')):
    for pattern in ('ReSukiSU_*.svg', 'zako*.svg'):
        for artwork in docs.glob(pattern):
            artwork.unlink()
    readme = docs / 'README.md'
    if readme.exists():
        readme.write_text(''.join(line for line in readme.read_text().splitlines(keepends=True)
                                  if '<img' not in line or 'ReSukiSU_' not in line))

# Keep all locales consistent where inherited text describes this fork's branding.
import re
branding_strings = {
    'join_telegram_group': 'KitsuSU support',
    'join_telegram_group_detail': 'Report issues and follow KitsuSU development on GitHub',
    'icon_switch_summary': 'Switch the KitsuSU launcher icon',
}
for strings in res.glob('values*/strings.xml'):
    content = strings.read_text()
    for key, replacement in branding_strings.items():
        pattern = r'(<string\s+name="' + re.escape(key) + r'"[^>]*>).*?(</string>)'
        content = re.sub(pattern, lambda match: match[1] + replacement + match[2],
                         content, flags=re.DOTALL)
    strings.write_text(content)

# Relocate the entire app namespace together: Java/Kotlin, R/BuildConfig,
# manifest components/actions, JNI exports/class descriptors, and keep rules.
old_package, new_package = 'com.resukisu.resukisu', 'app.kitsusu.manager'
old_path, new_path = old_package.replace('.', '/'), new_package.replace('.', '/')
old_jni, new_jni = old_package.replace('.', '_'), new_package.replace('.', '_')
source_suffixes = {'.kt', '.kts', '.java', '.xml', '.pro', '.c', '.cpp', '.h', '.properties'}
for source in Path('manager').rglob('*'):
    if source.is_file() and source.suffix in source_suffixes:
        content = source.read_text()
        updated = content.replace(old_package, new_package).replace(old_path, new_path).replace(old_jni, new_jni)
        if updated != content:
            source.write_text(updated)
old_source = Path('manager/app/src/main/java') / old_path
new_source = Path('manager/app/src/main/java') / new_path
if not old_source.is_dir() or new_source.exists():
    raise SystemExit('Unexpected manager namespace layout')
new_source.parent.mkdir(parents=True, exist_ok=True)
old_source.rename(new_source)
# Keep daemon default package and explicit CLI defaults aligned with the APK.
for name in ('userspace/ksud/build.rs', 'userspace/ksud/src/android/cli.rs'):
    source = Path(name)
    content = source.read_text()
    if old_package not in content:
        raise SystemExit(f'{source}: missing package default anchor')
    source.write_text(content.replace(old_package, new_package))
print(f'manager namespace and daemon defaults: {new_package}')
