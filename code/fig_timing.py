#!/usr/bin/env python3
"""Figure 2: how long each instrument took to answer, and how long it took to
return to a no-alarm state. Both bear on a responder's decision and neither is
quantified anywhere else in the paper.

No replicate records were retained, so the markers are the conditions
themselves, not estimates. A median tick is drawn rather than a min-max bar,
because a connector across a spread of conditions reads as an interval
estimate and there is none to show."""
import csv, os, statistics as st
import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

mpl.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.2,
                     "axes.linewidth": 0.8})
BLUE, ORANGE = "#2a78d6", "#eb6834"
INK, SEC, MUT, GRID, SURF = "#0b0b0b", "#52514e", "#8a8984", "#e2e1dc", "#fcfcfb"
TEAL = "#7d98a6"

_H = os.path.dirname(os.path.abspath(__file__))
def _D(n):
    for b in ("data/relabeled", "data", os.path.join(_H, "..", "data", "relabeled"),
              os.path.join(_H, "..", "data")):
        p = os.path.join(b, n)
        if os.path.exists(p): return p
    raise FileNotFoundError(n)
def rows(n): return list(csv.DictReader(open(_D(n), encoding="utf-8-sig")))

SRC = [("IMS-A", "table2_imsA_single.csv", BLUE),
       ("IMS-B", "table3_imsB_single.csv", ORANGE),
       ("DMS",   "table4_dms_single.csv",  TEAL)]

def series(fn, col):
    """(value, flagged) per condition. flagged marks the IMS-A conditions that
    were detected with no bar count displayed; their clear-down sits an order
    of magnitude below the rest and is a different display state, not a
    different speed."""
    out = []
    for r in rows(fn):
        v = (r.get(col) or "").strip()
        if not v: continue
        try: val = float(v)
        except ValueError: continue
        flagged = (r.get("bars", "").strip().strip("'") == "detected_only")
        out.append((val, flagged))
    return out

fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.9), dpi=200)
fig.patch.set_facecolor(SURF)
PANELS = [("detect_time_s", "Time to first report", "a"),
          ("stabilize_s",   "Time to return to the no-alarm state", "b")]

for ax, (col, title, tag) in zip(axes, PANELS):
    ax.set_facecolor(SURF)
    for i, (name, fn, c) in enumerate(SRC):
        vals = series(fn, col)
        y = len(SRC) - 1 - i
        for v, flagged in vals:
            if flagged:
                ax.plot(v, y, "o", ms=4.8, mfc="none", mec=c, mew=1.3, zorder=3)
            else:
                ax.plot(v, y, "o", ms=4.6, mfc=c, mec="white", mew=0.7,
                        alpha=0.85, zorder=3)
        if vals:
            med = st.median([v for v, _ in vals])
            ax.plot([med, med], [y - 0.26, y + 0.26], lw=1.9, color=INK,
                    solid_capstyle="butt", zorder=4)
            lab = f"{med:.1f}"
            ax.text(med, y + 0.40, lab, fontsize=6.6, color=INK,
                    ha="center", va="bottom")
    ax.set_yticks(range(len(SRC)))
    ax.set_yticklabels([f"{n}\n(n = {len(series(f, col))})"
                        for n, f, _ in reversed(SRC)], fontsize=7.6)
    ax.set_xscale("log")
    ax.set_xlabel("seconds (log scale)", fontsize=7.6, color=SEC)
    ax.set_title(title, fontsize=8.4, color=INK, pad=14, loc="left")
    ax.text(-0.19, 1.16, f"({tag})", transform=ax.transAxes,
            fontsize=9.2, fontweight="bold", color=INK)
    ax.set_ylim(-0.6, len(SRC) - 0.1)
    ax.grid(axis="x", color=GRID, lw=0.6, zorder=0)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(MUT)
    ax.tick_params(length=3, colors=SEC)

fig.legend(handles=[
    Line2D([], [], marker="o", ls="none", ms=4.6, mfc=MUT, mec="white",
           label="one substance\u2013mode condition"),
    Line2D([], [], marker="o", ls="none", ms=4.8, mfc="none", mec=MUT, mew=1.3,
           label="detected, no bar count displayed (IMS-A)"),
    Line2D([], [], color=INK, lw=1.9, label="median")],
    loc="lower center", bbox_to_anchor=(0.5, -0.20), ncol=3, frameon=False,
    fontsize=6.9, handletextpad=0.5, columnspacing=1.6)

fig.tight_layout()
os.makedirs(os.path.join(_H, "..", "figures"), exist_ok=True)
for ext in ("png", "pdf"):
    fig.savefig(os.path.join(_H, "..", "figures", f"fig_timing.{ext}"),
                bbox_inches="tight", facecolor=SURF)
print("-> figures/fig_timing.png / .pdf")
