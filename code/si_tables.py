#!/usr/bin/env python3
"""Generates Tables S1-S5 of the Supporting Information as LaTeX, directly
from the deposited CSVs, so the tabulated data and the machine-readable
deposit cannot drift apart. Writes manuscript/si_tables.tex."""
import csv, os
_HERE = os.path.dirname(os.path.abspath(__file__))
def _D(n):
    for b in ("data/relabeled", "data", os.path.join(_HERE, "..", "data"),
              os.path.join(_HERE, "..", "data", "relabeled")):
        p = os.path.join(b, n)
        if os.path.exists(p): return p
    raise FileNotFoundError(n)
def rows(n): return list(csv.DictReader(open(_D(n), encoding="utf-8-sig")))

def esc(t):
    t = (t or "").strip()
    if not t: return ""
    for a, b in (("&", r"\&"), ("%", r"\%"), ("_", r"\_"), ("#", r"\#"),
                 (">=", r"$\geq$")):
        t = t.replace(a, b)
    return t

EMPTY_CELL_NOTE = (r"{\footnotesize An empty cell means no value was recorded "
                   r"for that condition.\par}")

def table(num, caption, head, body, spec, note=None):
    """longtable, not table: these run past one page and a float would be
    silently truncated rather than broken across pages."""
    hd = " & ".join(head) + r" \\"
    o = [r"{\footnotesize\setstretch{1.05}",
         f"\\begin{{longtable}}{{{spec}}}",
         f"\\caption{{{caption}}}\\label{{tab:S{num}}}\\\\",
         r"\toprule", hd, r"\midrule", r"\endfirsthead",
         r"\multicolumn{%d}{l}{\footnotesize\itshape Table \thetable\ (continued)}\\" % len(head),
         r"\toprule", hd, r"\midrule", r"\endhead",
         r"\midrule\multicolumn{%d}{r}{\footnotesize\itshape continued on next page}\\" % len(head),
         r"\endfoot", r"\bottomrule", r"\endlastfoot"]
    o += [" & ".join(r) + r" \\" for r in body]
    o.append(r"\end{longtable}")
    if note: o.append(f"\\vspace{{-0.6em}}\n{{\\footnotesize {note}\\par}}")
    if any(c.strip() == "" for r in body for c in r):
        o.append(EMPTY_CELL_NOTE)
    o.append("}")
    return "\n".join(o)

out = []

# S1 -- IMS-A single agent
b = [[esc(r["mode"]), esc(r["agent"]), esc(r["detect_time_s"]),
      esc(r["bars"]), esc(r["stabilize_s"]), esc(r["spec_detectable"]),
      esc(r["note"])] for r in rows("table2_imsA_single.csv")]
out.append(table(1, "IMS-A, single-agent conditions. Bar count is the "
    "instrument's own intensity indicator; it reports no species name in any "
    "of its modes. \\emph{Spec.} is whether the substance is on the "
    "instrument's specification list (Table~S5).",
    ["Mode", "Substance", "Detect (s)", "Bars", "Stabilize (s)", "Spec.",
     "Operator note"], b,
    "llrlrlp{3.6cm}",
    "Lewisite conditions are shown but excluded from the counts reported in "
    "the main text; see S1.1."))

# S2 -- IMS-B single agent
b = [[esc(r["mode"]), esc(r["agent"]), esc(r["detect_time_s"]),
      esc(r["stabilize_s"]), esc(r["reported_species"]), esc(r["outcome"]),
      "off-list" if r["spec_footnote"] else "listed",
      ("2nd" if r["repeat_mark"] else "") + ("*" if r["confidence"] == "med" else ""),
      esc(r["note"])] for r in rows("table3_imsB_single.csv")]
out.append(table(2, "IMS-B, single-agent conditions, by operating mode. "
    "\\emph{Reported species} is the display verbatim, with the instrument's "
    "intensity figure in parentheses where one was shown.",
    ["Mode", "Substance", "Detect (s)", "Stab.\\ (s)", "Reported species",
     "Outcome", "Spec.", "Flag", "Operator note"], b,
    "llrrlllcp{2.6cm}",
    "\\mbox{VX-R} is the display's designation for VR; it is not aliased to "
    "VX in the coding. See S2. \\emph{Flag}: 2nd, identified only on a second "
    "attempt; *, reading recorded at medium confidence."))

# S3 -- DMS single agent
b = [[esc(r["mode"]), esc(r["agent"]), esc(r["detect_time_s"]),
      esc(r["stabilize_s"]), esc(r["conc_mg_m3"]), esc(r["outcome"]),
      "off-list" if r["spec_footnote"] else "listed",
      esc(r["source_mark"])] for r in rows("table4_dms_single.csv")]
out.append(table(3, "DMS, single-agent conditions. No species name is "
    "recorded for any single-agent DMS condition; a detection is therefore "
    "coded as a detection without an identification.",
    ["Mode", "Substance", "Detect (s)", "Stab.\\ (s)",
     "Conc.\\ (\\si{\\milli\\gram\\per\\cubic\\metre})",
     "Outcome", "Spec.", "Source"], b, "llrrrllp{2.2cm}"))

# S4 -- per-condition outcome codes
b = [[esc(r["instrument"]), esc(r["mode"]), esc(r["substance"]),
      esc(r["displayed"]), esc(r["in_specification"]),
      esc(r["outcome_code"]), esc(r["counted"])]
     for r in rows("single_agent_outcome_coding.csv")]
out.append(table(4, "Per-condition outcome codes for the two instruments "
    "that are coded: IMS-B, whose codes are produced by the decision chain in "
    "S2 as implemented in \\texttt{counts.py}, and DMS, whose codes apply the "
    "two further distinctions stated in S2 and were assigned by hand. IMS-A "
    "returns no species name and is not coded. \\emph{Counted} marks the "
    "conditions included in the counts reported in the main text.",
    ["Instrument", "Mode", "Substance", "Displayed", "In spec.", "Outcome code",
     "Counted"], b, "lllllll"))

# S5 -- specification lists
b = [[esc(r["instrument"]), esc(r["mode"]), esc(r["substance"]),
      esc(r["listed"])] for r in rows("instrument_specification_lists.csv")]
out.append(table(5, "The specification list of each instrument, by operating "
    "mode where the instrument's list differs between modes and as a single "
    "list for the instrument whose does not. Transcribed from the "
    "manufacturer documentation held with each unit.",
    ["Instrument", "Mode", "Substance", "Listed"], b, "llll"))

# write next to the manuscript when run from the working tree, else here
_m = os.path.join(_HERE, "..", "manuscript")
dest = os.path.join(_m if os.path.isdir(_m) else ".", "si_tables.tex")
open(dest, "w").write("\n\n".join(out) + "\n")
print(f"-> {os.path.normpath(dest)}  ({len(out)} tables)")
