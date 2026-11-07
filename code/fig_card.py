#!/usr/bin/env python3
"""Figure S1: a one-page field card condensing the practice recommendations
into a form usable at a tailgate briefing. No new data; every line is drawn
from the Implications section of the main text."""
import os
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

INK, SEC, SURF = "#1a1a18", "#5c5a54", "#fcfcfb"
BLUE, ORANGE, RED = "#2a78d6", "#eb6834", "#8c2d10"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7.6})

BLOCKS = [
    (BLUE, "BEFORE YOU DEPLOY", [
"Carry your instrument's list of nameable substances, per mode.",
        "Know it in both directions: off-list material can be named as an\n"
        "agent, and a listed agent can be missed.",
        "A locally built card from issue simulants finds the first failure.\n"
        "It cannot find the second — you do not hold the listed agents.",
        "Re-run the card after any firmware or library update, after\n"
        "calibration or depot service, and at a fixed review interval.",
        "If the card finds a failure, it goes to the manufacturer and the\n"
        "national equipment authority — not just the unit briefing pack.",
    ]),
    (ORANGE, "READING THE DISPLAY", [
        "Read the MODE off the display, not off what you selected.\n"
        "An instrument may switch itself; if it has, re-select the\n"
        "abandoned mode and re-read before excluding that class.",
        "Record EVERY name shown, including intermittent second names,\n"
        "and set the interim posture by the most protective of them.",
        "A class label is not an identification: no agent-specific\n"
        "antidote, no exposure history. An alarm on material outside the\n"
        "instrument's specification carries no warrant for the class it\n"
        "shows. Set posture from the most protective class the source\n"
        "information allows.",
    ]),
    (RED, "ACTING ON IT", [
        "A reading MAY RAISE protection on its own.\n"
        "A reading MAY NEVER LOWER it on its own.",
        "Extending a decontamination boundary is a separate decision —\n"
        "it commits people, water and casualty movement. Incident\n"
        "commander decides, on review, not on the display.",
        "NO ALARM IS NOT CLEARANCE. Absence of an alarm never by itself\n"
        "authorizes unmasking or the release of a space.",
        "Two instruments agreeing is not orthogonal confirmation if both\n"
        "separate by mobility. Confirm with a different principle.",
    ]),
    ("#7a5aa6", "RUNNING AN EXERCISE", [
        "Issue simulants raise AUTHENTIC-AGENT alarms on these units.\n"
        "Brief control, safety, evaluators, medical and decon first.",
        "Notify real detection assets and fixed monitoring in writing:\n"
        "simulant, quantity, location, time window.",
        "Agree a real-world break phrase and a named control contact.\n"
        "An alarm inconsistent with the scripted simulant, or outside\n"
        "the notified place or window, IS REAL until control says not.",
        "Purge and verify a return to the no-alarm state, by name,\n"
        "before the instrument goes back on the vehicle.",
    ]),
    ("#6b7f3a", "IF THE DISPLAY SAYS CK", [
        "A CK report does not by itself exclude a lung-damaging agent.\n"
        "[Rests on ONE off-list report, one unit, CWA mode only,\n"
        "carryover not excluded. The actions below are safe either way.]",
        "Picture CONVINCING for cyanide — abrupt collapse, seizure or\n"
        "apnoea, profound lactic acidosis without airway or pulmonary\n"
        "findings — cyanide measures proceed WITHOUT DELAY.",
        "Reasonable under diagnostic uncertainty: high-flow oxygen,\n"
        "sodium thiosulfate, hydroxocobalamin where carried.",
        "Otherwise WITHHOLD NITRITES — convincing, not merely displayed.\n"
        "A nitrite given for a lung-damaging agent adds\n"
        "methaemoglobinaemia to impaired gas exchange.",
        "Observe exposed people across the latent interval: 24 h. Shorten\n"
        "to 8 h only if FREE OF SIGNS AND SYMPTOMS and the chest film is\n"
        "clear. THE LOCAL MEDICAL AUTHORITY SETS THE FINAL FIGURE.\n"
        "Responders who were in the plume too.",
        "Enforce rest once they are out of the hazard area and under\n"
        "medical control: litter the default, no self-ambulation, no\n"
        "stairs. Self-rescue from the plume comes first; at mass-casualty\n"
        "scale apply by triage priority rather than abandon it.",
    ]),
]

# Layout is measured from the renderer rather than guessed, in two passes:
# the first measures every block at a nominal canvas size, the second sizes
# the canvas so the taller column fits and redraws. Without the second pass
# a block added later silently overruns the footer.
FS, HFS = 7.9, 9.6
GAP, AFTER_HEAD, AFTER_BLOCK = 0.016, 0.020, 0.030
HEAD_H = 0.040
# Three columns on an A4-landscape canvas, so the card prints at its native
# size on one sheet and still rotates into the SI text block near 1:1.
TOP, BOT, W = 0.880, 0.075, 0.285
COLX = (0.032, 0.357, 0.682)
WIDTH_IN = 11.69
# Bullets are stored unwrapped and re-wrapped to the column, so the card can
# be re-shaped without re-breaking every line by hand.
WRAP = 58
BLOCKS = [(c, h, [textwrap.fill(" ".join(t.split()), WRAP) for t in items])
          for c, h, items in BLOCKS]


def build(height_in, measure_only=False):
    fig = plt.figure(figsize=(WIDTH_IN, height_in), dpi=200)
    fig.patch.set_facecolor(SURF)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    fig.canvas.draw()
    R = fig.canvas.get_renderer()
    H = fig.get_size_inches()[1] * fig.dpi

    def h_of(txt, fs):
        t = ax.text(0, -5, txt, fontsize=fs, linespacing=1.42, wrap=False)
        bb = t.get_window_extent(renderer=R); t.remove()
        return bb.height / H

    def block_h(items):
        return (HEAD_H + AFTER_HEAD
                + sum(h_of(it, FS) + GAP for it in items) + AFTER_BLOCK)

    hs = [block_h(b[2]) for b in BLOCKS]
    # balance across three columns, blocks kept in order
    best, cuts = None, (1, 2)
    for a in range(1, len(hs) - 1):
        for b in range(a + 1, len(hs)):
            cols = (sum(hs[:a]), sum(hs[a:b]), sum(hs[b:]))
            d = max(cols) - min(cols)
            if best is None or d < best:
                best, cuts = d, (a, b)
    a, b = cuts
    groups = (BLOCKS[:a], BLOCKS[a:b], BLOCKS[b:])
    tallest = max(sum(hs[:a]), sum(hs[a:b]), sum(hs[b:]))
    if measure_only:
        plt.close(fig)
        return tallest

    ax.text(0.5, 0.982, "HAND-HELD CHEMICAL DETECTOR \u2014 FIELD CARD",
            ha="center", va="top", fontsize=15, fontweight="bold", color=INK)
    ax.text(0.5, 0.943,
            "What the reading can and cannot settle. Derived from one unit of "
            "each of three fielded types; build your own card for the unit you "
            "carry.", ha="center", va="top", fontsize=8.0, color=SEC)

    for x0, blocks in zip(COLX, groups):
        y = TOP
        for color, head, items in blocks:
            ax.add_patch(FancyBboxPatch((x0, y - HEAD_H), W, HEAD_H,
                         boxstyle="round,pad=0.003,rounding_size=0.006",
                         facecolor=color, edgecolor="none"))
            ax.text(x0 + 0.014, y - HEAD_H / 2, head, va="center",
                    fontsize=HFS, fontweight="bold", color="white")
            y -= HEAD_H + AFTER_HEAD
            for it in items:
                hh = h_of(it, FS)
                ax.add_patch(Rectangle((x0 + 0.006, y - hh), 0.0034, hh,
                             facecolor=color, edgecolor="none"))
                ax.text(x0 + 0.020, y, it, va="top", ha="left",
                        fontsize=FS, color=INK, linespacing=1.42)
                y -= hh + GAP
            y -= AFTER_BLOCK

    ax.plot([0.032, 0.968], [BOT] * 2, lw=0.8, color="#d8d6d0")
    ax.text(0.5, BOT - 0.014,
            "Record with every reading: displayed name(s) \u00b7 instrument type "
            "\u00b7 mode read off the display \u00b7 who read it \u00b7 clear-down time.   "
            "Mark it as a detector reading, not an identification.\n"
            "If a name is later retracted, the correction travels the original "
            "path and reaches every facility that took a casualty, within the "
            "shift.\nOff-list naming is a hypothesis from three cases on one "
            "unit, carryover not excluded; every action above is written to be "
            "safe either way.",
            ha="center", va="top", fontsize=7.4, color=SEC, linespacing=1.55)
    return fig


# pass 1: measure at a nominal height, then solve for the height at which the
# taller column exactly fills TOP-BOT; iterate once because the fractions move
h = 7.0
for _ in range(6):
    need = build(h, measure_only=True)
    target = h * need / (TOP - BOT)
    if abs(target - h) < 0.02:
        break
    h = target
fig = build(h)
print(f"canvas {WIDTH_IN} x {h:.2f} in")

os.makedirs("figures", exist_ok=True)
for ext in ("png", "pdf"):
    fig.savefig(f"figures/fig_card.{ext}", facecolor=SURF, bbox_inches="tight")
print("-> figures/fig_card.png / .pdf")
