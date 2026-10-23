// KitsuSU additions, SysopBP, 2026-10-23. GPL-3.0-or-later.
package app.kitsusu.manager.data.susfs

import app.kitsusu.manager.data.shell.KsuCliRepository
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

// Interface availability is not a functional test. Never persist a device-test verdict here.
data class KitsuSusfsRuntime(val path: Boolean?, val kstat: Boolean?, val redirect: Boolean?)

class KitsuSusfsRuntimeRepository(private val cli: KsuCliRepository) {
    suspend fun load(): KitsuSusfsRuntime = withContext(Dispatchers.IO) {
        runCatching {
            val shell = cli.getRootShell()
            if (!shell.isRoot) return@runCatching unknown()
            val result = shell.newJob().add("""
                if [ ! -d /sys/module/susfs_guard_lkm ]; then exit 1; fi
                echo KITSU_LKM
                if [ -r /proc/susfs_path ]; then
                    echo KITSU_PATH
                    cat /proc/susfs_path
                fi
                if [ -r /proc/susfs_kstat ]; then
                    echo KITSU_KSTAT
                    cat /proc/susfs_kstat
                fi
                if [ -r /proc/susfs_open_redirect ]; then
                    echo KITSU_REDIRECT
                    cat /proc/susfs_open_redirect
                fi
                if [ -r /proc/susfs_opath ]; then
                    echo KITSU_OPATH
                    cat /proc/susfs_opath
                fi
                echo KITSU_END
            """.trimIndent()).exec()
            if (!result.isSuccess) return@runCatching unknown()
            parse(result.out.joinToString("\n"))
        }.getOrElse {
            if (it is CancellationException) throw it
            unknown()
        }
    }

    companion object {
        fun unknown() = KitsuSusfsRuntime(null, null, null)

        fun parse(output: String): KitsuSusfsRuntime {
            val lines = output.lines()
            if ("KITSU_LKM" !in lines || "KITSU_END" !in lines) return unknown()
            fun section(marker: String): String = lines.dropWhile { it != marker }
                .drop(1).takeWhile { !it.startsWith("KITSU_") }.joinToString("\n")
            val path = section("KITSU_PATH")
            val kstat = section("KITSU_KSTAT")
            val redirect = section("KITSU_REDIRECT")
            val opath = section("KITSU_OPATH")
            // Recognize this LKM's status format before interpreting absent interfaces.
            if (!path.startsWith("hide_from_apps=") || !redirect.contains("hooks: forward=")) {
                return unknown()
            }
            val forward = Regex("hooks: forward=(\\d+)").find(redirect)
                ?.groupValues?.get(1)?.toIntOrNull()
            val installed = Regex("installed=(\\d+)").findAll(opath)
                .mapNotNull { it.groupValues[1].toIntOrNull() }.toList()
            return KitsuSusfsRuntime(
                path = true,
                kstat = if ("KITSU_KSTAT" !in lines) false
                    else if (kstat.contains("stat nr ")) true else null,
                // Zero forward hooks can simply mean no rules yet. Only a positive
                // installed open-entry status establishes prerequisites; otherwise unknown.
                redirect = when {
                    forward != null && forward > 0 -> true
                    installed.any { it > 0 } -> true
                    installed.isNotEmpty() && installed.all { it == 0 } -> false
                    else -> null
                },
            )
        }
    }
}
