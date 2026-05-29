# Publisher Visual Source Map

Use this reference when a figure must match a publisher, journal family, conference, thesis handbook, or an external figure-standard source.

## Rule

Do not invent publisher requirements. If a target venue is named and final artwork compliance matters, verify the current official author guide or ask the user to provide/download/screenshot inaccessible material.

If only a default standard is needed, use the conservative local references and report that they are defaults, not venue-specific compliance.

## Source Map

| Source | Use it for | Local references informed |
|---|---|---|
| Nature Research Figure Guide: preparing figures | editable text, standard fonts, 5-7 pt Nature text, axis/tick requirements, RGB, image DPI, scale bars, vector export | `publication-visual-standards.md`, `export-and-editability-standards.md`, `accessibility-and-color-standards.md`, `image-panel-integrity.md` |
| Nature Research Figure Guide: building/exporting panels | 89 mm/183 mm widths, 170 mm height, panel arrangement, accepted vector/layered formats, colour accessibility | `publication-visual-standards.md`, `multi-panel-layout-patterns.md`, `export-and-editability-standards.md` |
| Nature Research Figure Guide: image integrity | non-misleading image processing, original image representation, no generative/image-touchup misuse, gel/raw-image handling | `image-panel-integrity.md`, `ai-image-generation-gate.md` |
| PLOS figure guidelines | TIFF/EPS, 300-600 dpi, 8-12 pt fonts, captions outside image files, image manipulation cautions | `publication-visual-standards.md`, `export-and-editability-standards.md`, `image-panel-integrity.md` |
| Elsevier artwork overview | EPS/PDF/TIFF/JPEG selection, font family whitelist, embedded fonts, file naming | `export-and-editability-standards.md`, `publication-visual-standards.md` |
| IEEE Author Center graphics | vector preference, one/two-column widths, >300 dpi colour/grayscale, >600 dpi line art | `export-and-editability-standards.md`, `publication-visual-standards.md` |
| Springer Nature journal submission guidelines | EPS/TIFF preference, embedded fonts, 0.3 pt line minimum, 1200 dpi line art, 600 dpi combination art, 300 dpi halftone | `publication-visual-standards.md`, `export-and-editability-standards.md` |
| ACM figure descriptions | alt text / figure description separate from captions, plain text, function plus content, short description constraints | `accessibility-and-color-standards.md` |
| SIGACCESS describing figures | practical descriptions for charts, screenshots, flowcharts, architecture diagrams, photos | `accessibility-and-color-standards.md`, `drawio-engineering-diagram-standards.md` |
| JCB figure/video guidelines | 300/600/1000 dpi thresholds, font and line weights, RGB, scale bars, avoid red/green and decorative effects | `publication-visual-standards.md`, `image-panel-integrity.md`, `export-and-editability-standards.md` |
| `nature-figure` design theory and QA contract | Nature-style multi-panel information architecture, semantic palettes, editable SVG, panel anti-redundancy, QA mindset | `multi-panel-layout-patterns.md`, `chart-type-visual-standards.md`, `nature-matplotlib-protocol.md` |

## Verification Links

- Nature preparing figures: `https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/`
- Nature building/exporting panels: `https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/`
- Nature image integrity: `https://research-figure-guide.nature.com/figures/image-integrity/`
- PLOS figures: `https://journals.plos.org/plosone/s/figures`
- Elsevier artwork overview: `https://www.elsevier.com/about/policies-and-standards/author/artwork-and-media-instructions/artwork-overview`
- IEEE resolution and size: `https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-graphics-for-your-article/resolution-and-size/`
- ACM describing figures: `https://authors.acm.org/proceedings/production-information/describing-figures`
- SIGACCESS describing figures: `https://www.sigaccess.org/welcome-to-sigaccess/resources/describing-figures/`
- JCB figure and video guidelines: `https://rupress.org/jcb/pages/fig-vid-guidelines`
- Springer Nature example submission guidelines: `https://link.springer.com/journal/12553/submission-guidelines`
- `nature-figure` design theory: `https://raw.githubusercontent.com/Yuan1z0825/nature-skills/main/skills/nature-figure/references/design-theory.md`
- `nature-figure` QA contract: `https://raw.githubusercontent.com/Yuan1z0825/nature-skills/main/skills/nature-figure/references/qa-contract.md`

## Download Or Screenshot Gate

If a useful example figure, PDF guide, article page, or journal instruction is paywalled, blocked, not text-readable, or requires manual download:

1. Tell the user exactly which item is needed and why.
2. Ask the user to download, attach, or screenshot it.
3. Do not infer detailed visual style from inaccessible material.
4. Use only observable, provided, or publicly accessible content as concrete reference.

For paper examples, only use visible, legally accessible figures or user-provided files. Summarize visual patterns; do not copy figure artwork.
