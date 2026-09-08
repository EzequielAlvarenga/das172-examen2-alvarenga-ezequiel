"""
Módulo de cálculo y auditoría de carga matricial para aeronaves (AeroCargo-Matrix).
Contiene funciones puras e inmutables para validación, balance y sobrecarga.
"""

def validar_coherencia_dimensional(cargas_reales, capacidades_maximas):
    """Verifica dimensiones, regularidad y coherencia de valores en las matrices."""
    if not cargas_reales or not capacidades_maximas:
        return False
    
    n = len(cargas_reales)
    m = len(cargas_reales[0])
    
    if n < 2 or m < 2:
        return False
    
    if len(capacidades_maximas) != n:
        return False
        
    for i in range(n):
        if len(cargas_reales[i]) != m or len(capacidades_maximas[i]) != m:
            return False
        
        for j in range(m):
            peso = cargas_reales[i][j]
            capacidad = capacidades_maximas[i][j]
            
            if peso < 0 or capacidad <= 0:
                return False
                
    return True


def calcular_ocupacion_y_sobrecarga(cargas_reales, capacidades_maximas):
    """Genera la matriz de porcentaje de ocupación y lista celdas sobrecargadas (>100%)."""
    n = len(cargas_reales)
    m = len(cargas_reales[0])
    
    matriz_porcentajes = []
    celdas_sobrecargadas = []
    
    for i in range(n):
        fila_porcentajes = []
        for j in range(m):
            porcentaje = (cargas_reales[i][j] / capacidades_maximas[i][j]) * 100.0
            fila_porcentajes.append(porcentaje)
            
            if porcentaje > 100.0:
                celdas_sobrecargadas.append((i, j))
                
        matriz_porcentajes.append(fila_porcentajes)
        
    return {
        "matriz_porcentajes": matriz_porcentajes,
        "celdas_sobrecargadas": celdas_sobrecargadas
    }


def evaluar_balance_y_simetria(cargas_reales, tolerancia_kg):
    """Calcula pesos por fila longitudinal y evalúa desbalance lateral babor/estribor."""
    n = len(cargas_reales)
    m = len(cargas_reales[0])
    
    pesos_longitudinales = [sum(fila) for fila in cargas_reales]
    
    mitad_m = m // 2
    suma_izquierda = 0.0
    suma_derecha = 0.0
    
    for i in range(n):
        # Sumar lado izquierdo (babor)
        for j in range(mitad_m):
            suma_izquierda += cargas_reales[i][j]
            
        # Sumar lado derecho (estribor), ignorando columna central si M es impar
        inicio_derecha = mitad_m + 1 if m % 2 != 0 else mitad_m
        for j in range(inicio_derecha, m):
            suma_derecha += cargas_reales[i][j]
            
    desbalance_lateral = abs(suma_izquierda - suma_derecha)
    estado_balance = desbalance_lateral <= tolerancia_kg
    
    return {
        "pesos_longitudinales": pesos_longitudinales,
        "desbalance_lateral_kg": desbalance_lateral,
        "balance_aprobado": estado_balance
    }


def extraer_submatriz_sobrecarga_critica(matriz_porcentajes, k, p):
    """Encuentra la submatriz k x p con el mayor promedio de porcentaje de ocupación."""
    n = len(matriz_porcentajes)
    m = len(matriz_porcentajes[0])
    
    if k > n or p > m or k <= 0 or p <= 0:
        return []
        
    max_promedio = -1.0
    mejor_submatriz = []
    
    for i in range(n - k + 1):
        for j in range(m - p + 1):
            submatriz_actual = []
            suma_porcentajes = 0.0
            
            for sub_i in range(k):
                fila_sub = []
                for sub_j in range(p):
                    valor = matriz_porcentajes[i + sub_i][j + sub_j]
                    fila_sub.append(valor)
                    suma_porcentajes += valor
                submatriz_actual.append(fila_sub)
                
            promedio_actual = suma_porcentajes / (k * p)
            if promedio_actual > max_promedio:
                max_promedio = promedio_actual
                mejor_submatriz = submatriz_actual
                
    return mejor_submatriz
