"""
src/extract.py — Etapa de EXTRACCIÓN.
Lee el dataset de ventas desde un archivo CSV local.
"""
import os
import pandas as pd


def leer_csv(ruta: str) -> pd.DataFrame:
    """Lee el CSV de ventas. Lanza un error claro si el archivo no existe."""
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encontró el dataset de origen: {ruta}")
    df = pd.read_csv(ruta, parse_dates=["fecha"])
    print(f"[EXTRACT] {len(df)} filas leídas desde {ruta}")
    return df
