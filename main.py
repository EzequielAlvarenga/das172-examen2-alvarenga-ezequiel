"""
Punto de entrada CLI para la herramienta de auditoría de carga matricial AeroCargo-Matrix.
Proporciona un menú interactivo para ingresar datos de aeronaves y ejecutar análisis.
"""

import sys
from aerocargo import (
    validar_coherencia_dimensional,
    calcular_ocupacion_y_sobrecarga,
    evaluar_balance_y_simetria,
    extraer_submatriz_sobrecarga_critica
)


def leer_matriz(filas, columnas, mensaje):
    """Solicita e ingresa los valores numéricos de una matriz desde la consola."""
    print(f"\n--- {mensaje} ---")
    matriz = []
    for i in range(filas):
        while True:
            try:
                linea = input(f"Fila {i + 1} (ingrese {columnas} valores separados por espacio): ")
                valores = [float(x) for x in linea.strip().split()]
                if len(valores) != columnas:
                    print(f" Error: Se esperaban {columnas} valores, pero ingresó {len(valores)}.")
                    continue
                matriz.append(valores)
                break
            except ValueError:
                print(" Error: Ingrese números válidos separados por espacios.")
    return matriz


def mostrar_menu():
    """Despliega el menú principal de opciones."""
    print("\n==============================================")
    print("    AEROCARGO-MATRIX: SISTEMA DE AUDITORÍA    ")
    print("==============================================")
    print("1. Cargar datos de aeronave y ejecutar auditoría")
    print("2. Salir")
    print("==============================================")


def ejecutar_auditoria():
    """Coordina la lectura de matrices y ejecución de análisis."""
    try:
        print("\n--- Configuración de Dimensiones de Bodega ---")
        n = int(input("Número de filas longitudinales (N >= 2): "))
        m = int(input("Número de columnas transversales (M >= 2): "))
    except ValueError:
        print(" Error: Debe ingresar números enteros válidos para N y M.")
        return

    cargas_reales = leer_matriz(n, m, "Ingrese Matriz de Cargas Reales (kg)")
    capacidades_maximas = leer_matriz(n, m, "Ingrese Matriz de Capacidades Máximas (kg)")

    # 1. Validación
    if not validar_coherencia_dimensional(cargas_reales, capacidades_maximas):
        print("\n Error Crítico: Las matrices no cumplen con la coherencia dimensional o contienen valores inválidos.")
        return

    # 2. Ocupación y Sobrecarga
    res_ocupacion = calcular_ocupacion_y_sobrecarga(cargas_reales, capacidades_maximas)
    matriz_pct = res_ocupacion["matriz_porcentajes"]
    sobrecargadas = res_ocupacion["celdas_sobrecargadas"]

    print("\n Matriz de Porcentajes de Ocupación (%):")
    for fila in matriz_pct:
        print("  " + "  ".join(f"{val:6.2f}%" for val in fila))

    if sobrecargadas:
        print(f"\n Advertencia: Se detectaron {len(sobrecargadas)} celdas sobrecargadas:")
        for r, c in sobrecargadas:
            print(f"  - Celda [{r}, {c}]: Ocupación = {matriz_pct[r][c]:.2f}%")
    else:
        print("\n No se detectaron celdas sobrecargadas.")

    # 3. Balance y Simetría
    try:
        tolerancia = float(input("\nIngrese tolerancia de desbalance lateral (kg): "))
    except ValueError:
        tolerancia = 0.0

    res_balance = evaluar_balance_y_simetria(cargas_reales, tolerancia)
    print("\n Resultado de Balance Lateral:")
    print(f"  - Pesos por Fila Longitudinal: {res_balance['pesos_longitudinales']}")
    print(f"  - Desbalance Lateral: {res_balance['desbalance_lateral_kg']:.2f} kg")
    print(f"  - Estado de Balance: {'APROBADO' if res_balance['balance_aprobado'] else 'RECHAZADO'}")

    # 4. Extracción Submatriz Crítica
    print("\n--- Análisis de Submatriz Crítica ---")
    try:
        k = int(input(f"Filas submatriz (k <= {n}): "))
        p = int(input(f"Columnas submatriz (p <= {m}): "))
        submatriz = extraer_submatriz_sobrecarga_critica(matriz_pct, k, p)
        
        if submatriz:
            print(f"\n Submatriz crítica {k}x{p} con mayor sobrecarga promedio:")
            for fila in submatriz:
                print("  " + "  ".join(f"{val:6.2f}%" for val in fila))
        else:
            print(" Dimensiones k o p inválidas.")
    except ValueError:
        print(" Dimensiones de submatriz inválidas.")


def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-2): ").strip()
        
        if opcion == "1":
            ejecutar_auditoria()
        elif opcion == "2":
            print("\nSaliendo del sistema de auditoría AeroCargo. ¡Hasta luego!")
            sys.exit(0)
        else:
            print(" Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()
    