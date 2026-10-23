// KitsuSU additions, SysopBP, 2026-10-23. GPL-3.0-or-later.
package app.kitsusu.manager.ui.screen.susfs.subpages

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.twotone.Info
import androidx.compose.runtime.Composable
import androidx.compose.ui.res.stringResource
import app.kitsusu.manager.R
import app.kitsusu.manager.data.susfs.KitsuSusfsRuntime
import app.kitsusu.manager.ui.component.settings.SegmentedColumn
import app.kitsusu.manager.ui.component.settings.SettingsBaseWidget

@Composable
internal fun KitsuSusfsRuntimeCard(status: KitsuSusfsRuntime) {
    fun stateResource(value: Boolean?) = when (value) {
        true -> R.string.kitsu_susfs_runtime_available
        false -> R.string.kitsu_susfs_runtime_unavailable
        null -> R.string.kitsu_susfs_runtime_unknown
    }
    SegmentedColumn {
        item {
            SettingsBaseWidget(icon = Icons.TwoTone.Info,
                title = stringResource(R.string.kitsu_susfs_runtime_title),
                description = stringResource(R.string.kitsu_susfs_runtime_summary))
        }
        item {
            SettingsBaseWidget(title = stringResource(R.string.kitsu_susfs_runtime_path),
                description = stringResource(stateResource(status.path)))
        }
        item {
            SettingsBaseWidget(title = stringResource(R.string.kitsu_susfs_runtime_kstat),
                description = stringResource(stateResource(status.kstat)))
        }
        item {
            SettingsBaseWidget(title = stringResource(R.string.kitsu_susfs_runtime_redirect),
                description = stringResource(stateResource(status.redirect)))
        }
    }
}
