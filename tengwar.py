from functions import transcribe
from pyperclip import copy
import sys

if __name__ == "__main__":
    args = sys.argv[1:]
    texto = transcribe(args[0])
    print(texto)
    copy(texto)