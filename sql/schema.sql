-- schema.sql
-- DDL de la tabla de destino donde se persisten los datos agregados.
-- La clave primaria compuesta (anio, mes, categoria) evita duplicados:
-- no puede existir más de una fila para la misma categoría en el mismo mes.

CREATE TABLE IF NOT EXISTS ventas_mensuales (
    anio             INTEGER NOT NULL,
    mes              INTEGER NOT NULL,
    categoria        TEXT    NOT NULL,
    unidades         INTEGER NOT NULL,
    ingresos         REAL    NOT NULL,
    actualizado_en   TEXT    NOT NULL,
    PRIMARY KEY (anio, mes, categoria)
);
