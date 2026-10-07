# -*- coding: utf-8 -*-
import re
h = open('board_v1.html', encoding='utf-8').read()
N = '&nbsp;'
A = lambda u, t: '            <a href="%s" target="_blank" rel="noopener">%s</a>\n' % (u, t)
REST = 'https://visualizador.ideam.gov.co/gisserver/rest/services/StoryMaps_IDA/%s/MapServer/%s/query?where=1%%3D1&amp;outFields=%s&amp;returnGeometry=false&amp;f=json&amp;resultRecordCount=5000'

links = []
links.append(A('https://www.ideam.gov.co/file-download/download/public/23367',
 '<b>IDEAM</b> — <b>Informe Técnico Diario N.º 278</b> (5-oct 12:00 HLC, datos del <b>4 de octubre</b>, 84 láminas): <b>aumento nacional de lluvia del 18,3%</b>; máximo en 24'+N+'h en <b>Santa Rosa de Cabal (Risaralda) 90,0'+N+'mm</b>; y <b>tres récords de temperatura máxima de octubre</b> — La Aldea (Medellín) 29,0'+N+'°C, Aeropuerto El Caraño (Quibdó) 34,5 y Aeropuerto Alfonso Bonilla (Palmira) 33,4. Es el documento que fecha el servicio REST, y hoy con <b>veinticuatro valores coincidentes</b>, el mejor cruce de la serie. <b>No menciona El Niño, ENOS, sequía ni déficit en sus 84 láminas</b>, verificado buscando los literales en el PDF en disco'))
links.append(A('https://www.ideam.gov.co/file-download/download/public/23362',
 '<b>IDEAM</b> — <b>BAICV N.º 278</b> (incendios, 5-oct 12:00, vigente hasta hoy al mediodía): <b>«Alerta Alta: Sin municipios en alerta»</b> por segundo día; Moderada en <b>La Guajira, Huila, Nariño, Tolima, Cundinamarca y Santander</b> y Baja en <b>Bolívar, Casanare, Guainía, Norte de Santander, Santander, Tolima y Vichada</b>. <b>Dos de sus tres niveles coinciden exactos con el conteo REST; el tercero no:</b> el boletín pone a Santander en Moderada y el servicio tiene sus dos municipios en amarilla. <b>Primera discrepancia de la serie</b>, y no se puede resolver porque las tablas municipales pierden la agrupación por nivel al extraer el texto'))
links.append(A('https://www.ideam.gov.co/file-download/download/public/23361',
 '<b>IDEAM</b> — Pronóstico de la Amenaza por deslizamientos <b>N.º 278</b> (5-oct 12:00, <b>vigente hasta hoy al mediodía</b>): amenaza alta en <b>13</b> departamentos y moderada en <b>17</b>, idéntico al conteo leído por separado del servicio REST, <b>nombre por nombre</b> en las dos listas. Octavo día consecutivo de coincidencia exacta'))
links.append(A('https://www.ideam.gov.co/file-download/download/public/23372',
 '<b>IDEAM</b> — <b>Boletín semanal de datos extremos núm. 40</b> (5-oct, semana del <b>28-sep al 4-oct</b>), fuente oficial nueva en la ventana: máxima semanal <b>41,0'+N+'°C en Natagaima (est. Anchique)</b> el 29-sep; mínima <b>−0,6'+N+'°C en Cerinza</b>; <b>día más lluvioso del país el miércoles 30-sep</b> con 8.570,4'+N+'mm en toda la red; y máximo en 24'+N+'h de <b>148,6'+N+'mm en Carepa</b> el viernes 2. Trae además la <b>anomalía cerrada de septiembre</b> (déficits &gt;80% en el oriente del Caribe, excesos &gt;90% en el litoral nariñense, el piedemonte amazónico y el norte del Tolima) y la <b>predicción de anomalía de temperatura para octubre</b> (máximas 4,0-5,0'+N+'°C por encima de lo normal en el norte de Nariño y el sur del Amazonas). <b>No menciona El Niño</b>'))
links.append(A(REST % ('Datos_Precipitacion','0','ESTACION,MUNICIPIO,DEPARTAMEN,DATO,TECNOLOGIA'),
 '<b>IDEAM REST</b> — precipitación (656 estaciones): lluvia en <b>169 de ellas, el 25,8% del país</b>, casi igual que ayer. <b>Pero el reparto es el dato: el Caribe (0 de 92), la Orinoquía (0 de 41) y la Insular (0 de 3) no registran una sola lectura</b> — 136 estaciones en cero—, mientras el Pacífico sube del 28% al <b>42,1%</b>, la Andina del 18% al <b>30,4%</b> y la Amazonía baja del 41% al 22,6%. La Insular rompe cinco días con el 100% de su red'))
links.append(A(REST % ('Datos_TMaxima','0','ESTACION,MUNICIPIO,DEPARTAMEN,DATO'),
 '<b>IDEAM REST</b> — temperatura máxima (<b>150 estaciones con dato</b>): la máxima nacional sube a <b>37,2'+N+'°C en Manaure (La Guajira)</b> y <b>sale de la región Andina</b> por primera vez en cinco días; <b>vuelven dos estaciones por encima de 37'+N+'°C</b> (Manaure y Hacienda Túnez, en Fredonia) frente a ninguna ayer. <b>Manaure es, además, una de las seis estaciones que volvieron a reportar hoy</b> tras figurar ayer como «sin refrescar»'))
links.append(A(REST % ('Alertas_ICV','2','MPIO_CNMBR,DPTO_CNMBR,PROBABILID'),
 '<b>IDEAM REST</b> — alertas de incendios releídas 6-oct: la roja <b>repite en 0</b> por segundo día, pero el total con alguna alerta <b>más que se duplica, de 8 a 18</b> (8 naranja y 10 amarilla), revirtiendo cuatro días de caídas. Entran en naranja <b>Neiva, Íquira y Rivera</b> (Huila), <b>Cáqueza</b> (Cundinamarca) y <b>Pasto</b>; <b>Manaure sube de amarilla a naranja</b> y <b>Sabana de Torres baja de naranja a amarilla</b>'))
links.append(A(REST % ('Alertas__IDD','1','MPIO_CNMBR,DPTO_CNMBR,PROBABILID'),
 '<b>IDEAM REST</b> — alertas de deslizamiento releídas 6-oct: las rojas bajan de 86 a <b>78</b> y el total de 340 a <b>306</b>. <b>Pero el mapa se reordena: Antioquia pasa de 14 a 43 municipios en rojo y desplaza al Chocó (13) del primer puesto por primera vez en esta serie.</b> <b>Salen Carepa, Chigorodó y Nechí</b> —el eje de Urabá— y entran 32 del Valle de Aburrá y del norte y occidente, <b>Medellín incluida</b>. También entran <b>Santa Rosa de Cabal</b>, el municipio con el máximo nacional de lluvia, y <b>Armenia</b>'))
links.append(A(REST % ('Alertas_Hidrologicas','2','NOMSZH,NIVEL_A,ALERTA,DEP'),
 '<b>IDEAM REST</b> — alertas hidrológicas releídas 6-oct: el total se queda en <b>197</b> subzonas pero <b>las rojas se desploman de 12 a 4</b>, la mayor caída de esta capa en toda la serie. <b>Se levanta el bloque entero del Pacífico sur</b> —salen Río Tola, Telembí, Patía Medio, Patía Bajo, Timbiquí y San Juan del Micay, y solo queda Río Saija— y salen Río Sucio (Antioquia) y la <b>Ciénaga Grande de Santa Marta</b>, que entró ayer y <b>duró un día</b>. Quedan Río León, Río Mulatos, Bajo San Jorge'+N+'–'+N+'La Mojana y Río Saija'))
links.append(A('https://servapibi.xm.com.co/daily',
 '<b>XM</b> — API oficial, serie diaria releída el 6-oct (<code>VoluUtilDiarEner</code>, <code>CapaUtilDiarEner</code>, <code>AporEner</code>, <code>AporEnerMediHist</code>): el embalse agregado <b>cae a 75,16% el 5-oct</b> desde el 76,22% del 4, la mayor caída diaria de la serie en el titular. <b>Pero XM volvió a revisar la capacidad útil al alza</b> (de 17.465.538.144 a 17.652.543.144 kWh): a capacidad constante el valor sería <b>75,96%</b>, así que <b>unas cuatro quintas partes de la caída son denominador</b>. Es la tercera revisión en cuatro días. Los aportes quedan en <b>44,5%</b>, segunda jornada consecutiva por debajo del 45%'))
links.append(A('https://api-colombia.com/api/v1/Region',
 '<b>API Colombia</b> — catálogo de 6 regiones y 33 registros de departamento, usado para asignar la región de cada estación (respondió con normalidad)'))

group = ('        <div class="sources-group" id="fuentes-06oct">\n'
 '          <h4>Actualización 6-oct-2026 (refresco de datos en vivo del IDEAM y verificación en PDF oficiales)</h4>\n'
 '          <div class="sources-cols">\n' + ''.join(links) + '          </div>\n'
 '          <p class="src" style="margin-top:6px;">Refresco determinista de los datos embebidos: 41 de 45 lecturas de temperatura y 25 de 45 de lluvia cambiaron; 12 niveles de alerta municipal se movieron (3 de incendio, 9 de deslizamiento) y 31 resúmenes hidrológicos departamentales se recalcularon. '
 '<b>Cuatro de las 90 lecturas</b> no se refrescaron —iguala el mejor resultado de la serie— y quedan marcadas «sin refrescar hoy» con la fecha del dato: tres de temperatura (Demostración Granja/Ortega desde el 23-sep; El Callao/Valledupar desde el 1-oct; y <b>Carmen de Tonchalá</b>/Cúcuta desde hoy) y una de lluvia (<b>El Común</b>/Pupiales). '
 '<b>Y volvieron a reportar seis, el máximo de la serie:</b> Manaure, Jabalcón (Saldaña), Los Álamos (San Sebastián de Buenavista) y Surbata Bonza (Duitama) en temperatura, y Colegio Agropecuario (Pailitas) y Larandia (Florencia) en lluvia. <b>Manaure, además, se llevó el máximo nacional</b> — la contracara exacta de la lección que esta caja escribió ayer con esa misma estación.</p>\n'
 '        </div>\n')

anchor = '      <div class="sources-body">\n\n'
assert h.count(anchor) == 1
h = h.replace(anchor, anchor + group)
h = h.replace('<summary>Ver enlaces de fuentes citadas (~490 enlaces)</summary>',
              '<summary>Ver enlaces de fuentes citadas (~500 enlaces)</summary>')

open('board_v1.html','w',encoding='utf-8').write(h)
print('sources added; len', len(h))
