#!/usr/bin/env python3
"""Generates a visual report comparing body volume calculation models.

Produces graphs, tables, and humanoid figure illustrations that show how
each model behaves across a range of heights and weights.  All output is
saved to the ``report/`` directory as PNG images, and a companion
Markdown document (``REPORT.md``) is written to the repository root.

Usage::

    python generate_report.py
"""

import os
import textwrap

import matplotlib
matplotlib.use("Agg")  # non-interactive backend for headless rendering

import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.patches as mpatches  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402
import numpy as np  # noqa: E402

from human_body_volume import (  # noqa: E402
    get_bmi,
    get_bmi_body_volume,
    get_bmi_category,
    get_brozek_body_volume,
    get_cdda_original_volume,
    get_cdda_simple_brozek_volume,
    get_siri_body_volume,
    get_two_compartment_body_volume,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "report")
REPORT_MD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "REPORT.md")

WEIGHTS = np.arange(30, 201, 5)   # kg
HEIGHTS = np.arange(1.40, 2.11, 0.05)  # m  (reasonable adult range)

GENDER = "male"
AGE = 30

# Colour palette shared across all figures
MODEL_COLORS = {
    "BMI": "#e63946",
    "Brozek": "#457b9d",
    "Siri": "#e9c46a",
    "CDDA Original": "#2a9d8f",
    "CDDA Simple": "#264653",
    "Two-Compartment": "#a855f7",
}

BMI_CATEGORY_COLORS = {
    "Severe thinness": "#1d3557",
    "Moderate thinness": "#457b9d",
    "Mild thinness": "#a8dadc",
    "Normal": "#2a9d8f",
    "Overweight": "#e9c46a",
    "Obese (Class I)": "#f4a261",
    "Obese (Class II)": "#e76f51",
    "Obese (Class III)": "#e63946",
}

# ---------------------------------------------------------------------------
# Helper – compute volume grids
# ---------------------------------------------------------------------------

def _volume_grid(model_fn, weights, heights):
    """Return a 2-D NumPy array of volumes (rows=heights, cols=weights)."""
    grid = np.zeros((len(heights), len(weights)))
    for i, h in enumerate(heights):
        for j, w in enumerate(weights):
            result = model_fn(h, float(w))
            if isinstance(result, dict):
                grid[i, j] = result.get("volume", 0)
            else:
                grid[i, j] = result
    return grid


def _cdda_original_grid(weights, heights):
    """CDDA Original depends only on height."""
    grid = np.zeros((len(heights), len(weights)))
    for i, h in enumerate(heights):
        vol = get_cdda_original_volume(h)
        grid[i, :] = vol
    return grid


# ---------------------------------------------------------------------------
# Figure 1 – Heatmaps for each model
# ---------------------------------------------------------------------------

def make_heatmaps(weights, heights):
    """Generate one heatmap per model: weight on X, height on Y, volume as
    colour intensity.  Saved as ``report/heatmaps.png``."""

    models = {
        "BMI": lambda h, w: get_bmi_body_volume(h, w, GENDER, AGE),
        "Brozek": lambda h, w: get_brozek_body_volume(h, w, GENDER, AGE),
        "Siri": lambda h, w: get_siri_body_volume(h, w, GENDER, AGE),
        "Two-Compartment": lambda h, w: get_two_compartment_body_volume(
            h, w, GENDER
        ),
        "CDDA Simple": lambda h, w: get_cdda_simple_brozek_volume(h, w),
        "CDDA Original": lambda h, w: get_cdda_original_volume(h),
    }

    fig, axes = plt.subplots(2, 3, figsize=(18, 10), constrained_layout=True)
    fig.suptitle(
        "Body Volume (L) by Weight and Height — Six Models",
        fontsize=16,
        fontweight="bold",
    )

    # Common colour range so heatmaps are comparable
    vmin, vmax = 20, 250

    for ax, (name, fn) in zip(axes.flat, models.items()):
        grid = _volume_grid(fn, weights, heights)
        im = ax.imshow(
            grid,
            aspect="auto",
            origin="lower",
            extent=[weights[0], weights[-1], heights[0], heights[-1]],
            vmin=vmin,
            vmax=vmax,
            cmap="viridis",
        )
        ax.set_title(name, fontsize=13, color=MODEL_COLORS[name],
                      fontweight="bold")
        ax.set_xlabel("Weight (kg)")
        ax.set_ylabel("Height (m)")
        fig.colorbar(im, ax=ax, label="Volume (L)", shrink=0.85)

    path = os.path.join(REPORT_DIR, "heatmaps.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


# ---------------------------------------------------------------------------
# Figure 2 – Line plots at fixed heights
# ---------------------------------------------------------------------------

def make_line_plots(weights, heights):
    """For a selection of heights, plot volume vs weight for each model.
    Saved as ``report/line_plots.png``."""

    selected_heights = [1.55, 1.65, 1.75, 1.85, 2.00]

    fig, axes = plt.subplots(1, len(selected_heights), figsize=(22, 5),
                             sharey=True, constrained_layout=True)
    fig.suptitle(
        "Volume vs Weight at Fixed Heights",
        fontsize=16,
        fontweight="bold",
    )

    for ax, h in zip(axes, selected_heights):
        for name, color in MODEL_COLORS.items():
            vols = []
            for w in weights:
                w = float(w)
                if name == "BMI":
                    vols.append(
                        get_bmi_body_volume(h, w, GENDER, AGE)["volume"]
                    )
                elif name == "Brozek":
                    vols.append(
                        get_brozek_body_volume(h, w, GENDER, AGE)["volume"]
                    )
                elif name == "Siri":
                    vols.append(
                        get_siri_body_volume(h, w, GENDER, AGE)["volume"]
                    )
                elif name == "Two-Compartment":
                    vols.append(
                        get_two_compartment_body_volume(h, w, GENDER)
                    )
                elif name == "CDDA Simple":
                    vols.append(get_cdda_simple_brozek_volume(h, w))
                elif name == "CDDA Original":
                    vols.append(get_cdda_original_volume(h))
            ax.plot(weights, vols, label=name, color=color, linewidth=1.5)
        ax.set_title(f"Height = {h:.2f} m", fontsize=11)
        ax.set_xlabel("Weight (kg)")
        if ax is axes[0]:
            ax.set_ylabel("Volume (L)")
        ax.grid(True, alpha=0.3)

    axes[-1].legend(loc="upper left", fontsize=8)
    path = os.path.join(REPORT_DIR, "line_plots.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


# ---------------------------------------------------------------------------
# Figure 3 – BMI classification map
# ---------------------------------------------------------------------------

def make_bmi_classification_map(weights, heights):
    """Colour-coded BMI category map with weight on X and height on Y.
    Saved as ``report/bmi_classification.png``."""

    categories = list(BMI_CATEGORY_COLORS.keys())
    cat_to_idx = {c: i for i, c in enumerate(categories)}
    cmap = matplotlib.colors.ListedColormap(
        [BMI_CATEGORY_COLORS[c] for c in categories]
    )
    bounds = list(range(len(categories) + 1))
    norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)

    grid = np.zeros((len(heights), len(weights)))
    for i, h in enumerate(heights):
        for j, w in enumerate(weights):
            bmi = get_bmi(h, float(w))
            cat = get_bmi_category(bmi)
            grid[i, j] = cat_to_idx[cat]

    fig, ax = plt.subplots(figsize=(14, 7), constrained_layout=True)
    ax.imshow(
        grid,
        aspect="auto",
        origin="lower",
        extent=[weights[0], weights[-1], heights[0], heights[-1]],
        cmap=cmap,
        norm=norm,
        interpolation="nearest",
    )
    ax.set_xlabel("Weight (kg)", fontsize=12)
    ax.set_ylabel("Height (m)", fontsize=12)
    ax.set_title(
        "BMI Classification by Weight and Height",
        fontsize=16,
        fontweight="bold",
    )

    # Legend
    patches = [
        mpatches.Patch(color=BMI_CATEGORY_COLORS[c], label=c)
        for c in categories
    ]
    ax.legend(handles=patches, loc="upper left", fontsize=9,
              title="BMI Category")

    path = os.path.join(REPORT_DIR, "bmi_classification.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


# ---------------------------------------------------------------------------
# Figure 4 – Humanoid figure illustrations
# ---------------------------------------------------------------------------

def _draw_humanoid(ax, bmi_category, bmi_value, height_m, weight_kg):
    """Draw a stylised humanoid silhouette whose proportions reflect the
    BMI category.  Wider torso/limbs for higher BMI classes."""

    # Scale factor: how "wide" the figure appears
    width_scale = {
        "Severe thinness": 0.45,
        "Moderate thinness": 0.55,
        "Mild thinness": 0.70,
        "Normal": 1.0,
        "Overweight": 1.25,
        "Obese (Class I)": 1.50,
        "Obese (Class II)": 1.75,
        "Obese (Class III)": 2.0,
    }.get(bmi_category, 1.0)

    color = BMI_CATEGORY_COLORS.get(bmi_category, "#888888")

    # All coordinates are in a local [0,1]×[0,1] system
    cx = 0.5  # centre-x

    # Head
    head_r = 0.08
    head_y = 0.88
    head = plt.Circle((cx, head_y), head_r, color=color)
    ax.add_patch(head)

    # Torso (rounded rectangle)
    torso_w = 0.16 * width_scale
    torso_h = 0.30
    torso_y = head_y - head_r - torso_h - 0.01
    torso = FancyBboxPatch(
        (cx - torso_w / 2, torso_y),
        torso_w, torso_h,
        boxstyle="round,pad=0.02",
        facecolor=color,
        edgecolor="none",
    )
    ax.add_patch(torso)

    # Arms
    arm_w = 0.04 * width_scale
    arm_h = 0.26
    arm_y = torso_y + torso_h - 0.03
    for sign in (-1, 1):
        arm_x = cx + sign * (torso_w / 2 + arm_w / 2 + 0.01)
        arm = FancyBboxPatch(
            (arm_x - arm_w / 2, arm_y - arm_h),
            arm_w, arm_h,
            boxstyle="round,pad=0.01",
            facecolor=color,
            edgecolor="none",
        )
        ax.add_patch(arm)

    # Legs
    leg_w = 0.05 * width_scale
    leg_h = 0.32
    leg_y = torso_y
    gap = 0.01
    for sign in (-1, 1):
        leg_x = cx + sign * (leg_w / 2 + gap)
        leg = FancyBboxPatch(
            (leg_x - leg_w / 2, leg_y - leg_h),
            leg_w, leg_h,
            boxstyle="round,pad=0.01",
            facecolor=color,
            edgecolor="none",
        )
        ax.add_patch(leg)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")

    ax.text(
        cx, 0.05, f"BMI {bmi_value:.1f}\n{bmi_category}",
        ha="center", va="bottom", fontsize=9, fontweight="bold",
        color=color,
    )
    ax.text(
        cx, 0.0, f"{weight_kg} kg / {height_m:.2f} m",
        ha="center", va="bottom", fontsize=7, color="#555555",
    )


def make_humanoid_figures():
    """Draw humanoid figures for each BMI category, using representative
    height/weight pairs.  Saved as ``report/humanoid_figures.png``."""

    # Representative (height, weight) pairs for each BMI category
    representatives = [
        ("Severe thinness", 1.75, 42),
        ("Moderate thinness", 1.75, 50),
        ("Mild thinness", 1.75, 54),
        ("Normal", 1.75, 65),
        ("Overweight", 1.75, 80),
        ("Obese (Class I)", 1.75, 95),
        ("Obese (Class II)", 1.75, 112),
        ("Obese (Class III)", 1.75, 130),
    ]

    fig, axes = plt.subplots(
        1, len(representatives), figsize=(20, 6), constrained_layout=True,
    )
    fig.suptitle(
        "Humanoid Figures by BMI Classification",
        fontsize=16,
        fontweight="bold",
    )

    for ax, (cat, h, w) in zip(axes, representatives):
        bmi = get_bmi(h, w)
        _draw_humanoid(ax, cat, bmi, h, w)

    path = os.path.join(REPORT_DIR, "humanoid_figures.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


# ---------------------------------------------------------------------------
# Figure 5 – Model comparison at a fixed height
# ---------------------------------------------------------------------------

def make_model_comparison(weights):
    """Bar-chart style comparison of all six models at height = 1.75 m
    for a selection of weights.  Saved as ``report/model_comparison.png``."""

    h = 1.75
    sample_weights = [40, 60, 80, 100, 130, 160, 200]

    fig, ax = plt.subplots(figsize=(14, 7), constrained_layout=True)

    x = np.arange(len(sample_weights))
    bar_width = 0.13

    for i, (name, color) in enumerate(MODEL_COLORS.items()):
        vols = []
        for w in sample_weights:
            if name == "BMI":
                vols.append(
                    get_bmi_body_volume(h, w, GENDER, AGE)["volume"]
                )
            elif name == "Brozek":
                vols.append(
                    get_brozek_body_volume(h, w, GENDER, AGE)["volume"]
                )
            elif name == "Siri":
                vols.append(
                    get_siri_body_volume(h, w, GENDER, AGE)["volume"]
                )
            elif name == "Two-Compartment":
                vols.append(get_two_compartment_body_volume(h, w, GENDER))
            elif name == "CDDA Simple":
                vols.append(get_cdda_simple_brozek_volume(h, w))
            elif name == "CDDA Original":
                vols.append(get_cdda_original_volume(h))
        ax.bar(x + i * bar_width, vols, bar_width, label=name, color=color)

    ax.set_xlabel("Weight (kg)", fontsize=12)
    ax.set_ylabel("Volume (L)", fontsize=12)
    ax.set_title(
        "Model Comparison at Height = 1.75 m",
        fontsize=16,
        fontweight="bold",
    )
    ax.set_xticks(x + bar_width * 2.5)
    ax.set_xticklabels([f"{w} kg" for w in sample_weights])
    ax.legend(fontsize=9)
    ax.grid(axis="y", alpha=0.3)

    path = os.path.join(REPORT_DIR, "model_comparison.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


# ---------------------------------------------------------------------------
# Markdown table
# ---------------------------------------------------------------------------

def generate_comparison_table():
    """Return a Markdown string with a comparison table for selected
    height/weight combinations."""

    selected_heights = [1.50, 1.62, 1.75, 1.85, 2.00]
    selected_weights = [50, 60, 70, 80, 90, 100, 120, 150]

    lines = []
    for h in selected_heights:
        lines.append(f"\n#### Height = {h:.2f} m\n")
        header = (
            "| Weight (kg) | BMI | Category | BMI Vol (L) | Brozek Vol (L) "
            "| Siri Vol (L) | 2-Comp Vol (L) | CDDA Simple (L) "
            "| CDDA Original (L) |"
        )
        sep = "|" + "|".join(["---"] * 9) + "|"
        lines.append(header)
        lines.append(sep)
        for w in selected_weights:
            bmi = get_bmi(h, w)
            cat = get_bmi_category(bmi)
            v_bmi = get_bmi_body_volume(h, w, GENDER, AGE)["volume"]
            v_brz = get_brozek_body_volume(h, w, GENDER, AGE)["volume"]
            v_siri = get_siri_body_volume(h, w, GENDER, AGE)["volume"]
            v_tc = get_two_compartment_body_volume(h, w, GENDER)
            v_cs = get_cdda_simple_brozek_volume(h, w)
            v_co = get_cdda_original_volume(h)
            lines.append(
                f"| {w} | {bmi:.1f} | {cat} | {v_bmi:.1f} | {v_brz:.1f} "
                f"| {v_siri:.1f} | {v_tc:.1f} | {v_cs:.1f} | {v_co:.1f} |"
            )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Write REPORT.md
# ---------------------------------------------------------------------------

def write_report_md(table_md):
    """Write the companion Markdown document."""

    content = textwrap.dedent("""\
    # Body Volume Calculation — Model Comparison Report

    This document compares six body-volume calculation models across a
    range of heights and weights.  All graphs use **weight on the X axis**
    and **height on the Y axis** (where applicable).  The models compared
    are:

    | Model | Inputs | Notes |
    |-------|--------|-------|
    | **BMI** | Height, Weight, Gender, Age | Uses Deurenberg BMI→fat ratio then 4-compartment density |
    | **Brozek** | Height, Weight, Gender, Age | Iterative Brozek body-fat formula |
    | **Siri** | Height, Weight, Gender, Age | Iterative Siri body-fat formula |
    | **Two-Compartment** | Height, Weight, Gender | Direct Siri 1961 two-compartment physics model |
    | **CDDA Simple** | Height, Weight | Empirical density regression for game use |
    | **CDDA Original** | Height only | Cubic height scaling (no weight dependence) |

    All calculations assume a **30-year-old male** unless noted otherwise.

    ---

    ## 1. Volume Heatmaps

    Each panel shows the predicted body volume (litres) as a colour map,
    with weight on the X axis and height on the Y axis.

    ![Heatmaps](report/heatmaps.png)

    **Key observations:**
    - The BMI, Brozek, Siri, and Two-Compartment models produce very
      similar gradients — volume increases with both weight and height.
    - The CDDA Original model shows **horizontal bands** because it
      ignores weight entirely.
    - The CDDA Simple model diverges noticeably at extreme weights.

    ---

    ## 2. Volume vs Weight at Fixed Heights

    Line plots comparing all six models at five representative heights.

    ![Line Plots](report/line_plots.png)

    **Key observations:**
    - All weight-dependent models show a roughly linear relationship.
    - The CDDA Original line is flat (weight-independent).
    - Model agreement is best in the normal weight range (60–90 kg)
      and diverges at extremes.

    ---

    ## 3. BMI Classification Map

    A colour-coded map showing the WHO BMI classification at each
    weight/height combination.

    ![BMI Classification](report/bmi_classification.png)

    ---

    ## 4. Humanoid Figure Illustrations

    Stylised humanoid silhouettes whose body width reflects the BMI
    classification, from *Severe thinness* to *Obese (Class III)*.

    ![Humanoid Figures](report/humanoid_figures.png)

    ---

    ## 5. Model Comparison (Bar Chart)

    Side-by-side bar chart of all six models at height 1.75 m for
    selected weights.

    ![Model Comparison](report/model_comparison.png)

    ---

    ## 6. Detailed Comparison Tables

    The tables below show numerical results for each model at selected
    height/weight combinations.
    """)

    content += "\n" + table_md + "\n"

    with open(REPORT_MD, "w", encoding="utf-8") as fh:
        fh.write(content)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    """Generate all report artefacts."""
    os.makedirs(REPORT_DIR, exist_ok=True)

    print("Generating heatmaps …")
    make_heatmaps(WEIGHTS, HEIGHTS)

    print("Generating line plots …")
    make_line_plots(WEIGHTS, HEIGHTS)

    print("Generating BMI classification map …")
    make_bmi_classification_map(WEIGHTS, HEIGHTS)

    print("Generating humanoid figures …")
    make_humanoid_figures()

    print("Generating model comparison bar chart …")
    make_model_comparison(WEIGHTS)

    print("Generating comparison table …")
    table_md = generate_comparison_table()

    print("Writing REPORT.md …")
    write_report_md(table_md)

    print(f"Done — see {REPORT_MD} and {REPORT_DIR}/")


if __name__ == "__main__":
    main()
