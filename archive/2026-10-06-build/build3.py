# -*- coding: utf-8 -*-
import re
h = open('board_v1.html', encoding='utf-8').read()
N = '&nbsp;'
def rep(old, new, label=''):
    global h
    assert h.count(old) == 1, 'count=%d for %s' % (h.count(old), label)
    h = h.replace(old, new)

# ================= CHART A: estaciones mas calientes =================
rep('<h3 class="chart-title">Estaciones más calientes del país (IDEAM, releído el 5-oct-2026 · dato del 3-oct)</h3>',
    '<h3 class="chart-title">Estaciones más calientes del país (IDEAM, releído el 6-oct-2026 · dato del 4-oct)</h3>', 'chartA title')

old_lead = re.search(r'<p class="lead" style="margin:0 0 14px;">Consulta directa al servicio REST del IDEAM \(Datos_TMaxima.*?</p>', h, re.S).group(0)
new_lead = ('<p class="lead" style="margin:0 0 14px;">Consulta directa al servicio REST del IDEAM (Datos_TMaxima, <b>150 estaciones con dato</b>), con las cifras de la jornada del <b>domingo 4 de octubre</b>, fechadas contra el Informe Técnico Diario N.º 278. '
 'El eje <b>se mantiene en 33'+N+'°C</b>: la máxima nacional subió 0,8'+N+'°C y el rango de las seis primeras sigue siendo de 2,0'+N+'°C, así que la escala de ayer sigue siendo legible. En una escala Celsius el cero es arbitrario, así que conviene leer las barras como posiciones, no como proporciones. '
 '<b>La máxima nacional sube a 37,2'+N+'°C y sale de la región Andina: la marca Manaure (La Guajira)</b>, la misma estación que ayer figuraba «sin refrescar» y que hoy volvió a reportar. '
 '<b>Vuelven las barras de la banda superior:</b> dos estaciones alcanzan los 37'+N+'°C —Manaure y Hacienda Túnez (Fredonia, Antioquia)— frente a ninguna ayer, y se dibujan en el tono más oscuro. '
 'El ITD 278 confirma los seis valores uno por uno y registra <b>tres récords de temperatura máxima de octubre</b>, ninguno de ellos en esta lista: La Aldea (Medellín) 29,0'+N+'°C, Aeropuerto El Caraño (Quibdó) 34,5 y Aeropuerto Alfonso Bonilla (Palmira) 33,4.</p>')
h = h.replace(old_lead, new_lead)

old_svg = re.search(r'<svg viewBox="0 0 560 200".*?</svg>', h, re.S).group(0)
bars = [('Manaure (La Guajira)', 37.2, 'temp-4'),
        ('Hda. Túnez (Fredonia)', 37.0, 'temp-4'),
        ('San Alfonso (Villavieja)', 36.8, 'temp-3'),
        ('Anchique (Natagaima)', 36.6, 'temp-3'),
        ('A. Benito Salas (Neiva)', 36.0, 'temp-3'),
        ('Jabalcón (Saldaña)', 35.2, 'temp-3')]
AX, MX = 33.0, 37.2
aria = ('Gráfica de barras horizontales de la temperatura máxima del 4 de octubre de 2026, con el eje comenzando en 33 grados: '
        'Manaure (La Guajira) 37,2; Hacienda Túnez (Fredonia) 37,0; San Alfonso (Villavieja) 36,8; Anchique (Natagaima) 36,6; '
        'Aeropuerto Benito Salas (Neiva) 36,0; Jabalcón (Saldaña) 35,2 grados centígrados. Dos estaciones alcanzan los 37 grados.')
parts = ['<svg viewBox="0 0 560 200" role="img" aria-label="%s" xmlns="http://www.w3.org/2000/svg">' % aria,
         '        <line x1="190" y1="10" x2="190" y2="192" class="axis-line" stroke-width="1"/>']
y = 16
for name, v, col in bars:
    w = round((v - AX) / (MX - AX) * 280)
    parts.append('        <rect x="190" y="%d" width="%d" height="20" rx="2" fill="var(--%s)"/>' % (y, w, col))
    parts.append('        <text x="180" y="%d" text-anchor="end" class="bar-cat">%s</text>' % (y+14, name))
    parts.append('        <text x="%d" y="%d" class="bar-val">%s °C</text>' % (190+w+8, y+14, ('%.1f'%v).replace('.',',')))
    y += 30
parts.append('        <text x="190" y="199" text-anchor="start" class="bar-cat">33 °C</text>')
parts.append('        </svg>')
h = h.replace(old_svg, '\n'.join(parts))

# ================= CHART B: alertas rojas =================
old_lead2 = re.search(r'<p class="lead" style="margin:0 0 14px;">Municipios en alerta roja del IDEAM.*?</p>', h, re.S).group(0)
new_lead2 = ('<p class="lead" style="margin:0 0 14px;">Municipios en alerta roja del IDEAM, 5-oct frente al re-chequeo del 6-oct (detalle completo por nivel en el texto de arriba). '
 '<b>El fuego repite el cero por segundo día</b> —el BAICV N.º 278 vuelve a decir «Alerta Alta: Sin municipios en alerta»— y el <b>deslizamiento baja de 86 a 78</b> rojas. '
 '<b>Pero las dos cifras de «alerta roja» esconden hoy movimientos contrarios, y conviene decirlo aquí:</b> el total con <i>alguna</i> alerta de incendio <b>más que se duplica, de 8 a 18 municipios</b>, y el de deslizamiento baja de 340 a <b>306</b>. '
 'Es decir: el fuego no tiene ningún municipio en el nivel máximo y a la vez tiene el doble de municipios vigilados que ayer. La escala se deja anclada en el máximo de 86 de ayer. Barras desde cero; <b>los dos ceros del fuego se marcan con una línea sobre el eje, no con una barra</b>, para no representar con un rectángulo un valor que no existe.</p>')
h = h.replace(old_lead2, new_lead2)

old_svg2 = re.search(r'<svg viewBox="0 0 340 200".*?</svg>', h, re.S).group(0)
H86 = 140
h78 = round(H86 * 78 / 86)
new_svg2 = '\n'.join([
 '<svg viewBox="0 0 340 200" role="img" aria-label="Gráfica de barras desde cero: las alertas rojas de incendios se mantienen en 0 municipios del 5 al 6 de octubre, y las de deslizamientos bajaron de 86 a 78." xmlns="http://www.w3.org/2000/svg">',
 '          <line x1="30" y1="170" x2="320" y2="170" class="axis-line" stroke-width="1"/>',
 '          <line x1="50" y1="170" x2="84" y2="170" stroke="var(--warn)" stroke-width="2.5" stroke-opacity="0.45"/>',
 '          <text x="67" y="161" text-anchor="middle" class="bar-val">0</text>',
 '          <line x1="90" y1="170" x2="124" y2="170" stroke="var(--warn)" stroke-width="2.5"/>',
 '          <text x="107" y="161" text-anchor="middle" class="bar-val">0</text>',
 '          <rect x="210" y="%d" width="34" height="%d" rx="2" fill="var(--warn-soft)" stroke="var(--warn)" stroke-width="1"/>' % (170-H86, H86),
 '          <text x="227" y="24" text-anchor="middle" class="bar-val">86</text>',
 '          <rect x="250" y="%d" width="34" height="%d" rx="2" fill="var(--warn)"/>' % (170-h78, h78),
 '          <text x="267" y="%d" text-anchor="middle" class="bar-val">78</text>' % (170-h78-6),
 '          <text x="87" y="185" text-anchor="middle" class="bar-cat">Incendios</text>',
 '          <text x="247" y="185" text-anchor="middle" class="bar-cat">Deslizamientos</text>',
 '        </svg>'])
h = h.replace(old_svg2, new_svg2)
rep('<span class="sw"><span class="dot" style="background:var(--warn-soft);border:1px solid var(--warn)"></span> 4-oct</span>',
    '<span class="sw"><span class="dot" style="background:var(--warn-soft);border:1px solid var(--warn)"></span> 5-oct</span>', 'legendA')
rep('<span class="sw"><span class="dot" style="background:var(--warn)"></span> 5-oct (hoy)</span>',
    '<span class="sw"><span class="dot" style="background:var(--warn)"></span> 6-oct (hoy)</span>', 'legendB')

open('board_v1.html','w',encoding='utf-8').write(h)
print('charts rebuilt; len', len(h))
