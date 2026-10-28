# Proyecto 3: permutaciones y combinaciones

Programa de consola en español basado en Rosen, *Discrete Mathematics and Its Applications*, 8.ª edición, secciones 6.3, 6.5 y 6.6.

## Requisitos

Python 3.10 o posterior. No requiere instalar paquetes.

## Ejecutar

Este README está en `documentacion/`. Ejecuta los siguientes comandos desde la raíz del repositorio (si estás en esta carpeta, usa primero `cd ..`):

```bash
python3 proyecto.py
```

Este comando imprime **todas** las soluciones de los cuatro ejemplos solicitados, con totales **24, 12, 6 y 4**.

Para abrir el menú y consultar otros datos:

```bash
python3 proyecto.py --interactivo
```

También admite consultas directas:

```bash
python3 proyecto.py --caso pd --objetos a b c d
python3 proyecto.py --caso pi --objetos a a b c
python3 proyecto.py --caso cd --objetos a b c d --r 2
python3 proyecto.py --caso ci --objetos a a b c --r 2
```

- `pd`: permutaciones de objetos diferentes; se utilizan todos los objetos.
- `pi`: permutaciones de objetos iguales; las copias con la misma etiqueta son indistinguibles.
- `cd`: combinaciones de objetos diferentes, sin reposición.
- `ci`: combinaciones de objetos iguales, respetando las copias disponibles.

Los objetos se separan con espacios; una etiqueta puede tener varias letras. Las etiquetas distinguen mayúsculas y minúsculas. En las opciones de objetos diferentes se rechazan etiquetas repetidas.

Por defecto, las consultas muestran hasta 50 resultados. El total siempre es exacto; el límite solo afecta la lista. Para mostrar más:

```bash
python3 proyecto.py --caso pd --objetos a b c d e --limite 120
```

La consola admite hasta 100 objetos por consulta. Las combinaciones aceptan `0 <= r <= n`; una selección de tamaño cero es `()`. La entrada vacía tiene una permutación y una combinación de tamaño cero.

## Interpretación del cuarto ejemplo

Se seleccionan dos objetos **del multiconjunto finito** `a, a, b, c`: `(a,a), (a,b), (a,c), (b,c)`. No se permiten `(b,b)` ni `(c,c)` porque no hay dos copias disponibles. Esto es distinto de la repetición ilimitada de tipos, cuya fórmula sería `C(k+r-1,r)` y daría 6 para los tres tipos `a,b,c` con `r=2`.

## Pruebas

```bash
python3 -m unittest discover -s tests -v
```

Las diez pruebas cubren los cuatro ejemplos, entradas inválidas, etiquetas de varias letras, límites de visualización, casos vacíos y comparación de los algoritmos de multiconjuntos con un método independiente sobre 364 listas pequeñas. `documentacion/resultados.txt` registra la ejecución de los cuatro ejemplos.

## Archivos para entregar

- `proyecto.py`: programa completo y autónomo.
- `documentacion/informe.tex`: documentación en LaTeX.
- `documentacion/informe.pdf`: PDF compilado desde ese archivo TEX.

Las pruebas están en `tests/`. El informe, su fuente LaTeX, los resultados y este README están en `documentacion/`. Para recompilar el informe con una distribución LaTeX:

```bash
cd documentacion
pdflatex informe.tex
pdflatex informe.tex
```

O en Overleaf: crear un proyecto, subir `informe.tex` y compilar. El TEX es autónomo y no requiere archivos adicionales.

## Entrega y presentación

Adjuntar directamente en Canvas `proyecto.py`, `documentacion/informe.tex` y `documentacion/informe.pdf`. No sustituirlos por enlaces al repositorio. La exposición en clase es parte de la evaluación. `documentacion/guion_presentacion.txt` contiene una propuesta de demostración para el grupo.

Las entradas, resultados esperados y observados se registran en `documentacion/casos_verificados.txt`. La ejecución de las diez pruebas está en `documentacion/pruebas_automatizadas.txt`.
