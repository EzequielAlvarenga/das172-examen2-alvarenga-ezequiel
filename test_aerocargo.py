"""
Pruebas unitarias para el módulo aerocargo.py usando unittest.
Cubre casos de éxito, bordes y validaciones de matriz.
"""

import unittest
from aerocargo import (
    validar_coherencia_dimensional,
    calcular_ocupacion_y_sobrecarga,
    evaluar_balance_y_simetria,
    extraer_submatriz_sobrecarga_critica
)

class TestAeroCargo(unittest.TestCase):

    def setUp(self):
        self.cargas_validas = [
            [500, 600, 400],
            [300, 200, 500]
        ]
        self.capacidades_validas = [
            [1000, 1000, 1000],
            [1000, 1000, 1000]
        ]

    def test_validar_coherencia_dimensional_valida(self):
        res = validar_coherencia_dimensional(self.cargas_validas, self.capacidades_validas)
        self.assertTrue(res)

    def test_validar_coherencia_dimensional_invalidas(self):
        # Caso 1: Dimensiones de fila inconsistentes
        cargas_inval = [[500, 600], [300]]
        res1 = validar_coherencia_dimensional(cargas_inval, self.capacidades_validas)
        self.assertFalse(res1)

        # Caso 2: Capacidad negativa o cero
        cap_inval = [[1000, -100], [1000, 1000]]
        res2 = validar_coherencia_dimensional(self.cargas_validas, cap_inval)
        self.assertFalse(res2)

    def test_calcular_ocupacion_y_sobrecarga(self):
        cargas_sobrecargadas = [
            [1100, 600, 400],
            [300, 1200, 500]
        ]
        res = calcular_ocupacion_y_sobrecarga(cargas_sobrecargadas, self.capacidades_validas)
        
        self.assertEqual(res["matriz_porcentajes"][0][0], 110.0)
        self.assertIn((0, 0), res["celdas_sobrecargadas"])
        self.assertIn((1, 1), res["celdas_sobrecargadas"])
        self.assertEqual(len(res["celdas_sobrecargadas"]), 2)

    def test_evaluar_balance_y_simetria(self):
        res = evaluar_balance_y_simetria(self.cargas_validas, tolerancia_kg=100.0)
        
        self.assertEqual(res["pesos_longitudinales"], [1500, 1000])
        self.assertEqual(res["desbalance_lateral_kg"], 100.0)
        self.assertTrue(res["balance_aprobado"])

    def test_extraer_submatriz_sobrecarga_critica(self):
        matriz_p = [
            [50.0, 80.0, 90.0],
            [60.0, 110.0, 120.0]
        ]
        # Submatriz 2x2 más crítica
        sub = extraer_submatriz_sobrecarga_critica(matriz_p, 2, 2)
        esperada = [
            [80.0, 90.0],
            [110.0, 120.0]
        ]
        self.assertEqual(sub, esperada)

if __name__ == "__main__":
    unittest.main()
    