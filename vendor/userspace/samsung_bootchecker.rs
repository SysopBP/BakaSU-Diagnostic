// Samsung soft-reboot preflight. Do not stop, patch, or spoof bootchecker.
// GPL-3.0-or-later.
use std::{path::Path, process::Command, thread, time::{Duration, Instant}};

const WAIT_LIMIT: Duration = Duration::from_secs(90);
const POLL_INTERVAL: Duration = Duration::from_millis(250);

#[derive(Debug, Default)]
struct Snapshot {
    monitor: String,
    platform_complete: String,
    android_complete: String,
    animation: String,
    updatable_crashing: String,
    attempting_reboot: String,
    recovery_reboot: String,
}

fn is_true(value: &str) -> bool {
    matches!(value, "1" | "true")
}

fn ready(state: &Snapshot) -> Result<bool, String> {
    if is_true(&state.updatable_crashing)
        || is_true(&state.attempting_reboot)
        || is_true(&state.recovery_reboot)
    {
        return Err("Samsung crash recovery is already pending; soft reboot refused".into());
    }
    Ok(state.monitor == "stopped"
        && state.platform_complete == "1"
        && state.android_complete == "1"
        && state.animation == "stopped")
}

fn property(name: &str) -> Result<String, String> {
    let output = Command::new("/system/bin/getprop").arg(name).output()
        .map_err(|e| format!("cannot read {name}: {e}"))?;
    if !output.status.success() {
        return Err(format!("getprop {name} failed: {}", output.status));
    }
    Ok(String::from_utf8_lossy(&output.stdout).trim().to_owned())
}

fn snapshot() -> Result<Snapshot, String> {
    Ok(Snapshot {
        monitor: property("init.svc.bootchecker")?,
        platform_complete: property("dev.platform_bootcomplete")?,
        android_complete: property("sys.boot_completed")?,
        animation: property("init.svc.bootanim")?,
        updatable_crashing: property("sys.init.updatable_crashing")?,
        attempting_reboot: property("dev.attempting_reboot")?,
        recovery_reboot: property("crashrecovery.attempting_reboot")?,
    })
}

fn wait_with(
    mut read: impl FnMut() -> Result<Snapshot, String>,
    mut expired: impl FnMut() -> bool,
    mut pause: impl FnMut(),
) -> Result<(), String> {
    loop {
        let state = read()?;
        if ready(&state)? {
            return Ok(());
        }
        if expired() {
            return Err(format!("Samsung bootchecker did not finish within 90s; soft reboot refused: {state:?}"));
        }
        pause();
    }
}

pub fn wait_for_safe_boot() -> Result<(), String> {
    if !Path::new("/system/bin/bootchecker").is_file() {
        return Ok(());
    }
    // Only apply to the Samsung service contract verified in the captured RC.
    let rc = std::fs::read_to_string("/system/etc/init/bootchecker.rc")
        .map_err(|e| format!("cannot inspect Samsung bootchecker service: {e}"))?;
    if !rc.contains("service bootchecker /system/bin/bootchecker")
        || !rc.contains("dev.platform_bootcomplete")
    {
        return Err("unrecognized Samsung bootchecker service; soft reboot refused".into());
    }
    let deadline = Instant::now() + WAIT_LIMIT;
    wait_with(snapshot, || Instant::now() >= deadline, || thread::sleep(POLL_INTERVAL))
}

#[cfg(test)]
mod tests {
    use super::*;
    fn completed() -> Snapshot {
        Snapshot { monitor: "stopped".into(), platform_complete: "1".into(),
            android_complete: "1".into(), animation: "stopped".into(), ..Default::default() }
    }
    #[test]
    fn completed_android_does_not_bypass_running_bootchecker() {
        let mut state = completed();
        state.monitor = "running".into();
        assert!(!ready(&state).unwrap());
        state.monitor = "restarting".into();
        assert!(!ready(&state).unwrap());
    }
    #[test]
    fn requires_both_completion_signals_and_animation_exit() {
        assert!(ready(&completed()).unwrap());
        let mut state = completed(); state.platform_complete = "0".into();
        assert!(!ready(&state).unwrap());
        let mut state = completed(); state.android_complete = "0".into();
        assert!(!ready(&state).unwrap());
        let mut state = completed(); state.animation = "running".into();
        assert!(!ready(&state).unwrap());
    }
    #[test]
    fn recovery_takes_priority_over_completed_boot() {
        let mut state = completed(); state.updatable_crashing = "1".into();
        assert!(ready(&state).is_err());
        let mut state = completed(); state.attempting_reboot = "true".into();
        assert!(ready(&state).is_err());
        let mut state = completed(); state.recovery_reboot = "true".into();
        assert!(ready(&state).is_err());
    }
    #[test]
    fn waits_for_monitor_to_exit() {
        let mut reads = 0;
        let mut pauses = 0;
        wait_with(|| { reads += 1; let mut state = completed();
            if reads < 3 { state.monitor = "running".into(); } Ok(state)
        }, || false, || pauses += 1).unwrap();
        assert_eq!(reads, 3);
        assert_eq!(pauses, 2);
    }
    #[test]
    fn timeout_refuses_to_proceed() {
        assert!(wait_with(|| Ok(Snapshot::default()), || true, || panic!("must not sleep")).is_err());
    }
    #[test]
    fn read_error_refuses_to_proceed() {
        assert!(wait_with(|| Err("getprop failed".into()), || false, || panic!("must not sleep")).is_err());
    }
}
