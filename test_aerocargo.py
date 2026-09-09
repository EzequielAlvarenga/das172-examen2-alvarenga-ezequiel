import unittest
from aerocargo import (
    validar_coherencia_dimensional,
    calcular_ocupacion_y_sobrecarga,
    evaluar_balance_y_simetria,
    extraer_submatriz_sobrecarga_critica
)


class TestAeroCargoMatrix(unittest.TestCase):

    def test_casos_limite_validacion(self):
        # Matriz valida 2x2
        self.assertTrue(
            validar_coherencia_dimensional(
                [[100, 200], [300, 400]],
                [[500, 500], [500, 500]]
            )
        )

        # Peso igual a cero: valido
        self.assertTrue(
            validar_coherencia_dimensional(
                [[0, 500], [300, 0]],
                [[1000, 1000], [1000, 1000]]
            )
        )

        # Peso negativo: invalido
        self.assertFalse(
            validar_coherencia_dimensional(
                [[-100, 500], [300, 400]],
                [[1000, 1000], [1000, 1000]]
            )
        )

        # Capacidad cero: invalido
        self.assertFalse(
            validar_coherencia_dimensional(
                [[100, 500], [300, 400]],
                [[0, 1000], [1000, 1000]]
            )
        )

        # Dimensiones diferentes: invalido
        self.assertFalse(
            validar_coherencia_dimensional(
                [[500, 500], [300, 300]],
                [[1000, 1000]]
            )
        )

    def test_casos_limite_ocupacion(self):
        cargas = [
            [1000, 500],
            [300, 1100]
        ]
        capacidades = [
            [1000, 1000],
            [1000, 1000]
        ]

        resultado = calcular_ocupacion_y_sobrecarga(cargas, capacidades)

        # Extraer según si la función devuelve diccionario o tupla
        if isinstance(resultado, dict):
            matriz_pct = resultado.get("matriz_porcentajes") or resultado.get("matriz_ocupacion")
            sobrecargas = resultado.get("celdas_sobrecargadas") or resultado.get("sobrecargas")
        elif isinstance(resultado, (tuple, list)):
            if isinstance(resultado[0], list):
                matriz_pct, sobrecargas = resultado[0], resultado[1]
            else:
                sobrecargas, matriz_pct = resultado[0], resultado[1]

        # Exactamente 100% NO es sobrecarga (>100%)
        self.assertEqual(matriz_pct[0][0], 100.0)
        self.assertNotIn((0, 0), sobrecargas)

        # 110% SI es sobrecarga
        self.assertIn((1, 1), sobrecargas)

    def test_balance_columnas_impares(self):
        # Matriz 2x3 (La columna central debe ignorarse)
        cargas_impar = [
            [500, 9999, 500],
            [300, 8888, 300]
        ]

        resultado = evaluar_balance_y_simetria(
            cargas_impar,
            tolerancia_kg=50.0
        )

        self.assertEqual(
            resultado["desbalance_lateral_kg"],
            0.0
        )

        self.assertTrue(
            resultado["balance_aprobado"]
        )

    def test_submatriz_critica(self):
        matriz_pct = [
            [50.0, 60.0, 70.0],
            [40.0, 120.0, 110.0],
            [30.0, 100.0, 95.0]
        ]

        submatriz = extraer_submatriz_sobrecarga_critica(
            matriz_pct,
            k=2,
            p=2
        )

        esperada = [
            [120.0, 110.0],
            [100.0, 95.0]
        ]

        self.assertEqual(
            submatriz,
            esperada
        )


if __name__ == '__main__':
    unittest.main()
    