"""Per-agent comparison: was the agent named under single exposure, and in how many of the
5 mixtures containing it?  IMS-B (CWA mode single baseline) and DMS."""
import csv, re, os
_HERE = os.path.dirname(os.path.abspath(__file__))
def _D(name):
    for base in ('data/relabeled', 'data',
                 os.path.join(_HERE, '..', 'data'),
                 os.path.join(_HERE, '..', 'data', 'relabeled')):
        p = os.path.join(base, name)
        if os.path.exists(p): return p
    raise FileNotFoundError(name)
def rd(f): return list(csv.DictReader(open(_D(f), encoding='utf-8')))
AG = ['GB', 'VX', 'HD', 'Lewisite', 'AC', 'CK']
norm = lambda t: re.sub(r'\(.*?\)', '', t).strip().replace('VX-R', 'VX')
def names(s):
    out = set()
    for part in re.split(r'[;/]|\bor\b', s or ''):
        p = norm(part)
        if p: out.add(p)
    return out
# IMS-B single (CWA mode and STD mode)
single = {}
for r in rd('table3_imsB_single.csv'):
    single[(r['mode'], r['agent'])] = names(r['reported_species'])
mix_b = rd('table6_imsB_binary.csv')
mix_d = rd('table7_dms_binary.csv')
dms_single = {(r['mode'], r['agent']): r['outcome'] for r in rd('table4_dms_single.csv')}
rows = []
for a in AG:
    inm = [m for m in mix_b if a in m['mixture'].split('+')]
    nb = sum(a in names(m['reported_species']) for m in inm)
    inmd = [m for m in mix_d if a in m['mixture'].split('+')]
    nd = sum(a in names(re.sub(r':[\d.]+', '', m['reported_species_conc'])) for m in inmd)
    rows.append(dict(agent=a, n_mix=len(inm),
        imsb_single_cwa=int(a in single[('CWA', a)]), imsb_single_std=int(a in single[('STD', a)]),
        imsb_single_cwa_names='/'.join(sorted(single[('CWA', a)])), imsb_single_std_names='/'.join(sorted(single[('STD', a)])),
        imsb_named_in_mix=nb,
        dms_single_cwa_detected=int(dms_single.get(('CWA', a))=='detected'),
        dms_named_in_mix=nd))
w = csv.DictWriter(open('single_vs_mixture.csv', 'w', newline=''), fieldnames=rows[0].keys())
w.writeheader(); w.writerows(rows)
for r in rows: print(r)
