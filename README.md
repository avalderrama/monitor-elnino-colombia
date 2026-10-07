# Monitor diario de El Niño en Colombia

Seguimiento diario y verificado del fenómeno de El Niño 2026-2027 y sus efectos
en Colombia: sequía, incendios, desabastecimiento de agua, racionamientos,
emergencias declaradas, damnificados, precios de alimentos, cosechas, respuesta
del Estado y desinformación — todo localizado por **región, departamento y
municipio**, con fecha y fuente.

El resultado de cada corrida es un tablero HTML que se republica en la misma URL,
más una base de datos de hallazgos normalizados.

> **El tablero publicado:** https://claude.ai/artifact/KatWH67i8yqxcJkJMx5ezD
> *(enlace de solo lectura; ver la nota sobre visibilidad más abajo antes de
> hacer público este repositorio)*

---

## Qué tiene de distinto

Es un monitor **escéptico por diseño**. Tres reglas lo gobiernan, y están
implementadas, no solo enunciadas:

1. **Si la fuente no atribuye el hecho a El Niño, el monitor no se lo atribuye.**
   Se publica diciéndolo. Entre un tercio y la mitad de los hallazgos confirmados
   de un día típico caen en ese caso.
2. **Se verifica la fecha del HECHO, no la de publicación del portal.** El modo
   de fallo dominante no son cifras falsas: son notas viejas republicadas como si
   fueran de hoy. [La lista de casos ya detectados está en la metodología](docs/METODOLOGIA.md#5-reciclaje-verificar-la-fecha-del-hecho-no-la-de-publicación).
3. **Cuando la realidad cambia, se corrige el ítem viejo y se conserva la cita
   anterior**, para que la evolución quede visible. Incluye corregirse a sí mismo:
   el historial del tablero contiene sus propias retractaciones.

---

## Arquitectura

```
fetch_ideam.py ──> data/raw/<fecha>/*.json
                        │
        ┌───────────────┴────────────────┐
        │                                │
  refresh_ideam.py                  regions.py
  (reescribe IDEAM_CITY,          (cobertura y rankings
   marca lo no refrescado)          por región natural)
        │                                │
        └───────────────┬────────────────┘
                        v
                  board/index.html   ← PUBLICACIÓN 1 (no espera a la fase B)
                        ^
                        │
  research/*.workflow.js ──> 7 fuentes en paralelo + verificación adversarial
                        │
              build_hallazgos.py  (deduplica POR HECHO, no por agente)
                        │
                        v
              colección `hallazgos`  ← PUBLICACIÓN 2
```

**Fase A — refresco de datos (determinista).** Relee las cinco capas REST del
visualizador del IDEAM, la API de XM y API Colombia, y reescribe *todos* los
datos embebidos en el tablero: ~58 estaciones de temperatura y lluvia, los
niveles de alerta por municipio y los resúmenes hidrológicos por departamento.
Lo que hoy no reportó queda marcado **«sin refrescar hoy · dato del \<fecha\>»**
en la ficha, en el tooltip y en el pie del gráfico — un valor viejo nunca queda
indistinguible de uno vigente.

**Fase B — investigación (no determinista).** Siete agentes de búsqueda en
paralelo (IDEAM, UNGRD, DANE/SIPSA/Minagricultura, prensa nacional, prensa
regional, desinformación, respuesta del Estado), y cada hallazgo pasa por una
verificación adversarial que intenta **refutarlo** por fecha, por cifra y por
atribución antes de que se publique.

La fase A se publica sola en cuanto está lista. Así el tablero nunca queda
desactualizado si la corrida se corta a mitad.

---

## Correr el pipeline

Requiere Python 3.11+ (solo biblioteca estándar), `node` para validar, y
`pdftotext` (poppler-utils) para leer los boletines del IDEAM.

```bash
# 1. descargar las capas del día
python3 pipeline/fetch_ideam.py --out data/raw/$(date +%F) \
        --start 2026-10-01 --end $(date +%F)

# 2. cobertura y rankings por región
python3 pipeline/regions.py --raw data/raw/$(date +%F)

# 3. refrescar los datos embebidos en el tablero
#    OJO: --data-date es la fecha del DATO, dos días antes de la consulta
python3 pipeline/refresh_ideam.py \
        --board board/index.html \
        --raw data/raw/$(date +%F) \
        --data-date 5-oct \
        --out ideam_city_new.json

# 4. convertir los hallazgos confirmados en documentos de la colección
MONITOR_FECHA=$(date +%F) python3 pipeline/build_hallazgos.py confirmados.json
```

`data/raw/2026-10-07/` va versionado como muestra para que los pasos 2 y 3
puedan correrse sin descargar nada.

**Antes de publicar, siempre:** extraer los bloques `<script>` del tablero y
pasarlos por `node --check`. `IDEAM_CITY` se reescribe completo en cada corrida y
un error de sintaxis deja el mapa en blanco sin ningún aviso.

---

## Estructura

| Ruta | Qué es |
|---|---|
| `docs/METODOLOGIA.md` | **Empieza por aquí.** Endpoints no documentados, trampas confirmadas, casos de reciclaje, bloqueos conocidos y reglas editoriales |
| `pipeline/fetch_ideam.py` | Descarga las 5 capas del IDEAM + XM + API Colombia |
| `pipeline/refresh_ideam.py` | Reescribe `IDEAM_CITY` y marca lo no refrescado |
| `pipeline/regions.py` | Agregación por región natural |
| `pipeline/build_hallazgos.py` | Deduplicación por hecho y armado de documentos |
| `research/*.workflow.js` | El pipeline de investigación: 7 fuentes + verificación adversarial |
| `board/index.html` | El tablero publicado (corte del 6-oct-2026) |
| `data/reference/` | Catálogos de región y departamento de API Colombia |
| `data/hallazgos/<fecha>/` | Los hallazgos confirmados de cada corrida |
| `archive/<fecha>-build/` | Las ediciones quirúrgicas del HTML de ese día. Registro histórico del método, **no reutilizable**: cada script apunta a un estado concreto del tablero |

---

## Fuentes

**Oficiales.** IDEAM (visualizador REST, Informe Técnico Diario, BAICV, boletines
ENOS y de predicción climática, datos extremos semanales), UNGRD (API de
SharePoint, datasets abiertos, reportes anuales de emergencias), DANE (SIPSA
semanal y diario, IPC), XM (API del sector eléctrico), API Colombia, NOAA/CPC,
ministerios, gobernaciones y alcaldías.

**No oficiales**, siempre marcadas como tales: prensa nacional y regional,
gremios (Fedegán, Fedearroz, FNC, Asocapitales), verificadores (Colombiacheck,
La Silla Vacía).

Cada hallazgo lleva una insignia: ✅ confirmado por fuente oficial · 📰 prensa sin
confirmación oficial · 🏢 fuente gremial · ⚠️ sin datos verificables.

---

## Estado y limitaciones

* El monitor **no tiene una cifra consolidada de damnificados ni de muertes
  humanas** atribuidas a El Niño, porque no existe publicada. Se dice así.
* Varias fuentes oficiales están tras muros anti-bot. La lista, con lo que sí
  funciona para cada una, está en la metodología.
* La fase B depende de qué publicó la prensa ese día: una corrida sin hallazgos
  nuevos es un resultado válido, no un fallo.
* Las corridas son diarias y el histórico vive en el tablero, no en este
  repositorio: aquí está el código y los hallazgos normalizados.

---

## Licencia

**Sin definir todavía.** Hay que elegir una antes de abrir el repositorio a
colaboradores externos. El código es de biblioteca estándar y no incorpora
material de terceros; los **datos** provienen de fuentes públicas del Estado
colombiano y conservan las condiciones de uso de cada entidad.
