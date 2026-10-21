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
     'extra["defaultManagerAppName"] = "BakaSU"')
app = 'manager/app/build.gradle.kts'
edit(app, 'buildConfigField("boolean", "IS_PR_BUILD", isPrBuild.toString())',
     'buildConfigField("boolean", "IS_PR_BUILD", isPrBuild.toString())\n        // Samsung artifacts must not offer incompatible upstream manager updates.\n        buildConfigField("boolean", "SAMSUNG_BUILD", "true")')
edit(app, '"ReSukiSU_${managerVersionName}_${managerVersionCode}"',
     '"BakaSU_${managerVersionName}_${managerVersionCode}"')
home = 'manager/app/src/main/java/com/resukisu/resukisu/ui/screen/main/HomePage.kt'
edit(home, 'import androidx.compose.material3.LargeFlexibleTopAppBar',
     'import androidx.compose.material3.TopAppBar')
edit(home, '    LargeFlexibleTopAppBar(', '    TopAppBar(')
edit(home, 'if (!uiState.systemStatus.isOfficialSignature) {',
     'if (!uiState.systemStatus.isOfficialSignature &&\n                        !(BuildConfig.SAMSUNG_BUILD && uiState.systemStatus.isManager)) {')
usecase = 'manager/app/src/main/java/com/resukisu/resukisu/domain/usecase/CheckManagerUpdateUseCase.kt'
edit(usecase, 'import com.resukisu.resukisu.data.update.ManagerUpdateRepository',
     'import com.resukisu.resukisu.BuildConfig\nimport com.resukisu.resukisu.data.update.ManagerUpdateRepository')
edit(usecase, '        when (channel) {',
     '        if (BuildConfig.SAMSUNG_BUILD) null else when (channel) {')
for path, text in changes.items():
    path.write_text(text)
    print(f'patched {path}')
