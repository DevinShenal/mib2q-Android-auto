# Genuine Android Auto map zoom research

## Acceptance test

The steering-wheel roller must cause Google Maps or Waze to redraw the map sent
to the Virtual Cockpit with a different geographic scale and coverage. Roads,
labels or geographic area must change because the navigation app changed its map
camera. Cropping, stretching, display scaling, density changes, MMI zoom and the
Audi map's hidden scale do not pass.

## Findings

- Upstream `docs/android-auto/overview.md` says the AA cluster display has no
  zoom command; the roller changes only the hidden Audi map scale. Upstream issue
  #43 reports the same roller behavior on an MHI2Q/AA cluster setup.
- Owner observation: zooming Google Maps on the MMI does not change the VC AA map.
  Direct phone-side camera control of Google Maps or Waze has not been established
  by this repository audit.
- Google’s Android for Cars documentation describes a supported design for a
  **navigation app that implements its own map**: `NavigationTemplate` can draw
  an independent map on the instrument cluster, and its map action strip can
  provide zoom controls. The app can handle pan/scale input and redraw its own map
  surface. This establishes a standards-based avenue for a separate navigation
  app, not a control API for third-party Google Maps or Waze.
- Whether a new app can be distributed, approved and rendered on this specific
  MHI2Q Android Auto host, and whether the steering-wheel roller is exposed in a
  useful way, remain unverified. The docs establish API capabilities for supported
  car hosts, not compatibility with this Audi head unit or this fork.

## Status

**Direct Google Maps/Waze zoom from this MHI2Q fork: blocked / unproven.**
**Separate navigation-app research: technically plausible, host and distribution
compatibility unverified.**

Do not label genuine zoom as working until a controlled vehicle test shows
geographic scale/coverage changes in the VC map itself. Record app/version, phone,
head unit and firmware, selected VC layout, input action, before/after geography,
and whether the same map is independently changing on the MMI.

## Next research steps

1. Confirm the current Android for Cars app eligibility, review and distribution
   requirements from official Android documentation.
2. Determine whether the stock AA host on this MHI2Q exposes the documented
   cluster surface and non-touch input callbacks to a compliant navigation app.
3. If feasible, prototype a tiny independent navigation renderer using an
   authorized map SDK and a public camera/zoom control; prove on a bench/host first.
4. Keep Google Maps and Waze untouched. Do not inject into their processes, infer
   a private protocol from traffic, require root, defeat projection protections,
   or substitute a digital crop for zoom.

## Sources

- Google Android for Cars, [View a map in the cluster](https://developer.android.com/design/ui/cars/guides/app-types/view-map-in-cluster):
  explains the cluster map can be independent and created by the navigation app.
- Google Android for Cars, [Draw maps](https://developer.android.com/training/cars/apps/library/draw-maps):
  documents drawing a map to the app surface and cluster display.
- Google Android for Cars, [Let users interact with your map](https://developer.android.com/training/cars/apps/library/interact-map):
  documents map interactions and zoom actions for supported templates.
- AndroidX, [NavigationTemplate API reference](https://developer.android.com/reference/androidx/car/app/navigation/model/NavigationTemplate):
  documents the navigation template’s pan/zoom callbacks and map action strip.
