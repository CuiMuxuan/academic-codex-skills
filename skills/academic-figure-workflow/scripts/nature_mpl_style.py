"""Shared Matplotlib defaults for Nature-grade academic figures.

Import this helper from project-specific plotting scripts instead of rewriting
rcParams, palette choices, panel labels, and export settings each time.
"""

from __future__ import annotations

from pathlib import Path

MM_PER_INCH = 25.4
SINGLE_COLUMN_MM = 89
DOUBLE_COLUMN_MM = 183
MAX_HEIGHT_MM = 170

WONG_PALETTE = {
    "black": "#000000",
    "orange": "#E69F00",
    "sky_blue": "#56B4E9",
    "bluish_green": "#009E73",
    "yellow": "#F0E442",
    "blue": "#0072B2",
    "vermillion": "#D55E00",
    "reddish_purple": "#CC79A7",
    "grey": "#7A7A7A",
}

DEFAULT_ROLE_COLOURS = {
    "control": WONG_PALETTE["black"],
    "treatment": WONG_PALETTE["blue"],
    "comparison": WONG_PALETTE["orange"],
    "model": WONG_PALETTE["bluish_green"],
    "uncertainty": WONG_PALETTE["grey"],
    "negative": WONG_PALETTE["vermillion"],
    "positive": WONG_PALETTE["bluish_green"],
    "highlight": WONG_PALETTE["reddish_purple"],
}


def mm_to_inches(width_mm: float, height_mm: float) -> tuple[float, float]:
    return width_mm / MM_PER_INCH, height_mm / MM_PER_INCH


def nature_rcparams() -> dict:
    return {
        "figure.dpi": 300,
        "savefig.dpi": 450,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
        "savefig.transparent": False,
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 6,
        "axes.labelsize": 6,
        "axes.titlesize": 6,
        "xtick.labelsize": 5,
        "ytick.labelsize": 5,
        "legend.fontsize": 5,
        "axes.linewidth": 0.5,
        "xtick.major.width": 0.5,
        "ytick.major.width": 0.5,
        "xtick.major.size": 2.5,
        "ytick.major.size": 2.5,
        "lines.linewidth": 1.0,
        "lines.markersize": 3.0,
        "patch.linewidth": 0.5,
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "axes.grid": False,
        "legend.frameon": False,
    }


def apply_nature_style(matplotlib_module) -> None:
    matplotlib_module.rcParams.update(nature_rcparams())


def figure_size(column: str = "single", height_mm: float | None = None) -> tuple[float, float]:
    width_mm = DOUBLE_COLUMN_MM if column == "double" else SINGLE_COLUMN_MM
    if height_mm is None:
        height_mm = width_mm * 0.62
    height_mm = min(height_mm, MAX_HEIGHT_MM)
    return mm_to_inches(width_mm, height_mm)


def style_axes(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(direction="out")


def add_panel_label(ax, label: str, x: float = -0.18, y: float = 1.08) -> None:
    ax.text(
        x,
        y,
        label,
        transform=ax.transAxes,
        fontsize=8,
        fontweight="bold",
        va="top",
        ha="left",
    )


def save_nature_figure(fig, output_stem: str | Path, png_dpi: int = 450) -> dict[str, str]:
    stem = Path(output_stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    paths = {
        "svg": str(stem.with_suffix(".svg")),
        "pdf": str(stem.with_suffix(".pdf")),
        "png": str(stem.with_suffix(".png")),
    }
    fig.savefig(paths["svg"])
    fig.savefig(paths["pdf"])
    fig.savefig(paths["png"], dpi=png_dpi)
    return paths
