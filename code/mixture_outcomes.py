#!/usr/bin/env python3
"""Outcome counts and proportions across instruments for the binary-mixture outcomes.

Outcome categories are ordered by consequence to a responder, not by analytical
correctness: the ordering is the precedence used to assign codes, not a
severity ranking: whether a wrong name or a silent display is worse for a
responder is an assumption the omission literature leaves unsettled.
"""
import csv
from collections import Counter

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


SRC = _D("failure_mode_coding.csv")
INST = ["ims_a", "ims_b", "dms"]
LABEL = {"ims_a": "IMS-A", "ims_b": "IMS-B", "dms": "DMS"}

# raw code -> harmonised category
HARM = {"both": "both", "partial": "partial",
        "class_alarm_only": "class_only", "not_detected": "silent",
        "misID": "misID"}
ORDER = ["both", "partial", "class_only", "silent", "misID"]   # precedence order, not a severity ranking

rows = list(csv.DictReader(open(SRC, encoding="utf-8-sig")))
n = len(rows)
obs = {i: [HARM[r[i]] for r in rows] for i in INST}

print(f"binary mixtures n = {n}\n")
print("=== Outcome distribution (ordered by consequence) ===")
hdr = f"{'instr':6s} " + " ".join(f"{c:>10s}" for c in ORDER)
print(hdr); print("-" * len(hdr))
for i in INST:
    c = Counter(obs[i])
    print(f"{LABEL[i]:6s} " + " ".join(f"{c.get(k,0):>10d}" for k in ORDER))

# Proportions are reported as raw fractions. No confidence interval and no
# significance test is given, and the governing reason is the design: with one
# unit of each instrument type there is no replication at the level of the
# inferential unit, so a test over these conditions would treat them as
# replicates of a population the study never sampled. Two further reasons
# apply within that: the 15 mixtures are the complete set of pairs six agents
# allow rather than a sample, and each agent appears in five of them, so the
# units are not independent.

print("\n=== Proportion naming both components ===")
for i in INST:
    k = sum(1 for v in obs[i] if v == "both")
    print(f"{LABEL[i]:6s} {k:2d}/{n}  = {k/n:5.3f}")

print("\n=== Proportion giving no usable species information (silent + class_only + misID) ===")
for i in INST:
    k = sum(1 for v in obs[i] if v in ("silent", "class_only", "misID"))
    print(f"{LABEL[i]:6s} {k:2d}/{n}  = {k/n:5.3f}")
