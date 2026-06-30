"""Render the QuantumSafe architecture diagram to docs/architecture.png.

Pure matplotlib (no seaborn, no native SVG libs), so it runs anywhere matplotlib
is installed. The hand-authored vector source lives alongside it as
docs/architecture.svg; this script produces the raster version embedded in the
README.

Usage:  python docs/make_architecture.py
"""

from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

BG = "#070912"
PANEL = "#0b1120"
BOX = "#0e1426"
BOX2 = "#141c30"
STROKE = "#27324d"
CYAN = "#34d6ff"
VIOLET = "#9d7bff"
TXT = "#e8eefc"
SUB = "#8aa0c4"
EDGE = "#5b6b80"

HERE = os.path.dirname(os.path.abspath(__file__))


def box(ax, x, y, w, h, title, sub="", *, fc=BOX, ec=STROKE, accent=False):
    ax.add_patch(
        FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.0,rounding_size=0.12",
            linewidth=1.8 if accent else 1.4,
            edgecolor=CYAN if accent else ec, facecolor=fc, zorder=2,
        )
    )
    ax.text(x + 0.18, y + h - 0.34, title, color=TXT, fontsize=11,
            fontweight="bold", zorder=3, va="top")
    if sub:
        ax.text(x + 0.18, y + h - 0.66, sub, color=SUB, fontsize=8.2,
                zorder=3, va="top")


def arrow(ax, p1, p2, color=EDGE, lw=1.6, style="-|>", rad=0.0):
    ax.add_patch(
        FancyArrowPatch(
            p1, p2, arrowstyle=style, mutation_scale=12, lw=lw,
            color=color, zorder=1,
            connectionstyle=f"arc3,rad={rad}",
        )
    )


def grp(ax, x, y, text):
    ax.text(x, y, text, color=CYAN, fontsize=9.5, fontweight="bold", zorder=3)


def main() -> None:
    fig, ax = plt.subplots(figsize=(13, 8.2))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 26)
    ax.set_ylim(0, 16.5)
    ax.axis("off")

    # Title
    ax.text(0.5, 15.9, "QuantumSafe — System Architecture", color=CYAN,
            fontsize=20, fontweight="bold")
    ax.text(0.5, 15.3, "Attack ➔ Detection ➔ Fix  ·  one shared engine behind three surfaces",
            color=SUB, fontsize=10.5)

    # Entry points
    grp(ax, 0.5, 14.4, "ENTRY POINTS")
    box(ax, 0.5, 12.7, 4.6, 1.4, "CLI", "pip install quantumsafe")
    box(ax, 0.5, 10.9, 4.6, 1.4, "Web dashboard", "static site · vanilla JS")
    box(ax, 0.5, 9.1, 4.6, 1.4, "REST API", "Flask · JWT · API keys")

    # Shared engine panel
    grp(ax, 6.2, 14.4, "SHARED DETECTION ENGINE · cli/ (quantumsafe)")
    ax.add_patch(FancyBboxPatch((6.2, 8.6), 12.4, 5.4,
                 boxstyle="round,pad=0,rounding_size=0.18", linewidth=1.8,
                 edgecolor=VIOLET, facecolor=PANEL, zorder=0))
    box(ax, 6.8, 12.3, 5.4, 1.25, "scanner", "AST (Python) + regex · 11 langs", accent=True)
    box(ax, 12.9, 12.3, 5.1, 1.25, "scorer", "0–100 risk + band", accent=True)
    box(ax, 6.8, 10.6, 5.4, 1.25, "recommender", "NIST / FIPS mapping", accent=True)
    box(ax, 12.9, 10.6, 5.1, 1.25, "reporter", "json·html·sarif·cbom·svg", accent=True)
    box(ax, 9.4, 9.0, 6.0, 1.05, "Findings", "file · line · family · severity", fc=BOX2)

    # internal flow
    arrow(ax, (12.2, 12.9), (12.9, 12.9), CYAN, 1.8)
    arrow(ax, (15.45, 12.3), (15.45, 11.85), CYAN, 1.8)
    arrow(ax, (12.9, 11.2), (12.2, 11.2), CYAN, 1.8)
    arrow(ax, (9.5, 10.6), (10.5, 10.05), CYAN, 1.8)

    # entry -> engine
    arrow(ax, (5.1, 13.4), (6.8, 13.0), EDGE, rad=-0.12)
    arrow(ax, (5.1, 11.6), (6.2, 12.6), EDGE, rad=-0.1)
    arrow(ax, (5.1, 9.8), (6.2, 12.4), EDGE, rad=-0.25)

    # Output + DB
    grp(ax, 19.2, 14.4, "OUTPUT")
    box(ax, 19.2, 12.4, 6.2, 1.6, "Reports", "JSON · HTML · SARIF · CBOM · SVG")
    box(ax, 19.2, 10.4, 6.2, 1.6, "Database", "users · scans · findings (SQLite/PG)")
    arrow(ax, (18.0, 11.2), (19.2, 11.2), EDGE)
    arrow(ax, (15.4, 9.6), (19.2, 12.9), EDGE, rad=-0.2)

    # Companions
    grp(ax, 0.5, 7.7, "RUNNABLE COMPANIONS — justify the ratings & implement the fix (off the request path)")
    box(ax, 0.5, 3.4, 12.0, 3.9, "quantum/  —  the attack", "“why is it vulnerable?”")
    box(ax, 1.0, 5.4, 5.2, 1.0, "shor.py", "breaks RSA / ECC", fc=BOX2)
    box(ax, 6.6, 5.4, 5.4, 1.0, "grover.py", "halves symmetric strength", fc=BOX2)
    box(ax, 1.0, 3.9, 11.0, 1.0, "resources.py", "qubit / depth / gate cost vs RSA-2048", fc=BOX2)

    box(ax, 13.4, 3.4, 12.0, 3.9, "pqc/  —  the fix", "“what do I replace it with?”")
    box(ax, 13.9, 5.4, 5.2, 1.0, "lwe_kem.py", "quantum-safe KEM", fc=BOX2)
    box(ax, 19.5, 5.4, 5.4, 1.0, "benchmark.py", "sizes / latency vs ML-KEM", fc=BOX2)
    box(ax, 13.9, 3.9, 11.0, 1.0, "LWE", "the math behind CRYSTALS-Kyber / ML-KEM (FIPS 203)", fc=BOX2)

    arrow(ax, (10.5, 9.0), (6.5, 7.3), EDGE, rad=-0.15)
    arrow(ax, (15.4, 9.0), (19.0, 7.3), EDGE, rad=0.15)

    # Deployment footer
    ax.add_patch(FancyBboxPatch((0.5, 1.3), 24.9, 1.2,
                 boxstyle="round,pad=0,rounding_size=0.15", linewidth=1.2,
                 edgecolor=STROKE, facecolor=PANEL, zorder=0))
    ax.text(0.9, 1.9,
            "Deploy:  Vercel (frontend)  ─HTTPS/CORS→  Render (Flask API)  →  Render Postgres        ·        "
            "PyPI: quantumsafe CLI  ─sync→  /api/v1/scan/import",
            color=SUB, fontsize=9.2, family="monospace", va="center")

    out = os.path.join(HERE, "architecture.png")
    fig.savefig(out, dpi=150, facecolor=BG, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)
    print(f"wrote {os.path.relpath(out, os.path.dirname(HERE))}")


if __name__ == "__main__":
    main()
