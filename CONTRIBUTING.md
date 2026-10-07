# Cómo colaborar

Gracias por el interés. Este monitor vive o muere por su credibilidad, así que
las reglas de abajo no son burocracia: son lo que lo distingue de un agregador.

## Las tres reglas que no se negocian

1. **No atribuyas a El Niño lo que la fuente no atribuye.** Si una nota reporta
   un corte de agua y no menciona el fenómeno, el hallazgo se publica diciendo
   expresamente que la fuente no lo atribuye. Una cifra real con una causa
   inventada es más dañina que una cifra falsa, porque resiste la primera
   comprobación.

2. **Verifica la fecha del hecho, no la del portal.** Antes de agregar cualquier
   cifra, abre la fuente y busca la fecha dentro del texto. Revisa la [lista de
   casos ya descartados](docs/METODOLOGIA.md#5-reciclaje-verificar-la-fecha-del-hecho-no-la-de-publicación)
   antes de reportar algo como nuevo.

3. **Ninguna cita textual de un documento oficial entra sin el PDF en disco.**
   Esta regla existe porque se violó: el tablero publicó durante cinco días una
   cita inventada que nadie había comprobado contra el documento.

## Qué ayuda más ahora mismo

* **Fuentes territoriales.** El punto ciego persistente son los reportes
  operativos de gobernaciones y alcaldías: el monitor ve las alertas del IDEAM
  pero a menudo no encuentra qué hizo el municipio.
* **Desbloquear fuentes.** Varias entidades están tras muros anti-bot
  ([lista](docs/METODOLOGIA.md#7-bloqueos-conocidos--no-gastar-tiempo-reintentando)).
  Cualquier vía legítima de lectura es bienvenida.
* **Extracción de los PDF del IDEAM.** Las tablas de embalses y de sensación
  térmica vienen como imagen; las del BAICV pierden la agrupación por nivel al
  extraerse. Eso ya impidió resolver una discrepancia real.
* **Pruebas.** Hoy no hay suite de pruebas. Es la carencia más grande del
  repositorio.

## Al abrir un PR

* Di **qué fuente** usaste y **de qué fecha es el hecho**.
* Si tocas el tablero, confirma que pasaste los bloques `<script>` por
  `node --check` y que `IDEAM_CITY` sigue teniendo sus 58 entradas.
* Si corriges algo ya publicado, **conserva la cita anterior** y di que cambió.
  No borramos el error: lo dejamos visible al lado de la corrección.
* No subas `data/raw/` de días nuevos: son cientos de megas y se regeneran con
  `fetch_ideam.py`.

## Reportar un error del tablero

Abre un issue con la URL del ítem, qué dice, qué debería decir y la fuente que lo
respalda. Los errores del propio monitor se corrigen **en el tablero, a la
vista**, no en silencio.
