# Transcpción a *tengwar* en Python

## Requisitos

Este programa funciona de manera local y no requiere conexión a Internet. Para emplearlo es necesario que el equipo tenga Python 3 y que el entorno en el que se ejecute cuente con el módulo [pyperclip](https://pypi.org/project/pyperclip/).

## Instrucciones de uso

```
python tengwar.py [-h] [-i INPUT] [-ie INPUTENCODING] [-o OUTPUT]
                         [-oe OUTPUTENCODING] [-p] [-c]
                         [texto]

argumentos posicionales:
  texto                 Texto a transcribir

argumentos opcionales:
  -h, --help            muestra la ayuda
  -i INPUT, --input INPUT
                        Archivo con el texto de entrada
  -ie INPUTENCODING, --inputencoding INPUTENCODING
                        Codificación del texto de entrada
  -o OUTPUT, --output OUTPUT
                        Archivo en el que escribir el texto de salida
  -oe OUTPUTENCODING, --outputencoding OUTPUTENCODING
                        Codificación del texto de salida
  -p, --print           Imprimir la transcripción en pantalla
  -c, --clipboard       Copiar la transcripción al portapapeles
```

## Modos de transcripción y codificación de texto y *tengwar*

Actualmente las transcripciones se hacen únicamente según el [modo de escritura para castellano](http://lambenor.free.fr/tengwar/espanol_2006),
según la [propuesta de codificación de *tengwar* para Unicode](https://www.evertype.com/standards/iso10646/pdf/tengwar.pdf)
con las adaptaciones de la fuente [Tengwar Telcontar](https://freetengwar.sourceforge.net/tengtelc.html).

La codificación de los textos considerada por defecto es [UTF-8](https://es.wikipedia.org/wiki/UTF-8). Véanse otras codificaciones de texto que pueden emplearse con Python en:
https://docs.python.org/3/library/codecs.html#standard-encodings

## Consejos de uso

Para visualizar correctamente las transcripciones, es necesario tener una fuente compatible con la codificación de *tengwar* empleada,
y un visor o editor de texto que permita la correcta representación de esas fuentes.
En particular, para visualizar la fuente Tengwar Telcontar es necesario que soporte
el sistema [Graphite](https://graphite.sil.org/) para *smart fonts*.

Entre otras aplicaciones compatibles con Graphite, se encuentran:
* Todas las herramientas de [LibreOffice](https://www.libreoffice.org/) (y también [OpenOffice](https://www.openoffice.org/es/) desde la versión 3.2): Text, Calc, Impress, etc.
* El navegador de Mozilla [Firefox](https://www.mozilla.org/es-ES/firefox/) y el gestor de correo [Thunderbird](https://www.thunderbird.net/es-ES/).
* El sistema de composición tipográfica para TeX [XeTeX](https://xetex.sourceforge.net/).

Entre las aplicaciones más populares, se puede destacar que el procesador de texto MS Word y el navegador Chrome **no son compatibles con Graphite** (y por tanto tampoco con la fuente Tengwar Telcontar).


## Relacion con [Tecendil](https://tecendil.com/)

Las reglas para hacer las transcripciones se definen en archivos `jsonc` que siguen las [especificaciones de Tecendil](https://github.com/arnog/tecendil-js/blob/master/modes/README.md) (de hecho pueden utilizarse los mismos archivos).

El programa está diseñado para realizar las transcripciones de la manera más parecida posible a como se hace en Tecendil, aunque está desarrollado de manera independiente, y pueden existir diferencias.

Si encuentras discrepancias entre los resultado de Tecendil y de este programa, siéntete libre de informar en la sección de "Problemas" ([Issues](https://github.com/heliosdrm/tengwar-transcript/issues)) —y si te animas, incluso de proponer mejoras del código a través [Pull Requests](https://github.com/heliosdrm/tengwar-transcript/pulls).

Por otro lado, si encuentras algún error en la transcripción que también ocurra en Tecendil, es preferible reportarlo en el [repositorio de Tecendil](https://github.com/arnog/tecendil-js) —que tratará de sincronizarse con este en la medida de lo posible—.
