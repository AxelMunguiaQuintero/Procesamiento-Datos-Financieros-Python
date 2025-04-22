# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import wallstreet
from twelvedata import TDClient
import pandas_datareader as pdr
from alpha_vantage.timeseries import TimeSeries
import investpy # pip install investpy 
import pandas as pd

# Conectar a Cliente de Twelve Data
API_KEY = "TOKEN"
td = TDClient(apikey=API_KEY)

# Obtener Índices Disponibles
indices = td.get_indices_list().as_json()
for n, indice in enumerate(indices):
    print(f"Índice No. {n} ->", str(indice))
    
# Extraer Datos
fecha_inicio = "2024-01-01"
fecha_final = "2025-01-01"
try:
    datos = td.time_series(
        
        symbol=indices[0]["symbol"],
        interval="1day",
        start_date=fecha_inicio,
        end_date=fecha_final,
        outputsize=None
        
        ).as_pandas()
except Exception as error:
    print("Error ->", error)
    
# Extraer Datos con Diferentes APIs
indices = {
    
    "S&P 500": "^GSPC",
    "IBEX 35": "^IBEX",
    "DAX 40": "^GDAXI",
    "Nikkei 225": "^N225",
    "FTSE 100": "^FTSE"
    
    }

# Yahoo Finance
datos = {}
for clave, indice in indices.items():
    datos[indice] = yf.download(tickers=indice, start=fecha_inicio, end=fecha_final, interval="1d", progress=False)
    print(f"Datos descargados para Índice: {clave}\n\n")
    print(datos[indice])
    print("\n" + "-" * 60 + "\n")

# Pandas Data Reader
dict_indices = {clave: pdr.get_data_stooq(symbols=indice, start=fecha_inicio, end=fecha_final) 
                for clave, indice in indices.items()}
for clave in dict_indices:
    if len(dict_indices[clave]) > 0:
        print(f"Datos descargados {clave}\n\n")
        print(dict_indices[clave])
        print("\n" + "-" * 60 + "\n")
        
# Volver a Descargar
indices_stooq = ["^SPX", "^IBEX", "^DAX", "^NKX", "^FTM"]
pdr_datos = {indice: pdr.get_data_stooq(symbols=indice, start=fecha_inicio, end=fecha_final) 
                for indice in indices_stooq}
for clave in pdr_datos:
    print(f"Datos descargados {clave}\n\n")
    print(pdr_datos[clave])
    print("\n" + "-" * 60 + "\n")
        
# Extraer Datos con Alpha Vantage
api_key = "TOKEN"
ts = TimeSeries(key=api_key, output_format="pandas")
indices_alp_vant = ["SPY",  # ETF que replica el S&P 500
                    "EWP",  # ETF que sigue el rendimiento de las empresas más representativas de España
                    "EWG",  # ETF que sigue el rendimiento de las empresas más representativas de Alemania
                    "EWJ",  # ETF que sigue el rendimiento de las empresas más representativas de Japón
                    "ISF"]  # ETF que sigue el índice FTSE 100

alp_van_datos = {}
for indice_etf in indices_alp_vant:
    try:
        alp_van_datos[indice_etf], _ = ts.get_daily(symbol=indice_etf, outputsize="compact")
    except Exception as error:
        print("Error ->", error)
    # Mostrar en Consola
    if indice_etf in alp_van_datos:
        print(f"Datos de {indice_etf}:\n\n")
        print(alp_van_datos[indice_etf])
        print("\n" + "-" * 60 + "\n")

# Obtener Datos en Tiempo Real S&P 500
indice = wallstreet.Stock(quote="^GSPC")
print("Precio Actual del S&P 500:", indice.price)

# Obtener Datos en Tiempo Real SPY
indice_etf = wallstreet.Stock(quote="SPY")
print("Precio Actual que replica al S&P 500 (SPY):", indice_etf.price)

# Obtener Todos los Índices del Mundo
indices_all = investpy.indices.get_indices_dict()
indices_all = pd.DataFrame(indices_all)
print("Total de Índices:", len(indices_all))
print(indices_all.head(10))

# Obtener Países con Índices
paises_indices = investpy.indices.get_index_countries()
print("Total Países:", len(paises_indices))

# Obtener todos los índices para un país
paises_usa = investpy.indices.get_indices_dict(country="united states")
paises_usa = pd.DataFrame(paises_usa)
print("Total de Índices en Estados Unidos:", len(paises_usa))
# Filtrar por índice específico
print("Información del S&P 500:\n\n", paises_usa[paises_usa["symbol"] == "SPX"].T)

# Obtener Datos con Investing
try:
    datos_investing = investpy.get_index_historical_data(index="S&P 500", country="united states", 
                                                         from_date="01/01/2024", to_date="01/01/2025")
    print(datos_investing)
except Exception as error:
    print("Error ->", error)

# Recordatorio:
#   - Los índices bursátiles son una herramienta clave para evaluar la salud general del mercado, representando
#     el comportamiento de un grupo de acciones que reflejan una economía o un sector específico.
#   - Invertir en un índice bursátil permite diversificar el riesgo, ya que se invierte en un conjutno de activos.
#     Esto reduce el impacto de las fluctuaciones de precios de una sola acción en particular.
