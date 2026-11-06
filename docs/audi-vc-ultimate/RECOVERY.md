# Recovery and safe-state policy

This document describes development safeguards; it is not an installation guide.
Use the upstream deployment documentation for its documented procedures, and do
not run a development branch on the head unit.

## Before any future approved trial

- Keep the known-working v1.3.1 release and its media available as a rollback reference.
- Record the exact firmware train, MU, hardware part number, mod version and
  diagnostic trouble codes before a change.
- Back up every file a procedure proposes to modify and verify the backup can be read.
- Produce and review a dry-run list of target paths and configuration changes.
- Stop if the detected model, exact firmware, existing mod or file hash is unknown
  or conflicts with the expected profile.
- Collect no private stock binary into the public repository.

## Failure response

1. Stop applying further changes; do not repeatedly reboot or rerun an installer.
2. Preserve logs and identify the last successful step and exact artifact hashes.
3. Restore only from a verified backup using the documented recovery procedure.
4. Compare diagnostics with the recorded baseline; do not assign a pre-existing
   fault such as B2005 to the new build without evidence.
5. If the documented recovery does not apply cleanly, stop and obtain qualified
   head-unit support before further changes.

No recovery procedure can guarantee repair for every interrupted write or
firmware variant. Development builds are not vehicle-ready packages.
