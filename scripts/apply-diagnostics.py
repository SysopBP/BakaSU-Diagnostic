from pathlib import Path
p = Path("manager/app/src/main/java/com/sukisu/ultra/ui/viewmodel/HomeViewModel.kt")
s = p.read_text()

def replace(a, b):
    global s
    count = s.count(a)
    if count != 1:
        raise SystemExit(f"Expected exactly one match, got {count}: {a[:100]!r}")
    s = s.replace(a, b, 1)

replace("import android.content.Context\n", "import android.content.Context\nimport android.util.Log\n")
replace("""                val isManager = try {
                    Natives.isManager
                } catch (_: Exception) {
                    false
                }

                val ksuVersion = if (isManager) Natives.version else null""", """                // Diagnostic v2: never conflate manager authorization with driver presence.
                val isManager = try {
                    Natives.isManager.also { Log.i("BakaSU-DIAG", "managerAuthorized=$it") }
                } catch (e: Throwable) {
                    Log.e("BakaSU-DIAG", "managerAuthorizationCheckFailed", e)
                    false
                }

                val rawVersion = try {
                    Natives.version.also { Log.i("BakaSU-DIAG", "rawDriverVersion=$it") }
                } catch (e: Throwable) {
                    Log.e("BakaSU-DIAG", "driverVersionCheckFailed", e)
                    null
                }
                val driverResponsive = rawVersion != null && rawVersion > 0
                val diagnosticState = when {
                    driverResponsive && isManager -> "DRIVER_DETECTED_MANAGER_AUTHORIZED"
                    driverResponsive -> "DRIVER_DETECTED_MANAGER_NOT_AUTHORIZED"
                    else -> "DRIVER_NOT_CONFIRMED_BY_NATIVE_API"
                }
                Log.i("BakaSU-DIAG", "diagnosticState=$diagnosticState rawVersion=$rawVersion minimumKernel=${Natives.MINIMAL_SUPPORTED_KERNEL}")
                // Keep upstream feature gates intact until authorization is understood.
                val ksuVersion = if (isManager) rawVersion else null""")
replace("""                val fullVersion = try {
                    Natives.getFullVersion()
                } catch (_: Exception) {
                    "Unknown"
                }""", """                val fullVersion = try {
                    Natives.getFullVersion()
                } catch (e: Throwable) {
                    Log.e("BakaSU-DIAG", "fullVersionCheckFailed", e)
                    "Unknown"
                }.also { Log.i("BakaSU-DIAG", "fullVersion=$it") }""")
replace("                systemStatus = SystemStatus(", """                Log.i("BakaSU-DIAG", "status manager=$isManager driverResponsive=$driverResponsive version=$ksuVersion root=$isRootAvailable requireNewKernel=$requireNewKernel lkm=$lkmMode")
                systemStatus = SystemStatus(""")
replace("""                isCoreDataLoaded = true
            } catch (_: Exception) {
            }""", """                isCoreDataLoaded = true
            } catch (e: Throwable) {
                Log.e("BakaSU-DIAG", "loadCoreDataFailed", e)
            }""")
p.write_text(s)
print("Applied BakaSU Diagnostic v2 (read-only status classification)")
