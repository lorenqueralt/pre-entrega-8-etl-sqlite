"""
src/load.py — Etapa de CARGA (capa de persistencia).
Crea la tabla destino en SQLite y carga los datos de forma idempotente
(sin generar duplicados al re-ejecutar el pipeline).
"""
import os
import sqlite3
from datetime import datetime

import pandas as pd


def _crear_tabla(con: sqlite3.Connection, ruta_schema: str) -> None:
    """Ejecuta el DDL (CREATE TABLE IF NOT EXISTS) desde el archivo schema.sql."""
    with open(ruta_schema, "r", encoding="utf-8") as f:
        con.executescript(f.read())


def cargar(df: pd.DataFrame, ruta_db: str, ruta_schema: str) -> None:
    """
    Carga el DataFrame agregado en SQLite.

    Anti-duplicados: la tabla tiene PK (anio, mes, categoria) y se usa
    'INSERT OR REPLACE', por lo que re-ejecutar el pipeline actualiza las filas
    existentes en lugar de duplicarlas (carga idempotente).
    """
    try:
        con = sqlite3.connect(ruta_db)
    except sqlite3.Error as e:
        print(f"[ERROR] No se pudo conectar a la base SQLite: {e}")
        raise

    try:
        _crear_tabla(con, ruta_schema)
        ahora = datetime.now().isoformat(timespec="seconds")

        filas = [
            (int(r.anio), int(r.mes), r.categoria, int(r.unidades),
             float(r.ingresos), ahora)
            for r in df.itertuples(index=False)
        ]
        con.executemany(
            """
            INSERT OR REPLACE INTO ventas_mensuales
                (anio, mes, categoria, unidades, ingresos, actualizado_en)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            filas,
        )
        con.commit()
        total = con.execute("SELECT COUNT(*) FROM ventas_mensuales").fetchone()[0]
        print(f"[LOAD] {len(filas)} filas cargadas. Total en la tabla: {total}")
    except sqlite3.Error as e:
        con.rollback()
        print(f"[ERROR] Falló la carga de datos: {e}")
        raise
    finally:
        con.close()
