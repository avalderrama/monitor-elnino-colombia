#!/usr/bin/env python3
"""Convierte los hallazgos confirmados del Workflow en documentos para la coleccion
`hallazgos` de ArtifactData. Deduplica POR HECHO, no por agente."""
"""Convierte los hallazgos confirmados del Workflow en documentos de la colección
`hallazgos`, deduplicando POR HECHO y no por agente.

    MONITOR_FECHA=2026-10-07 python3 pipeline/build_hallazgos.py confirmados.json

Lee `apic_region.json` y `apic_dept.json` de $MONITOR_DATA (por defecto
data/reference) y consulta API Colombia para normalizar municipios, con caché en
disco. Escribe `hallazgos_docs.json`, listo para un batch de ArtifactData.

La deduplicación es el punto del script: siete agentes de búsqueda traen el mismo
hecho con textos distintos. Agrupa por misma URL, o mismo lugar + mismo tema, o
mismo lugar + cifras compartidas; el documento más completo manda y los demás
aportan sus fuentes como corroboración.
"""
import json, os, re, sys, unicodedata, difflib
from collections import defaultdict

S = '/tmp/claude-0/-home-user/48d7769d-8b45-5855-b6c8-668730527f99/scratchpad'
FECHA_CORTE = '2026-10-06'

def norm(s):
    s = unicodedata.normalize('NFD', str(s or ''))
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return ' '.join(re.sub(r'[^a-z0-9 ]', ' ', s.lower()).split())

# --- region por departamento, de API Colombia (regionId, cache de esta corrida) ---
import os, subprocess
regs = {r['id']: r['name'] for r in json.load(open(f'{S}/apic_region.json'))}
depts = json.load(open(f'{S}/apic_dept.json'))
DEP2REG, DEP_CANON = {}, {}
for d in depts:
    DEP2REG[norm(d['name'])] = regs.get(d.get('regionId'), '')
    DEP_CANON[norm(d['name'])] = d['name']
# Bogota y el archipielago, que API Colombia no lista como departamento del mismo modo
DEP2REG[norm('Bogota D.C.')] = 'Andina'; DEP_CANON[norm('Bogota D.C.')] = 'Bogotá D.C.'
DEP2REG[norm('Bogota')] = 'Andina';      DEP_CANON[norm('Bogota')] = 'Bogotá D.C.'
for a in ('san andres y providencia', 'san andres', 'archipielago de san andres providencia y santa catalina'):
    DEP2REG[a] = 'Insular'; DEP_CANON.setdefault(a, 'San Andrés y Providencia')

# --- municipio -> departamento, normalizado contra API Colombia (con cache en disco) ---
CITY_CACHE = f'{S}/apic_city_cache.json'
_cc = json.load(open(CITY_CACHE)) if os.path.exists(CITY_CACHE) else {}

def resolver_municipio(nombre):
    """Devuelve (municipio_canonico, departamento_canonico) o (nombre, '')."""
    if not nombre: return ('', '')
    k = norm(nombre)
    if k in _cc: return tuple(_cc[k])
    try:
        from urllib.parse import quote
        url = 'https://api-colombia.com/api/v1/City/search/' + quote(nombre)
        out = subprocess.run(['curl', '-sS', '--max-time', '25', url],
                             capture_output=True, text=True, timeout=40).stdout
        arr = json.loads(out)
        hit = None
        for c in (arr if isinstance(arr, list) else []):
            if norm(c.get('name')) == k: hit = c; break
        if hit is None and isinstance(arr, list) and arr: hit = arr[0]
        if hit:
            did = hit.get('departmentId')
            dep = next((d['name'] for d in depts if d['id'] == did), '')
            _cc[k] = [hit.get('name') or nombre, dep]
        else:
            _cc[k] = [nombre, '']
    except Exception:
        _cc[k] = [nombre, '']
    json.dump(_cc, open(CITY_CACHE, 'w'), ensure_ascii=False)
    return tuple(_cc[k])

def region_de(dep, mun=''):
    n = norm(dep)
    if n in DEP2REG: return DEP2REG[n]
    if n and 'nacional' not in n:
        partes = [p.strip() for p in re.split(r'[,/]| y ', dep) if p.strip()]
        rr = {DEP2REG.get(norm(p)) for p in partes}
        rr.discard(None); rr.discard('')
        if rr: return ' / '.join(sorted(rr))
    if mun:  # el agente puso un municipio donde iba el departamento, o dejo el depto vacio
        _, dep2 = resolver_municipio(mun)
        if dep2: return DEP2REG.get(norm(dep2), 'Nacional')
    return 'Nacional'

def canon_dep(dep, mun=''):
    n = norm(dep)
    if n in DEP_CANON: return DEP_CANON[n]
    if n and 'nacional' not in n:
        partes = [p.strip() for p in re.split(r'[,/]| y ', dep) if p.strip()]
        cc = [DEP_CANON.get(norm(p), p) for p in partes]
        if len(cc) > 1: return ', '.join(cc)
    if mun:
        _, dep2 = resolver_municipio(mun)
        if dep2: return dep2
    return dep if n and 'nacional' not in n else 'Nacional'

BADGE_DESINFO = 'b-nodata'
def badge_de(h):
    if h.get('categoria') == 'desinformacion':
        return 'b-ok' if h.get('confianza') == 'alta' else BADGE_DESINFO
    if h.get('confianza') == 'sin verificar':
        return BADGE_DESINFO
    if h.get('oficial'):
        return 'b-ok'
    fn = norm(h.get('fuente_nombre'))
    if any(g in fn for g in ('fedegan','fedearroz','fedecafe','asocana','fenavi','fedepapa',
                             'augura','asocapitales','gremio','camara','andesco','acolgen',
                             'centroabastos','surabastos','asogaboy','asoganorte','fedemunicipios')):
        return 'b-gremio'
    return 'b-press'

def tema(h):
    t = norm(h.get('texto'))
    for k, v in [('racionamient','racionamiento'), ('carrotanque','carrotanques'),
                 ('calamidad','calamidad'), ('incendio','incendios'), ('embalse','embalses'),
                 ('decreto','decreto'), ('record','record-temperatura'), ('precio','precios'),
                 ('cosecha','cosechas'), ('ganad','ganaderia'), ('muert','muertes'),
                 ('desabastecimiento','desabastecimiento'), ('caudal','caudales'),
                 ('rio','caudales'), ('alerta','alertas'), ('sequia','sequia'),
                 ('agua','agua'), ('energia','energia'), ('lluvia','lluvia')]:
        if k in t: return v
    return (h.get('categoria') or 'hallazgo')

def doc_id(h):
    lugar = norm(h.get('municipio')) or norm(canon_dep(h.get('departamento'))) or 'nacional'
    lugar = re.sub(r'\s+', '-', lugar)[:28]
    return f"{FECHA_CORTE}-{lugar}-{tema(h)}"

# --- dedup POR HECHO ---
def clave_hecho(h):
    """Firma del hecho: lugar + tema + las cifras que aparecen en el texto."""
    nums = tuple(sorted(set(re.findall(r'\d[\d.,]{1,}', h.get('texto') or ''))))[:4]
    return (norm(h.get('municipio')) or norm(h.get('departamento')), tema(h), nums)

def _url_key(h):
    u = (h.get('fuente_url') or '').strip().lower()
    u = re.sub(r'[#?].*$', '', u).rstrip('/')
    return u

def mismo_hecho(a, b):
    # 1) misma URL exacta => es la misma nota, el mismo hecho
    ua, ub = _url_key(a), _url_key(b)
    if ua and ua == ub: return True
    ka, kb = clave_hecho(a), clave_hecho(b)
    # 2) mismo lugar y mismas cifras
    if ka == kb: return True
    if ka[0] != kb[0]: return False          # lugares distintos => hechos distintos
    ta, tb = norm(a.get('texto'))[:420], norm(b.get('texto'))[:420]
    sim = difflib.SequenceMatcher(None, ta, tb).ratio()
    # 3) mismo lugar + mismo tema => basta un parecido moderado
    if ka[1] == kb[1] and sim >= 0.50: return True
    # 4) mismo lugar + cifras compartidas => mismo hecho aunque el tema se etiquete distinto
    comunes = set(ka[2]) & set(kb[2])
    if comunes and sim >= 0.38: return True
    # 5) mismo lugar y textos muy parecidos
    return sim >= 0.70

def agrupar(items):
    grupos = []
    for h in items:
        for g in grupos:
            if any(mismo_hecho(h, x) for x in g):
                g.append(h); break
        else:
            grupos.append([h])
    return grupos

def fundir(g):
    """Se queda con el mas completo y suma las fuentes de los demas."""
    g = sorted(g, key=lambda h: (not h.get('oficial'), -len(h.get('texto') or '')))
    base = dict(g[0])
    extras = []
    for h in g[1:]:
        fn = h.get('fuente_nombre')
        if fn and norm(fn) != norm(base.get('fuente_nombre')):
            extras.append(fn)
    base['_corroboran'] = sorted(set(extras))
    base['_n_agentes'] = len({h.get('_fuente') or h.get('fuente_agente') or '?' for h in g})
    return base

def a_documento(h):
    texto = (h.get('texto') or '').strip()
    if not h.get('atribuido_a_elnino'):
        texto += ' La fuente NO atribuye el hecho a El Niño, la sequía ni el calor extremo; se registra tal cual.'
    if h.get('confianza') == 'sin verificar':
        texto += ' Cifra sin verificar.'
    if h.get('por_verificar'):
        texto += f" Pendiente de verificar: {h['por_verificar']}."
    if h.get('_corroboran'):
        texto += ' Corroborado además por: ' + ', '.join(h['_corroboran']) + '.'
    mun_raw = (h.get('municipio') or '').strip()
    mun = resolver_municipio(mun_raw)[0] if mun_raw else ''
    return {
        'fecha': h.get('fecha_hecho') or FECHA_CORTE,
        'region': region_de(h.get('departamento'), mun_raw),
        'departamento': canon_dep(h.get('departamento'), mun_raw),
        'municipio': mun,
        'categoria': h.get('categoria') or 'efecto',
        'badge': badge_de(h),
        'texto': texto,
        'fuente_nombre': h.get('fuente_nombre') or '',
        'fuente_url': h.get('fuente_url') or '',
    }

if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else f'{S}/wf_confirmados.json'
    items = json.load(open(src))
    grupos = agrupar(items)
    docs = {}
    for g in grupos:
        h = fundir(g)
        d = a_documento(h)
        did = doc_id(h)
        n = 2
        base_id = did
        while did in docs:
            did = f'{base_id}-{n}'; n += 1
        docs[did] = d
    json.dump(docs, open(f'{S}/hallazgos_docs.json', 'w'), ensure_ascii=False, indent=1)
    print(f'{len(items)} confirmados -> {len(grupos)} hechos -> {len(docs)} documentos')
    for did, d in docs.items():
        print(f"  {did}  [{d['badge']}] {d['region']} · {d['categoria']}")
