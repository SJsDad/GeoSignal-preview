---
layout: default
title: Method
description: Conceptual layout-review workflow and interpretation limits
permalink: /method/
---

# Method

GeoSignal connects layout review and simplified optical visualization. This page explains the user-facing concepts; [Technical Notes]({{ '/notes/' | relative_url }}) develops the standard optical principles.

## 1. Conceptual workflow

Layout → candidate regions → local optical images → contour comparison → human review.

Geometry checks identify locations worth examining. Optical views then help show how nearby shapes affect the selected pattern. The preview does not simulate every point of a full layout.

## 2. Geometry and optical views

Geometry review concerns widths, gaps and surrounding shapes. The optical image describes modeled light intensity; its contour provides a separate view of the selected pattern. Keeping these views together helps distinguish design geometry from predicted image shape.

## 3. Focus and relative dose

Changing focus can alter interference and image contrast. Relative dose changes the modeled exposure relative to a comparison baseline. Focus/dose comparisons are meaningful only within the stated model and acceptance criteria; a threshold contour is not a calibrated resist process.

## 4. Reading the public examples

Use [Demo]({{ '/demo/' | relative_url }}) for the example's wavelength, illumination, units and comparison conditions. Compare the same location across conditions and read shape changes before drawing conclusions from a single width or image.

The public figures are representative illustrations, not universal accuracy or speed benchmarks. Internal implementation, calibration procedures and detailed engineering evaluations are maintained separately.

## 5. Scope and limitations

The preview uses idealized scalar optical concepts and thin binary masks. It does not establish vector/high-NA scanner fidelity, mask-3D scattering, resist chemistry, etch behavior or manufacturing signoff. Layout examples are public or synthetic; no confidential input should be uploaded to the public demo.

## Related pages

* [Demo]({{ '/demo/' | relative_url }})
* [6f simulator]({{ '/simulator/' | relative_url }})
* [Abbe Imaging]({{ '/notes/abbe-imaging/' | relative_url }})
* [Release Notes]({{ '/release-notes/' | relative_url }})
