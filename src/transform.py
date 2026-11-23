"""
src/transform.py — Etapa de TRANSFORMACIÓN.
Limpieza básica + agregación mensual por categoría.
"""
import pandas as pd


def limpiar(df: pd.DataFrame) -> pd.DataFrame:
    """Elimina duplicados y filas con cantidad nula (no se puede agregar sin ella)."""
    antes = len(df)
    df = df.drop_duplicates()
    df = df.dropna(subset=["cantidad"]).copy()
    df["cantidad"] = df["cantidad"].astype(int)
    print(f"[TRANSFORM] Limpieza: {antes} -> {len(df)} filas "
          f"(duplicados y nulos eliminados)")
    return df


def agregar_mensual(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega las ventas por año, mes y categoría:
      - unidades: suma de cantidades
      - ingresos: suma de cantidad * precio_unitario
    """
    df = df.copy()
    df["anio"] = df["fecha"].dt.year
    df["mes"] = df["fecha"].dt.month
    df["importe"] = df["cantidad"] * df["precio_unitario"]

    agg = (
        df.groupby(["anio", "mes", "categoria"], as_index=False)
          .agg(unidades=("cantidad", "sum"),
               ingresos=("importe", "sum"))
    )
    agg["ingresos"] = agg["ingresos"].round(2)
    print(f"[TRANSFORM] Agregación: {len(agg)} filas (año/mes/categoría)")
    return agg
