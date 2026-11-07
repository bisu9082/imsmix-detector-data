#!/usr/bin/env python3
"""Figure: outcome distribution across three detector architectures for the 15
binary mixtures, ordered by consequence to a responder. Style matches
pa/make_fig_rotamer.py (project convention)."""
import csv, math
from collections import Counter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

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

HARM = {"both":"both","partial":"partial","class_alarm_only":"class_only",
        "not_detected":"silent","misID":"misID"}
ORDER = ["both","partial","class_only","silent","misID"]
NICE  = {"both":"Both named","partial":"One named","class_only":"Class alarm only",
         "silent":"No output","misID":"Wrong name"}
# best -> worst, blue through neutral to orange
FILL  = {"both":BLUE, "partial":"#7fb0e4", "class_only":"#cfcdc6",
         "silent":"#f2b394", "misID":ORANGE}
INST  = [("ims_a","IMS-A"),("ims_b","IMS-B"),("dms","DMS")]

rows = list(csv.DictReader(open(_D("failure_mode_coding.csv"),encoding="utf-8-sig")))
n = len(rows)
cnt = {k: Counter(HARM[r[k]] for r in rows) for k,_ in INST}


plt.rcParams.update({"font.family":"DejaVu Sans","font.size":9,
    "axes.edgecolor":MUT,"axes.labelcolor":SEC,"xtick.color":SEC,
    "ytick.color":SEC,"text.color":INK})
fig,(ax1,ax2)=plt.subplots(1,2,figsize=(7.6,3.1),facecolor=SURF,
                           gridspec_kw={"width_ratios":[2.05,1]})
for ax in (ax1,ax2):
    ax.set_facecolor(SURF)
    for s in ("top","right"): ax.spines[s].set_visible(False)

# --- (a) stacked outcome distribution ---
ypos=range(len(INST))
for y,(key,lab) in enumerate(INST):
    left=0
    for c in ORDER:
        v=cnt[key].get(c,0)
        if not v: continue
        ax1.barh(y,v,left=left,height=0.62,color=FILL[c],
                 edgecolor=SURF,linewidth=1.2,zorder=3)
        ax1.text(left+v/2,y,str(v),ha="center",va="center",fontsize=8.5,
                 color="white" if c in ("both","misID") else INK,
                 fontweight="bold",zorder=4)
        left+=v
ax1.set_yticks(list(ypos)); ax1.set_yticklabels([l for _,l in INST])
ax1.invert_yaxis()
ax1.set_xlim(0,n); ax1.set_xticks(range(0,n+1,3))
ax1.set_xlabel(f"Binary mixtures (n = {n})")
ax1.grid(axis="x",color=GRID,lw=0.7,zorder=0); ax1.set_axisbelow(True)
ax1.set_ylim(2.62,-0.62)
ax1.set_title("(a) Outcome by instrument",loc="left",fontsize=9.5,
              color=INK,fontweight="bold",pad=10)

# --- (b) no usable species information ---
BAD={"class_only","silent","misID"}
for y,(key,lab) in enumerate(INST):
    k=sum(cnt[key].get(c,0) for c in BAD)
    p=k/n
    ax2.scatter([p],[y],s=66,color=ORANGE if p>0.5 else BLUE,zorder=4,
                edgecolor=SURF,lw=1.4)
    ha,dx = ("right",-0.035) if p>0.5 else ("left",0.035)
    ax2.text(p+dx,y,f"{k}/{n}",ha=ha,va="center",fontsize=8,color=SEC)
ax2.set_yticks(list(ypos)); ax2.set_yticklabels([]); ax2.set_ylim(2.62,-0.62)
ax2.set_xlim(-0.04,1.04); ax2.set_xticks([0,0.5,1.0])
ax2.set_xticklabels(["0","0.5","1"])
ax2.set_xlabel("Proportion of the 15 mixtures")
ax2.grid(axis="x",color=GRID,lw=0.7,zorder=0); ax2.set_axisbelow(True)
ax2.set_title("(b) No usable species information",loc="left",fontsize=9.5,
              color=INK,fontweight="bold",pad=10)
h=[plt.Rectangle((0,0),1,1,color=FILL[c]) for c in ORDER]
fig.legend(h,[NICE[c] for c in ORDER],loc="lower center",bbox_to_anchor=(0.5,-0.055),
           ncol=5,frameon=False,fontsize=7.8,handlelength=1.2,handleheight=0.9,
           labelcolor=SEC,columnspacing=1.6,handletextpad=0.5)
fig.tight_layout(w_pad=2.0)
_os.makedirs("figures", exist_ok=True)
for ext in ("png","pdf"):
    fig.savefig(f"figures/fig_outcomes.{ext}",dpi=200,facecolor=SURF,
                bbox_inches="tight")
print("-> figures/fig_outcomes.png / .pdf")
