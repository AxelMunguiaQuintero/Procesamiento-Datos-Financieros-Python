# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import yfinance as yf
import sqlite3
import schedule
import time
import os

# Definir nombres
DB_NAME = "trading_data.db"
TABLE_NAME = "precios_historicos"

# Función para conectar a SQLite y asegurarse de que la BD y tabla existen
def inicializar_bd(db_name: str, table_name: str):
    
    """
    Función que crea la base de datos si no existe.
    """
    
    # Establecer Conexión
    conexion = sqlite3.connect(database=db_name)
    cursor = conexion.cursor()
    
    # Crear la tabla si no existe
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            
            date DATETIME UNIQUE PRIMARY KEY,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER
            )
                   """)
                   
    # Guardar
    conexion.commit()
    
    return conexion, cursor

# Ejecutar la función
conexion, cursor = inicializar_bd(db_name=DB_NAME, table_name=TABLE_NAME)

# Validar que existe
if os.path.isfile(DB_NAME):
    print("¡La base de datos ha sido creada exitosamente!")
    # Validar la estructura de la tabla creada
    estructura_tabla = pd.read_sql_query(sql=f"PRAGMA table_info({TABLE_NAME})", con=conexion)
    print(estructura_tabla)

# Función para obtener datos de Yahoo Finance y guardarlos en SQLite
def obtener_y_guardar_datos(ticker: str = "BTC-USD", conexion: sqlite3.Connection = conexion,
                            cursor: sqlite3.Cursor = cursor):
    
    """
    Función que se encarga de obtener y almacenar los datos.
    """

    # Obtener última fecha guardada
    df_historicos = pd.read_sql_query(sql=f"SELECT * FROM {TABLE_NAME} ORDER BY date DESC LIMIT 1", con=conexion)
    if df_historicos.empty:
        df = yf.download(tickers=ticker, interval="1m", period="8d", multi_level_index=False)
    else:
        ultima_fecha = df_historicos["date"].iloc[0]
        ultima_fecha_str = pd.to_datetime(ultima_fecha).strftime("%Y-%m-%d")
        # Descargar solo los datos desde la última fecha
        df = yf.download(tickers=ticker, interval="1m", start=ultima_fecha_str, multi_level_index=False)
        df = df.loc[ultima_fecha:]
        df = df.iloc[1:].copy()
        
    # Si hay datos nuevos, guardarlos en la BD
    if not df.empty:
        df.reset_index(inplace=True)
        df["Datetime"] = df["Datetime"].astype(str)
        df.rename(columns={"Datetime": "date", "Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume": "volume"},
                  inplace=True)
        df.to_sql(name=TABLE_NAME, con=conexion, if_exists="append", index=False)
        print(f"\nDatos de {ticker} guardados correctamente en la base de datos")
    else:
        print("\nNo hay datos nuevos para guardar.")
        
    # Guardar cambios
    conexion.commit()

# Probar que funciona
obtener_y_guardar_datos()

# Cargar Datos
df_hist = pd.read_sql_query(sql=f"SELECT * FROM {TABLE_NAME}", con=conexion)
print(df_hist)

# Almacenar los nuevos datos generados (Debe de haber pasado mínimo un minuto)
obtener_y_guardar_datos()

# Programar la ejecución automática cada 2 minutos
schedule.every(interval=2).minutes.do(obtener_y_guardar_datos)

# Bucle infinito para mantener el scheduler en ejecución
while True:
    schedule.run_pending()
    # Obtener tiempo de espera
    tiempo_espera = schedule.idle_seconds()
    print("Tiempo a Esperar:", tiempo_espera)
    # Dormir Código
    time.sleep(tiempo_espera)
    
# Recordatorio:
#   - Automatizar la descarga, procesamiento y almacenamiento de datos nos permite contar con información
#     siempre actualizada sin intervención manual, lo que ahorra tiempo y reduce errores humanos.
