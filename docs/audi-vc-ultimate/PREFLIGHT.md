# Read-only preflight and dry-run

This milestone adds a host-side audit tool only. It has no device transport,
mount, copy, config-edit, uninstall or restore code. There is no apply mode.
Never treat a clean report as authorization to install.

## Run it

Prepare three local inputs from a candidate release:

1. A target report captured by a future read-only collector. Include exact platform,
   vehicle, hardware part number, firmware train, MU, receiver/gal hashes, active
   mod ID/version/hash, and path/hash state for all destinations and config backups.
2. A release manifest with one `artifacts` item per staged asset:
   `{"source":"libcarplay_hook.so","sha256":"<64 lowercase hex characters>"}`.
   Hashes must describe the exact candidate files in the package directory.
3. The staged release directory matching the current installer payload names.

Then invoke:

```sh
python3 scripts/audi_vc_preflight.py --dry-run \
  --target-report /path/to/target-report.json \
  --release-manifest /path/to/release-manifest.json \
  --package-dir /path/to/staged-release
```

Exit code 0 means only that the supplied report and candidate plan passed these
host checks. Exit code 2 means blocked or invalid. The tool always prints a plan
including fixed file destinations, config mutations, backup names and conditional
deletions. It never opens a device connection or modifies its inputs.

## Current A5 result

The checked-in example contains only owner-reported facts for the A5 F5,
MHI2Q_ER_AUG22_P5092 / MU1329, part 8W5 035 036 C, Full and Classic layouts,
and the working v1.3.1 baseline. It deliberately has no receiver hashes or
machine-captured active-mod/path inventory. The profile registry marks it
unverified and ineligible. This target must therefore fail closed.

## Known installer risk found by the audit

The current upstream installer removes `NavActiveIgnore.jar`,
`navignore_audi.jar`, and `navignore_vw.jar` if found, without backing them up.
The dry-run requires a read-only inventory proving each is absent; otherwise it
blocks. This is not changed by the host tool. Do not use this tool as a reason to
run the existing installer.

## Limits

This preflight validates only the supplied JSON, package file hashes, path
allowlists and declared operation contract. The report is not authenticated by
the tool; a forged or stale report can produce misleading results. It does not
verify a device filesystem, build QNX binaries, prove a restore on MHI2Q, or
change the upstream installer. The A5 target remains unsupported for installation
until receiver compatibility, active-mod state, config backup/restore and
interruption behavior are reviewed and independently tested.
