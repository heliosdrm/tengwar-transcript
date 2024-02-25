# coding: utf-8
#%%
import json
import re

#%%

def extdelimiters(dicregex):
    """
    Amplía un diccionario de expresiones regulares haciendo para que
    los delimitadores de posicion ("^", "$") también sean delimitadores de palabras
    (si no los hay ya)
    """
    for k in dicregex.copy():
        if k.startswith("^"):
            kb = "\\b"+k[1:]
            if not kb not in dicregex:
                dicregex[kb] = dicregex[k]
    for k in dicregex.copy():
        if k.endswith("$"):
            kb = k[:-1]+"\\b"
            if kb not in dicregex:
                dicregex[kb] = dicregex[k]
    return dicregex

with open("modes/spanish.json", "r", encoding="utf-8") as f:
    rules = json.load(f)

extdelimiters(rules["preprocess"])
extdelimiters(rules["map"])

with open("encodings/telcontar-encoding.json", "r", encoding="utf-8") as f:
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

def addreplacements(oldrep, newrep):
    """
    `oldrep` y `newrep` son listas de tuplas `(p, r)` formadas por
    un rango de posiciones `p` y una cadena de texto de reemplazo `r`.
    Esta función amplía `oldrep` añadiendo los casos de `newrep`
    en los que los rangos no se solapan.
    """
    candidatos = [m for m in newrep] # copiar lista
    for (p, r) in candidatos.copy():
        first, last = p
        for rep in oldrep:
            a, b = rep[0]
            if (a <= first < b) or (a < last <= b): # solapamiento
                candidatos.remove((p, r))
                break
    oldrep.extend(candidatos)

def reemplazar(texto, dicregex):
    """
    Modifica `texto` aplicando los reemplazos por expresiones regulares
    definidos en el diccionario `dicregex`.
    """
    patrones = priorizaregex(dicregex.keys())
    reemplazos = []
    for pat in patrones:
        matches = [m for m in re.finditer(pat, texto)]
        newrep = [(m.span(), m.expand(dicregex[pat])) for m in matches]
        addreplacements(reemplazos, newrep)
    if len(reemplazos) == 0:
        return texto
    reemplazos.sort(key=lambda mr: mr[0][0]) # ordenar
    # montar texto
    tokens = []
    posicion = 0
    for (m, r) in reemplazos:
        first, last = m
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
        dic["(^|\\b)"+w+"($|^\\b)"] = r
    dic.update(rules["map"])
    tengwar = reemplazar(texto, dic)
    # vocales sueltas
    if tengwar.startswith("["):
        tengwar = "{telco}" + tengwar
    # invertir silme con tehtar
    tengwar = tengwar.replace("{silme}[", "{silme-nuquerna}[")
    # otros ajustes para hacer usable en Tecendil
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
    if font == "telcontar":
        texto = encode(texto)
    return texto


# %%
