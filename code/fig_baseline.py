#!/usr/bin/env python3
"""Figure 1: single-agent baseline. What each identifying architecture reports
when a single agent is presented, by operating mode. Style follows the project
convention in pa/make_fig_rotamer.py."""
import csv, re
import matplotlib.patheffects as pe
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['hatch.linewidth'] = 0.6
from matplotlib.patches import Rectangle

import os as _os
# resolve the data directory whether run from the working tree
# (data/relabeled/) or from the deposited package (data/)
_HERE = _os.path.dirname(_os.path.abspath(__file__))
def _D(name):
    for base in ("data/relabeled", "data",
                 _os.path.join(_HERE, "..", "data"),
                 _os.path.join(_HERE, "..", "data", "relabeled")):
        p = _os.path.join(base, name)
        if _os.path.exists(p): return p
    raise FileNotFoundError(name)


BLUE, ORANGE = "#2a78d6", "#eb6834"
INK, SEC, MUT, GRID, SURF = "#0b0b0b", "#52514e", "#8a8984", "#e2e1dc", "#fcfcfb"
# Hue alone does not separate every pair in greyscale. Sweeping all pairs of
# legend keys by WCAG relative luminance, six fall below dY = 0.10:
# merge/missed 0.017, oos/seen 0.018, class/oos 0.024, class/seen 0.042,
# match/class 0.066 and match/oos 0.090. Each of those pairs therefore has a hatch on exactly one
# member, and the hatches differ in type rather than only in direction, since
# mirrored diagonals carry the same texture energy. The excluded lewisite
# cells are marked with a cross-hatch and a heavy border rather than dimmed,
# which would map them onto a neighbouring category's colour.
V_FILL = {"match": BLUE, "merge": "#9ec6ef", "class": "#8e8a7d",
          "mismatch": "#8c2d10", "missed": "#c3bfb4", "oos": ORANGE,
          "oos_none": "#eef4f7", "seen": "#7d98a6"}
V_TXT  = {"match": "white", "merge": INK, "class": "white",
          "mismatch": "white", "missed": "#4a4740", "oos": "white",
          "oos_none": "#7b8b95", "seen": "white"}
NICE   = {"match": "Correct name", "merge": "Merged / ambiguous",
          "class": "Class label only", "mismatch": "Name of a different agent",
          "missed": "Not detected", "oos": "Off-list substance,\nagent name returned",
          "oos_none": "Off-list, no output", "seen": "Detected,\nno name recorded"}
ORDER_V = ["match", "merge", "class", "mismatch", "oos", "seen", "missed", "oos_none"]

AGENTS = ["GA","GB","GD","GF","VX","HD","HN3","Lewisite","CK","AC","CG","DPGME","MS"]
GROUPS = [("Nerve",0,5),("Blister",5,8),("Blood / choking",8,11),("Simulants",11,13)]

def short(s):
    s = re.sub(r"\(\s*[\d/]+\s*\)", "", s or "").strip()
    s = s.replace("Lewisite", "Lew").replace(" or ", " / ").replace("; ", " ; ")
    return s or "—"

# ---- IMS-B ----
r3 = list(csv.DictReader(open(_D("table3_imsB_single.csv"), encoding="utf-8-sig")))
imsb = {}
for x in r3:
    raw = x["reported_species"] or ""
    rep = raw.split("(")[0].strip()
    # names actually offered by the instrument, however punctuated
    offered = [t for t in re.split(r"[;/]| or ", re.sub(r"\(\s*[\d/]+\s*\)", "", raw))
               if t.strip()]
    offered = [t.strip() for t in offered]
    # Coding rule as stated in the manuscript Methods, applied in this order:
    #  1. no output                      -> missed
    #  2. only hazard-class labels (TIC) -> class (what the display shows is
    #     tested before the substance's specification status, so that an
    #     off-list substance shown under a class label alone is not counted
    #     as having been given an agent name)
    #  3. substance not on the list      -> oos
    #  4. sole name == the substance     -> match
    #  5. substance among names offered  -> merge
    #  6. otherwise                      -> mismatch (a name that was not the
    #     substance presented). VX-R is NOT aliased to VX: VR / Russian VX is
    #     a distinct agent, so a VX exposure displayed as VX-R falls here.
    CLASS_LABELS = {"TIC"}
    norm = list(offered)
    oos = bool(x.get("spec_footnote"))
    if x["outcome"] != "detected":                  v = "missed"
    elif all(t in CLASS_LABELS for t in norm):      v = "class"
    elif oos:                                       v = "oos"
    elif len(norm) == 1 and norm[0] == x["agent"]:  v = "match"
    elif x["agent"] in norm:                        v = "merge"   # right name, but ambiguous
    else:                                           v = "mismatch"
    imsb[(x["mode"], x["agent"])] = (v, short(x["reported_species"]))

# ---- DMS ----
r4 = list(csv.DictReader(open(_D("table4_dms_single.csv"), encoding="utf-8-sig")))
dms = {}
for x in r4:
    o = x["outcome"]
    # table4 records no species name for the single-agent DMS conditions,
    # so a detection cannot be scored as a correct identification.
    # Specification status is resolved per mode, as for IMS-B.
    if x.get("spec_footnote"):
        v = "oos_none"
    else:
        v = {"detected":"seen","not_detected":"missed"}[o]
    lab = "detected" if o == "detected" else ("—" if o == "not_detected" else "n/a")
    dms[(x["mode"], x["agent"])] = (v, lab)

plt.rcParams.update({"font.family":"DejaVu Sans","font.size":9,
    "axes.edgecolor":MUT,"axes.labelcolor":SEC,"xtick.color":SEC,
    "ytick.color":SEC,"text.color":INK})
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 5.0), facecolor=SURF,
                               gridspec_kw={"width_ratios":[1.32, 1]})

# redundant, non-colour channel for the categories a greyscale or 1-bit
# rendering would otherwise merge
# Hatches differ by TYPE, not by direction: two mirrored diagonals have the
# same texture statistics at legend size and do not separate in greyscale.
# Sparse densities: the label sits in the cell and a dense hatch buries it.
HATCH = {"oos": "///", "oos_none": "///", "merge": "..",
         "seen": "+", "class": "x"}

def panel(ax, data, modes, title, fs):
    ax.set_facecolor(SURF)
    for s in ax.spines.values(): s.set_visible(False)
    for j, a in enumerate(AGENTS):
        for i, m in enumerate(modes):
            if (m, a) not in data:
                raise KeyError(f"no coded outcome for {a} in {m} mode")
            v, lab = data[(m, a)]
            # Lewisite is shown but excluded from the counts. Its cells keep
            # the full category colour -- dimming them shifted them onto a
            # neighbouring category's swatch -- and are marked instead with a
            # grey cross-hatch and border, which no category uses.
            excl = (a == "Lewisite")
            ax.add_patch(Rectangle((i+0.03, j+0.08), 0.94, 0.84,
                         facecolor=V_FILL[v],
                         edgecolor=INK if excl else SURF,
                         lw=1.6 if excl else 1.3,
                         hatch="xxxx" if excl else HATCH.get(v),
                         zorder=3))
            # a halo keeps the label readable where the cell is hatched
            t = ax.text(i+0.5, j+0.5, lab, ha="center", va="center",
                        fontsize=fs, color=V_TXT[v], zorder=4,
                        fontweight="bold" if v in ("match","mismatch")
                        else "normal")
            if v in HATCH:
                t.set_path_effects([pe.withStroke(
                    linewidth=2.2,
                    foreground=V_FILL[v] if v != "excl" else SURF)])
    ax.set_xlim(0, len(modes)); ax.set_ylim(len(AGENTS), 0)
    ax.set_xticks([i+0.5 for i in range(len(modes))])
    ax.set_xticklabels(modes, fontsize=8.5)
    ax.xaxis.set_ticks_position("top"); ax.xaxis.set_label_position("top")
    ax.set_yticks([j+0.5 for j in range(len(AGENTS))])
    # lewisite stock was 67% pure with the balance uncharacterized, so its
    # conditions are shown but excluded from the counts reported in the text
    ax.set_yticklabels([x + "*" if x == "Lewisite" else x for x in AGENTS],
                       fontsize=8.5)
    ax.tick_params(length=0)
    for _, s, e in GROUPS:
        if s: ax.axhline(s, color=MUT, lw=0.9, zorder=5)
    ax.set_title(title, loc="left", fontsize=9.5, color=INK,
                 fontweight="bold", pad=22)

panel(ax1, imsb, ["CWA","STD"], "(a) IMS-B: reported species", 7.3)
panel(ax2, dms,  ["CWA","TIC"], "(b) DMS: detection", 7.8)
ax2.set_yticklabels([])

# group labels on the far left
for name, s, e in GROUPS:
    ax1.text(-0.60, (s+e)/2, name, rotation=90, ha="center", va="center",
             fontsize=7.4, color=MUT)

h = [Rectangle((0,0),1,1, facecolor=V_FILL[v], hatch=HATCH.get(v),
               edgecolor=SURF) for v in ORDER_V]
# tinted, not SURF: filled with the background it collided with the
# "off-list, no output" key at dE00 = 3.5
h.append(Rectangle((0,0),1,1, facecolor="#dcd8cf", hatch="xxxx", edgecolor=INK))
LAB = [NICE[v] for v in ORDER_V] + ["Excluded from counts\n(lewisite, 67% pure)"]
fig.legend(h, LAB, loc="lower center",
           bbox_to_anchor=(0.5,-0.075), ncol=5, frameon=False, fontsize=7.8,
           handlelength=1.2, handleheight=0.9, labelcolor=SEC,
           columnspacing=1.5, handletextpad=0.5)
fig.text(0.5, 0.955, "IMS-A reports no species information in any of its modes "
         "(bar count and hazard class only)", ha="center", fontsize=7.6,
         color=SEC, style="italic")
fig.tight_layout(rect=[0.015, 0.045, 1, 0.945], w_pad=1.4)
_os.makedirs("figures", exist_ok=True)
for ext in ("png","pdf"):
    fig.savefig(f"figures/fig_baseline.{ext}", dpi=200, facecolor=SURF,
                bbox_inches="tight")
print("-> figures/fig_baseline.png / .pdf")
