# -*- coding: utf-8 -*-
import re
h = open('board_v1.html', encoding='utf-8').read()
N = '&nbsp;'
def rep(old, new, label=''):
    global h
    assert h.count(old) == 1, 'count=%d for %s' % (h.count(old), label)
    h = h.replace(old, new)

# ---------- map figcaption (tempMap) ----------
old = re.search(r'<figcaption>Cada punto es una estación/ciudad con lectura directa del IDEAM.*?</figcaption>', h, re.S).group(0)
new = ('<figcaption>Cada punto es una estación/ciudad con lectura directa del IDEAM, <b>refrescada el 6-oct-2026</b> contra los servicios REST Datos_TMaxima y Datos_Precipitacion (mismo dato que su ficha en la sección 03). '
 '<b>El dato es del 4 de octubre</b>, dos días antes de la consulta, fechado contra el Informe Técnico Diario N.º 278. '
 'Hoy <b>4 de las 90 lecturas</b> no se refrescaron y conservan su última cifra, marcadas «sin refrescar hoy» en su tooltip y en su ficha — <b>iguala el mejor resultado de la serie</b>: tres de temperatura (Demostración Granja en Ortega, sin reportar desde el 23-sep; El Callao en Valledupar, desde el 1-oct; y una nueva de hoy, <b>Carmen de Tonchalá</b> en Cúcuta) y una de lluvia (<b>El Común</b> en Pupiales). '
 '<b>Y volvieron a reportar seis, un récord de la serie:</b> <b>Manaure</b> —que además se llevó el máximo nacional con 37,2'+N+'°C—, <b>Jabalcón</b> (Saldaña), <b>Los Álamos</b> (San Sebastián de Buenavista) y <b>Surbata Bonza</b> (Duitama) en temperatura, y <b>Colegio Agropecuario</b> (Pailitas) y <b>Larandia</b> (Florencia) en lluvia. '
 'Es la contracara exacta de la lección que esta caja escribió ayer: una estación muda no es una estación seca, y hoy cuatro de las que callaban volvieron con dato. '
 '<b>Salvedad de Cúcuta, que se repite:</b> Carmen de Tonchalá no reportó, pero el Aeropuerto Camilo Daza y Cinera-Villa Olga, del mismo municipio, sí — la ficha queda marcada como obsoleta aunque la ciudad tenga dato. '
 '<b>Límite importante de la lluvia, y hoy pesa más que nunca:</b> el punto muestra la lectura más alta entre los pluviómetros del IDEAM del municipio, y en este servicio un <b>0'+N+'mm no se distingue de «la estación no reportó»</b> — ver la nota de método del 25-sep. Hoy <b>tres regiones completas (Caribe, Orinoquía e Insular, 136 estaciones) marcan cero</b>, así que esa advertencia es la clave de lectura del mapa de hoy.</figcaption>')
h = h.replace(old, new)

# ---------- 04: incendios ----------
old = re.search(r'<tr><td>Incendios de cobertura vegetal</td>.*?</tr>', h, re.S).group(0)
new = ('<tr><td>Incendios de cobertura vegetal</td><td><b>0</b> municipios en alerta roja al 6-oct (segundo día en cero), pero <b>8 naranja y 10 amarilla</b> — <b>18</b> con alguna alerta, <b>más del doble que ayer</b></td>'
 '<td><b>Releído en vivo 6-oct — el cero se mantiene y la huella se duplica: las dos cosas a la vez.</b> La alerta roja repite en <b>0</b> municipios por segundo día consecutivo —el <b>BAICV N.º 278</b> (actualizado el 5-oct a las 12:00 y vigente hasta hoy al mediodía) lo escribe otra vez con las mismas palabras, «<i>Alerta Alta: Sin municipios en alerta</i>»— mientras el total con alguna alerta pasa de <b>8 a 18</b>, revirtiendo cuatro días de caídas (55 → 26 → 12 → 8 → <b>18</b>). '
 '<b>Las naranjas suben de 2 a 8:</b> <b>Neiva, Íquira y Rivera</b> (Huila), <b>Cáqueza</b> (Cundinamarca), <b>Uribia</b> (que se mantiene) y <b>Manaure</b> (que sube de amarilla) en La Guajira, <b>Pasto</b> (Nariño) y <b>Dolores</b> (Tolima). '
 '<b>Las amarillas suben de 6 a 10:</b> Cácota, Mutiscua y Silos (Norte de Santander), <b>Sabana de Torres</b> (que baja de naranja) y Girón (Santander), Cartagena de Indias (Bolívar), Ambalema (Tolima), Paz de Ariporo (Casanare), Inírida (Guainía) y Puerto Carreño (Vichada); salen Pesca (Boyacá) y Trinidad (Casanare). '
 '<b>Cómo leerlo sin pasarse:</b> cero en el nivel máximo significa que el pronóstico a 24 horas no ve condiciones críticas en ningún municipio; el salto de 8 a 18 significa que hay el doble de municipios con condiciones de vigilancia. <b>No son cifras contradictorias: son dos umbrales distintos del mismo pronóstico</b>, y el titular fácil —«se duplican las alertas de incendio»— es tan incompleto como el de ayer, «se acabó el riesgo». '
 '<b>Cruce independiente, y por primera vez en la serie no cuadra del todo:</b> el BAICV N.º 278 pone la Alerta Alta <b>sin municipios</b> (mis 0 rojas, ✓) y la Alerta Baja en <b>Bolívar, Casanare, Guainía, Norte de Santander, Santander, Tolima y Vichada</b> — exactamente los siete departamentos de mis 10 amarillas, uno por uno (✓). '
 '<b>Pero la Moderada nombra seis departamentos —La Guajira, Huila, Nariño, Tolima, Cundinamarca y Santander— y mis naranjas están en cinco:</b> Santander aparece en el boletín y en el servicio REST sus dos municipios (Sabana de Torres y Girón) figuran en amarilla. '
 '<b>No se puede resolver cuál de los dos tiene razón</b>: las tablas municipales del BAICV pierden la agrupación por nivel al extraer el texto del PDF, un límite que este monitor ya tenía anotado desde el 1-oct. Se deja escrito como discrepancia abierta y no como coincidencia</td>'
 '<td><span class="badge b-ok">✅ IDEAM REST (Alertas_ICV, releído 6-oct) + BAICV N.º 278</span></td></tr>')
h = h.replace(old, new)

# ---------- 04: deslizamientos ----------
old = re.search(r'<tr><td>Deslizamientos de tierra</td>.*?</tr>', h, re.S).group(0)
new = ('<tr><td>Deslizamientos de tierra</td><td><b>306</b> municipios con alerta hoy (6-oct) — suma de los tres niveles, frente a los 340 del 5-oct, con la alerta roja bajando de 86 a <b>78</b></td>'
 '<td><b>Releído en vivo 6-oct:</b> 138 amarilla + 90 naranja + <b>78 roja</b> = 306. Segundo día consecutivo en que las dos cifras bajan juntas. '
 '<b>Pero el total nacional esconde el movimiento más grande de la jornada, y es un cambio de mapa:</b> <b>Antioquia pasa de 14 a 43 municipios en rojo</b> —32 entradas y 3 salidas— y <b>desplaza al Chocó del primer puesto por primera vez en toda esta serie</b>. '
 '<b>Y la dirección importa:</b> salen <b>Carepa, Chigorodó y Nechí</b>, es decir el eje de Urabá que este tablero siguió dos días, y entra el <b>Valle de Aburrá y el norte y occidente del departamento</b>: <b>Medellín</b>, Bello, Urrao, Yarumal, Santa Rosa de Osos, Belmira, Entrerríos, San Pedro de los Milagros, San José de la Montaña, San Andrés de Cuerquía, Angostura, Briceño, Toledo, Peque, Sabanalarga, Buriticá, Liborina, Olaya, Sopetrán, San Jerónimo, Ebéjico, Heliconia, Anzá, Caicedo, Giraldo, Abriaquí, Betulia, Concordia, Armenia, Remedios, Santa Fe de Antioquia y Vigía del Fuerte. '
 '<b>Carepa cierra su arco:</b> marcó 148,6'+N+'mm el 2-oct, 25,9 el 3 y <b>0'+N+'mm</b> el 4, y hoy sale de la alerta roja. La cadena lluvia → ladera → río que este monitor trazó en Urabá <b>se cerró donde empezó</b>, tres días después. '
 '<b>El Chocó baja de 20 a 13 de sus 30 municipios</b> —siguen Quibdó, Bagadó, Bahía Solano, Bajo Baudó, Bojayá, Carmen del Darién, Cértegui, El Carmen de Atrato, Lloró, Medio Atrato, Nóvita, Riosucio y Río Iró; salen Acandí y Unguía, que entraron ayer—. '
 'Desglose completo de rojas: <b>Antioquia 43, Chocó 13, Nariño 5, Cauca 3, Córdoba 3, Valle del Cauca 3, Meta 2</b>, y una cada uno en Bolívar, Boyacá, Magdalena, Putumayo, Quindío y Risaralda. '
 '<b>Dos entradas que vale la pena nombrar:</b> <b>Santa Rosa de Cabal</b> (Risaralda), el municipio con el máximo nacional de lluvia del día (90,0'+N+'mm), y <b>Armenia</b> (Quindío), capital que no figuraba en esta capa. '
 '<b>De los municipios del explorador de la sección 03 se mueven siete:</b> <b>Medellín entra en roja</b> desde amarilla, <b>Sonsón vuelve a entrar</b> en amarilla, <b>Tiquisio, Villavicencio, Yopal y Florencia bajan de roja a naranja</b>, <b>Pailitas baja a amarilla</b> y <b>Aguachica y Valledupar salen por completo</b>. Se mantienen en roja <b>Quibdó y Santa Marta</b>. '
 '<b>Cruce independiente que coincide exactamente, por octavo día:</b> el Pronóstico de la Amenaza por deslizamientos <b>N.º 278</b> (5-oct 12:00 HLC, vigente hasta hoy al mediodía) lista amenaza alta en <b>13 departamentos</b> —Antioquia, Bolívar, Boyacá, Cauca, Chocó, Córdoba, Magdalena, Meta, Nariño, Putumayo, Quindío, Risaralda y Valle del Cauca— y moderada en <b>17</b>, y las dos listas coinciden <b>nombre por nombre</b> con lo que arrojó este conteo por separado del servicio REST</td>'
 '<td><span class="badge b-ok">✅ IDEAM REST (Alertas_IDD, releído 6-oct) + Pronóstico N.º 278</span></td></tr>')
h = h.replace(old, new)

# ---------- 04: hidrologicas ----------
old = re.search(r'<tr><td>Crecientes súbitas / alertas hidrológicas</td>.*?</tr>', h, re.S).group(0)
new = ('<tr><td>Crecientes súbitas / alertas hidrológicas</td><td><b>197</b> subzonas hidrográficas con alerta (6-oct), el mismo total de ayer — pero la roja se desploma de <b>12 a 4</b></td>'
 '<td><b>Releído en vivo 6-oct:</b> 116 amarilla, 77 naranja, <b>4 roja</b>. <b>Y aquí está el vuelco del día:</b> ayer esta fila decía que los ríos eran la única de las tres capas que no cedía, con doce rojas clavadas; <b>hoy ceden ocho de las doce de golpe</b>, la mayor caída de esta capa en toda la serie. '
 '<b>El bloque que se levanta es el del Pacífico sur</b>, que llevaba cuatro días sin un solo cambio: salen <b>Río Tola, Río Telembí, Río Patía Medio y Río Patía Bajo</b> (Nariño) y <b>Río Timbiquí y Río San Juan del Micay</b> (Cauca) — de las siete de esa vertiente <b>solo queda Río Saija</b>. '
 'Salen también <b>Río Sucio</b> (Antioquia) y la <b>Ciénaga Grande de Santa Marta</b> (Magdalena), que había entrado ayer como la primera roja del Magdalena de la serie y <b>duró exactamente un día</b> — el mismo patrón de 24 horas que este tablero ya tuvo que corregir con la alerta de incendio de Quibdó el 4-oct. '
 '<b>Las cuatro que quedan:</b> <b>Río León</b> y <b>Río Mulatos y otros directos al Caribe</b> (Antioquia), <b>Bajo San Jorge'+N+'–'+N+'La Mojana</b> (Bolívar) y <b>Río Saija</b> (Cauca). '
 '<b>Antioquia conserva dos de las cuatro</b> y sigue siendo el departamento con más subzonas en alerta de cualquier nivel (26), seguido de Chocó (23), Cauca y Valle del Cauca (16 cada uno), Tolima (14), Boyacá y Nariño (11), Norte de Santander (10), Cundinamarca y Meta (9). '
 '<b>Salvedad de método, que conviene repetir:</b> este servicio solo devuelve las subzonas que tienen alerta, así que su número de filas <i>es</i> el conteo de alertas. '
 '<b>El ITD N.º 278 lo confirma por su lado:</b> nombra alta probabilidad de crecientes súbitas o niveles altos en <b>Caribe'+N+'-'+N+'Litoral, Bajo Magdalena'+N+'-'+N+'Cauca'+N+'-'+N+'San Jorge y Tapaje'+N+'-'+N+'Dagua y Directos</b> —las tres áreas hidrográficas donde caen mis cuatro rojas— y moderada en catorce más, entre ellas Atrato'+N+'-'+N+'Darién. '
 '<b>Y la lectura honesta del conjunto:</b> hoy las tres capas bajan a la vez por segundo día, pero el que más cede es justamente el que ayer no se movía. En siete días esta cifra hizo 1 → 11 → 12 → 12 → <b>4</b>: son fotos de 24 horas, no una tendencia</td>'
 '<td><span class="badge b-ok">✅ IDEAM REST (Alertas_Hidrologicas, releído 6-oct) + ITD N.º 278</span></td></tr>')
h = h.replace(old, new)

open('board_v1.html','w',encoding='utf-8').write(h)
print('ok len', len(h))
