# Audi VC Ultimate architecture

## Baseline

This workstream is based on the existing `mib2q-carplay` fork at upstream commit
`e6ac2b9a4522a97005205b60786d760b8d651b0a`. It preserves the original source tree,
commit history, GPL-3.0-or-later notices, and upstream relationship. See
[`BASELINE.md`](BASELINE.md) for the source audit and exact firmware evidence.

## Existing runtime components

| Component | Role | Main risk boundary |
| --- | --- | --- |
| `java_patch/` and `java_resources/` | HMI class overrides; Android Auto events, cluster state and route data | Must be built against the owner's private `lsd.jxe`; never commit it |
| `hook/` | iAP2 interception, route-guidance and vehicle data | Runs in the stock `dio_manager` process |
| `aa_hook/` | Android Auto cluster stream and navigation translation | Injected into the stock `gal` process; receiver profiles are firmware-specific |
| `altscreen_hook/`, `altscreen_render/` | Cluster-map stream interception and decode | Shares head-unit video/decoder resources with the main display |
| `maneuver_render/`, `common/` | Virtual Cockpit maneuver overlay and display support | Geometry and graphics lifecycle depend on the actual cluster/firmware |
| `deploy/`, `mods/` | Startup, installer, settings and recovery scripts | Can modify head-unit files/configuration; never run on-car from CI |
| `scripts/`, `tests/`, `.github/workflows/` | Builds, host checks and CI | Host tests are not proof of in-car safety or compatibility |

The fork's first independent tool is the host-side diagnostic scrubber at
`scripts/diagnostic_scrubber.py`. It reads text and prints a sanitized preview;
it has no upload, filesystem mutation, vehicle connection, or installation code.

## Change boundaries

1. Keep changes in focused feature branches and preserve upstream history.
2. Do not add proprietary firmware, stock HMI classes, OEM libraries, credentials,
   vehicle logs, VINs, routes, or captured device identifiers.
3. Treat `gal`, `libautoreceiver.so`, MU train and cluster geometry as separate
   compatibility inputs. Unknown profiles fail closed.
4. No user-facing release or car-ready claim without hardware evidence for the
   exact profile and a reviewed recovery path.
5. Genuine map zoom is a separate research track. Rendering transformations do
   not count as geographic zoom.

## Upstream relationship

`kamgurgul/mib2q-carplay` is the upstream. Keep `master` aligned for syncs and
put fork work on feature branches. General fixes should be proposed upstream
only after the fork change has evidence, compatible licensing, and a focused
patch.
