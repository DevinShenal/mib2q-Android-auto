# Source and firmware baseline

Audit snapshot: 2026-11-06. Source: the public upstream repository and its GitHub API.

## Revisions inspected

| Ref | Commit | Finding |
| --- | --- | --- |
| `v1.4` | `5c460600c9205cdafa2c4fecd7e2210b8606aedb` | Release tag is annotated and unsigned. Adds MMI CarPlay settings, AA trip details, decoder recovery and other fixes. |
| `master` | `e6ac2b9a4522a97005205b60786d760b8d651b0a` | One commit past v1.4; adds Android Auto main-screen decoder yielding and associated tests/docs. |

The current master changelog proposes 1.4.1 behavior. It says the renderer yield
and `SIGPIPE` handling address early AA drops, while in-car validation remains
pending. Open [issue #48](https://github.com/kamgurgul/mib2q-carplay/issues/48)
therefore remains a reproduction and validation item, not evidence that the fix
is confirmed on the owner's unit. [Issue #19](https://github.com/kamgurgul/mib2q-carplay/issues/19)
records a crash associated with the experimental AA day/night switch; keep that
switch off in any future test plan until isolated testing establishes safety.

## Repository structure and build

The inspected tree has 690 tracked paths. The runtime is split across native
QNX C/C++, Java HMI overlays, deployment scripts and supporting documentation.
`scripts/build_all.sh` orchestrates artifacts; native components use the QNX
6.5 ARMv7 toolchain and Java compilation needs the unit's private `lsd.jxe`
converted to a local stock jar. The stock jar is intentionally absent from the
public repository. Host tests run through `scripts/run_tests.sh` and GitHub
Actions; Java suites needing the private jar remain local.

The original repository is GPL-3.0-or-later with third-party notices. Preserve
those notices and the existing upstream history. Do not add private HMI files,
firmware dumps, logs or car captures to this public fork.

## Owner-specific evidence

| Item | Evidence | Status for this fork |
| --- | --- | --- |
| Audi A5 Sportback F5, 2017 / MY2018 | Owner-provided configuration | Target, not yet tested with this fork |
| `MHI2Q_ER_AUG22_P5092`, MU1329 | Owner-provided version | Exact target; fresh unit readout still required before any deployment decision |
| CarPlay on upstream v1.3.1 | Owner report | Working baseline; preserve installation until a replacement is validated |
| Android Auto on this fork and exact target | No test result | Unknown |
| Full and Classic cluster layouts | Owner reports these are available | Only these may be configured; no Sport profile for this vehicle |
| B2005 invalid data record | Historical owner report | Existing fault; do not attribute it to this fork without before/after evidence |

Reports for P5092/MU1329 elsewhere in the upstream issue tracker do not prove
this branch works on the owner's individual vehicle or phone. The owner's v1.3.1
CarPlay experience does not validate a later build or Android Auto.

## Evidence-graded feature matrix

| Capability | Grade | Basis / next evidence |
| --- | --- | --- |
| Existing upstream CarPlay functions | Supported upstream; owner-reported on v1.3.1 | Regression-test against retained setup before considering replacement |
| Existing upstream AA cluster video and route overlays | Supported on listed upstream profiles; unverified on this fork's target | Exact P5092/MU1329 smoke test on isolated setup |
| 1.4.1 decoder yield and SIGPIPE recovery | Experimental | Host tests exist; in-car validation pending upstream |
| Full and Classic geometry presets for this A5 | Future work | Capture safe-area screenshots/test grids from this vehicle |
| Sport layout on this A5 | Not supported / do not expose | Vehicle does not offer Sport layout |
| Genuine Google Maps or Waze geographic zoom from wheel roller | Blocked / unproven | No demonstrated phone-side API or cluster zoom command |
| Digital crop, scale or renderer zoom | Explicitly excluded | Changes pixels, not map geography |
