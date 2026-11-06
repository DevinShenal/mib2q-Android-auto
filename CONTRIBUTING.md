# Contributing

## Workflow

- Keep changes focused on a feature branch and open a pull request against `master`.
- Preserve upstream GPL and third-party notices; retain origin attribution when
  modifying upstream files.
- Add host tests for behavior changes and describe tests that cannot run without
  the private stock HMI jar or actual head unit.
- Never include private stock HMI files, proprietary firmware, raw vehicle logs,
  route data, VINs, MACs or user identifiers.
- Do not state a firmware combination is compatible without exact evidence.
- Do not add digital cropping or scaling under a geographic-zoom feature name.

## Local checks

Run `sh scripts/run_tests.sh`. Java suites that require the private stock jar are
run locally and must not upload that jar to CI. For diagnostics, run
`python3 -I tests/test_diagnostic_scrubber.py` and inspect only synthetic fixtures.

## Vehicle testing

Changes that write to a real unit require explicit owner approval, a clean dry-run,
exact firmware detection, verified backups and a documented rollback path. CI and
review do not substitute for that approval or for supervised vehicle validation.
