# AeroCargo-Matrix (Auditoría de Carga Matricial)

Herramienta CLI para el procesamiento, análisis y auditoría de distribución de carga en aeronaves comerciales y de carga.

## Estructura del Proyecto

- `aerocargo.py`: Módulo principal con funciones puras para procesamiento matricial, validación, balance lateral y submatrices críticas.
- `test_aerocargo.py`: Suite de pruebas unitarias implementadas con `unittest`.
- `main.py`: Interfaz de línea de comandos (CLI) interactiva.
- `.gitignore`: Configuración de archivos excluidos del control de versiones.

## Requisitos

- Python 3.8+

## Instrucciones de Uso

### Ejecutar la aplicación interactiva
```bash
python main.py
python -m unittest test_aerocargo.py
```