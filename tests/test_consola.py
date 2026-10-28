"""Pruebas de uso real por consola, sin modificar el programa."""
from pathlib import Path
import subprocess
import sys
import unittest

PROGRAMA = Path(__file__).resolve().parents[1] / 'proyecto.py'


class PruebasConsola(unittest.TestCase):
    def ejecutar(self, *argumentos, entrada=None):
        return subprocess.run([sys.executable, str(PROGRAMA), *argumentos],
                              input=entrada, text=True, capture_output=True, timeout=10)

    def test_ejemplos_completos(self):
        salida = self.ejecutar()
        self.assertEqual(salida.returncode, 0)
        bloques = salida.stdout.split('=== Ejemplo ')[1:]
        self.assertEqual(len(bloques), 4)
        for bloque, total in zip(bloques, [24, 12, 6, 4]):
            self.assertIn(f'Total: {total}\n', bloque)
            filas = [linea for linea in bloque.splitlines()
                     if linea.strip().split('. ', 1)[0].isdigit()]
            self.assertEqual(len(filas), total)
        self.assertNotIn('Se muestran', salida.stdout)

    def test_cuatro_opciones_del_menu(self):
        consultas = [('1\na b c d\n0\n', 24), ('2\na a b c\n0\n', 12),
                     ('3\na b c d\n2\n0\n', 6), ('4\na a b c\n2\n0\n', 4)]
        for entrada, total in consultas:
            with self.subTest(total=total):
                salida = self.ejecutar('--interactivo', entrada=entrada)
                self.assertEqual(salida.returncode, 0)
                self.assertIn(f'Total: {total}\n', salida.stdout)

    def test_recuperacion_tras_error(self):
        # Primera consulta: r=5 es inválido; segunda consulta: r=2 es válida.
        salida = self.ejecutar('--interactivo', entrada='4\na a b c\n5\n4\na a b c\n2\n0\n')
        self.assertEqual(salida.returncode, 0)
        self.assertIn('Error:', salida.stdout)
        self.assertIn('r debe ser un entero entre 0 y 4.', salida.stdout)
        self.assertIn('Total: 4\n', salida.stdout)
        self.assertNotIn('Traceback', salida.stdout + salida.stderr)
        salida = self.ejecutar('--interactivo', entrada='4\na a b c\ndos\n0\n')
        self.assertEqual(salida.returncode, 0)
        self.assertIn('Error:', salida.stdout)

    def test_errores_en_consultas_directas(self):
        consultas = [(['--caso', 'cd', '--objetos', 'a', 'a', 'b', '--r', '2'],
                      'todos los objetos deben ser diferentes'),
                     (['--caso', 'ci', '--objetos', 'a', 'a', 'b', '--r', '4'],
                      'r debe ser un entero entre 0 y 3'),
                     (['--caso', 'ci', '--objetos', 'a', 'a', 'b', '--r', '-1'],
                      'r debe ser un entero entre 0 y 3')]
        for argumentos, mensaje in consultas:
            with self.subTest(argumentos=argumentos):
                salida = self.ejecutar(*argumentos)
                self.assertEqual(salida.returncode, 2)
                self.assertIn(mensaje, salida.stderr)
                self.assertNotIn('Traceback', salida.stderr)


if __name__ == '__main__':
    unittest.main()
