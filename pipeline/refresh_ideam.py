#!/usr/bin/env python3
"""Refresca TODOS los datos de estación y alerta embebidos en el tablero.

Reescribe el objeto `IDEAM_CITY` completo a partir de las capas descargadas por
`fetch_ideam.py`, y marca explícitamente como «sin refrescar hoy · dato del
<fecha>» cualquier estación que hoy no reportó, para que un valor viejo nunca
quede indistinguible de uno vigente.

    python3 pipeline/refresh_ideam.py \
        --board board/index.html --raw data/raw/2026-10-07 \
        --data-date 5-oct --out ideam_city_new.json

`--data-date` es la fecha a la que corresponde el DATO, no la de la consulta: el
feed de estaciones va dos días por detrás (ver docs/METODOLOGIA.md).

Imprime un recuento de qué cambió, qué quedó sin refrescar y qué estación volvió
a reportar. Ese recuento es lo que se publica en la nota de metodología del día.
"""
import argparse, json, re, unicodedata, collections, os, sys

ap = argparse.ArgumentParser(description=__doc__,
                             formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('--board', default='board/index.html', help='HTML del tablero')
ap.add_argument('--raw', default='data/raw/latest', help='directorio con las capas descargadas')
ap.add_argument('--data-date', required=True, help='fecha del DATO, p. ej. 5-oct')
ap.add_argument('--out', default='ideam_city_new.json')
args = ap.parse_args()


def norm(s):
    if s is None: return ''
    s = unicodedata.normalize('NFD', str(s))
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = s.lower()
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    return ' '.join(s.split())

html = open(args.board, encoding='utf-8').read()

# --- extract IDEAM_CITY ---
m = re.search(r'var IDEAM_CITY = (\{.*\});\s*$', html, re.M)
CITY = json.loads(m.group(1))
print('IDEAM_CITY entries:', len(CITY))

# --- extract DEPARTMENTS: dept name -> city names ---
dep_block = html[html.index('var DEPARTMENTS = ['):html.index('var dotsLayer')]
city2dep = {}
cur = None
for mm in re.finditer(r"\{key:'([a-z]+)', name:'([^']+)'|\{name:'((?:[^'\\]|\\.)*)'", dep_block):
    if mm.group(1):
        cur = mm.group(2)
    else:
        nm = mm.group(3).replace("\\'", "'")
        city2dep[nm] = cur
print('cities mapped:', len(city2dep))
missing = [k for k in CITY if k not in city2dep]
print('CITY keys without dept:', missing)

def load(n):
    p = os.path.join(args.raw, n + '.json')
    if not os.path.exists(p):
        sys.exit('falta la capa %s — corre primero pipeline/fetch_ideam.py' % p)
    d = json.load(open(p, encoding='utf-8'))
    return [f['attributes'] for f in d.get('features', [])]

tmax = load('tmax'); lluvia = load('lluvia')
icv = load('icv'); idd = load('idd'); hidro = load('hidro')

# tmax index: (norm station) -> list of rows
tmax_by_est = collections.defaultdict(list)
for a in tmax:
    if a.get('DATO') is None: continue
    tmax_by_est[norm(a['ESTACION'])].append(a)
lluvia_by_est = collections.defaultdict(list)
lluvia_by_mun = collections.defaultdict(list)
for a in lluvia:
    if a.get('DATO') is None: continue
    lluvia_by_est[norm(a['ESTACION'])].append(a)
    lluvia_by_mun[(norm(a['MUNICIPIO']), norm(a['DEPARTAMEN']))].append(a)

# alert indexes
def alert_idx(rows):
    d = {}
    for a in rows:
        d[(norm(a.get('MPIO_CNMBR')), norm(a.get('DPTO_CNMBR')))] = a.get('PROBABILID')
    return d
icv_i = alert_idx(icv); idd_i = alert_idx(idd)
LEVEL = {0:'normal', 1:'amarilla', 2:'naranja', 3:'roja'}

DEP_ALIAS = {
    'san andres y providencia': 'san andres providencia y santa catalina',
}
hidro_by_dep = collections.defaultdict(lambda: {'total':0,'rojas':[],'naranjas':[]})
for a in hidro:
    dep = norm(a.get('DEP'))
    lvl = a.get('ALERTA')
    h = hidro_by_dep[dep]
    h['total'] += 1
    if lvl == 3: h['rojas'].append(a['NOMSZH'])
    elif lvl == 2: h['naranjas'].append(a['NOMSZH'])

TODAY_DATA = args.data_date   # el feed de estaciones va 2 días por detrás
stats = {'tmax_changed':0,'tmax_same':0,'tmax_stale_new':[],'tmax_stale_keep':[],'tmax_returned':[],
         'll_changed':0,'ll_same':0,'ll_stale_new':[],'ll_stale_keep':[],'ll_returned':[],
         'alert_moves':[], 'hidro_changed':0}

for city, m in CITY.items():
    dep = city2dep.get(city)
    depn = norm(dep) if dep else None
    # ---- tmax ----
    if 'tmax' in m:
        t = m['tmax']
        key = norm(t['est'])
        cand = tmax_by_est.get(key, [])
        pick = None
        for a in cand:
            if norm(a['MUNICIPIO']) == norm(t['mun']): pick = a; break
        if pick is None and cand: pick = cand[0]
        if pick is not None:
            if t.get('stale'): stats['tmax_returned'].append((city, t['est']))
            old = t.get('v')
            t['v'] = pick['DATO']
            t['est'] = pick['ESTACION']; t['mun'] = pick['MUNICIPIO']
            t.pop('stale', None)
            if old != pick['DATO']: stats['tmax_changed'] += 1
            else: stats['tmax_same'] += 1
        else:
            if t.get('stale'): stats['tmax_stale_keep'].append((city, t['est'], t['stale']))
            else:
                t['stale'] = TODAY_DATA
                stats['tmax_stale_new'].append((city, t['est'], t['mun']))
    # ---- lluvia ----
    if 'lluvia' in m:
        L = m['lluvia']
        key = norm(L['est'])
        cand = lluvia_by_est.get(key, [])
        pick = None
        for a in cand:
            if norm(a['MUNICIPIO']) == norm(L['mun']): pick = a; break
        if pick is None and cand: pick = cand[0]
        if pick is not None:
            if L.get('stale'): stats['ll_returned'].append((city, L['est']))
            old = L.get('v')
            L['v'] = pick['DATO']
            L['est'] = pick['ESTACION']; L['mun'] = pick['MUNICIPIO']
            L.pop('stale', None)
            muns = lluvia_by_mun.get((norm(pick['MUNICIPIO']), norm(pick['DEPARTAMEN'])), [])
            L['nmun'] = len(muns)
            L['vmax'] = max([x['DATO'] for x in muns]) if muns else pick['DATO']
            L['conv'] = any('Convencional' in (x.get('TECNOLOGIA') or '') for x in muns)
            if old != pick['DATO']: stats['ll_changed'] += 1
            else: stats['ll_same'] += 1
        else:
            if L.get('stale'): stats['ll_stale_keep'].append((city, L['est'], L['stale']))
            else:
                L['stale'] = TODAY_DATA
                stats['ll_stale_new'].append((city, L['est'], L['mun']))
    # ---- icv / idd ----
    for fld, idx, label in (('icv', icv_i, 'incendio'), ('idd', idd_i, 'deslizamiento')):
        if fld in m:
            for e in m[fld]:
                lvl = idx.get((norm(e['mun']), depn))
                if lvl is None:
                    # try any dept match
                    cands = [v for (mn, dn), v in idx.items() if mn == norm(e['mun'])]
                    lvl = cands[0] if len(cands) == 1 else None
                new = LEVEL.get(lvl, 'normal') if lvl is not None else e['nivel']
                if new != e['nivel']:
                    stats['alert_moves'].append((label, city, e['mun'], e['nivel'], new))
                    e['nivel'] = new
    # ---- hidro ----
    if 'hidro' in m and depn:
        k = DEP_ALIAS.get(depn, depn)
        h = hidro_by_dep.get(k, {'total':0,'rojas':[],'naranjas':[]})
        new = {'total': h['total'], 'rojas': sorted(set(h['rojas'])), 'naranjas': sorted(set(h['naranjas']))}
        if new != m['hidro']:
            stats['hidro_changed'] += 1
            m['hidro'] = new

print('\n=== STATS ===')
print('tmax changed/same:', stats['tmax_changed'], stats['tmax_same'])
print('lluvia changed/same:', stats['ll_changed'], stats['ll_same'])
print('tmax stale NEW:', stats['tmax_stale_new'])
print('tmax stale KEEP:', stats['tmax_stale_keep'])
print('tmax returned:', stats['tmax_returned'])
print('lluvia stale NEW:', stats['ll_stale_new'])
print('lluvia stale KEEP:', stats['ll_stale_keep'])
print('lluvia returned:', stats['ll_returned'])
print('hidro summaries changed:', stats['hidro_changed'])
print('alert moves (%d):' % len(stats['alert_moves']))
for a in stats['alert_moves']: print('  ', a)

json.dump(CITY, open(args.out, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('\nescrito', args.out, os.path.getsize(args.out), 'bytes')
print('Pega este objeto en el tablero como `var IDEAM_CITY = {...};` y valida con node --check.')
