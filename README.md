# AeroCargo-Matrix (Auditoría de Carga Matricial)

Sistema interactivo en Python para la auditoría, procesamiento matricial, análisis de balance físico y detección de sobrecargas en aeronaves comerciales y de carga.

---

## 1. Descripción del Problema y Marco Teórico

En el ámbito aeronáutico, la distribución del peso dentro de la cabina de carga es un factor crítico de seguridad operacional. La carga se organiza como una matriz bidimensional $N \times M$, donde $N$ representa las filas (secciones longitudinales de proa a popa) y $M$ las columnas (posiciones laterales de babor a estribor).

* **Celda $(i, j)$**: Representa un contenedor o bahía individual de carga.
* **Capacidad del Piso**: Límite físico en kilogramos que puede soportar una sección de la estructura de la aeronave sin comprometer la integridad estructural.
* **Distribución Longitudinal**: Suma de pesos por filas. Influye directamente en el centro de gravedad ($CG$) a lo largo del eje longitudinal y el trimado del elevador.
* **Balance Lateral**: Simetría de pesos entre el lado izquierdo (babor) y el lado derecho (estribor). Un desbalance superior a la tolerancia genera momentos de guiñada/alabeo no compensados.

---

## 2. Arquitectura Modular

El proyecto se estructura bajo el principio de separación de responsabilidades e inmutabilidad de datos:

```text
              ┌──────────────────────┐
              │       main.py        │
              │   Interfaz CLI       │
              └──────────┬───────────┘
                         │
                         ▼
           ┌──────────────────────────┐
           │ validar_coherencia_      │
           │ dimensional()            │
           └────────────┬─────────────┘
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
   ┌──────────────────┐   ┌──────────────────┐
   │ calcular_        │   │ evaluar_balance_ │
   │ ocupacion()      │   │ y_simetria()     │
   └────────┬─────────┘   └────────┬─────────┘
            │                      │
            └──────────┬───────────┘
                       ▼
          ┌─────────────────────────┐
          │ extraer_submatriz_      │
          │ sobrecarga_critica()    │
          └─────────────────────────┘
Módulos Principalesaerocargo.py: Contiene funciones puras de procesamiento matricial sin efectos secundarios ni variables globales.main.py: Punto de entrada que gestiona la interacción con el usuario y la visualización de reportes.test_aerocargo.py: Batería de pruebas unitarias implementada con unittest.3. Complejidad Computacional (Big-O)Validación de Coherencia ($O(N \times M)$): Recorre cada celda de ambas matrices una sola vez para verificar no negatividad y dimensiones.Cálculo de Ocupación y Sobrecargas ($O(N \times M)$): Opera elemento a elemento creando una nueva matriz de porcentajes de dimensión $N \times M$.Evaluación de Balance ($O(N \times M)$): Acumula sumas por fila y por mitad de columna recorriendo la matriz completa una vez.Búsqueda de Submatriz Crítica ($O((N-k+1)(M-p+1) \cdot k \cdot p)$): Para una ventana deslizable de tamaño $k \times p$, la complejidad es proporcional al número de posiciones de ventana multiplicadas por el tamaño de la submatriz. Para valores constantes de $k$ y $p$, se simplifica a $O(N \times M)$.Complejidad Espacial: El cálculo de ocupación requiere una nueva matriz de tamaño $N \times M$, por lo que utiliza $O(N \times M)$ memoria adicional. Las funciones de balance y validación utilizan memoria adicional proporcional al vector de pesos longitudinales o a variables escalares. Considerando el flujo completo, el espacio requerido es $O(N \times M)$.4. Instrucciones de Uso y EjecuciónRequisitosPython 3.8 o superior.Ejecución de la aplicaciónBashpython main.py
Ejecución de Pruebas UnitariasBashpython -m unittest test_aerocargo.py
5. Ejemplo de Ejecución ReproducibleMatriz de Cargas Reales (kg)Plaintext[500, 600, 1200]
[400, 500, 600]
Matriz de Capacidades Máximas (kg)Plaintext[1000, 1000, 1000]
[1000, 1000, 1000]
Salida del Reporte de AuditoríaPlaintext==================================================
        AEROCARGO-MATRIX: INFORME FINAL
==================================================

1. MATRIZ DE OCUPACIÓN (%):
  [ 50.00%,  60.00%, 120.00%]
  [ 40.00%,  50.00%,  60.00%]

2. CELDAS SOBRECARGADAS (>100%):
  - Fila 0, Columna 2: 120.00%

3. BALANCE Y SIMETRÍA:
  - Pesos Longitudinales: [2300.0 kg, 1500.0 kg]
  - Desbalance Lateral: 900.0 kg
  - Estado: RECHAZADO (Excede tolerancia)