// KitsuSU additions, SysopBP, 2026-10-23. GPL-3.0-or-later.
package app.kitsusu.manager.ui.screen.main

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Security
import androidx.compose.material.icons.filled.Tune
import androidx.compose.material.icons.filled.Shield
import androidx.compose.material.icons.filled.RestartAlt
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.PowerSettingsNew
import androidx.compose.runtime.*
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import app.kitsusu.manager.R
import app.kitsusu.manager.Natives
import app.kitsusu.manager.data.recovery.KitsuRecoveryRepository
import app.kitsusu.manager.data.shell.KsuCliRepository
import app.kitsusu.manager.data.susfs.SuSFSRepository
import app.kitsusu.manager.ui.component.ConfirmResult
import app.kitsusu.manager.ui.component.rememberConfirmDialog
import app.kitsusu.manager.ui.component.settings.SegmentedColumn
import app.kitsusu.manager.ui.component.settings.SettingsJumpPageWidget
import app.kitsusu.manager.ui.component.settings.SettingsSwitchWidget
import app.kitsusu.manager.ui.navigation.LocalNavigator
import app.kitsusu.manager.ui.navigation.Route
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.koin.compose.koinInject

@Composable
internal fun KitsuRecoveryControls() {
    val context = LocalContext.current
    val navigator = LocalNavigator.current
    val cli = koinInject<KsuCliRepository>()
    val susfs = koinInject<SuSFSRepository>()
    val recovery = remember(cli) { KitsuRecoveryRepository(cli) }
    val scope = rememberCoroutineScope()
    val confirm = rememberConfirmDialog()
    var supported by remember { mutableStateOf(false) }
    var enabled by remember { mutableStateOf(false) }
    var busy by remember { mutableStateOf(true) }
    var status by remember { mutableStateOf(R.string.kitsu_checking) }
    var version by remember { mutableStateOf("") }
    var lkm by remember { mutableStateOf(false) }
    LaunchedEffect(Unit) {
        val result = withContext(Dispatchers.IO) {
            runCatching {
                Triple(susfs.getStatus(), susfs.loadConfig().enabled, Natives.isLkmMode)
            }
        }
        result.onSuccess { (info, config, isLkm) ->
            supported = info.enabled
            enabled = config
            version = info.version
            lkm = isLkm
            status = if (supported) R.string.kitsu_susfs_available else R.string.kitsu_susfs_unsupported
        }.onFailure { status = R.string.kitsu_check_failed }
        busy = false
    }
    SegmentedColumn(title = stringResource(R.string.kitsu_root_management), content = {
        item {
            SettingsSwitchWidget(
                icon = Icons.Filled.Security,
                title = stringResource(R.string.kitsu_susfs_title),
                description = stringResource(R.string.kitsu_susfs_summary),
                checked = enabled, enabled = supported && !busy,
                onCheckedChange = { value ->
                    busy = true
                    scope.launch {
                        val ok = withContext(Dispatchers.IO) {
                            runCatching { susfs.setConfigEnabled(value) }.getOrDefault(false)
                        }
                        if (ok) enabled = value
                        status = if (ok) R.string.kitsu_config_saved else R.string.kitsu_action_failed
                        busy = false
                    }
                }
            )
        }
        item {
            SettingsJumpPageWidget(
                icon = Icons.Filled.Tune,
                title = stringResource(R.string.kitsu_susfs_status),
                description = stringResource(status) + if (version.isBlank()) "" else "\n$version",
                enabled = supported && !busy,
                onClick = { navigator.push(Route.SuSFSConfig) }
            )
        }
    })
    SegmentedColumn(title = stringResource(R.string.kitsu_recovery_management), content = {
        item {
            SettingsJumpPageWidget(
                icon = Icons.Filled.Shield,
                title = stringResource(R.string.kitsu_vaultguard),
                description = stringResource(R.string.kitsu_vaultguard_summary),
                onClick = {
                    val intent = context.packageManager.getLaunchIntentForPackage("com.sysopbp.fragx")
                    if (intent != null) context.startActivity(intent)
                    else android.widget.Toast.makeText(context, R.string.kitsu_fragx_missing,
                        android.widget.Toast.LENGTH_LONG).show()
                }
            )
        }
        for ((action, title, description) in listOf(
            Triple(0, R.string.kitsu_restart_zygote, R.string.kitsu_restart_zygote_summary),
            Triple(1, R.string.kitsu_soft_reboot, R.string.kitsu_soft_reboot_summary),
            Triple(2, R.string.kitsu_unroot, R.string.kitsu_unroot_summary)
        )) {
            item {
                SettingsJumpPageWidget(
                    icon = when (action) {
                        0 -> Icons.Filled.RestartAlt
                        1 -> Icons.Filled.Refresh
                        else -> Icons.Filled.PowerSettingsNew
                    },
                    title = stringResource(title), description = stringResource(description),
                    enabled = !busy && (action != 2 || lkm),
                    onClick = {
                        busy = true
                        scope.launch {
                            try {
                                if (confirm.awaitConfirm(title = context.getString(title),
                                        content = context.getString(description)) == ConfirmResult.Confirmed) {
                                    val ok = recovery.perform(action)
                                    android.widget.Toast.makeText(context,
                                        if (ok) R.string.kitsu_request_sent else R.string.kitsu_action_failed,
                                        android.widget.Toast.LENGTH_LONG).show()
                                }
                            } finally { busy = false }
                        }
                    }
                )
            }
        }
    })
}
