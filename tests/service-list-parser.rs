#[test]
fn real_service_list_with_indices_9_10_and_100() {
    let mut input = String::from("Found 101 services:\n");
    for index in 0..101 {
        let name = match index {
            9 => "activity".to_owned(),
            10 => "IntelligentBatterySaverService".to_owned(),
            100 => "android.hardware.boot.IBootControl/default".to_owned(),
            _ => format!("service{index}"),
        };
        input.push_str(&format!("{index}\t{name}: [example.IService]\n"));
    }
    let services = parse_service_list(&input).unwrap();
    assert_eq!(services.len(), 101);
    assert_eq!(services[9], "activity");
    assert_eq!(services[10], "IntelligentBatterySaverService");
    assert_eq!(services[100], "android.hardware.boot.IBootControl/default");
}

#[test]
fn samsung_entry_and_empty_interface_descriptor() {
    let input = "Found 2 services:\n10\tPkgPredictorService: [com.samsung.android.ipm.IIpmManager]\n100\tactivity: []\n";
    assert_eq!(parse_service_list(input).unwrap(), vec!["PkgPredictorService", "activity"]);
}

#[test]
fn malformed_entries_and_count_mismatch_still_fail() {
    for input in [
        "", "Found nope services:\n", "Found 1 services:\n",
        "Found 1 services:\nx\tactivity: []\n",
        "Found 1 services:\n10\tactivity []\n",
        "Found 1 services:\n10\tactivity: [] garbage\n",
    ] {
        assert!(parse_service_list(input).is_err(), "accepted {input:?}");
    }
}
