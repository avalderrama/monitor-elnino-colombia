# -*- coding: utf-8 -*-
h = open('board_v1.html', encoding='utf-8').read()
N = '&nbsp;'
def rep(old, new, label=''):
    global h
    assert h.count(old) == 1, 'count=%d %s' % (h.count(old), label)
    h = h.replace(old, new)

# --- Antioquia transitions, precise ---
old = ('<b>Y el hallazgo del día está aquí, en dos piezas.</b> <b>Primera:</b> <b>Antioquia pasa de 14 a 43 municipios en alerta roja de deslizamiento</b> —más de la mitad del total nacional, y 29 entradas nuevas en un día—, con la huella saliéndose del eje de Urabá hacia el norte y el Valle de Aburrá: entran <b>Medellín</b>, Bello, Urrao, Yarumal, Santa Rosa de Osos, Belmira, Sopetrán, Liborina, Ebéjico, Heliconia, Anzá, Buriticá, Caicedo, Giraldo, Olaya, Peque, Sabanalarga, Toledo, Angostura, Briceño, Concordia, Betulia, Entrerríos, Remedios, Armenia (Ant.), San Jerónimo, San Pedro de los Milagros, San José de la Montaña, San Andrés de Cuerquía y Vigía del Fuerte, además de los de Urabá que ya estaban. ')
new = ('<b>Y el hallazgo del día está aquí, y da un giro al relato de los dos días anteriores.</b> <b>Antioquia pasa de 14 a 43 municipios en alerta roja de deslizamiento</b> —más de la mitad del total nacional, con <b>32 entradas y 3 salidas</b> en un día—, pero <b>la huella se muda:</b> sale del eje de Urabá y se instala en el Valle de Aburrá y el norte y occidente del departamento. '
 '<b>Salen Carepa, Chigorodó y Nechí</b> — y Carepa es justamente el municipio que marcó los 148,6'+N+'mm del 2-oct y que hoy reporta <b>0'+N+'mm</b>: la cadena lluvia → ladera que este tablero trazó dos días seguidos en Urabá <b>se cerró ahí</b>. '
 '<b>Entran 32, y la lista dice dónde está ahora el riesgo:</b> <b>Medellín</b>, Bello, Urrao, Yarumal, Santa Rosa de Osos, Belmira, Entrerríos, San Pedro de los Milagros, San José de la Montaña, San Andrés de Cuerquía, Angostura, Briceño, Toledo, Peque, Sabanalarga, Buriticá, Liborina, Olaya, Sopetrán, San Jerónimo, Ebéjico, Heliconia, Anzá, Caicedo, Giraldo, Abriaquí, Betulia, Concordia, Armenia (Ant.), Remedios, Santa Fe de Antioquia y Vigía del Fuerte. '
 '<b>Siguen en rojo</b> Apartadó, Turbo, Mutatá, Murindó, Dabeiba, Frontino, Cañasgordas, Uramita, Ituango, Salgar y El Bagre. ')
rep(old, new, 'antioquia')

# --- Chocó exits, only what is defensible ---
old = ('con <b>Quibdó todavía en roja</b> y salidas en Acandí, Unguía, Alto Baudó, Istmina, Medio San Juan, Sipí y Unión Panamericana.')
new = ('con <b>Quibdó todavía en roja</b> y con la salida de <b>Acandí y Unguía</b>, los dos municipios del Darién que habían entrado ayer. <i>Los demás municipios que salieron no se nombran porque este tablero no publicó ayer el listado completo de los veinte, y nombrarlos de memoria sería inventar.</i>')
rep(old, new, 'choco')

open('board_v1.html','w',encoding='utf-8').write(h)
print('ok len', len(h))
