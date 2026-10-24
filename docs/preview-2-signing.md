# Preview 2 release candidates

Branch: release/preview-2. Push builds artifacts only; no release or tag is created.

The release branch requires repository secrets KITSUSU_KEYSTORE (base64 keystore),
KITSUSU_KEY_ALIAS and KITSUSU_KEYSTORE_PASSWORD, and repository variable
KITSUSU_CERT_SHA256 (64 hex characters: SHA256 of the DER certificate).
Use the existing permanent KitsuSU signing identity if available. Do not rotate
it without recording the effect on APK upgrades and manager authorization.
Never paste keys or passwords into issues, chat, source files or artifacts.

Preparation exports the public certificate, validates its pinned hash, and gives
all eight driver builds that certificate size/hash. APK signing restores the
same secret privately and checks its certificate against the preparation output.
Only the public certificate is uploaded on release branches. Driver binaries
are embedded into ksud and the final manager APK is checked byte-for-byte against
that daemon. Final APK signature and package identity are validated in CI.

For this preview the manager retains the phone-tested debug build variant with
a release-optimized daemon. Permanent signing does not turn it into a production
release variant; the existing application-debuggable validation remains explicit.
A switch to a release manager variant requires a separate device acceptance test.

SusFS jobs are skipped on the release preparation branch. The optional SusFS
candidate remains run 40059969066, source 8ab4500, with separate feature validation.

FragX stages libksud.so from the selected installed manager. Its embedded DFRoot
bootstrap modules are different from the KitsuSU drivers bundled inside ksud.
Install and reroot with the complete selected package pair before acceptance.

Confirmed maintainer firmware: SM-S948U1, Android 17,
samsung/m3quew/m3q:17/CP2A.260605.016/S948U1UEU4BZID_OYM4BZID:user/release-keys,
security patch 2026-09-05,
kernel 6.12.69-android16-6-pee899be-abogkiS948USQU4BZID-4k.
Root and soft reboot reported working; this is not a per-feature SusFS pass.

## Reported working devices

Galaxy S23 Ultra, S25 Ultra, S26 Ultra, Fold 8, and Tab 11 / Tab 11 Pro
(exact tablet model to be confirmed). S23 Ultra success confirmed by the
maintainer on 2026-10-24; exact variant and firmware not recorded.
Tablet root was reported working; soft reboot still requires separate acceptance.
These are FragX/KitsuSU reports, not per-feature SusFS verification or blanket
support for every firmware. No successful S24 Ultra test is recorded here.
