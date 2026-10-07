# -*- coding: utf-8 -*-
import json, re, sys
h = open('board.html', encoding='utf-8').read()
orig_len = len(h)
def rep(old, new, n=1, label=''):
    global h
    c = h.count(old)
    assert c == n, 'count=%d expected=%d for %s :: %r' % (c, n, label, old[:120])
    h = h.replace(old, new)

NB = '&nbsp;'

# ---------- 1. header date ----------
rep('<span>Corte: <b>5 oct. 2026</b></span>', '<span>Corte: <b>6 oct. 2026</b></span>', 1, 'corte')

# ---------- 2. IDEAM_CITY ----------
newcity = open('ideam_city_new.json', encoding='utf-8').read().strip()
m = re.search(r'(  var IDEAM_CITY = )(\{.*?\})(;\n)', h, re.S)
assert m, 'IDEAM_CITY not found'
h = h[:m.start(2)] + newcity + h[m.end(2):]

# ---------- 3. section 03 ficha header date ----------
rep("'<h5>Datos IDEAM en tiempo real (consulta del 5-oct-2026, datos del 3-oct-2026, servicios REST del visualizador)</h5><table class=\"mini\">'",
    "'<h5>Datos IDEAM en tiempo real (consulta del 6-oct-2026, datos del 4-oct-2026, servicios REST del visualizador)</h5><table class=\"mini\">'",
    1, 'ficha date')

# ---------- 4. section 02 note ----------
old_note = '''las temperaturas y lluvias de estación se releyeron en vivo el <b>5-oct-2026</b> contra los servicios REST del IDEAM (142 estaciones de temperatura con dato, 625 de precipitación). <b>Ese dato corresponde al <b>3 de octubre</b>, dos días antes de la consulta</b>, verificado contra el Informe Técnico Diario N.º 277 del IDEAM, que lista trece de estos mismos valores y cuantifica la caída nacional de lluvia en <b>&minus;79,9%</b> (ver la caja de correcciones).'''
# the literal in the file uses −
old_note = old_note.replace('&minus;', '−')
new_note = '''las temperaturas y lluvias de estación se releyeron en vivo el <b>6-oct-2026</b> contra los servicios REST del IDEAM (150 estaciones de temperatura con dato, 656 de precipitación). <b>Ese dato corresponde al <b>4 de octubre</b>, dos días antes de la consulta</b>, verificado contra el Informe Técnico Diario N.º 278 del IDEAM, que lista <b>veinticuatro</b> de estos mismos valores y cuantifica un <b>aumento</b> nacional de lluvia del <b>18,3%</b> (ver la caja de correcciones).'''
rep(old_note, new_note, 1, 'nota sec 02')

json.dump({'ok': True}, open('step1.json','w'))
open('board_v1.html','w',encoding='utf-8').write(h)
print('step1 done; len', orig_len, '->', len(h))
