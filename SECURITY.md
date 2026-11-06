# Security policy

Report security-sensitive defects privately to the repository owner through
GitHub's private vulnerability reporting when enabled. Do not post credentials,
VINs, device identifiers, route traces, raw logs, private firmware files or
exploit details in a public issue.

This software modifies head-unit processes and configuration. Use development
artifacts only for code review and host testing. Do not install them on a car.
Public CI must not receive proprietary `lsd.jxe`, `base.jar`, firmware images,
tokens or vehicle captures. Scrub and inspect diagnostics before sharing.

Dependency and artifact hashes should be documented when packages are introduced.
A checksum is an integrity aid, not a signature or proof of trusted provenance.
