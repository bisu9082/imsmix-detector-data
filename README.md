# Detector response data: three fielded chemical detectors, single agents and binary mixtures

Measurement data supporting the manuscript *"When a Training Simulant Is Named
as the Agent: Library and Mode Effects on Fielded Hand-Held Chemical Warfare
Agent Detectors"* (Kim & Kang).

Measurements were made in September 2026 at the CBRN Defense Research
Institute, ROK CBRN Defense Command, a laboratory designated by the OPCW for
the analysis of authentic environmental samples. That designation covers the
accredited scope and the holding of Schedule 1 materials; it does not extend
to this work, which lies outside the accredited scope and was done without
the records that scope requires.

## What is here

| File | Contents |
|---|---|
| `data/table2_imsA_single.csv` | IMS-A, single-agent exposure: mode, detection time, bar count, stabilization time, whether the agent is on the specified list |
| `data/table3_imsB_single.csv` | IMS-B, single-agent exposure: mode, detection time, **species reported**, stabilization time, outcome, out-of-spec flag, repeat marker, note |
| `data/table4_dms_single.csv` | DMS, single-agent exposure: mode, detection time, reported concentration, stabilization time, outcome |
| `data/instrument_specification_lists.csv` | What each instrument is specified to detect, by operating mode |
| `data/single_agent_outcome_coding.csv` | The outcome code for each IMS-B and DMS single-agent condition. IMS-B is coded by the decision chain in `code/counts.py`; the two DMS-specific codes are an addition to that chain and were assigned by hand; IMS-A returns no species name and is not coded, with the display, the specification status and whether it enters the counts |
| `data/table5_imsA_binary.csv` | IMS-A, binary mixtures (16, including the simulant pair DPGME+MS) |
| `data/table6_imsB_binary.csv` | IMS-B, 15 binary mixtures |
| `data/table7_dms_binary.csv` | DMS, 15 binary mixtures |
| `data/failure_mode_coding.csv` | The 15 agent pairs with a coded mixture outcome per detector. Scope note: this file covers the agent pairs only, not the 16th IMS-A condition (the simulant pair DPGME+MS), and it carries no mode-switch column. The two VX mixtures are coded `partial` because the display returned VX-R, which the Methods rule treats as the name of a different agent; an earlier revision coded them `both`. A `delta_volatility_rank` column that was never documented has been removed. The mixture claims in the paper are derived from `table5_imsA_binary.csv`, not from this file, which exists to drive `mixture_outcomes.py` and `fig_outcomes.py` |
| `data/agent_class.csv` | Agent to hazard-class mapping |
| `code/counts.py` | Prints every count reported in the paper's Results, including the binary mode-switch breakdowns and the second-attempt conditions |
| `code/mixture_outcomes.py` | Counts and proportions for the binary mixtures, which the paper does not report (no kappa; see Statistics) |
| `code/fig_baseline.py` | Figure 1 |
| `code/fig_outcomes.py` | Binary-mixture outcomes; not a figure in the paper |
| `code/single_vs_mixture.py` | Per-agent comparison of single-agent and mixture results |
| `code/vapor_ratio.py` | Pure-component vapor-pressure ratio for each mixture, and the two saturation concentrations quoted in SI S3 |
| `code/fig_toc.py` | Table-of-contents graphic |
| `code/fig_card.py` | Figure 3, the one-page field card |
| `code/fig_timing.py` | Figure 2, time to first report and time to clear down |
| `data/transcription_audit.csv` | The nine adjudicated items of the transcription audit reported in SI S1.3, anonymised and translated |
| `code/si_tables.py` | Regenerates Tables S1--S5 of the Supporting Information from these CSVs |
| `LICENSE` | CC BY 4.0 for the data, MIT for the code |

## Conventions

- **Detectors** are designated `IMS-A`, `IMS-B` and `DMS` by instrument type.
  Commercial model names are not given, and no file, column or variable in
  this package identifies a model.
- **Agents** use standard designations: GA, GB, GD, GF, VX (nerve); HD, HN3,
  lewisite (blister); CK, AC (blood); CG (choking). `DPGME` (dipropylene
  glycol monomethyl ether) and `MS` (methyl salicylate) are training simulants.
- **Lewisite is excluded from the substance-level counts in the paper** (the
  material was 67% pure with an uncharacterized balance). Anyone recomputing
  from these files without applying that exclusion will get different
  denominators; `code/counts.py` applies it.
- **`VX-R`** in `table3` is the designation the instrument itself displayed
  for a VX exposure. VR (Russian VX) is a distinct agent, not a synonym for
  VX, so this is coded throughout as the name of a *different* agent, not as
  naming VX. No VR was presented at any point in the campaign.
- **`TIC`** in `table3` is a hazard-class label with no species name, and is
  counted as a class alarm rather than as an incorrect name.
- **Specification status is mode-dependent** and is taken from
  `instrument_specification_lists.csv`. Phosgene is the case that matters:
  it is *not* on IMS-B's CWA list, but it *is* on that instrument's TIC list,
  so it is out of specification in CWA mode and within specification in STD
  mode. The two CG rows in `table3` are coded accordingly.
- **Modes** differ by instrument: IMS-A uses hazard-class modes (nerve,
  blister, blood); IMS-B uses CWA and STD; DMS uses CWA and TIC. All binary
  mixtures were run in CWA mode on IMS-B and DMS.
- **Outcome codes** in `failure_mode_coding.csv`: `both` (both components
  named), `partial` (one named), `class_alarm_only`, `not_detected`, `misID`
  (a name returned that was not present).
- Empty cells mean the condition was not measured in that mode, not a zero.
- Operator notes are given in English. They are translations of the Korean
  annotations in the source record; the originals are held by the laboratory.

## Limitations of these data

- Exposure was to uncontrolled vapor above an open vial inside a fume hood
  with a face velocity of about 1.5 m/s. This is **not** a saturated or
  equilibrated headspace: the hood sweeps the vapor continuously. No
  concentration was set or measured, so no limit of detection, calibration or
  sensitivity follows from any value here. Because sampling was close to the
  source and sustained for tens of seconds, these are favourable conditions
  rather than representative field conditions.
- Each condition was measured at least five times. *Where a name was
  returned* it was stable across the repetitions of that condition, but
  secondary names were not, and for four conditions the primary name was not
  present throughout: four
  conditions are marked as identified only on a second attempt, and in STD
  mode VX was accompanied by a second nerve-agent name in a minority of
  readings. The individual replicate records were not retained, so this rests
  on the recollection of the operators and cannot be documented from these
  files. Every value here is a single campaign
  representative and **no dispersion can be computed**. Response and
  clear-down times should not be compared across conditions.
- No clean-air blank was recorded as a condition in its own right, the purge
  between conditions was not independently verified, and the run order was not
  kept. **Carryover cannot be excluded for any report of a substance that was
  not present**, which includes the three DMS lewisite reports in mixtures
  containing none.
- Agent purity was above 95% except lewisite, which was 67%; the remaining
  third was not characterized.
- These are three instruments, one of each of three types, from one campaign
  at one laboratory. Instrument type is confounded with manufacturer, library,
  firmware, calibration state and the individual unit. Library contents and
  firmware of other units will differ.

## Statistics

`mixture_outcomes.py` reports counts and raw proportions. **No Cohen's kappa is
reported**: the three instruments do not share a response set, so the
statistic is not interpretable here. No test of association between instrument
and outcome is computed either, because the same conditions were presented to
all three instruments (so the observations are paired rather than
independent) and one instrument returns a single category by design (so any
such association is circular). No inferential statistic is reported, and the
governing reason is the design: with one unit of each instrument type there is
no replication at the level of the inferential unit, so a test over these
conditions would treat them as replicates of a population the study never
sampled. Proportions also carry no confidence interval because the replicate
ledger that would support one was not retained;
the conditions measured are also a complete set rather than a sample from a
population.

## Reproducing the analysis

```
python3 code/counts.py             # every count reported in the Results
python3 code/mixture_outcomes.py          # counts and proportions, binary mixtures only
python3 code/fig_baseline.py       # Figure 1
python3 code/fig_toc.py            # table-of-contents graphic
python3 code/fig_card.py           # Figure 3, the field card
python3 code/fig_timing.py         # Figure 2, detect and clear-down times
python3 code/si_tables.py          # regenerates SI Tables S1-S5 from these CSVs
python3 code/fig_outcomes.py       # binary-mixture outcomes (not in the paper)
python3 code/single_vs_mixture.py  # per-agent single vs mixture (not in the paper)
python3 code/vapor_ratio.py       # vapor-pressure ratios (not in the paper)
```
Requires Python 3.13 and Matplotlib. No numerical or statistical library (NumPy, SciPy) is used.
Run from the directory holding `data/`.

## Citation

The version of record for these data is the Supporting Information of the
published article, which carries its own DOI. This repository is a convenience
copy and may change.

## License

Data: CC BY 4.0. Code: MIT.
