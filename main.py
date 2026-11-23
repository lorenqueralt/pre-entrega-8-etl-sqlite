"""
main.py — Orquestador del pipeline ETL.

Flujo:  CSV local  ->  limpieza + agregación mensual  ->  carga en SQLite

Uso:
    python main.py
"""
import os

from src.extract import leer_csv
from src.transform import limpiar, agregar_mensual
from src.load import cargar

RUTA_CSV = os.path.join("data", "ventas.csv")
RUTA_DB = os.path.join("data", "ventas.db")
RUTA_SCHEMA = os.path.join("sql", "schema.sql")


def main():
    print("=== Pipeline ETL: ventas -> SQLite ===")
    df = leer_csv(RUTA_CSV)                 # EXTRACT
    df = limpiar(df)                        # TRANSFORM (limpieza)
    agg = agregar_mensual(df)              #           (agregación)
    cargar(agg, RUTA_DB, RUTA_SCHEMA)      # LOAD
    print(f"=== Listo. Base generada en {RUTA_DB} ===")


if __name__ == "__main__":
    main()
