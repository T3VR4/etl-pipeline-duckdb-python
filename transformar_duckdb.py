import duckdb
import os

def procesar_datos_duckdb():
    print("Iniciando procesamiento analítico con DuckDB...")
    
    # Conectarse a una base de datos DuckDB local (crea un archivo .duckdb)
    conn = duckdb.connect('data/finanzas_analitica.duckdb')
    
    # 1. Cargar el archivo CSV crudo en una tabla temporal de DuckDB
    conn.execute("""
        CREATE OR REPLACE TABLE transacciones_raw AS 
        SELECT * FROM read_csv_auto('data/transacciones_raw.csv');
    """)
    
    print("Tabla raw cargada correctamente en DuckDB.")

    # 2. Crear una tabla agregada por categoría y método de pago (Modelo analítico)
    conn.execute("""
        CREATE OR REPLACE TABLE resumen_por_categoria AS
        SELECT 
            categoria,
            metodo_pago,
            COUNT(id_transaccion) AS total_transacciones,
            SUM(monto) AS monto_total,
            ROUND(AVG(monto), 2) AS ticket_promedio
        FROM transacciones_raw
        GROUP BY categoria, metodo_pago
        ORDER BY monto_total DESC;
    """)
    
    # 3. Consultar un resumen rápido para mostrar en consola
    resultado = conn.execute("SELECT * FROM resumen_por_categoria LIMIT 5;").fetchdf()
    print("\n--- Vista previa del resumen analítico (Top 5) ---")
    print(resultado)
    
    # 4. Exportar el resultado transformado a un CSV limpio o Parquet para reportes
    os.makedirs('output', exist_ok=True)
    conn.execute("""
        COPY resumen_por_categoria TO 'output/resumen_categorias.csv' (HEADER, DELIMITER ',');
    """)
    
    conn.close()
    print("\n¡Proceso ETL completado con éxito! Revisa la carpeta 'output/' y tu base DuckDB.")

if __name__ == '__main__':
    procesar_datos_duckdb()