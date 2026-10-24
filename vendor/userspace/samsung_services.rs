// Retained from BakaSU 239e1e8; Samsung multi-digit parser fix by SysopBP.
// GPL-3.0-or-later. Used only when waitsys cannot become ready.
use std::{collections::HashSet, process::{Command, Output}, thread, time::{Duration, Instant}};
use anyhow::{Context, Result, bail, ensure};
use log::{info, warn};
use regex_lite::Regex;

const SERVICE_PATH: &str = "/system/bin/service";
const GET_SERVICE_PID_TRANSACTION: &str = "1599097156";
const SYSTEM_SERVER_FALLBACK_SERVICES: [&str; 3] = ["activity", "package", "user"];
const SERVICE_POLL_INTERVAL: Duration = Duration::from_millis(200);
const SERVICE_STOP_TIMEOUT: Duration = Duration::from_secs(5);

fn command_stdout(output: Output, description: &str) -> Result<String> {
    ensure!(
        output.status.success(),
        "{description} failed with {}: {}",
        output.status,
        String::from_utf8_lossy(&output.stderr).trim()
    );

    String::from_utf8(output.stdout).with_context(|| format!("{description} output is not UTF-8"))
}

fn parse_service_list(output: &str) -> Result<Vec<String>> {
    let mut lines = output.lines();
    let header = lines.next().context("service list output is empty")?;
    let service_count = header
        .strip_prefix("Found ")
        .and_then(|header| header.strip_suffix(" services:"))
        .context("invalid service list header")?
        .parse::<usize>()
        .context("invalid service count")?;

    let service_pattern = Regex::new(r"^\d+\s+([^\s:]+):\s+\[[^\]]*\]$")?;
    let services = lines
        .filter(|line| !line.trim().is_empty())
        .map(|line| {
            service_pattern
                .captures(line)
                .and_then(|captures| captures.get(1))
                .map(|service| service.as_str().to_owned())
                .with_context(|| format!("invalid service list entry: {line}"))
        })
        .collect::<Result<Vec<_>>>()?;

    ensure!(
        services.len() == service_count,
        "service list declared {service_count} services but contained {}",
        services.len()
    );

    Ok(services)
}

fn parse_service_pid(output: &str) -> Result<u32> {
    let parcel_pattern =
        Regex::new(r"^Result:\s+Parcel\(\s*([0-9A-Fa-f]{8})\s+'[^'\r\n]{4}'\s*\)\s*$")?;
    let Some(pid) = parcel_pattern
        .captures(output)
        .and_then(|captures| captures.get(1))
    else {
        bail!("invalid service PID response: {}", output.trim());
    };

    u32::from_str_radix(pid.as_str(), 16).context("invalid PID in service response")
}

pub fn list_services() -> Result<Vec<String>> {
    let output = Command::new(SERVICE_PATH)
        .arg("list")
        .output()
        .context("failed to execute service list")?;
    let stdout = command_stdout(output, "service list")?;
    parse_service_list(&stdout)
}

pub fn get_service_pid(service: &str) -> Result<u32> {
    let output = Command::new(SERVICE_PATH)
        .args(["call", service, GET_SERVICE_PID_TRANSACTION])
        .output()
        .with_context(|| format!("failed to query service {service}"))?;
    let stdout = command_stdout(output, "service PID query")?;
    parse_service_pid(&stdout)
}

fn is_fallback_service(service: &str) -> bool {
    SYSTEM_SERVER_FALLBACK_SERVICES.contains(&service)
}

fn find_system_server_services<F>(services: Vec<String>, mut get_pid: F) -> Vec<String>
where
    F: FnMut(&str) -> Option<u32>,
{
    let Some(activity_pid) = get_pid("activity") else {
        return services
            .into_iter()
            .filter(|service| is_fallback_service(service))
            .collect();
    };

    services
        .into_iter()
        .filter(|service| {
            if service == "activity" {
                return true;
            }

            get_pid(service).map_or_else(|| is_fallback_service(service), |pid| pid == activity_pid)
        })
        .collect()
}

pub(super) fn collect_system_server_services() -> Result<Vec<String>> {
    let services = list_services()?;
    let system_server_services =
        find_system_server_services(services, |service| match get_service_pid(service) {
            Ok(pid) => Some(pid),
            Err(err) => {
                log::debug!("failed to get PID for service {service}: {err:#}");
                None
            }
        });

    info!(
        "tracking {} system_server services",
        system_server_services.len()
    );
    Ok(system_server_services)
}

fn remaining_services(tracked: &[String], running: &[String]) -> Vec<String> {
    let running: HashSet<&str> = running.iter().map(String::as_str).collect();
    tracked
        .iter()
        .filter(|service| running.contains(service.as_str()))
        .cloned()
        .collect()
}

pub(super) fn wait_for_system_server_services(system_server_services: &[String]) {
    if system_server_services.is_empty() {
        return;
    }

    let deadline = Instant::now() + SERVICE_STOP_TIMEOUT;
    let mut remaining = system_server_services.to_vec();
    let mut list_error_logged = false;

    loop {
        match list_services() {
            Ok(running) => remaining = remaining_services(system_server_services, &running),
            Err(err) if !list_error_logged => {
                warn!("failed to list services while waiting for system_server: {err:#}");
                list_error_logged = true;
            }
            Err(_) => {}
        }

        if remaining.is_empty() {
            info!("system_server services stopped");
            return;
        }

        let remaining_time = deadline.saturating_duration_since(Instant::now());
        if remaining_time.is_zero() {
            warn!(
                "timed out waiting for system_server services to stop: {}",
                remaining.join(", ")
            );
            return;
        }

        thread::sleep(SERVICE_POLL_INTERVAL.min(remaining_time));
    }
}

