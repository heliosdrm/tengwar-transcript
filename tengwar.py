from functions import transcribe
from pyperclip import copy
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Transcribir a Tengwar')
    parser.add_argument('texto', nargs='?', help="Texto a transcribir", default="")
    parser.add_argument('-p', '--print', action="store_true", help="Imprimir la transcripción en pantalla")
    parser.add_argument('-i', '--input', help="Archivo con el texto de entrada")
    parser.add_argument('-ie', '--inputencoding', help="Codificación del texto de entrada", default="utf-8")
    parser.add_argument('-o', '--output', help="Archivo en el que escribir el texto de salida")
    parser.add_argument('-oe', '--outputencoding', help="Codificación del texto de salida", default="utf-8")
    args = parser.parse_args()

    if args.input is not None:
        with open(args.input, encoding=args.inputencoding) as f:
            input = f.read()
    else:
        input = args.texto
    
    output = transcribe(input)
    
    if args.print:
        print(output)
    
    if args.output is not None:
        with open(args.output, "w", encoding=args.outputencoding) as f:
            f.write(output)
    else:
        copy(output)