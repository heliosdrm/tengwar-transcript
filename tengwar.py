# coding: utf-8

from functions import transcribe
from pyperclip import copy
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="python tengwar.py",
        description="""
        Transcribir textos a Tengwar.

        Puede transcribir texto de un archivo o introducido en el comando.
        El texto transcrito puede escribirse en otro archivo, imprimirse en pantalla
        o copiarse al portapapeles.
        
        La codificación de los textos por defecto es UTF-8.
        Véanse otras codificaciones de texto que pueden emplearse con Python en:
        https://docs.python.org/3/library/codecs.html#standard-encodings

        Más información: https://github.com/heliosdrm/tengwar-transcript
        """
    )
    parser.add_argument('texto', nargs='?', help="Texto a transcribir", default="")
    parser.add_argument('-i', '--input', help="Archivo con el texto de entrada")
    parser.add_argument('-ie', '--inputencoding', help="Codificación del texto de entrada", default="utf-8")
    parser.add_argument('-o', '--output', help="Archivo en el que escribir el texto de salida")
    parser.add_argument('-oe', '--outputencoding', help="Codificación del texto de salida", default="utf-8")
    parser.add_argument('-p', '--print', action="store_true", help="Imprimir la transcripción en pantalla")
    parser.add_argument('-c', '--clipboard', action="store_true", help="Copiar la transcripción al portapapeles")
    args = parser.parse_args()

    if args.input is not None:
        with open(args.input, encoding=args.inputencoding) as f:
            input = f.read()
    else:
        input = args.texto
    
    output = transcribe(input)
    
    if args.print:
        print(output)

    if args.clipboard:
        copy(output)
    
    if args.output is not None:
        with open(args.output, "w", encoding=args.outputencoding) as f:
            f.write(output)