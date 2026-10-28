"""Pruebas de resultados, invariantes y comparación con un oráculo independiente."""
import itertools
from collections import Counter
from contextlib import redirect_stdout
from io import StringIO
import unittest

import proyecto as p


class PruebasCombinatoria(unittest.TestCase):
    def test_cuatro_ejemplos(self):
        casos = [('pd', ['a', 'b', 'c', 'd'], None, 24),
                 ('pi', ['a', 'a', 'b', 'c'], None, 12),
                 ('cd', ['a', 'b', 'c', 'd'], 2, 6),
                 ('ci', ['a', 'a', 'b', 'c'], 2, 4)]
        for caso, objetos, r, esperado in casos:
            with self.subTest(caso=caso):
                total, generador = p.calcular(caso, objetos, r)
                resultados = list(generador)
                self.assertEqual(total, esperado)
                self.assertEqual(len(resultados), total)
                self.assertEqual(len(set(resultados)), total)
        self.assertEqual(list(p.combinaciones_iguales(['a', 'a', 'b', 'c'], 2)),
                         [('a', 'a'), ('a', 'b'), ('a', 'c'), ('b', 'c')])

    def test_multiconjuntos_con_oraculo_por_posiciones(self):
        # 1+3+9+...+3^5 = 364 entradas; orden arbitrario y multiplicidades variadas.
        for n in range(6):
            for datos in itertools.product('abc', repeat=n):
                with self.subTest(datos=datos):
                    esperado = set(itertools.permutations(datos))
                    obtenido = list(p.permutaciones_iguales(datos))
                    self.assertEqual(set(obtenido), esperado)
                    self.assertEqual(len(obtenido), len(esperado))
                    self.assertEqual(p.contar_permutaciones_iguales(datos), len(esperado))
                    for r in range(n + 1):
                        esperado_c = {tuple(sorted(c)) for c in itertools.combinations(datos, r)}
                        obtenido_c = list(p.combinaciones_iguales(datos, r))
                        self.assertEqual(set(obtenido_c), esperado_c)
                        self.assertEqual(len(obtenido_c), len(esperado_c))
                        self.assertEqual(p.contar_combinaciones_iguales(datos, r), len(esperado_c))
                        for seleccion in obtenido_c:
                            self.assertFalse(Counter(seleccion) - Counter(datos))

    def test_diferentes_y_bordes(self):
        for n in range(7):
            datos = list('abcdef'[:n])
            for caso in ['pd', 'pi']:
                total, gen = p.calcular(caso, datos)
                self.assertEqual(total, len(list(gen)))
            for r in range(n + 1):
                total, gen = p.calcular('cd', datos, r)
                self.assertEqual(total, len(list(gen)))
        self.assertEqual(list(p.permutaciones_iguales([])), [()])
        self.assertEqual(list(p.combinaciones_iguales([], 0)), [()])
        self.assertEqual(p.contar_combinaciones_iguales(['a'] * 100, 50), 1)
        self.assertEqual(p.contar_permutaciones_iguales(['a'] * 100), 1)

    def test_etiquetas_completas_y_orden(self):
        self.assertEqual(list(p.permutaciones_iguales(['rojo', 'azul', 'rojo'])),
                         [('azul', 'rojo', 'rojo'), ('rojo', 'azul', 'rojo'),
                          ('rojo', 'rojo', 'azul')])
        self.assertEqual(list(p.combinaciones_iguales(['b', 'a', 'a'], 2)),
                         [('a', 'a'), ('a', 'b')])

    def test_entradas_invalidas(self):
        for funcion in [p.contar_permutaciones_diferentes, p.permutaciones_diferentes]:
            with self.assertRaises(ValueError):
                funcion(['a', 'a'])
        for caso in ['cd', 'ci']:
            for r in [-1, 4, 1.5, True, None]:
                with self.subTest(caso=caso, r=r), self.assertRaises(ValueError):
                    p.calcular(caso, ['a', 'b', 'c'], r)
        for datos in [[''], [7], 'abc']:
            with self.assertRaises(ValueError):
                p.contar_permutaciones_iguales(datos)
        with self.assertRaises(ValueError):
            p.calcular('inexistente', ['a'])

    def test_limite_no_modifica_el_total(self):
        salida = StringIO()
        with redirect_stdout(salida):
            p.mostrar('pd', ('a', 'b', 'c', 'd'), None, limite=2)
        self.assertIn('Total: 24', salida.getvalue())
        self.assertIn('Se muestran 2 de 24', salida.getvalue())
        self.assertNotIn('  3.', salida.getvalue())


if __name__ == '__main__':
    unittest.main()
