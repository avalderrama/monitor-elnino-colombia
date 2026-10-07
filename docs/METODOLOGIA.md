# Metodología y memoria operativa

Este archivo es el activo más valioso del repositorio. No es documentación de
cortesía: son las trampas que el monitor ya pisó, con la corrección al lado. Si
vas a trabajar sobre este proyecto, léelo antes de tocar el código.

---

## 1. Las dos fases de la corrida diaria

El monitor no es un scraper. Son dos fases con garantías distintas:

| | Fase A — refresco de datos | Fase B — investigación de prensa |
|---|---|---|
| Qué es | Relectura determinista de servicios REST | Búsqueda en 7 fuentes con verificación adversarial |
| Resultado | Siempre el mismo con la misma entrada | Depende de qué publicó la prensa |
| Duración | Minutos | ~60-90 min |
| Orden | Se publica **primero**, sin esperar la fase B | Se publica **después**, como segunda versión |

**El orden importa y es una decisión, no una casualidad.** La fase A se publica
sola en cuanto está lista, para que el tablero nunca quede desactualizado si la
corrida se corta a mitad. La fase B llega después y actualiza la misma URL.

---

## 2. Servicios del IDEAM — lo que no está documentado en ninguna parte

Raíz: `https://visualizador.ideam.gov.co/gisserver/rest/services/StoryMaps_IDA`
(La raíz correcta es `/gisserver/rest/services`, **no** `/arcgis` ni `/server`.)

| Capa local | Servicio | MapServer | Cruce |
|---|---|---|---|
| `tmax` | `Datos_TMaxima` | `/0` | `ESTACION` + `MUNICIPIO` |
| `lluvia` | `Datos_Precipitacion` | `/0` | `ESTACION` + `MUNICIPIO` |
| `icv` (incendios) | `Alertas_ICV` | `/2` | `MPIO_CNMBR` + `DPTO_CNMBR` |
| `idd` (deslizamientos) | `Alertas__IDD` | `/1` | `MPIO_CNMBR` + `DPTO_CNMBR` |
| `hidro` | `Alertas_Hidrologicas` | `/2` | `DEP`, `NOMSZH` |

### Trampas confirmadas

* **`Alertas__IDD` lleva doble guión bajo.** No es un error de tipeo.
* **Las capas de alerta solo se pueden cruzar por `MPIO_CNMBR` + `DPTO_CNMBR`.**
  Son los únicos campos poblados en las 1.121 filas; `MUNICIPIO` y `DEPARTAMEN`
  vienen vacíos y usarlos devuelve cero coincidencias.
* **`PROBABILID` / `ALERTA`: 3 roja, 2 naranja, 1 amarilla, 0 sin alerta.**
  Verificar el significado contra un caso conocido antes de confiar en él.
* **Las capas de estación NO tienen campo de fecha, y el feed va dos días por
  detrás de la consulta.** Es la trampa más importante de todo el proyecto. La
  única forma de fechar el dato es cruzarlo contra el **Informe Técnico Diario
  (ITD)** del IDEAM y verificar que coincidan los valores. En producción esto se
  ha confirmado ocho días seguidos, una vez con 24 valores de estación
  coincidentes. **Las capas de alerta, en cambio, sí están al día.**
* **`0 mm` no se distingue de «la estación no reportó».** El servicio de
  precipitación no diferencia las dos cosas y **520 de ~646 pluviómetros son de
  lectura manual diaria** (campo `TECNOLOGIA`). Un punto sin lluvia **no prueba
  que no llovió**. Hay que decirlo cada vez.
* **La red es intermitente, no estable.** Una estación puede desaparecer del feed
  y reaparecer días después. Hay que marcar explícitamente
  «sin refrescar hoy · dato del \<fecha\>» en la ficha, en el tooltip y en el pie
  del gráfico. Que una estación vuelva no significa que se quede.

### PDF del IDEAM

Los boletines están en `ideam.gov.co/file-download/download/public/<id>` con ids
consecutivos. Se descubren barriendo ids con
`curl --max-filesize 16000000` y filtrando por la cabecera `%PDF`; se leen con
`pdftotext`. Documentos útiles: **ITD** (temperaturas por estación y récords),
**BAICV** (alertas de incendio por departamento), **pronóstico de deslizamientos**,
**boletín semanal de datos extremos**, **boletín ENOS**.

**Límites conocidos de la extracción:** la tabla «Estado de los Embalses» y las
láminas de sensación térmica vienen **embebidas como imagen**, no como texto; y
las tablas municipales del BAICV **pierden la agrupación por nivel** al extraer el
texto, lo que ya impidió resolver una discrepancia real entre el boletín y el
servicio REST.

---

## 3. XM (sector eléctrico)

`POST https://servapibi.xm.com.co/daily` con
`{"MetricId": ..., "StartDate": ..., "EndDate": ..., "Entity": "Sistema"}`.
Métricas: `VoluUtilDiarEner`, `CapaUtilDiarEner`, `AporEner`, `AporEnerMediHist`.

* **Los valores están anidados en `Items[].DailyEntities[]` con `Id == "Sistema"`,
  y vienen COMO CADENAS.** No existe un `DailyEntity` plano. Suponer lo contrario
  produce `TypeError: float() argument must be a string or a real number, not
  'NoneType'`.
* `VoluUtilDiarEner` no existe en `/hourly`, solo en `/daily`.
* **Siempre publicar la capacidad útil junto al porcentaje.** XM revisa
  `CapaUtilDiarEner` sin aviso — tres veces en cuatro días en octubre de 2026—, y
  una caída del embalse puede ser casi toda **cambio de denominador y no pérdida
  de agua**. En un caso, 0,80 de una caída de 1,06 puntos era denominador.

---

## 4. Regla de atribución (la más importante del proyecto)

> **Si la fuente no atribuye el hecho a El Niño, no se lo atribuyas tú.**
> Publícalo diciendo expresamente que la fuente no lo atribuye.

No es un detalle de estilo. Buena parte de lo que circula como «impacto de El
Niño» son cifras **reales, verificables y recientes** a las que alguien añadió el
eslabón causal. Una cifra real con una causa inventada **resiste la primera
comprobación mejor que una cifra falsa**, y por eso es más difícil de desmontar.

En una corrida típica, entre un tercio y la mitad de los hallazgos confirmados no
están atribuidos a El Niño por su propia fuente. Todos se publican diciéndolo.

---

## 5. Reciclaje: verificar la fecha del HECHO, no la de publicación

El modo de fallo dominante. Casos ya detectados y descartados — **no volver a
reportarlos como nuevos**:

| Cifra que circula | Fecha real |
|---|---|
| Minvivienda, «102 municipios con afectaciones en el servicio de agua» | feb 2020 |
| Minvivienda, «32 municipios con desabastecimiento» | ene 2020 |
| Minvivienda, «108 municipios sin agua potable» | feb 2019 |
| Gobernación de Nariño, PMU de incendios | sep 2024 |
| Fedegán, «$75.327 millones / 15.515 animales muertos» | corte 31-ago-2026 |
| Fedegán, «$122.400 millones en 45 días» | dic 2023 – ene 2024 |
| Minagricultura, «23.986 ha de cultivos afectadas» | evento 2018-19 / 2023-24 |
| «392.614 personas desplazadas» | son **animales** (Fedegán), no personas |
| OCHA, «+535.000 personas afectadas» | inundaciones ene-abr 2026, **no El Niño** |
| UNGRD, «155.000 familias damnificadas, +574%» | 25-mar-2026, **por lluvias**; la región más golpeada fue Córdoba por desbordamiento del Sinú |
| «Riesgo de racionamiento de energía en octubre, 5 departamentos» | 17-sep-**2025**, por mantenimiento de la regasificadora, no por El Niño |
| Gobernación del Atlántico, calamidad por sequía | 29-ene-2024 |
| Gobernación de Santander, «+20 municipios en calamidad» | 16-feb-2024 |
| «Inflación anual 11,44% impulsada por alimentos» | no corresponde al 6,24% vigente |
| UNGRD, «44.874 ha quemadas en septiembre» | septiembre **2024** |

---

## 6. Corregir el tablero cuando la realidad cambia

Si un hecho nuevo contradice algo ya publicado, **no se agrega al lado: se
corrige el ítem viejo**, se dice expresamente que cambió y **se conserva la cita
anterior** para que la evolución quede visible.

Ejemplo canónico: Emcali descartó el racionamiento en Cali el 31-ago y lo aplicó
el 22-sep. El tablero conserva el boletín del 31-ago citado, con la corrección al
lado.

Esto incluye **corregirse a sí mismo**. El historial del tablero contiene una
retractación por una cita inventada por un agente y aceptada sin abrir el PDF, y
una corrección de un conteo arrastrado durante cuatro días teniendo el PDF en
disco sin abrir. **Regla que salió de ahí: ninguna cita textual de un documento
oficial entra sin que el PDF esté descargado y consultado en disco.**

---

## 7. Bloqueos conocidos — no gastar tiempo reintentando

| Fuente | Estado |
|---|---|
| `presidencia.gov.co`, `dapre.presidencia.gov.co` | anti-bot Imperva. Verificar decretos por prensa que dé número y fecha explícitos |
| `portal.gestiondelriesgo.gov.co` páginas `.aspx` | 503 a lectura automatizada, pero **cargan con `curl` y user-agent de navegador** |
| API SharePoint de la UNGRD | **sí funciona** y lista el archivo de noticias por año; el endpoint `/$value` para el cuerpo devuelve 403 / `UnauthorizedAccessException`, así que solo se obtienen titular y fecha |
| `colombiacheck.com` | 403 por WebFetch, **carga con `curl` + user-agent**; su buscador no es accesible (302/404) |
| `cambiocolombia.com`, AFP Factual, EFE Verifica | 403 persistente |
| `superservicios.gov.co`, `tolima.gov.co`, `seguimiento.co` | muro anti-bot / 403 (el último incluso con curl) |
| `car.gov.co` | no entrega su boletín hidrológico |
| `minagricultura.gov.co/noticias` | 404 |
| `diariodelsur.com.co` | HTTP 522 |

Endpoint útil de la UNGRD:

```
https://portal.gestiondelriesgo.gov.co/_api/web/GetFolderByServerRelativeUrl('/Paginas/Noticias/2026')/Files?$select=Name,TimeCreated&$orderby=TimeCreated%20desc&$top=15
```

**Calendarios:** el boletín semanal SIPSA del DANE sale los **viernes** —confirmar
el número vigente antes de darlo por nuevo—; el IPC sale a comienzos de mes.

---

## 8. Dimensionamiento del Workflow de investigación

La fase B corre 7 agentes de búsqueda en paralelo y luego verifica cada hallazgo.
**La concurrencia real del entorno es de ~2 agentes a la vez**, no la que anuncia
el límite teórico. Eso define el dimensionamiento:

* **Una lente combinada por hallazgo** (fecha + cifra + atribución en un
  veredicto): ~53 agentes de verificación, ~60-90 min. **Es lo que funciona.**
* **Dos o tres lentes por hallazgo**: 106-159 agentes, más de tres horas. Se ha
  tenido que abortar y relanzar **cuatro veces** por esta razón.

Si hay que relanzar: `TaskStop` con el **task id** (no el run id) y luego
`Workflow({scriptPath, resumeFromRunId})` — los agentes de búsqueda ya terminados
**vuelven de caché** y no se pierde el tiempo de búsqueda.

**Efecto secundario a tener presente:** con una sola lente la tasa de refutación
baja (antes bastaba que uno de dos verificadores refutara). El filtro es menos
severo, no los hallazgos mejores. Hay que decirlo en la nota del día.

---

## 9. Deduplicar por HECHO, no por agente

Siete agentes traen el mismo hecho con textos distintos. Sin deduplicar, el
tablero publica el mismo racionamiento siete veces. Agrupar por:

1. **misma URL** (normalizada, sin fragmento ni query),
2. **mismo lugar + mismo tema** con similitud de texto moderada,
3. **mismo lugar + cifras compartidas** aunque el tema se etiquete distinto.

El documento más completo manda; los demás aportan sus fuentes como
corroboración. En producción: 53 confirmados → 29 registros; 19 → 13; 46 → 29.

**No sobre-fusionar los hechos nacionales:** «lluvia nacional», «récords» y
«alertas» pueden parecerse y ser hechos distintos.

---

## 10. Validación antes de publicar

`IDEAM_CITY` se reescribe completo en cada corrida. **Un error de sintaxis deja el
mapa y el explorador en blanco sin ningún aviso.** Obligatorio:

```bash
# extraer los bloques <script> y validarlos
node --check bloque.js
```

Más el balance de etiquetas (`div`, `section`, `tr`, `td`, `p`, `li`, `svg`,
`span`, `a`) y una relectura de `IDEAM_CITY` con `json.loads` para confirmar que
sigue teniendo las 58 entradas.
