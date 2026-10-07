#!/usr/bin/env python3
"""Agrega las estaciones por región natural usando la regionalización de API Colombia.

Produce la cobertura de lluvia por región (estaciones con dato > 0 sobre el total)
y los rankings de lluvia y temperatura que alimentan la tabla de la sección 02.

    python3 pipeline/regions.py --raw data/raw/2026-10-07

Bogotá D.C. y el archipiélago de San Andrés no salen de `regionId`, así que van
forzados a Andina e Insular respectivamente.
"""
import argparse, json, re, unicodedata, collections, os, sys

ap = argparse.ArgumentParser(description=__doc__,
                             formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('--raw', default='data/raw/latest', help='directorio con las capas descargadas')
args = ap.parse_args()

def norm(s):
    if s is None: return ''
    s=unicodedata.normalize('NFD',str(s)); s=''.join(c for c in s if unicodedata.category(c)!='Mn')
    s=s.lower(); s=re.sub(r'[^a-z0-9 ]',' ',s); return ' '.join(s.split())
reg={x['id']:x['name'] for x in json.load(open(os.path.join(args.raw,'apic_region.json'), encoding='utf-8'))}
dep2reg={}
for x in json.load(open(os.path.join(args.raw,'apic_dept.json'), encoding='utf-8')):
    rid=x.get('regionId')
    dep2reg[norm(x['name'])]=reg.get(rid) if rid else None
# fixes / aliases
dep2reg.setdefault('bogota d c','Andina'); dep2reg['bogota d c']='Andina'
dep2reg['bogota  d c']='Andina'
for k in ['archipielago de san andres providencia y santa catalina','san andres y providencia','san andres providencia y santa catalina','archipielago de san andres','san andres']:
    dep2reg[k]='Insular'
print('Valle:',dep2reg.get('valle del cauca'),'Cauca:',dep2reg.get('cauca'),'Narino:',dep2reg.get('narino'),'Choco:',dep2reg.get('choco'))
unresolved=[k for k,v in dep2reg.items() if v is None]
print('sin region:',unresolved)

def load(n):
    pth=os.path.join(args.raw, n+'.json')
    if not os.path.exists(pth): sys.exit('falta %s — corre primero pipeline/fetch_ideam.py'%pth)
    d=json.load(open(pth, encoding='utf-8')); return [f['attributes'] for f in d.get('features',[])]
tmax=load('tmax'); lluvia=load('lluvia')
def regof(dep):
    n=norm(dep)
    if n.startswith('bogota'): return 'Andina'
    if 'san andres' in n: return 'Insular'
    return dep2reg.get(n)
# region stats
print('\n=== LLUVIA por región ===')
agg=collections.defaultdict(lambda:[0,0])
unk=set()
for a in lluvia:
    if a.get('DATO') is None: continue
    r=regof(a['DEPARTAMEN'])
    if r is None: unk.add(a['DEPARTAMEN']); continue
    agg[r][0]+=1
    if a['DATO']>0: agg[r][1]+=1
tot=[0,0]
for r,(n,w) in sorted(agg.items(), key=lambda x:-x[1][0]):
    tot[0]+=n; tot[1]+=w
    print(f'{r:12s} {w:4d}/{n:4d} = {100*w/n:5.1f}%')
print(f'{"TOTAL":12s} {tot[1]:4d}/{tot[0]:4d} = {100*tot[1]/tot[0]:5.1f}%')
print('dep sin region en lluvia:',unk)

print('\n=== TOP LLUVIA por región ===')
byreg=collections.defaultdict(list)
for a in lluvia:
    if a.get('DATO') is None: continue
    r=regof(a['DEPARTAMEN'])
    if r: byreg[r].append((a['DATO'],a['ESTACION'],a['MUNICIPIO'],a['DEPARTAMEN']))
for r in byreg:
    byreg[r].sort(reverse=True)
    print(r, byreg[r][:7])

print('\n=== TMAX por región ===')
tbyreg=collections.defaultdict(list)
for a in tmax:
    if a.get('DATO') is None: continue
    r=regof(a['DEPARTAMEN'])
    if r: tbyreg[r].append((a['DATO'],a['ESTACION'],a['MUNICIPIO'],a['DEPARTAMEN']))
for r in tbyreg:
    tbyreg[r].sort(reverse=True)
    print(f'{r:12s} n={len(tbyreg[r]):3d}', tbyreg[r][:7])
