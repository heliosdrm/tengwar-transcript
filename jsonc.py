import json
import re

def removeunquotedcomment(match):
    s = match.group(0)
    if s.startswith('/'): # not quoted
        return " "
    else:
        return s

def removecomments(text):
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, removeunquotedcomment, text)

def loads(s, *args, **kwargs):
    return json.loads(removecomments(s), *args, **kwargs)

def load(fp, *args, **kwargs):
    return loads(fp.read(), *args, **kwargs)