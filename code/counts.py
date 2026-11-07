#!/usr/bin/env python3
"""Prints every count reported in the Results of the manuscript, from the
deposited single-agent tables, applying the coding rule and precedence stated
in the Methods. Lewisite is excluded from the substance-level counts because
its material was 67% pure with the balance uncharacterized."""
import csv, re, os
from collections import Counter

_HERE = os.path.dirname(os.path.abspath(__file__))
def _D(name):
    for base in ("data/relabeled", "data",
                 os.path.join(_HERE, "..", "data"),
                 os.path.join(_HERE, "..", "data", "relabeled")):
        p = os.path.join(base, name)
        if os.path.exists(p): return p
    raise FileNotFoundError(name)

EXCLUDED = {"Lewisite"}          # non-conforming material, see Methods
CLASS_LABELS = {"TIC"}

def rows(f): return list(csv.DictReader(open(_D(f), encoding="utf-8-sig")))

def names(raw):
    raw = re.sub(r"\(\s*[\d/]+\s*\)", "", raw or "")
    return [t.strip() for t in re.split(r"[;/]| or ", raw) if t.strip()]

def code(r):
    """The Methods precedence, in order."""
    if r["outcome"] != "detected":            return "no output"
    off = names(r["reported_species"])
    # What the display shows is tested before the substance's specification
    # status, so that an off-list substance shown under a hazard-class label
    # alone is not counted as having been given an agent name.
    if all(t in CLASS_LABELS for t in off):   return "class label only"
    if r["spec_footnote"]:                    return "off-list, agent name"
    if len(off) == 1 and off[0] == r["agent"]:return "correct name"
    if r["agent"] in off:                     return "named with a second name"
    return "name of a different agent"

b = [r for r in rows("table3_imsB_single.csv") if r["agent"] not in EXCLUDED]
print("IMS-B, substance-level counts (lewisite excluded)")
for mode in ("CWA", "STD"):
    m = [r for r in b if r["mode"] == mode]
    ins = [r for r in m if not r["spec_footnote"]]
    print(f"  {mode}: {len(ins)} substances within specification")
    for k, v in sorted(Counter(code(r) for r in ins).items()):
        print(f"      {v:>2}  {k}")
    print(f"      {len(m)-len(ins):>2}  off the list "
          f"({', '.join(r['agent'] for r in m if r['spec_footnote'])})")

# mode comparison, on the reported NAMES only (bar counts are not part of the
# identification and are not compared)
byagent = {}
for r in b:
    byagent.setdefault(r["agent"], {})[r["mode"]] = r["reported_species"]
diff = [a for a, d in byagent.items()
        if len(d) == 2 and names(d["CWA"]) != names(d["STD"])]
kind = [a for a in diff
        if all(t in CLASS_LABELS for t in names(byagent[a]["STD"]))
        != all(t in CLASS_LABELS for t in names(byagent[a]["CWA"]))]
print(f"\nMode comparison: {len(byagent)-len(diff)} of {len(byagent)} same, "
      f"{len(diff)} differ ({', '.join(sorted(diff))}), "
      f"{len(kind)} differ in kind ({', '.join(sorted(kind))})")

a = [r for r in rows("table2_imsA_single.csv") if r["agent"] not in EXCLUDED]
nobar = [r for r in a if r["bars"] == "detected_only"]
print(f"\nIMS-A: {len(a)} agent-mode conditions, "
      f"{len(nobar)} detected without a bar count "
      f"({', '.join(r['agent'] for r in nobar)})")
blood = [r for r in a if r["mode"] == "blood"]
sw = [r for r in blood if "switch" in str(r).lower()]
print(f"  blood/choking mode: {len(sw)} of {len(blood)} switched to blister "
      f"({', '.join(r['agent'] for r in sw)})")
oos = [r for r in a if r["spec_detectable"] == "N"]
print(f"  outside specification and alarmed anyway: "
      f"{', '.join(r['mode']+'/'+r['agent'] for r in oos)}")

d = [r for r in rows("table4_dms_single.csv") if r["agent"] not in EXCLUDED]
print("\nDMS (specification resolved per mode, as for IMS-B)")
for mode in ("CWA", "TIC"):
    m = [r for r in d if r["mode"] == mode]
    ins = [r for r in m if not r["spec_footnote"]]
    det = [r for r in ins if r["outcome"] == "detected"]
    print(f"  {mode}: {len(det)} detected of {len(ins)} on this mode's list "
          f"({', '.join(r['agent'] for r in det) or 'none'})")
print("  no species name is recorded for any single-agent DMS condition")

# ---------- IMS-A binary mixtures: the self-switch counts ----------
# table5 holds one row per mixture-mode, so aggregate to the mixture.
bm_rows = rows("table5_imsA_binary.csv")
mixes = {}
for r in bm_rows:
    mixes.setdefault(r["mixture"], []).append(r)
# Substances that present to IMS-A as blister agents. The set is read off
# IMS-A's OWN single-agent data, not from what another instrument named: in
# blood/choking mode presented alone, HD, HN3, Lewisite and MS each triggered
# the self-switch and CK, AC and CG each did not (table2_imsA_single.csv).
# The set is therefore defined by the single-agent conditions and then
# applied to the mixtures, rather than read off the mixture result it is
# used to explain.
BLISTER = ("HD", "HN3", "LEWISITE", "MS")
def _sw(rs):   return any("switch" in (r["note"] or "").lower() for r in rs)
def _lew(name): return "lewisite" in name.lower()
def _blis(name): return any(c.upper() in BLISTER for c in name.split("+"))

sw = [m for m, rs in mixes.items() if _sw(rs)]
print(f"\nIMS-A binary mixtures: {len(sw)} of {len(mixes)} switched to blister mode")
for label, sel in (("all", list(mixes)),
                   ("lewisite-free", [m for m in mixes if not _lew(m)])):
    b_s = sum(1 for m in sel if _blis(m) and _sw(mixes[m]))
    n_n = sum(1 for m in sel if not _blis(m) and not _sw(mixes[m]))
    h_n = sum(1 for m in sel if _blis(m) and not _sw(mixes[m]))
    n_s = sum(1 for m in sel if not _blis(m) and _sw(mixes[m]))
    print(f"  {label} ({len(sel)}): blister+switch {b_s}, none+no-switch {n_n}, "
          f"blister+no-switch {h_n}, none+switch {n_s} "
          f"-> documented trigger accounts for {b_s + n_n} of {len(sel)}")

# ---------- DMS lewisite reports in lewisite-free mixtures ----------
dm = rows("table7_dms_binary.csv")
lew_free = [r for r in dm if not _lew(r["mixture"])
            and "lewisite" in (r["reported_species_conc"] or "").lower()]
print(f"\nDMS: lewisite quantified for {len(lew_free)} mixtures containing none "
      f"({', '.join(r['mixture'] for r in lew_free)})")

# ---------- conditions identified only on a second attempt ----------
second = [r for r in rows("table3_imsB_single.csv")
          if "second" in str(r).lower()]
print(f"\nIMS-B: {len(second)} conditions identified only on a second attempt "
      f"({', '.join(r['mode']+'/'+r['agent'] for r in second)})")
