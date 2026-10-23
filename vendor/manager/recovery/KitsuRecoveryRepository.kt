// KitsuSU additions, SysopBP, 2026-10-23. GPL-3.0-or-later.
package app.kitsusu.manager.data.recovery

import app.kitsusu.manager.Natives
import app.kitsusu.manager.data.shell.KsuCliRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class KitsuRecoveryRepository(private val cli: KsuCliRepository) {
    suspend fun perform(action: Int): Boolean = withContext(Dispatchers.IO) {
        runCatching {
            val shell = cli.getRootShell()
            if (!shell.isRoot) return@runCatching false
            when (action) {
                0 -> shell.newJob().add("setprop ctl.restart zygote").exec().isSuccess
                1 -> cli.execKsud("soft-reboot", newShell = true, globalMnt = true)
                2 -> {
                    if (!Natives.isLkmMode) return@runCatching false
                    // Only disable the boot entry point. Do not edit another app's
                    // preferences, uninstall the manager, or touch boot partitions.
                    val disabled = shell.newJob().add(
                        "pm disable --user 0 com.sysopbp.fragx/df.root.BootReceiver"
                    ).exec().isSuccess
                    if (!disabled) return@runCatching false
                    shell.newJob().add("/system/bin/svc power reboot").exec().isSuccess
                }
                else -> false
            }
        }.getOrDefault(false)
    }
}
