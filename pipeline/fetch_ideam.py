#!/usr/bin/env python3
"""Descarga las capas del visualizador del IDEAM y los agregados de XM / API Colombia.

Es el primer paso del refresco diario: deja en `out/` los JSON que consumen
`refresh_ideam.py` y `regions.py`.

    python3 pipeline/fetch_ideam.py --out data/raw/$(date +%F)

Notas de operación aprendidas en producción (ver docs/METODOLOGIA.md):

* Las capas de ESTACIÓN (tmax, lluvia) **no tienen campo de fecha** y el feed va
  **dos días por detrás** de la fecha de consulta. La única forma de fecharlas es
  cruzarlas contra el Informe Técnico Diario (ITD) del IDEAM.
* Las capas de ALERTA (icv, idd, hidro) sí están al día.
* `Alertas__IDD` lleva **doble guión bajo**. No es un error de tipeo.
* Las capas de alerta deben cruzarse por `MPIO_CNMBR` + `DPTO_CNMBR`: son los
  únicos campos poblados en las 1.121 filas.
* `PROBABILID` / `ALERTA`: 3 roja, 2 naranja, 1 amarilla, 0 sin alerta.
* El servicio de precipitación **no distingue «0 mm» de «la estación no reportó»**.
"""
import argparse, json, os, sys, urllib.parse, urllib.request

GIS = ('https://visualizador.ideam.gov.co/gisserver/rest/services/StoryMaps_IDA'
       '/{service}/MapServer/{layer}/query')

# nombre local -> (servicio, capa, campos)
LAYERS = {
    'tmax':   ('Datos_TMaxima',       0, 'ESTACION,MUNICIPIO,DEPARTAMEN,DATO'),
    'lluvia': ('Datos_Precipitacion', 0, 'ESTACION,MUNICIPIO,DEPARTAMEN,DATO,TECNOLOGIA'),
    'icv':    ('Alertas_ICV',         2, 'MPIO_CNMBR,DPTO_CNMBR,PROBABILID'),
    'idd':    ('Alertas__IDD',        1, 'MPIO_CNMBR,DPTO_CNMBR,PROBABILID'),
    'hidro':  ('Alertas_Hidrologicas',2, 'NOMSZH,NIVEL_A,ALERTA,DEP'),
}

APIC = {
    'apic_region': 'https://api-colombia.com/api/v1/Region',
    'apic_dept':   'https://api-colombia.com/api/v1/Department',
}

XM_URL = 'https://servapibi.xm.com.co/daily'
XM_METRICS = ['VoluUtilDiarEner', 'CapaUtilDiarEner', 'AporEner', 'AporEnerMediHist']

UA = {'User-Agent': 'Mozilla/5.0 (compatible; monitor-elnino-colombia)'}


def get(url, data=None, headers=None):
    req = urllib.request.Request(url, data=data, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read().decode('utf-8'))


def fetch_layer(name, out_dir):
    service, layer, fields = LAYERS[name]
    qs = urllib.parse.urlencode({
        'where': '1=1', 'outFields': fields, 'returnGeometry': 'false',
        'f': 'json', 'resultRecordCount': 5000,
    })
    d = get(f'{GIS.format(service=service, layer=layer)}?{qs}')
    feats = d.get('features', [])
    path = os.path.join(out_dir, f'{name}.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False)
    con_dato = sum(1 for x in feats if (x.get('attributes') or {}).get('DATO') is not None)
    extra = f', {con_dato} con dato' if name in ('tmax', 'lluvia') else ''
    print(f'  {name:7s} {len(feats):5d} filas{extra}  -> {path}')
    return feats


def fetch_xm(out_dir, start, end):
    """Los valores vienen anidados en Items[].DailyEntities[] con Id=="Sistema",
    COMO CADENAS. No hay un `DailyEntity` plano: esa suposición rompió la corrida
    del 6-oct con un TypeError sobre NoneType."""
    out = {}
    for metric in XM_METRICS:
        body = json.dumps({'MetricId': metric, 'StartDate': start,
                           'EndDate': end, 'Entity': 'Sistema'}).encode()
        try:
            out[metric] = get(XM_URL, data=body,
                              headers={'Content-Type': 'application/json'})
            print(f'  XM {metric:20s} ok')
        except Exception as e:                      # noqa: BLE001
            out[metric] = {'error': str(e)}
            print(f'  XM {metric:20s} FALLO: {e}', file=sys.stderr)
    path = os.path.join(out_dir, 'xm_daily.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False)
    print(f'  -> {path}')


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', default='data/raw/latest', help='directorio de salida')
    ap.add_argument('--start', help='XM: fecha inicial AAAA-MM-DD')
    ap.add_argument('--end', help='XM: fecha final AAAA-MM-DD')
    ap.add_argument('--skip-xm', action='store_true')
    ap.add_argument('--only', help='solo estas capas, separadas por coma')
    a = ap.parse_args()

    os.makedirs(a.out, exist_ok=True)
    names = a.only.split(',') if a.only else list(LAYERS)

    print(f'IDEAM — visualizador ({len(names)} capas)')
    for n in names:
        if n not in LAYERS:
            sys.exit(f'capa desconocida: {n} (opciones: {", ".join(LAYERS)})')
        fetch_layer(n, a.out)

    print('API Colombia — regiones y departamentos')
    for name, url in APIC.items():
        d = get(url)
        path = os.path.join(a.out, f'{name}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False)
        print(f'  {name:12s} {len(d):3d} registros -> {path}')

    if not a.skip_xm:
        if not (a.start and a.end):
            print('XM: omitido (requiere --start y --end)')
        else:
            print(f'XM — serie diaria {a.start} a {a.end}')
            fetch_xm(a.out, a.start, a.end)

    print(f'\nListo. Fechar las capas de estación contra el ITD del IDEAM antes de usarlas.')


if __name__ == '__main__':
    main()
