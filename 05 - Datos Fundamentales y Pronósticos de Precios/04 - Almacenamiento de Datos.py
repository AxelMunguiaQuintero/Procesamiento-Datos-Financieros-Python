# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import sqlite3 # pip install sqlite3
import pandas as pd
import json

# Definir función para descargar datos fundamentales
def descargar_datos(ticker: str):
    
    """
    Función que descarga datos fundamentales para un activo.
    """
    
    # Descargar los estados financieros
    accion = yf.Ticker(ticker)
    income_statement = accion.financials.transpose()
    cashflow = accion.cashflow.transpose()
    balance_sheet = accion.balance_sheet.transpose()
    
    return income_statement, cashflow, balance_sheet

# Probar Funcionamiento
ticker = "AAPL"
income_statement, cashflow, balance_sheet = descargar_datos(ticker)
print(income_statement)

# Definir función para guardar los datos en un archivo csv
def guardar_csv(data: pd.DataFrame, ticker: str, filename: str):
    
    """
    Función que almacena de forma local los archivos en ficheros csv
    """
    
    # Definir ruta y guardar
    filepath = f"{filename}_{ticker}.csv"
    data.to_csv(filepath, index=True)
    print(f"Datos guardados en CSV: {filepath}")
    
# Guardar los datos en csv
guardar_csv(data=income_statement, ticker=ticker, filename="../datos/income_statement")
guardar_csv(data=cashflow, ticker=ticker, filename="../datos/cashflow")
guardar_csv(data=balance_sheet, ticker=ticker, filename="../datos/balance_sheet")

# Función para guardar los datos en una Base de Datos
def guardar_sqlite(data: pd.DataFrame, db_name: str, table_name: str, ticker: str):
    
    """
    Función que guarda datos en una base de datos.
    """
    
    # Conectar a la base de datos (se crea si no existe)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Crear la tabla si no existe
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name}_{ticker} (
        date TEXT PRIMARY KEY,
        data TEXT
        )
                   """)
                   
    # Insertar Datos
    for index, row in data.iterrows():
        # Ajustar formato del Índice
        date = pd.to_datetime(str(index))
        date_str = date.strftime("%Y-%m-%d")
        # Convertir los datos a formato JSON
        data_str = row.to_json()
        # Almacenar
        try: 
            cursor.execute(f"""
            INSERT INTO {table_name}_{ticker} (date, data)
            VALUES (?, ?)  
            """, (date_str, data_str))
        except Exception as error:
            print(error)
            
    # Guardar cambios y cerrar la conexión
    conn.commit()
    conn.close()
    print(f"Datos guardados en SQLite en la tabla: {table_name}_{ticker}")
    
# Lista de tickers a procesar
tickers = ["AAPL", "AMZN", "GOOGL"]

# Base de Datos SQLite
db_name = "datos_financieros.db"

# Ejecutar el script para cada ticker
for ticker in tickers:
    # Descargar Datos
    income_statement, cashflow, balance_sheet = descargar_datos(ticker)
    # Guardar Datos
    guardar_sqlite(data=income_statement, db_name=db_name, table_name="income_statement", ticker=ticker)
    guardar_sqlite(data=cashflow, db_name=db_name, table_name="cashflow", ticker=ticker)
    guardar_sqlite(data=balance_sheet, db_name=db_name, table_name="balance_sheet", ticker=ticker)

# Validar que los datos se han almacenado
conn = sqlite3.connect(db_name)
tablas_existentes = pd.read_sql(sql="SELECT * FROM sqlite_master WHERE type='table'", con=conn)
print(tablas_existentes["name"])

# Leer Datos
tabla_prueba = "income_statement_GOOGL"
income_statement_AAPL = pd.read_sql(sql=f"SELECT * FROM {tabla_prueba}", con=conn)
print(income_statement_AAPL)

# Convertir la columna "data" de JSON a un DataFrame
df_final = income_statement_AAPL["data"].apply(json.loads).apply(pd.Series)
df_final.index = income_statement_AAPL["date"]
print(df_final.T.head())

# Recordatorio:
#   - SQLite3 es un sistema de bases de datos relacional ligero y autocontenido. Utiliza archivos
#     locales para almacenar datos, no requiere servidor y es ideal para aplicaciones pequeñas o integradas.
