# coding: utf-8
#%%
import json
import re

#%%
with open("spanish.json", "r", encoding="utf-8") as f:
    rules = json.load(f)

with open("telcontar-encoding.json", "r", encoding="utf-8") as f:
    telcontarcodes = json.load(f)

# %%
def priorizaregex(patterns):
    """
    Ordena una colección de patrones de expresiones regulares de más a menos prioritarias:
    Las más prioritarias son las que indican un comienzo (empieza por '^')
    o final (acaban por '$'). Luego se priorizan por número de caracteres.
    """
    priorizadas = [x for x in patterns if x.startswith("^") or x.endswith("$")]
    interiores = [x for x in patterns if x not in priorizadas]
    priorizadas.sort(key=len, reverse=True)
    interiores.sort(key=len, reverse=True)
    priorizadas.extend(interiores)
    return priorizadas

def addmatches(oldmatches, newmatches):
    """
    Añadir tuplas de "Matches" acompañadas con las cadenas de reemplazo a una lista,
    seleccionando solo los casos en los que los "Matches" no se solapan.
    """
    candidatos = [m for m in newmatches] # copiar lista
    for (m, r) in candidatos.copy():
        first, last = m.span()
        for o in oldmatches:
            a, b = o[0].span()
            if (a <= first < b) or (a < last <= b): # overlaps
                candidatos.remove((m, r))
                break
    oldmatches.extend(candidatos)

def reemplazar(texto, reemplazos):
    patterns = priorizaregex(reemplazos.keys())
    matches = []
    for pat in patterns:
        newmatches = [m for m in re.finditer(pat, texto)]
        newreplacements = [m.expand(reemplazos[pat]) for m in newmatches]
        addmatches(matches, zip(newmatches, newreplacements))
    if len(matches) == 0:
        return texto
    matches.sort(key=lambda mr: mr[0].span()[0]) # ordenar
    tokens = []
    posicion = 0
    for (m, r) in matches:
        first, last = m.span()
        if posicion < first:
            tokens.append(texto[posicion:first])
        tokens.append(r)
        posicion = last
    tokens.append(texto[posicion:])
    return "".join(tokens)

# %%
def preprocess(texto):
    return reemplazar(texto.lower(), rules["preprocess"])

def maptengwar(texto):
    dic = {}
    # Reglas para palabras completas
    for (w, r) in rules["words"].items():
        dic["(^|[^\\w])"+w+"($|[^\\w])"] = "\\1"+r+"\\2"
    dic.update(rules["map"])
    return reemplazar(texto, dic)

def fixtengwar(tengwar):
    # vocales sueltas
    if tengwar.startswith("["):
        tengwar = "{telco}" + tengwar
    tengwar = tengwar.replace(" [", " {telco}[")
    tengwar = tengwar.replace("{}[", "{telco}[")
    tengwar = tengwar.replace("{}", "")
    return tengwar

def encode(texto):
    for (k,v) in telcontarcodes.items():
        texto = texto.replace(k, v)
    return texto

def transcribe(texto, font="telcontar"):
    texto = preprocess(texto)
    texto = maptengwar(texto)
    texto = fixtengwar(texto)
    if font == "telcontar":
        texto = encode(texto)
    return texto

