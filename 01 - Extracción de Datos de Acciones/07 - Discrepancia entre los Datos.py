# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import pandas_datareader as pdr
from twelvedata import TDClient
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import matplotlib.pyplot as plt

# Definir claves
ALPHA_VANTAGE_API_KEY = "TOKEN"
TWELVE_DATA_API_KEY = "TOKEN"

# Funciones para obtener datos de diferentes proveedores
def obtener_datos_yfinance(ticker: str, start: str, end: str, intervalo: str):
    
    """
    Función que obtiene precios históricos desde la API de Yahoo Finance
    """
    
    datos = yf.download(tickers=ticker, start=start, end=end, interval=intervalo, multi_level_index=False, auto_adjust=False)
    
    return datos["Close"]

def obtener_datos_pandas_datareader(ticker: str, start: str, end: str):
    
    """
    Función que obtiene precios históricos utilizando Pandas DataReader
    """
    
    datos = pdr.get_data_stooq(symbols=ticker, start=start, end=end)
    
    return datos["Close"][::-1]

def obtener_datos_twelvedata(ticker: str, start: str, end: str, intervalo: str, api_token: str):
    
    """
    Función que obtiene datos históricos desde la API de Twelve Data.
    """
    
    td = TDClient(apikey=api_token)
    ts = td.time_series(symbol=ticker, interval=intervalo, start_date=start, end_date=end, outputsize=None)
    datos = ts.as_pandas()
    
    return datos["close"][::-1]

def obtener_datos_alpha_vantage(ticker: str, start: str, end: str, api_token: str):
    
    """
    Función que obtiene datos históricos desde la API de Alpha Vantage
    """
    
    ts = TimeSeries(key=api_token, output_format="pandas")
    datos, _ = ts.get_daily(symbol=ticker, outputsize="full")
    datos = datos[::-1].loc[start:end]
    
    return datos["4. close"]


# Configurar parámetros
ticker = "AAPL"
start_date = "2023-01-01"
end_date = "2025-01-01"    
    
# Obtener datos de los proveedores
data_yf = obtener_datos_yfinance(ticker=ticker, start=start_date, end=end_date, intervalo="1d")
data_pdr = obtener_datos_pandas_datareader(ticker=ticker, start=start_date, end=end_date)
data_td = obtener_datos_twelvedata(ticker=ticker, start=start_date, end=end_date, intervalo="1day", api_token=TWELVE_DATA_API_KEY)
data_av = obtener_datos_alpha_vantage(ticker=ticker, start=start_date, end=end_date, api_token=ALPHA_VANTAGE_API_KEY)
    
print("Yahoo Finance:", data_yf.shape)
print("Pandas Data Reader:", data_pdr.shape)
print("Twelve Data:", data_td.shape)
print("Alpha Vantage:", data_av.shape) 
    
# Consolidar datos en un DataFrame
resultados = pd.DataFrame({
    "Yahoo Finance": data_yf,
    "Pandas DataReader": data_pdr,
    "Twelve Data": data_td,
    "Alpha Vantage": data_av
    })
    
# Visualizar Discrepancias en un solo gráfico
plt.figure(figsize=(22, 8), dpi=300)
for proveedor in resultados.columns:
    if resultados[proveedor].isnull().all():
        continue
    plt.plot(resultados.index, resultados[proveedor], label=proveedor, alpha=0.7)
    
plt.title(f"Discrepancias en los datos de cierre {ticker}", fontsize=16)
plt.xlabel("Fecha", fontsize=14)
plt.ylabel("Precio de Cierre", fontsize=14)
plt.legend()
plt.grid()
plt.show()
    
# Calcular diferencias absolutas entre proveedores
def calcular_diferencias(resultados):
    
    """
    Calcula las diferencias absolutas entre los precios de cierre proporciondos por cada proveedor
    """
    
    diferencias = resultados.copy()
    # Tomar a Yahoo Finance como Serie Temporal Base
    base = resultados.iloc[:, 0]
    for columna in resultados.columns:
        diferencias[columna] = abs(resultados[columna] - base)
        
    return diferencias

diferencias = calcular_diferencias(resultados=resultados)
    
# Visualizar diferencias absolutas
fig, axes = plt.subplot_mosaic("ABCD;EEEE", figsize=(22, 10))
plots_colores = {"Yahoo Finance": "red", "Pandas DataReader": "blue", "Twelve Data": "green", "Alpha Vantage": "orange"}
for proveedor, ax in zip(diferencias.columns, list(axes.values())):
    ax.plot(diferencias.index, diferencias[proveedor], color=plots_colores[proveedor], lw=2)
    ax.set_title(f"{proveedor} vs Yahoo Finance")
    ax.grid()
    axes["E"].plot(diferencias.index, diferencias[proveedor], color=plots_colores[proveedor], lw=2,
                   label=f"{proveedor} vs Yahoo Finance")
    
axes["E"].set_title(f"Diferencias absolutas en los datos de cierre para {ticker}")
axes["E"].legend()
axes["E"].grid()
fig.suptitle("Comparación de discrepancias entre diferentes proveedores de datos", fontsize=18, fontweight="bold")
plt.show()
    
# Recordatorio:
#   - La discrepancias en los precios entre diferentes proveedores de datos pueden generar decisiones inconsistentes
#     al diseñar estrategias de trading o realizar análisis técnico. Por ejemplo, un precio incorrecto o desfazado
#     podría activar señales de compra o venta erróneas, afectando la rentabilidad de las operaciones.
