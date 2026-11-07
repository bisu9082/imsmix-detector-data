#!/usr/bin/env python3
"""TOC graphic: single-agent exposures in which the naming instrument (IMS-B)
displayed something other than the substance presented. Drawn from the
measured single-agent data (table3_imsB_single.csv); no generative image
tools used. Every substance shown here is off the instrument's list for the mode in
force, so all cells carry Figure 1's off-list orange."""
import csv, re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
def _D(name):
    for base in ("data/relabeled", "data",
                 _os.path.join(_HERE, "..", "data"),
                 _os.path.join(_HERE, "..", "data", "relabeled")):
        p = _os.path.join(base, name)
        if _os.path.exists(p): return p
    raise FileNotFoundError(name)

ORANGE = "#eb6834"
INK, SEC, SURF, GRID = "#0b0b0b", "#52514e", "#fcfcfb", "#d9d8d3"

rows = list(csv.DictReader(open(_D("table3_imsB_single.csv"),
                                encoding="utf-8-sig")))

def names(raw):
    raw = re.sub(r"\(\s*[\d/]+\s*\)", "", raw or "")
    return " ; ".join(t.strip() for t in re.split(r";| or ", raw) if t.strip())

# CWA mode is the mode in which every one of these substances was presented
cwa = {r["agent"]: r for r in rows if r["mode"] == "CWA"}
# only genuinely off-list substances: VX is excluded because VX/VR is a
# mobility degeneracy, not a library failure (see Discussion)
CASES = [("CG",    True),
         ("DPGME", True),
         ("MS",    True)]

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9,
                     "text.color": INK})
fig, ax = plt.subplots(figsize=(3.25, 1.75), facecolor=SURF)
ax.set_facecolor(SURF)
for sp in ax.spines.values(): sp.set_visible(False)
ax.set_xticks([]); ax.set_yticks([]); ax.tick_params(length=0)
ax.set_xlim(0, 1); ax.set_ylim(0, 1)

ax.text(0.0, 0.965, "In the vial", fontsize=6.8, color=SEC, va="center")
ax.text(0.55, 0.965, "On the display", fontsize=6.8, color=SEC, va="center")
ax.text(1.0, 0.965, "CWA mode", fontsize=6.4, color=SEC, va="center",
        ha="right", style="italic")

y0, dy = 0.835, 0.175
for i, (ag, oos) in enumerate(CASES):
    y = y0 - i * dy
    assert oos, f"fig_toc shows off-list substances only; {oos!r}"
    fill = ORANGE
    ax.text(0.0, y, ag, fontsize=8.2, va="center", color=INK,
            fontweight="bold")
    ax.annotate("", xy=(0.53, y), xytext=(0.27, y),
                arrowprops=dict(arrowstyle="-|>", color=GRID, lw=1.1,
                                shrinkA=0, shrinkB=0))
    ax.add_patch(plt.Rectangle((0.55, y - 0.052), 0.45, 0.104,
                               color=fill, zorder=3))
    ax.text(0.775, y, names(cwa[ag]["reported_species"]), fontsize=7.8,
            ha="center", va="center", color="white", fontweight="bold",
            zorder=4)

ax.text(0.0, 0.245, "Not on the list.\nNamed as an agent anyway.",
        fontsize=8.4, fontweight="bold", color=INK, va="center",
        linespacing=1.35)

ax.text(1.0, 0.245, "Nothing on the display\nmarked them as off-list.",
        fontsize=6.8, color=SEC, va="center", ha="right", linespacing=1.3)

fig.subplots_adjust(left=0.02, right=0.99, top=0.97, bottom=0.10)
import os as _os2; _os2.makedirs("figures", exist_ok=True)
fig.savefig("figures/fig_toc.png", dpi=400, facecolor=SURF)
fig.savefig("figures/fig_toc.pdf", facecolor=SURF)
print("-> figures/fig_toc.png / .pdf")
