#%%
import json
import re

#%%
with open("spanish.json", "r") as f:
    rules = json.load(f)

with open("telcontar-encoding.json", "r") as f:
    telcontarcodes = json.load(f)

# %%

def greedymatch(substr, dic_re):
    regexp = ""
    match = None
    for pat in dic_re:
        m = pat.match(substr)
        if m is not None and len(pat.pattern) > len(regexp):
            regexp = pat.pattern
            match = m
    return regexp, match

def reemplazar(texto, reemplazos):
    # rep = dict((re.compile(k), v) for (k,v) in reemplazos.items())
    rep = [re.compile(s) for s in reemplazos]
    sout = ""
    while len(texto) > 0:
        regexp, match = greedymatch(texto, rep)
        if match is None:
            sout += texto[0]
            texto = texto[1:]
        else:
            cut = match.span()[-1]
            sout += re.sub(regexp, reemplazos[regexp], texto[:cut])
            texto = texto[cut:]
    return sout


# %%
def preprocess(texto):
    return reemplazar(texto.lower(), rules["preprocess"])

def maptengwar(texto):
    dic = {}
    for (w, r) in rules["words"].items():
        dic["^"+w+"$"] = r
        dic["([^\\w])"+w+"$"] = "\\1"+r
        dic["^"+w+"([^\\w])"] = r+"\\1"
        dic["([^\\w])"+w+"([^\\w])"] = "\\1"+r+"\\2"
    dic.update(rules["map"])
    return reemplazar(texto, dic)

def cleanbrackets(tengwar):
    # vocales sueltas
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
    texto = cleanbrackets(texto)
    if font == "telcontar":
        texto = encode(texto)
    return texto
# %%
