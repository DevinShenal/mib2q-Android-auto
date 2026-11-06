# Test matrix

| Area | Host test | Isolated / car evidence required | Current status |
| --- | --- | --- | --- |
| Diagnostic scrubbing | Unit tests for identifier, location, line-ending and CLI behavior | Review sanitized preview before any sharing | Initial scrubber tests pass locally |
| Build and static checks | Existing `scripts/run_tests.sh` and Actions workflow | QNX build/runtime check | Upstream host workflow exists; fork CI pending this branch |
| AA reliability | Event-sequence, decoder-yield and SIGPIPE tests | Cold boot, early connect, sustained drive; preserve logs before recovery | Upstream 1.4.1 host fix exists; car test pending |
| CarPlay regression | Existing route/render/installer tests | Verify v1.3.1 behavior on exact target before any replacement | Owner reports v1.3.1 CarPlay working; fork not tested |
| Full layout | Profile/config/geometry validation | Screenshot grid, route/no-route, call, sleep/wake and infotainment restart | Not tested on this fork |
| Classic layout | Profile/config/geometry validation | Screenshot grid, route/no-route, call, sleep/wake and infotainment restart | Not tested on this fork |
| Sport layout | Feature-detection guard | Do not test or expose on target unless the vehicle reports it | Not available on target |
| Google Maps / Waze geographic zoom | Protocol/API review and harness | Confirm actual map coverage changes in the phone-generated VC stream | Not demonstrated; no fake zoom shipped |
| Recovery | Dry-run, backup integrity and restore simulation | Owner-approved, supervised validation on the target | Not implemented yet |

Host tests cannot establish a firmware profile, decoder stability, or safe
installation on a vehicle. The private stock jar is not placed in CI.
