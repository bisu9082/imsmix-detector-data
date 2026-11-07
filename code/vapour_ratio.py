"""Pure-component vapour-pressure ratio for each binary mixture (ideal-mixing upper bound on how
unequal the vapour above the vial can be).  All vapour pressures are at 25 C, so the ratios and the saturation
concentrations quoted in SI S3 rest on one temperature.  GB and VX: NIOSH
Emergency Response Safety and Health Database.  HD, Lewisite, AC: OPCW,
Physicochemical Properties & Relative Toxicity of CW Agents.  CK: gas near
room temperature (bp 12.8 C, NIOSH NPG 0162), no value used."""
import csv, os
_HERE = os.path.dirname(os.path.abspath(__file__))
def _D(name):
    for base in ('data/relabeled', 'data',
                 os.path.join(_HERE, '..', 'data'),
                 os.path.join(_HERE, '..', 'data', 'relabeled')):
        p = os.path.join(base, name)
        if os.path.exists(p): return p
    raise FileNotFoundError(name)
VP = {'GB': 2.9, 'VX': 0.0007, 'HD': 0.072, 'Lewisite': 0.394, 'AC': 742.0}   # mm Hg at 25 C

def c_sat(mmHg, M_g_mol, T=298.15):
    """Saturation concentration in mg/m3 from the ideal-gas law, c = PM/RT."""
    return (mmHg / 760.0) * M_g_mol * 1e6 / (0.082057 * T)
GAS = {'AC', 'CK'}
b = {r['mixture']: r for r in csv.DictReader(open(_D('table6_imsB_binary.csv'), encoding='utf-8'))}
rows = []
for m, r in b.items():
    a1, a2 = m.split('+')
    if a1 in VP and a2 in VP:
        hi, lo = (a1, a2) if VP[a1] >= VP[a2] else (a2, a1)
        ratio = VP[hi] / VP[lo]
        txt = f'{ratio:.1f}'
    else:
        hi = a1 if a1 in GAS else a2
        lo = a2 if hi == a1 else a1
        ratio = None
        txt = 'gas-phase component (CK or AC)'
    rows.append(dict(mixture=m, more_volatile=hi, less_volatile=lo, vp_ratio=txt, imsb_reported=r['reported_species']))
w = csv.DictWriter(open('vapour_ratio.csv', 'w', newline='', encoding='utf-8'), fieldnames=rows[0].keys())
w.writeheader(); w.writerows(rows)
for r in rows: print(r)

# The two saturation concentrations quoted in SI S3, so that they are
# re-derivable from the deposit rather than only stated.
for name, M in (('VX', 267.37), ('GB', 140.09)):
    print(f"c_sat({name}, 25 C) = {c_sat(VP[name], M):.3g} mg/m3")
print(f"GB/VX saturation ratio = {c_sat(VP['GB'],140.09)/c_sat(VP['VX'],267.37):.0f}")
