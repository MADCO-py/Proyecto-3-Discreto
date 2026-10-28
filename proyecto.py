#!/usr/bin/env python3
"""Permutaciones y combinaciones de conjuntos y multiconjuntos finitos.

Python 3.10 o posterior; solo utiliza la biblioteca estándar.
Ejecutar ejemplos: python3 proyecto.py
Menú interactivo:  python3 proyecto.py --interactivo
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations, islice, permutations
from math import comb, factorial, prod
from typing import Iterable, Iterator

Objetos = tuple[str, ...]


def _objetos(valores: Iterable[str], distintos: bool = False) -> Objetos:
    """Valida etiquetas; objetos iguales tienen exactamente la misma etiqueta."""
    if isinstance(valores, (str, bytes)):
        raise ValueError("Usa una lista de etiquetas, por ejemplo ['a', 'b'].")
    resultado = tuple(valores)
    if any(not isinstance(x, str) or not x.strip() for x in resultado):
        raise ValueError("Cada objeto debe tener una etiqueta de texto no vacía.")
    if distintos and len(set(resultado)) != len(resultado):
        raise ValueError("En este caso todos los objetos deben ser diferentes.")
    return resultado


def _tamano(r: int, n: int) -> None:
    if isinstance(r, bool) or not isinstance(r, int) or not 0 <= r <= n:
        raise ValueError(f"r debe ser un entero entre 0 y {n}.")


def contar_permutaciones_diferentes(objetos: Iterable[str]) -> int:
    """Número de ordenaciones completas de n objetos diferentes: n!."""
    return factorial(len(_objetos(objetos, distintos=True)))


def permutaciones_diferentes(objetos: Iterable[str]) -> Iterator[Objetos]:
    """Genera cada ordenación completa una vez."""
    return permutations(sorted(_objetos(objetos, distintos=True)))


def contar_permutaciones_iguales(objetos: Iterable[str]) -> int:
    """Número de ordenaciones de un multiconjunto: n! / producto(m_i!)."""
    datos = _objetos(objetos)
    return factorial(len(datos)) // prod(factorial(m) for m in Counter(datos).values())


def permutaciones_iguales(objetos: Iterable[str]) -> Iterator[Objetos]:
    """Backtracking por frecuencias: no genera copias equivalentes."""
    datos = _objetos(objetos)
    frecuencias = Counter(datos)
    etiquetas = sorted(frecuencias)
    camino: list[str] = []

    def generar() -> Iterator[Objetos]:
        if len(camino) == len(datos):
            yield tuple(camino)
            return
        for etiqueta in etiquetas:
            if frecuencias[etiqueta] > 0:
                frecuencias[etiqueta] -= 1
                camino.append(etiqueta)
                yield from generar()
                camino.pop()
                frecuencias[etiqueta] += 1

    return generar()


def contar_combinaciones_diferentes(objetos: Iterable[str], r: int) -> int:
    """Número de selecciones sin orden de r objetos diferentes: C(n,r)."""
    datos = _objetos(objetos, distintos=True)
    _tamano(r, len(datos))
    return comb(len(datos), r)


def combinaciones_diferentes(objetos: Iterable[str], r: int) -> Iterator[Objetos]:
    datos = _objetos(objetos, distintos=True)
    _tamano(r, len(datos))
    return combinations(sorted(datos), r)


def contar_combinaciones_iguales(objetos: Iterable[str], r: int) -> int:
    """Cuenta selecciones de un multiconjunto finito con programación dinámica.

    dp[j] cuenta las selecciones de tamaño j usando los tipos ya procesados.
    Para una multiplicidad m: nuevo[j] = suma(dp[j-t], 0 <= t <= m).
    Una ventana deslizante evalúa cada transición en tiempo constante.
    """
    datos = _objetos(objetos)
    _tamano(r, len(datos))
    dp = [1] + [0] * r
    for multiplicidad in Counter(datos).values():
        nuevo = [0] * (r + 1)
        ventana = 0
        for j in range(r + 1):
            ventana += dp[j]
            if j > multiplicidad:
                ventana -= dp[j - multiplicidad - 1]
            nuevo[j] = ventana
        dp = nuevo
    return dp[r]


def combinaciones_iguales(objetos: Iterable[str], r: int) -> Iterator[Objetos]:
    """Genera selecciones sin orden respetando las existencias de cada tipo."""
    datos = _objetos(objetos)
    _tamano(r, len(datos))
    frecuencias = Counter(datos)
    etiquetas = sorted(frecuencias)
    camino: list[str] = []

    def generar(inicio: int) -> Iterator[Objetos]:
        if len(camino) == r:
            yield tuple(camino)
            return
        for indice in range(inicio, len(etiquetas)):
            etiqueta = etiquetas[indice]
            if frecuencias[etiqueta] > 0:
                frecuencias[etiqueta] -= 1
                camino.append(etiqueta)
                # Reutilizar el índice permite otra copia del mismo tipo,
                # mientras su frecuencia restante sea positiva.
                yield from generar(indice)
                camino.pop()
                frecuencias[etiqueta] += 1

    return generar(0)


TITULOS = {
    "pd": "Permutaciones de objetos diferentes",
    "pi": "Permutaciones de objetos iguales",
    "cd": "Combinaciones de objetos diferentes",
    "ci": "Combinaciones de objetos iguales",
}


def calcular(caso: str, objetos: Iterable[str], r: int | None = None) -> tuple[int, Iterator[Objetos]]:
    """Devuelve el total exacto y un generador para uno de los cuatro casos."""
    datos = _objetos(objetos)
    if caso == "pd":
        return contar_permutaciones_diferentes(datos), permutaciones_diferentes(datos)
    if caso == "pi":
        return contar_permutaciones_iguales(datos), permutaciones_iguales(datos)
    if caso in ("cd", "ci"):
        if r is None:
            raise ValueError("Las combinaciones requieren el tamaño r.")
        if caso == "cd":
            return contar_combinaciones_diferentes(datos, r), combinaciones_diferentes(datos, r)
        return contar_combinaciones_iguales(datos, r), combinaciones_iguales(datos, r)
    raise ValueError("El caso debe ser pd, pi, cd o ci.")


def mostrar(caso: str, datos: Objetos, r: int | None, limite: int = 50) -> None:
    total, generador = calcular(caso, datos, r)
    print(TITULOS[caso])
    print("Objetos:", ", ".join(datos) or "(vacío)")
    if caso in ("cd", "ci"):
        print(f"Tamaño de selección: {r}")
    print(f"Total: {total}")
    for indice, resultado in enumerate(islice(generador, limite), 1):
        # Las comas distinguen etiquetas de varias letras: ('ab', 'c').
        print(f"{indice:>3}. ({', '.join(resultado)})")
    if total > limite:
        print(f"Se muestran {limite} de {total} resultados. El total es exacto.")


def ejemplos(limite: int = 50) -> None:
    casos = [("pd", ("a", "b", "c", "d"), None),
             ("pi", ("a", "a", "b", "c"), None),
             ("cd", ("a", "b", "c", "d"), 2),
             ("ci", ("a", "a", "b", "c"), 2)]
    for numero, (caso, datos, r) in enumerate(casos, 1):
        print(f"\n=== Ejemplo {numero} ===")
        mostrar(caso, datos, r, limite)


def interactivo(limite: int) -> None:
    opciones = {str(i): caso for i, caso in enumerate(TITULOS, 1)}
    while True:
        print("\nCALCULADORA DE PERMUTACIONES Y COMBINACIONES")
        for opcion, caso in opciones.items():
            print(f"{opcion}. {TITULOS[caso]}")
        print("5. Ejecutar los cuatro ejemplos\n0. Salir")
        try:
            opcion = input("Opción: ").strip()
            if opcion == "0":
                return
            if opcion == "5":
                ejemplos(limite)
                continue
            if opcion not in opciones:
                print("Opción inválida.")
                continue
            caso = opciones[opcion]
            datos = tuple(input("Objetos separados por espacios (ej.: a a b c): ").split())
            if len(datos) > 100:
                raise ValueError("El menú admite hasta 100 objetos por consulta.")
            r = int(input("Cantidad a seleccionar r: ")) if caso in ("cd", "ci") else None
            mostrar(caso, datos, r, limite)
        except ValueError as error:
            print(f"Error: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nFin del programa.")
            return


def entero_positivo(texto: str) -> int:
    try:
        valor = int(texto)
    except ValueError as error:
        raise argparse.ArgumentTypeError("Debe ser un entero positivo.") from error
    if valor < 1:
        raise argparse.ArgumentTypeError("Debe ser un entero positivo.")
    return valor


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--interactivo", action="store_true", help="Abrir el menú de consultas.")
    parser.add_argument("--caso", choices=TITULOS, help="pd, pi, cd o ci.")
    parser.add_argument("--objetos", nargs="*", help="Etiquetas separadas por espacios.")
    parser.add_argument("--r", type=int, help="Cantidad de objetos a seleccionar.")
    parser.add_argument("--limite", type=entero_positivo, default=50,
                        help="Máximo de resultados a mostrar (por defecto: 50).")
    args = parser.parse_args()
    if args.interactivo and (args.caso is not None or args.objetos is not None or args.r is not None):
        parser.error("Usa --interactivo sin --caso, --objetos ni --r.")
    if args.interactivo:
        interactivo(args.limite)
    elif args.caso is not None:
        if args.objetos is None:
            parser.error("Indica --objetos después de --caso.")
        if len(args.objetos) > 100:
            parser.error("La consola admite hasta 100 objetos por consulta.")
        if args.caso in ("pd", "pi") and args.r is not None:
            parser.error("Las permutaciones usan todos los objetos; omite --r.")
        try:
            mostrar(args.caso, tuple(args.objetos), args.r, args.limite)
        except ValueError as error:
            parser.error(str(error))
    else:
        if args.objetos is not None or args.r is not None:
            parser.error("Indica --caso para proporcionar objetos o r.")
        ejemplos(args.limite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
