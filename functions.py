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

def reemplazar_coincidencia(match, dicregex):
    """
    Busca entre las claves del diccionario `dicregex` una expresión regular (compilada)
    `regex` que coincida con el texto capturado en `match`.
    Si existe, devuelve el valor `match.expand(dicregex[regex])`;
    si no, se devuelve el texto capturado de `match` sin modificar
    """
    for regex in dicregex:
        m = regex.fullmatch(match.group())
        if m is not None:
            return match.expand(dicregex[regex])
    return match.group()

def addmatches(oldmatches, newmatches):
    """
    Añadir "Matches" a una lista, seleccionando solo los que no se solapan.
    """
    candidatos = [m for m in newmatches] # copiar lista
    for m in candidatos.copy():
        first, last = m.span()
        for o in oldmatches:
            a, b = o.span()
            if (a <= first < b) or (a < last <= b): # overlaps
                candidatos.remove(m)
                break
    oldmatches.extend(candidatos)

def reemplazar(texto, reemplazos):
    dicregex = dict((re.compile(k), v) for (k,v) in reemplazos.items())
    patterns = priorizaregex(reemplazos.keys())
    matches = []
    for pat in patterns:
        newmatches = re.finditer(pat, texto)
        addmatches(matches, newmatches)
    if len(matches) == 0:
        return texto
    matches.sort(key=lambda m: m.span()[0]) # ordenar
    tokens = []
    posicion = 0
    for m in matches:
        first, last = m.span()
        if posicion < first:
            tokens.append(texto[posicion:first])
        tokens.append(reemplazar_coincidencia(m, dicregex))
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

