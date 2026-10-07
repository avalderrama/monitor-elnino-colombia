export const meta = {
  name: 'monitor-elnino-colombia',
  description: 'Investiga el estado de El Nino en Colombia por fuente, con verificacion adversarial de cada hallazgo',
  phases: [
    { title: 'Fuentes', detail: '7 agentes, uno por tipo de fuente (IDEAM, UNGRD, agro/precios, prensa nacional, prensa regional, desinformacion, gobierno)' },
    { title: 'Verificar', detail: 'verificacion adversarial de cada hallazgo: fecha del hecho, atribucion a El Nino, cifra' },
  ],
}

const HOY = args && args.hoy ? args.hoy : '2026-10-06'

const CONTEXTO = `
Hoy es ${HOY}. Eres parte de un monitor diario del fenomeno de El Nino en COLOMBIA.
Usa WebSearch (carga el schema con ToolSearch "select:WebSearch,WebFetch") y WebFetch.
Busca en espanol. Responde en espanol.

REGLA CRITICA — CONTENIDO RECICLADO: el modo de fallo dominante son notas viejas
republicadas como si fueran de hoy. Verifica siempre la fecha del HECHO, no la fecha de
publicacion del portal. Casos ya detectados y DESCARTADOS en corridas anteriores (no los
vuelvas a reportar como nuevos):
- Minvivienda "102 municipios con afectaciones en el servicio de agua" -> feb 2020.
- Minvivienda "32 municipios con desabastecimiento" -> ene 2020.
- Gobernacion de Narino, PMU de incendios y escasez de agua -> sep 2024.
- Fedegan "$75.327 millones y 15.515 animales muertos" -> corte 31-ago-2026.
- "23.986 ha de cultivos afectadas" (Minagricultura) -> evento 2018-19 / 2023-24.
- "392.614 personas desplazadas" -> son ANIMALES (Fedegan), no personas.
- "+535.000 personas afectadas" (OCHA) -> inundaciones ene-abr 2026, no El Nino.
Hechos YA PUBLICADOS en el tablero (reportalos solo si hay novedad o cambio de estado):
racionamiento de agua en Cali aplicado por Emcali el 22-sep-2026 (antes descartado el
31-ago); racionamiento en Medellin; anuncio de emergencia economica.

REGLA: si una fuente no atribuye el hecho a El Nino / sequia / calor extremo, NO se lo
atribuyas tu. Dilo tal cual.

Prioriza hechos ocurridos entre el 28-sep-2026 y ${HOY}. Un hecho de hace mas de 10 dias
solo vale si es un cambio de estado o una cifra oficial nueva.

BLOQUEOS YA VERIFICADOS (no pierdas tiempo): presidencia.gov.co da anti-bot Imperva;
las paginas .aspx de portal.gestiondelriesgo.gov.co dan 503 (pero su API de SharePoint
si funciona: https://portal.gestiondelriesgo.gov.co/_api/web/GetFolderByServerRelativeUrl('/Paginas/Noticias/2026')/Files?$select=Name,TimeCreated&$orderby=TimeCreated%20desc&$top=15 );
cambiocolombia.com, AFP Factual y EFE Verifica dan 403; Colombiacheck da 403 por WebFetch
pero carga con curl y user-agent de navegador.

Devuelve COMO MAXIMO 8 hallazgos, los mas importantes y mas verificables. Es mejor
devolver 3 hallazgos solidos que 8 dudosos. Si no encuentras nada nuevo, devuelve lista vacia.
`

const FUENTES = [
  { key: 'ideam', label: 'IDEAM', prompt: `${CONTEXTO}

TU FUENTE: IDEAM (oficial). Revisa:
- El boletin ENOS / Prediccion Climatica mas reciente (ideam.gov.co): en que fase esta el
  ENOS hoy (El Nino, La Nina, neutral), probabilidades, y el pronostico de lluvias por region
  para oct-nov-dic 2026.
- Comunicados y alertas del IDEAM de los ultimos 10 dias: alertas por incendios de cobertura
  vegetal, alertas hidrologicas por niveles bajos de rios, avisos de temperaturas maximas.
- El Informe Tecnico Diario del IDEAM (PDF diario, en ideam.gov.co/file-download/download/public/<id>):
  trae temperaturas maximas/minimas por estacion, RECORDS HISTORICOS ROTOS y pronostico de
  amenaza por incendios municipio a municipio. Busca el del dia o el mas reciente e intenta
  leerlo. Si rompio un record de temperatura en alguna estacion, eso es un hallazgo de alta prioridad.
- Tambien mira la cuenta @IDEAMColombia si puedes.
Reporta la FASE del ENOS explicitamente como uno de los hallazgos, aunque no haya cambiado.` },

  { key: 'ungrd', label: 'UNGRD y emergencias', prompt: `${CONTEXTO}

TU FUENTE: UNGRD y declaratorias de emergencia (oficial). Revisa:
- La API de SharePoint de la UNGRD (ver el enlace arriba) para los titulares y fechas de las
  noticias mas recientes de 2026. Luego busca en prensa el contenido de los titulares relevantes.
- Declaratorias de CALAMIDAD PUBLICA por sequia, desabastecimiento de agua o incendios en
  cualquier municipio o departamento de Colombia, en los ultimos 15 dias. Busca por
  "calamidad publica" + sequia / desabastecimiento / incendios + 2026.
- Declaratorias de desastre, alertas rojas y naranjas vigentes.
- Cifras de damnificados: personas y familias afectadas, con fecha de corte.
- Muertes de personas atribuidas a sequia, calor, incendios o falta de agua.
- Reportes de incendios de cobertura vegetal activos: hectareas, municipios.
Para cada declaratoria: numero de decreto o resolucion, municipio, departamento, fecha.` },

  { key: 'agro', label: 'Agro, precios y alimentos', prompt: `${CONTEXTO}

TU FUENTE: alimentos, precios y cosechas. Revisa:
- El boletin semanal SIPSA del DANE (sale los VIERNES; dane.gov.co). Confirma el NUMERO del
  boletin vigente y su fecha antes de darlo por nuevo. Que productos subieron y bajaron de
  precio, en que ciudades, y si el DANE atribuye el movimiento a clima/sequia.
- El IPC de alimentos de septiembre 2026 del DANE si ya salio (suele salir a inicios de mes).
- Minagricultura: cosechas malogradas, hectareas afectadas por sequia, censos de afectacion.
  OJO con cifras recicladas de eventos anteriores.
- Gremios: Fedegan (ganaderia, mortalidad de animales, pastos), Fedearroz, Fedecafe,
  Fenavi, Asocana, Fedepapa, Augura. Busca declaraciones de los ultimos 10 dias.
- Desabastecimiento o alzas en plazas de mercado (Corabastos y centrales regionales).
Para cada hallazgo: producto, zona (municipio/departamento), magnitud con cifra, fecha de corte.` },

  { key: 'prensa-nacional', label: 'Prensa nacional', prompt: `${CONTEXTO}

TU FUENTE: prensa nacional colombiana (NO oficial; marca badge de prensa). Revisa
El Tiempo, El Espectador, Semana, La Republica, Portafolio, Blu Radio, W Radio, Caracol,
RCN, Infobae Colombia, La Silla Vacia.
Busca de los ultimos 7-10 dias: sequia, racionamiento de agua, desabastecimiento,
incendios forestales, calor extremo, embalses y nivel del Guavio/Chingaza/Betania,
generacion de energia y riesgo de apagon, precio de la energia en bolsa, impactos en
salud (IRA, EDA, golpe de calor), educacion (clases suspendidas) y transporte fluvial
(Magdalena, Meta, Atrato: restricciones de navegacion por bajos niveles).
Para cada hallazgo: titular, medio, URL, fecha de PUBLICACION y fecha del HECHO.` },

  { key: 'prensa-regional', label: 'Prensa regional', prompt: `${CONTEXTO}

TU FUENTE: prensa REGIONAL colombiana (NO oficial). Esta es la fuente que mas aporta
hechos nuevos, porque los efectos locales no llegan a la prensa nacional. Revisa por region:
- Caribe: El Heraldo (Barranquilla), El Universal (Cartagena), La Opinion (Cucuta),
  Hoy Diario del Magdalena, Seguimiento.co (Santa Marta), La Guajira: desabastecimiento
  en Uribia, Manaure, Maicao, Riohacha.
- Pacifico: El Pais (Cali), Diario del Cauca, Diario del Sur (Pasto), Chocó7dias.
- Andina: El Colombiano (Medellin), La Patria (Manizales), Vanguardia (Bucaramanga),
  El Nuevo Dia (Ibague), La Cronica (Armenia), Q'hubo, Extra.
- Orinoquia y Amazonia: Llano Siete Dias, Periodico del Meta, Caqueta.
Busca: racionamientos de agua municipales nuevos, carrotanques, pozos secos, incendios,
rios secos, muerte de ganado y de fauna, cultivos perdidos, acueductos rurales sin agua.
Para cada hallazgo: municipio, departamento, cifra si la hay, medio, URL, fecha del hecho.` },

  { key: 'desinformacion', label: 'Desinformacion', prompt: `${CONTEXTO}

TU FUENTE: desinformacion y verificacion de datos. Revisa:
- Colombiacheck (colombiacheck.com) — da 403 por WebFetch pero SI carga con curl y
  user-agent de navegador; usa Bash con curl si WebFetch falla.
- La Silla Vacia (Detector de Mentiras), Maldita.es si cubre Colombia, Reuters Fact Check,
  Snopes si aplica.
- Busca rumores circulando sobre: cortes de agua masivos falsos, apagones nacionales
  anunciados sin fuente, cifras inflades de muertos o damnificados, videos de sequias de
  otros paises presentados como Colombia, supuestos anuncios del gobierno que no existen.
- Tambien: cifras oficiales mal citadas por medios (por ejemplo confundir animales con
  personas, o usar cortes viejos sin fecha).
Para cada hallazgo: que se afirma, quien lo desmiente, URL del desmentido, fecha.
Si no hay desinformacion nueva verificable, devuelve lista vacia — no inventes.` },

  { key: 'gobierno', label: 'Respuesta del gobierno', prompt: `${CONTEXTO}

TU FUENTE: respuesta del Estado. DISTINGUE SIEMPRE LO ANUNCIADO DE LO EJECUTADO, con fecha.
Revisa:
- Gobierno nacional: Presidencia (bloqueada: verifica decretos por prensa que de NUMERO y
  FECHA explicitos), Minambiente, Minvivienda, Minagricultura, Minminas, Minsalud, UNGRD,
  CREG y XM (energia). Busca: decretos, emergencia economica, recursos girados vs anunciados,
  planes de abastecimiento, importacion de energia, resoluciones de la CREG.
- Gobernaciones y alcaldias: Valle del Cauca y Cali (Emcali), Antioquia y Medellin (EPM),
  Bogota (EAAB), Atlantico, Bolivar, Magdalena, La Guajira, Santander, Tolima, Huila,
  Narino, Cauca, Cesar, Cordoba.
- Para cada medida: QUE se anuncio, QUIEN, CUANDO, y si hay evidencia de EJECUCION
  (recursos efectivamente girados, carrotanques efectivamente entregados, decreto
  efectivamente firmado y publicado). Si solo hay anuncio, dilo y anota que hay que
  verificar despues.
- Senala explicitamente lo que queda PENDIENTE DE VERIFICAR en la proxima corrida.` },
]

const HALLAZGOS_SCHEMA = {
  type: 'object',
  properties: {
    hallazgos: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          texto: { type: 'string', description: 'El hecho en 1-3 frases, con cifra si la hay' },
          categoria: { type: 'string', description: 'efecto | emergencia | damnificados | muerte | alimentos | cosechas | gobierno | desinformacion' },
          departamento: { type: 'string' },
          municipio: { type: 'string', description: 'vacio si es departamental o nacional' },
          fecha_hecho: { type: 'string', description: 'AAAA-MM-DD del HECHO, no de la publicacion' },
          fecha_publicacion: { type: 'string' },
          oficial: { type: 'boolean', description: 'true si la fuente es oficial (IDEAM, UNGRD, DANE, ministerio, gobernacion, alcaldia)' },
          fuente_nombre: { type: 'string' },
          fuente_url: { type: 'string' },
          cifra: { type: 'string', description: 'la cifra clave aislada, vacio si no hay' },
          atribuido_a_elnino: { type: 'boolean', description: 'true solo si la FUENTE lo atribuye a El Nino/sequia/calor' },
          confianza: { type: 'string', description: 'alta | media | sin verificar' },
          por_verificar: { type: 'string', description: 'que queda pendiente de confirmar, vacio si nada' },
        },
        required: ['texto', 'categoria', 'departamento', 'fecha_hecho', 'oficial', 'fuente_nombre', 'fuente_url', 'atribuido_a_elnino', 'confianza'],
      },
    },
    bloqueos: { type: 'array', items: { type: 'string' }, description: 'fuentes que no pudiste leer y por que' },
    nota: { type: 'string', description: 'contexto breve de que revisaste' },
  },
  required: ['hallazgos', 'bloqueos', 'nota'],
}

const VERDICTO_SCHEMA = {
  type: 'object',
  properties: {
    refutado: { type: 'boolean', description: 'true si el hallazgo NO debe publicarse' },
    razon: { type: 'string' },
    fecha_hecho_corregida: { type: 'string', description: 'la fecha real del hecho si la original estaba mal, vacio si estaba bien' },
    cifra_corregida: { type: 'string', description: 'vacio si la cifra estaba bien' },
    texto_corregido: { type: 'string', description: 'version corregida del texto si hace falta, vacio si no' },
    confianza_final: { type: 'string', description: 'alta | media | sin verificar' },
  },
  required: ['refutado', 'razon', 'confianza_final'],
}

const LENTE_COMBINADA = `LENTE UNICA Y COMBINADA. Tu unico trabajo es intentar REFUTAR este hallazgo.
Aplica los tres filtros siguientes; si FALLA CUALQUIERA, refutado=true. Por defecto refuta.

(1) FECHA DEL HECHO. Abre la URL. Busca la fecha real del hecho dentro del texto (no la de
publicacion ni la del pie de pagina). Comprueba si la misma cifra aparece en notas de 2020, 2023,
2024 o principios de 2026. Si el hecho ocurrio antes del 1-sep-2026 y no es un cambio de estado
nuevo, refuta. Si no puedes abrir la URL ni confirmar la fecha por otra via, refuta.

(2) CIFRA. Verifica que la cifra exista literalmente en la fuente y no este redondeada, inflada o
confundida (animales vs personas, familias vs personas, hectareas vs municipios, millones vs miles).
Verifica tambien que la entidad citada sea la que de verdad dio el dato.

(3) ATRIBUCION. Verifica si la fuente REALMENTE atribuye el hecho a El Nino, sequia o calor extremo,
y no a inundaciones, a un problema de infraestructura, a un dano en una bocatoma o a un conflicto.
IMPORTANTE: que la fuente NO lo atribuya a El Nino no es por si solo motivo de refutacion — en ese
caso NO refutes por esto, pero dilo expresamente en la razon y escribe el texto_corregido dejando
constancia de que la fuente no atribuye el hecho al fenomeno. Solo refuta por atribucion si el
hallazgo afirma una causa que la fuente contradice.`

const resultados = await pipeline(
  FUENTES,
  (f) => agent(f.prompt, { label: `fuente:${f.key}`, phase: 'Fuentes', schema: HALLAZGOS_SCHEMA }),
  (res, f) => {
    if (!res || !res.hallazgos || res.hallazgos.length === 0) {
      return { fuente: f.key, bloqueos: (res && res.bloqueos) || [], nota: (res && res.nota) || '', confirmados: [], descartados: 0 }
    }
    const items = res.hallazgos.slice(0, 8)
    return parallel(items.map((h, i) => () =>
      agent(
        `${LENTE_COMBINADA}

Hoy es ${HOY}. Carga WebSearch/WebFetch con ToolSearch "select:WebSearch,WebFetch". Tambien
puedes usar Bash con curl y user-agent de navegador si WebFetch falla con 403.

HALLAZGO A REFUTAR:
texto: ${h.texto}
categoria: ${h.categoria}
lugar: ${h.municipio || '(sin municipio)'}, ${h.departamento}
fecha del hecho declarada: ${h.fecha_hecho}
fecha de publicacion declarada: ${h.fecha_publicacion || '(no dada)'}
cifra: ${h.cifra || '(ninguna)'}
fuente: ${h.fuente_nombre} — ${h.fuente_url}
atribuido a El Nino por la fuente: ${h.atribuido_a_elnino}

Responde con el veredicto estructurado. Se escueto en la razon (1-2 frases).`,
        { label: `verif:${f.key}:${i}`, phase: 'Verificar', schema: VERDICTO_SCHEMA }
      )
        .then((v) => {
          if (!v || v.refutado) return null
          return Object.assign({}, h, {
            texto: v.texto_corregido || h.texto,
            fecha_hecho: v.fecha_hecho_corregida || h.fecha_hecho,
            cifra: v.cifra_corregida || h.cifra,
            confianza: v.confianza_final || h.confianza,
            fuente_agente: f.key,
            notas_verificacion: v.razon || '',
          })
        })
    )).then((vs) => ({
      fuente: f.key,
      bloqueos: res.bloqueos || [],
      nota: res.nota || '',
      confirmados: vs.filter(Boolean),
      descartados: items.length - vs.filter(Boolean).length,
    }))
  }
)

const ok = resultados.filter(Boolean)
const confirmados = ok.flatMap((r) => r.confirmados)
const bloqueos = [...new Set(ok.flatMap((r) => r.bloqueos))]
const porFuente = ok.map((r) => ({ fuente: r.fuente, confirmados: r.confirmados.length, descartados: r.descartados, nota: r.nota }))

log(`Confirmados: ${confirmados.length} | fuentes: ${ok.length}/${FUENTES.length}`)

return { hoy: HOY, confirmados, bloqueos, porFuente }
