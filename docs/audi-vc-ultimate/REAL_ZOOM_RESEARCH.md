# Genuine Android Auto map zoom research

## Acceptance test

The steering-wheel roller must cause Google Maps or Waze to redraw the map sent
to the Virtual Cockpit with a different geographic scale and coverage. Roads,
labels or geographic area must change because the navigation app changed its map
camera. Cropping, stretching, display scaling, density changes, MMI zoom and the
Audi map's hidden scale do not pass.

## Evidence so far

- Upstream `docs/android-auto/overview.md` states that the AA cluster display has
  no zoom command and that the roller changes only the hidden Audi map scale.
- Upstream issue #43 reports the same roller behavior on an MHI2Q/AA cluster setup.
- Owner observations: MMI Google Maps zoom and VC Android Auto map are independent;
  Waze has not been shown to expose phone-side cluster zoom either.
- No supported or independently validated phone-side control has been established
  in this audit. Therefore the status remains **blocked / unproven**.

## Research boundary

Next, inspect current public Android for Cars and Android Auto projection
documentation, then identify whether any public API sends navigation-camera
controls to a secondary cluster display. Distinguish documented API behavior
from protocol guesses or observations of proprietary app traffic. A separate
navigation app proof of concept is only viable if it has an authorized map SDK,
compliant Android Auto projection path and a testable phone-side camera API.

Do not hook or modify Google Maps/Waze, require root, defeat Android Auto
protections, or ship a digital crop as zoom. Record negative results, test method
and protocol limits before changing the status.
