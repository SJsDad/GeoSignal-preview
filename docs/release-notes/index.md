---
layout: default
title: Release Notes
description: Version notes and implementation changes for GeoSignal Preview
permalink: /release-notes/
---

<p class="language-switch"><a href="{{ '/ko/release-notes/' | relative_url }}" lang="ko">한국어로 보기</a></p>

# Release Notes

This section records major implementation changes, evaluation notes, and technical decisions behind **GeoSignal Preview**.

Versions v0.1 through v0.4 are historical milestones reconstructed from the
repository commit history. Detailed benchmark artifacts were not preserved for
every early version, so these pages describe only changes supported by the
source history. v0.5 and later include the more detailed evaluation records
created during development.

General visitors can read [Home]({{ '/' | relative_url }}), [Demo]({{ '/demo/' | relative_url }}), and [Method]({{ '/method/' | relative_url }}) first. These notes are mainly for readers who want to understand how the preview evolved across versions.

## Versions

| Version | Main Focus |
| --- | --- |
| [v0.1]({{ '/release-notes/v0.1/' | relative_url }}) | Initial CLI and SVRF-like geometry-rule experiments |
| [v0.2]({{ '/release-notes/v0.2/' | relative_url }}) | Flask web prototype and layout preview |
| [v0.3]({{ '/release-notes/v0.3/' | relative_url }}) | Modular geometry engine, width/space analysis, and density |
| [v0.4]({{ '/release-notes/v0.4/' | relative_url }}) | Raster, Abbe imaging, contours, and hotspot evaluation |
| [v0.5]({{ '/release-notes/v0.5/' | relative_url }}) | Selectable pya backend comparison beside the existing gdstk path |
| [v0.6]({{ '/release-notes/v0.6/' | relative_url }}) | pya-native geometry path, candidate overview update, and printed metric refinement |
| [v0.7]({{ '/release-notes/v0.7/' | relative_url }}) | Combined review GDS, candidate-specific contours, and bounded-memory imaging |
| [v0.8]({{ '/release-notes/v0.8/' | relative_url }}) | Focus/dose process-window analysis, calibration, and PW artifacts |
| [v0.8.1]({{ '/release-notes/v0.8.1/' | relative_url }}) | Backend-neutral imaging contract and focus/dose performance refactor |
| [v0.9]({{ '/release-notes/v0.9/' | relative_url }}) | Exact Hopkins/TCC/SOCS cross-validation and bounded optical-mode caching |

v0.8.0 and v0.8.1 are tagged application releases. v0.9 records the
completed engineering milestone currently present on the application v0.9
branch; a release tag had not yet been created when this Pages update was
prepared.

## Reading Guide

The public pages keep the main story short:

```text
Home / Demo / Method
    -> what the preview is
    -> what the images show
    -> how to interpret the result

Release Notes
    -> why implementation choices changed
    -> what was compared
    -> what remains limited
```

The notes below are technical records. They are not required to understand the live demo.

## Related Pages

* [Home]({{ '/' | relative_url }})
* [Demo]({{ '/demo/' | relative_url }})
* [Method]({{ '/method/' | relative_url }})
* [Technical Notes]({{ '/notes/' | relative_url }})
