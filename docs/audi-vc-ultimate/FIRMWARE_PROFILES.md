# Firmware profiles and compatibility evidence

Profile selection must require an exact recognized receiver and firmware match;
do not apply a nearest profile when detection is incomplete. The AA cluster hook
depends on `libautoreceiver.so`; the companion `gal` build and object layouts may
also matter. A matching symbol address alone is not full ABI proof.

| Profile | Public upstream evidence | Target fork evidence |
| --- | --- | --- |
| MU0918 receiver baseline | Built-in upstream AA receiver profile | Not tested on owner unit |
| MU1316 / P5152-associated `gal` | Upstream reports and source profile | Not the owner's reported software train |
| MU1329 / P5092, part `8W5 035 036 C` | External reports for upstream releases; not this fork/vehicle instance | Owner target; fresh readout and controlled validation still required |
| Unknown `gal` / receiver | Upstream crash guard exists for certain untested builds | Fail closed; preserve stock AA behavior |

The owner reports Full and Classic Virtual Cockpit layouts and no Sport layout.
Profile detection must expose only observed layouts. Do not set a default based
on an assumed cluster geometry. Before any test, capture firmware train, MU,
receiver hashes and the head-unit part number, with identifiers scrubbed.
