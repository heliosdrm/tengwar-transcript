#%%
import json
import re

#%%
with open("spanish.json", "r") as f:
    rules = json.load(f)

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
    return reemplazar(texto, rules["preprocess"])

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
    tengwar = tengwar.replace(" [", " {short-carrier}[")
    tengwar = tengwar.replace("{}[", "{short-carrier}[")
    tengwar = tengwar.replace("{}", "")
    return tengwar

def transcribe(texto):
    texto = preprocess(texto)
    texto = maptengwar(texto)
    texto = cleanbrackets(texto)
    return texto
# %%
