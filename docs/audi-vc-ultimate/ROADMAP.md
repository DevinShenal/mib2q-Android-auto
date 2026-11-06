# Audi VC Ultimate roadmap

This is a development roadmap, not an installation promise. Work proceeds through
host-testable changes first. In-car tests require a separate explicit owner approval.

## Milestones

1. **Repository foundation** — source baseline, architecture, safety, recovery,
   firmware evidence, test policy and privacy scrubber. Keep changes on a feature
   branch and review through a PR.
2. **Diagnostics and reliability** — define redacted session events and test
   state transitions; reproduce early AA disconnects; compare decoder-yield and
   SIGPIPE behavior with upstream 1.4.1; add bounded recovery only after evidence.
3. **Full / Classic profile quality** — profile schema, validation, explicit
   defaults, safe-area calibration and import/export tests. Do not infer Sport
   support for the target A5.
4. **Recovery and installation safety** — dry-run inventory, exact firmware and
   conflict checks, backups, integrity verification, idempotency and rollback tests.
5. **Genuine zoom research** — independently evaluate supported phone-side
   controls for Google Maps and Waze. Accept only a test showing the app redraws
   different geographic coverage in the VC stream. No crop/scale substitute.
6. **Release readiness** — exact target evidence, host test suite, clean recovery
   test, CarPlay regression, AA Full/Classic checks and reviewed release notes.

## Release gates

- No unknown firmware profile falls through to a nearest-match configuration.
- No public package is built from private `lsd.jxe` or other stock files.
- A candidate build is not called compatible based only on host tests or another
  owner's report.
- Existing v1.3.1 installation stays untouched until replacement validation.
- Any change requiring writing to the car stops for explicit owner approval.
