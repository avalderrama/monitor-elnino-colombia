# -*- coding: utf-8 -*-
import re
h = open('board_v1.html', encoding='utf-8').read()
N = '&nbsp;'

def repl_tr(tid, new_html):
    global h
    pat = re.compile(r'<tr id="pron-%s">.*?</tr>' % tid, re.S)
    m = pat.search(h)
    assert m, 'row %s not found' % tid
    h = h[:m.start()] + new_html + h[m.end():]

TR = '<tr id="pron-%s"><td>%s</td><td>%s</td><td>%s</td><td><span class="badge b-ok">%s</span></td></tr>'

caribe_t = ('<b>Estaciones IDEAM, releídas 6-oct (dato del 4-oct):</b> <b>Manaure recupera el máximo del Caribe y se lleva además el máximo nacional con 37,2</b>'+N+'<b>°C</b> — la estación que ayer figuraba «sin refrescar» vuelve a reportar por segunda vez en tres días—, seguida de Los Álamos (San Sebastián de Buenavista, Magdalena) 34,8'+N+'°C, Aeropuerto Rafael Núñez (Cartagena) 34,4, Colegio Agropecuario (Pailitas) y Aeropuerto Alfonso López (Valledupar) empatados en 34,2, Escuela Agrícola Carraipía (Maicao) 34,0 y Villa Rosa (Valledupar) 33,8, con 20 estaciones reportando. <b>El valor de Manaure es el que el propio ITD 278 encabeza en su listado de estaciones por encima de 35'+N+'°C.</b> Anomalía media &gt;+2,0'+N+'°C en el oriente de la región (jul-2026)')

caribe_p = ('<b>Observado jul-2026:</b> muy por debajo del promedio en el centro y sur de la región, incluida el área insular. <b>Lluvia hoy — y aquí está el dato del día: CERO. Ni una sola de las 92 estaciones del Caribe registró lluvia</b>, frente al 48% de ayer. '
 'Es la primera vez en esta serie que la región entera aparece en blanco, y no es la única: la Orinoquía (41 estaciones) y la Insular (3) también marcan cero. <b>Entre las tres suman 136 estaciones sin un milímetro.</b> '
 '<b>Salvedad obligatoria, y es la de siempre:</b> en este servicio un 0'+N+'mm no se distingue de «la estación no reportó», y 525 de los 656 pluviómetros son de lectura manual — así que lo que se puede afirmar es que <i>ninguna estación del Caribe reportó lluvia</i>, no que no cayera una gota en toda la región. '
 '<b>Y las alertas acompañan en direcciones opuestas.</b> La <b>Ciénaga Grande de Santa Marta sale de la alerta hidrológica roja tras un solo día</b> —entró ayer como la primera roja del Magdalena de la serie—, mientras <b>Bajo San Jorge'+N+'–'+N+'La Mojana</b> (Bolívar) repite por enésima jornada. En incendios la Alta Guajira vuelve a subir: <b>Manaure pasa de amarilla a naranja</b> y Uribia se mantiene en naranja; <b>Cartagena de Indias entra en amarilla</b>. '
 'En deslizamientos <b>Santa Marta sigue en roja</b>, <b>Tiquisio baja de roja a naranja</b>, Pailitas baja a amarilla y <b>Aguachica y Valledupar salen por completo del listado</b>. '
 '<b>Pronóstico IDEAM SON:</b> por debajo de lo normal en septiembre (&gt;70%), octubre y noviembre (&gt;50%) en el Caribe continental; excepciones por encima en Providencia (sep, nov) y puntos de La Guajira (sep) y Córdoba (oct)')

andina_t = ('<b>Estaciones IDEAM, releídas 6-oct (dato del 4-oct):</b> el calor rebota <b>0,8'+N+'°C</b> y la máxima nacional <b>sale de la región Andina</b> por primera vez en cinco días, pero el segundo puesto se queda aquí: <b>Hacienda Túnez (Fredonia, Antioquia) 37,0</b>'+N+'<b>°C</b>, seguida de San Alfonso (Villavieja, Huila) 36,8, <b>Anchique (Natagaima, Tolima) 36,6</b>, Aeropuerto Benito Salas (Neiva) 36,0, <b>Jabalcón (Saldaña) 35,2</b> —que vuelve a reportar tras un día muda— y Cinera-Villa Olga (Cúcuta) 35,0, con 85 estaciones reportando. '
 '<b>Vuelven a haber estaciones por encima de 37'+N+'°C</b>: dos, frente a ninguna ayer. Anomalía &gt;+2,0'+N+'°C en sectores de Antioquia, Santander, Risaralda, Cundinamarca y Tolima (jul-2026)')

andina_p = ('<b>Observado jul-2026:</b> por encima en el altiplano cundiboyacense, Huila y Tolima. <b>Lluvia hoy — la región se recupera del 18% al 30,4%</b>, <b>114 de 375</b> estaciones, y se queda con el máximo nacional: <b>Pez Fresco (Santa Rosa de Cabal, Risaralda) con 90,0'+N+'mm</b>, el valor más alto del país desde los 148,6 de Carepa. Detrás, Aeropuerto Furatena (Quípama, Boyacá) 52,5'+N+'mm, Salamina (Caldas) 36,0, Ataco y Cunday (Tolima) 31,0, Cruz Roja (Ibagué) 26,0 y La Pintada Alertas (Antioquia) 25,9. '
 '<b>Y el hallazgo del día está aquí, en dos piezas.</b> <b>Primera:</b> <b>Antioquia pasa de 14 a 43 municipios en alerta roja de deslizamiento</b> —más de la mitad del total nacional, y 29 entradas nuevas en un día—, con la huella saliéndose del eje de Urabá hacia el norte y el Valle de Aburrá: entran <b>Medellín</b>, Bello, Urrao, Yarumal, Santa Rosa de Osos, Belmira, Sopetrán, Liborina, Ebéjico, Heliconia, Anzá, Buriticá, Caicedo, Giraldo, Olaya, Peque, Sabanalarga, Toledo, Angostura, Briceño, Concordia, Betulia, Entrerríos, Remedios, Armenia (Ant.), San Jerónimo, San Pedro de los Milagros, San José de la Montaña, San Andrés de Cuerquía y Vigía del Fuerte, además de los de Urabá que ya estaban. '
 '<b>Segunda, y cierra la cadena en un solo municipio:</b> <b>Santa Rosa de Cabal</b> marca el máximo nacional de lluvia <i>y</i> entra en alerta roja de deslizamiento el mismo día. '
 '<b>El récord del día también es de aquí, y es de clima frío:</b> la estación <b>La Aldea, en Medellín, superó su máximo histórico de octubre con 29,0'+N+'°C</b> (antes 28,6 del 01/10/2023) — la misma ciudad que hoy entra en alerta roja de ladera. '
 'En incendios, <b>Neiva, Íquira y Rivera (Huila) y Cáqueza (Cundinamarca) entran en naranja</b>, <b>Sabana de Torres baja a amarilla</b> y entran en amarilla Girón, Cácota, Mutiscua, Silos y Ambalema; <b>Pesca (Boyacá) sale</b>. '
 '<b>Pronóstico IDEAM SON:</b> por debajo de lo normal los tres meses (sep &gt;70%, oct-nov &gt;50%); solo zonas puntuales de Antioquia con probabilidad por encima en octubre')

pac_t = ('<b>Estaciones IDEAM, releídas 6-oct (dato del 4-oct):</b> el primer puesto regional <b>vuelve al Chocó y lo hace rompiendo un récord</b>: <b>Aeropuerto El Caraño (Quibdó) 34,5</b>'+N+'<b>°C</b>, que supera su máximo histórico de octubre (34,2 del 05/10/2005) — <b>el segundo récord de octubre de esa misma estación en cinco días</b>, tras los 34,3 del 1.º—, y es un salto de <b>+5,7'+N+'°C</b> frente a los 28,8 de ayer. '
 'Le sigue el <b>Aeropuerto Alfonso Bonilla (Palmira) con 33,4</b>'+N+'<b>°C, que también rompe récord de octubre</b> (33,2 del 27/10/2018), y después Palmira ICA 33,0, Aeropuerto de Guapi 32,8, Cenicaña (Florida) 32,4 y Lomitas (Santander de Quilichao) 31,6, con 23 estaciones reportando. Anomalía &gt;+2,0'+N+'°C en sectores de Nariño (jul-2026)')

pac_p = ('<b>Observado jul-2026:</b> por debajo en el centro-oriente de Nariño; normal en el resto. <b>Lluvia hoy — la región recupera el primer puesto nacional: del 28% al 42,1%</b>, <b>48 de 114</b> estaciones. Encabezan Cumbarco (Sevilla, Valle) 43,6'+N+'mm, Junín (Barbacoas, Nariño) 35,0, Palmira ICA 34,4, Ceilán (Bugalagrande) 30,0, Venta de Cajibío (Cauca) 26,7 y Palmasola (Cartago) 26,0. '
 '<b>Y el movimiento grande del día es hidrológico y va a favor:</b> de las siete alertas rojas que la vertiente del Pacífico sur mantuvo sin un solo cambio durante cuatro días, <b>seis se levantaron</b> — salen <b>Río Tola, Río Telembí, Río Patía Medio y Río Patía Bajo</b> (Nariño) y <b>Río Timbiquí y Río San Juan del Micay</b> (Cauca), y <b>solo queda Río Saija</b>. '
 '<b>El Chocó también cede y pierde el primer puesto nacional de deslizamientos por primera vez en esta serie:</b> baja de 20 a <b>13 de sus 30 municipios</b> en rojo, por detrás de los 43 de Antioquia, con <b>Quibdó todavía en roja</b> y salidas en Acandí, Unguía, Alto Baudó, Istmina, Medio San Juan, Sipí y Unión Panamericana. Nariño baja a 5 rojas, el Valle se queda en 3 y el Cauca en 3. '
 '<b>Pronóstico IDEAM SON:</b> sep por debajo (&gt;70%) salvo puntos del Chocó por encima; oct Chocó por debajo, Cauca y Nariño con puntos por encima (~50%); nov por debajo en general con el sur de la región por encima (~50%)')

ori_t = ('<b>Estaciones IDEAM, releídas 6-oct (dato del 4-oct):</b> <b>Paz de Ariporo (Casanare) 35,0</b>'+N+'<b>°C</b> se lleva el primer puesto regional, seguida de un empate en 34,6 entre Cumaribo y el Aeropuerto Puerto Carreño (Vichada), Las Gaviotas (Cumaribo) 34,2, La Macarena (Meta) 33,2 y Módulos (Orocué) 33,1. Quince estaciones con dato. Anomalía &gt;+2,0'+N+'°C en Casanare (jul-2026)')

ori_p = ('<b>Observado jul-2026:</b> por encima en el suroccidente; muy por debajo en el norte de Arauca. <b>Lluvia hoy — tercer día de repliegue y llega al fondo: CERO de 41 estaciones</b>, desde el 21% de ayer y el 79% de hace dos días. '
 '<b>Es la segunda de las tres regiones que hoy no registran una sola lectura de lluvia</b>, junto con el Caribe y la Insular. <b>Servita (Villavicencio) repite en 0'+N+'mm</b> por segundo día. '
 '<b>Pero las alertas de ladera ceden:</b> <b>Villavicencio y Yopal bajan de roja a naranja</b> —las dos llevaban días en el nivel máximo— y el <b>Meta baja de 4 a 2 municipios en rojo</b> (quedan Cubarral y El Castillo, dos de los tres que la UNGRD inspeccionó en el río Ariari el 2-oct). <b>Fortul, Saravena y Tame (Arauca) siguen en amarilla.</b> '
 '<b>Pronóstico IDEAM SON:</b> sectores por encima de lo normal en septiembre (&gt;60%) y noviembre (~50%); en octubre puntos de Meta y Guaviare por encima y el resto por debajo; flanco occidental por debajo en noviembre')

ama_t = ('<b>Estaciones IDEAM, releídas 6-oct (dato del 4-oct):</b> Puerto Inírida (Guainía) <b>35,6</b>'+N+'<b>°C</b> —valor que el ITD 278 confirma en su listado—, Valparaíso (Caquetá) 34,6'+N+'°C, Mitú (Vaupés) 34,0, El Trueno (El Retorno, Guaviare) 32,8 y Aeropuerto Vásquez Cobo (Leticia) 32,5. <b>Cinco estaciones con dato</b>, la red más delgada del país')

ama_p = ('<b>Observado jul-2026:</b> sin mención específica en el Boletín 216. <b>Lluvia hoy — sigue cediendo: del 41% al 22,6%</b>, <b>7 de 31</b> estaciones. Encabezan Mitú (Vaupés) 13,0'+N+'mm, Valparaíso (Caquetá) 10,0, <b>Larandia (Florencia) 6,0</b> —vuelve a reportar tras un día muda—, Puerto Ospina (Puerto Leguízamo) 5,0 y Balsayaco (Santiago) 0,6. '
 '<b>Y las alertas de ladera se relajan:</b> el <b>Putumayo baja de 3 a 1 municipio en alerta roja de deslizamiento</b> —solo queda <b>Mocoa</b>; salen San Miguel y Villagarzón— y <b>Florencia baja de roja a naranja</b>, con lo que el Caquetá se queda sin rojas. '
 '<b>Pronóstico IDEAM SON:</b> áreas menores por encima de lo normal en septiembre (&gt;60%); en octubre puntos de Guainía, Vaupés, Caquetá y Amazonas por encima (~50%) y sectores por debajo; el sur con lluvias en ascenso')

ins_t = ('<b>Estaciones IDEAM, releídas 6-oct (dato del 4-oct):</b> Aeropuerto El Embrujo (isla de Providencia) <b>32,1</b>'+N+'<b>°C</b> y Aeropuerto Sesquicentenario (isla de San Andrés) 32,0'+N+'°C. <b>Providencia pasa al primer puesto del archipiélago</b> por medio grado, y las dos islas quedan por encima de todo el Caribe continental salvo Manaure, Los Álamos y Cartagena')

ins_p = ('<b>Observado jul-2026:</b> por debajo del promedio. <b>Lluvia hoy — se rompe la racha: CERO de 3 estaciones</b>, después de <b>cinco días consecutivos con el 100% de la red</b>. '
 '<b>Es la tercera de las tres regiones que hoy no reportan una sola lectura de lluvia</b>, y en una red de tres pluviómetros el paso del 100% al 0% en un día es tan fácil como que las tres marquen cero — razón de más para leer esta región con cuidado y no como una tendencia. '
 'Las <b>2 subzonas hidrológicas del archipiélago siguen en amarilla</b>, y sigue siendo la zona que el Boletín ENOS marca con el mayor déficit del Caribe. <b>Pronóstico IDEAM SON:</b> Providencia con probabilidad por encima de lo normal en septiembre y noviembre; el área insular por debajo en octubre')

BOK = '✅ IDEAM (REST + Boletín 216)'
repl_tr('caribe',   TR % ('caribe','Caribe', caribe_t, caribe_p, BOK))
repl_tr('andina',   TR % ('andina','Andina', andina_t, andina_p, BOK))
repl_tr('pacifica', TR % ('pacifica','Pacífica (Chocó, Valle, Cauca, Nariño)', pac_t, pac_p, BOK))
repl_tr('orinoquia',TR % ('orinoquia','Orinoquía', ori_t, ori_p, BOK))
repl_tr('amazonia', TR % ('amazonia','Amazonía', ama_t, ama_p, '✅ IDEAM (REST + predicción sep)'))
repl_tr('insular',  TR % ('insular','Insular (San Andrés y Providencia)', ins_t, ins_p, BOK))

open('board_v1.html','w',encoding='utf-8').write(h)
print('region table rebuilt; len', len(h))
