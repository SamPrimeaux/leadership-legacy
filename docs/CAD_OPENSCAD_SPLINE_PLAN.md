# CAD, OpenSCAD, GLB, and Spline Plan

Connor’s unique advantage is the overlap between engineering/CAD and AI systems.

## OpenSCAD

Use OpenSCAD for:

```txt
parametric CAD generation
scripted mechanical parts
STL generation
technical demos
engineering configurators
CAD-to-video workflows
```

Suggested repo folders:

```txt
cad/
cad/openscad/
cad/templates/
cad/outputs/
cad/metadata/
```

Suggested R2 prefixes:

```txt
assets/models/
snapshots/cad/
exports/cad/
```

Production warning:

```txt
Never execute untrusted OpenSCAD scripts without sandboxing.
```

## GLB / 3D Models

Use GLB files for:

```txt
product demos
technical hero visuals
dashboard previews
case study media
CAD-to-video pipelines
```

Store metadata in CMS:

```txt
cms_assets.asset_type = model
cms_assets.usage_context = hero_3d | case_study | cad_demo
```

## Spline

Spline can be used for:

```txt
homepage hero scene
AI network visual
engineering workflow animation
product demo scene
```

CMS fields:

```txt
visual_type
visual_url
visual_embed_url
fallback_image_url
reduced_motion_fallback
```

Performance rules:

```txt
lazy-load 3D
use static fallbacks
disable heavy animation for reduced motion
do not load Spline on every route by default
```
