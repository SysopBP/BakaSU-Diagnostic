#!/usr/bin/env python3
"""Brand the pinned Samsung manager without changing its package or driver checks."""
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
