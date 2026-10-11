from pathlib import Path
p=Path("manager/app/src/main/java/com/sukisu/ultra/ui/viewmodel/HomeViewModel.kt")
s=p.read_text()
def replace(a,b):
    global s
    if s.count(a)!=1:
        raise SystemExit(f"Expected one source match, got {s.count(a)}: {a[:100]!r}")
    s=s.replace(a,b,1)
replace("import android.content.Context\n","import android.content.Context\nimport android.util.Log\n")
replace("""                val isManager = try {
                    Natives.isManager
                } catch (_: Exception) {
                    false
                }

                val ksuVersion = if (isManager) Natives.version else null""","""                // Read-only diagnostic: preserve the original authorization decision.
                val isManager = try {
                    Natives.isManager.also { Log.i("BakaSU-DIAG", "native isManager=$it") }
                } catch (e: Throwable) {
                    Log.e("BakaSU-DIAG", "native isManager failed", e)
                    false
                }

                val rawVersion = try {
                    Natives.version.also { Log.i("BakaSU-DIAG", "native version=$it") }
                } catch (e: Throwable) {
                    Log.e("BakaSU-DIAG", "native version failed", e)
                    null
                }
                Log.i("BakaSU-DIAG", "minimumKernel=${Natives.MINIMAL_SUPPORTED_KERNEL}; root authorization independent")
                val ksuVersion = if (isManager) rawVersion else null""")
replace("""                val fullVersion = try {
                    Natives.getFullVersion()
                } catch (_: Exception) {
                    "Unknown"
                }""","""                val fullVersion = try {
                    Natives.getFullVersion()
                } catch (e: Throwable) {
                    Log.e("BakaSU-DIAG", "native fullVersion failed", e)
                    "Unknown"
                }.also { Log.i("BakaSU-DIAG", "native fullVersion=$it") }""")
replace("                systemStatus = SystemStatus(","                Log.i(\"BakaSU-DIAG\", \"status manager=$isManager version=$ksuVersion root=$isRootAvailable requireNewKernel=$requireNewKernel lkm=$lkmMode\")\n                systemStatus = SystemStatus(")
replace("""                isCoreDataLoaded = true
            } catch (_: Exception) {
            }""","""                isCoreDataLoaded = true
            } catch (e: Throwable) {
                Log.e("BakaSU-DIAG", "loadCoreData failed", e)
            }""")
p.write_text(s)
print("Applied diagnostic changes")
