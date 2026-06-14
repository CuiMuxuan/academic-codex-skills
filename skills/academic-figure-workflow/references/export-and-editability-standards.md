# Export And Editability Standards

Use this reference before exporting, packaging, or calling a figure submission-ready.

## Format Selection

| Figure content | Preferred source | Preferred export | Notes |
|---|---|---|---|
| Plot, line art, schematic, architecture, workflow | script, SVG, or Draw.io | SVG and PDF/EPS | Preserve editable text, strokes, arrows, and symbols. |
| DOCX thesis insertion draft | SVG or PDF source plus PNG preview | PNG preview plus editable source | Keep the editable source even if Word receives raster output. |
| Photograph or microscopy plate | original image plus layout source | TIFF or high-quality PNG/JPEG as required | Keep crop, scale bar, and processing notes. |
| Mixed raster/vector figure | layout source with embedded original raster | PDF/EPS/SVG plus raster export if required | Confirm embedded bitmap resolution at final size. |
| Journal portal requiring raster | editable source plus submission raster | TIFF/JPEG/PNG per venue | Raster export is not a replacement for editable source. |

Never treat a screenshot as a final source for a plot, diagram, or table-like figure.

## Editable Text And Fonts

- Keep text editable in SVG/PDF/EPS unless the venue explicitly requires outlines.
- For Matplotlib, set `svg.fonttype = "none"` and `pdf.fonttype = 42`.
- For Matplotlib, use a final-size `figsize` and avoid resizing the figure later in Word, PowerPoint, or LaTeX unless the final text size is rechecked.
- Export a PNG preview for visual QA before packaging final vector files.
- Embed fonts in PDF/EPS when required by the target venue.
- Use standard fonts such as Arial, Helvetica, Times, Courier, or Symbol when a publisher restricts font families.
- Inspect exported vector files when possible. If text becomes paths unexpectedly, rerun export before final delivery.

## Raster Resolution

Use final physical size, not arbitrary DPI inflation. Increasing the DPI metadata after export does not repair low-resolution source elements.

Conservative defaults:

| Artwork type | Default minimum |
|---|---|
| Halftone/photo | 300 dpi |
| Combination image with text or line art | 500-600 dpi |
| Line art raster | 800-1200 dpi |
| PLOS-like all-figure requirement | 300-600 dpi |
| Nature-like images | at least 450 dpi for image content; extended data may have different constraints |

When the venue specifies a maximum resolution or file size, obey it and report the tradeoff.

## Colour, Crop, And File Hygiene

- Use RGB unless the venue guide requires another colour space.
- Crop tightly to the figure area; do not leave hidden or off-canvas data.
- Use tight bounding boxes carefully: they should remove blank margins without clipping panel labels, axis labels, legends, or colorbars.
- Keep one editable source file per figure and one export packet per intended use.
- Name files so the figure number, short topic, and source/export role are unambiguous.
- Do not place caption text, figure number/title, article title, or author names inside the image file unless a target template specifically requires it.
- For Draw.io figures, keep and report the `.drawio` source path even when the manuscript receives SVG, PDF, PNG, or DOCX output.
- When a user has manually edited a Draw.io source, preserve that source as the style baseline and avoid regenerating it unless redraw is explicitly requested.

## Export Packet

For each generated figure, report:

```text
Editable source:
Draw.io source, if applicable:
Vector exports:
Raster preview/submission exports:
Rendered QA preview:
Final size:
DOCX/PDF insertion preview checked: yes/no
Font/editability status:
DPI or vector status:
Colour space:
Caption/legend location:
Figure-internal text removed or retained:
Unresolved export risks:
```

## Source Basis

This standard consolidates public export guidance from Nature, PLOS, Elsevier, IEEE, Springer Nature, and JCB-style journal artwork pages. Exact journal instructions override these defaults.
