# Pre-entrega · Automatización de Proceso ETL con Capa de Persistencia

**Curso:** Data Science II — Coderhouse

Pipeline ETL automatizado por código que extrae datos de ventas desde un CSV local,
aplica una transformación (limpieza + agregación) y **persiste el resultado en una base
de datos SQLite local**. Aplica los conceptos de *capas de persistencia* y
*automatización de procesos ETL*: se pasa de ejecutar consultas a mano a un flujo
orquestado por un único comando.

## Patrón de datos

- **Fuente:** `data/ventas.csv` — transacciones de ventas (fecha, categoría, producto,
  cantidad, precio unitario).
- **Transformación:** se eliminan duplicados y filas sin `cantidad`, y se **agregan** las
  ventas por **año, mes y categoría** (unidades vendidas e ingresos).
- **Destino:** tabla `ventas_mensuales` en SQLite, con una fila por combinación
  año/mes/categoría.

Es un patrón **ETL batch con carga idempotente**: el destino es un resumen agregado que
se puede regenerar en cada corrida sin duplicar datos.

## Estructura

```
preentrega8-etl-sqlite/
├── main.py                 # orquesta el flujo Extract -> Transform -> Load
├── src/
│   ├── extract.py          # lectura del CSV
│   ├── transform.py        # limpieza + agregación mensual
│   └── load.py             # conexión SQLite, DDL y carga idempotente
├── sql/
│   └── schema.sql          # DDL de la tabla de destino (CREATE TABLE IF NOT EXISTS)
├── data/
│   └── ventas.csv          # dataset de origen (la base .db se genera al correr)
├── requirements.txt
├── .gitignore
└── README.md
```

## Requisitos

- Python 3.9+
- pandas (ver `requirements.txt`). SQLite viene incluido en la librería estándar de
  Python (`sqlite3`), no requiere instalación aparte.

## Pasos para ejecutar

```bash
# 1. (opcional) entorno virtual
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 2. instalar dependencias
pip install -r requirements.txt

# 3. ejecutar el pipeline
python main.py
```

Al terminar se crea/actualiza la base `data/ventas.db` con la tabla `ventas_mensuales`.
Para inspeccionarla:

```bash
sqlite3 data/ventas.db "SELECT * FROM ventas_mensuales LIMIT 10;"
```

## Esquema de la tabla de destino (DDL)

Definido en `sql/schema.sql`:

```sql
CREATE TABLE IF NOT EXISTS ventas_mensuales (
    anio             INTEGER NOT NULL,
    mes              INTEGER NOT NULL,
    categoria        TEXT    NOT NULL,
    unidades         INTEGER NOT NULL,
    ingresos         REAL    NOT NULL,
    actualizado_en   TEXT    NOT NULL,
    PRIMARY KEY (anio, mes, categoria)
);
```

## Cómo se evita la duplicidad de datos

Dos mecanismos combinados:

1. **`CREATE TABLE IF NOT EXISTS`** — no recrea la tabla si ya existe.
2. **Clave primaria `(anio, mes, categoria)` + `INSERT OR REPLACE`** — al re-ejecutar el
   pipeline, cada fila agregada reemplaza a la existente de esa misma clave en lugar de
   insertar una nueva. La carga es **idempotente**: correr el flujo dos veces deja la
   tabla con la misma cantidad de filas.

## Manejo de errores

La etapa de carga captura errores de conexión y de SQL (`sqlite3.Error`), hace
`rollback` ante un fallo en la transacción y cierra la conexión en un bloque `finally`.
La extracción valida que el archivo de origen exista antes de leerlo.
