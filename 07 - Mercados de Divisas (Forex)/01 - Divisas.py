# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
from twelvedata import TDClient
from alpha_vantage import foreignexchange
import json

# Obtener Datos con Yahoo Finance

# Tickers de divisas
divisas = {
    
    "EUR/USD": "EURUSD=X", # Euro/Dólar
    "GBP/USD": "GBPUSD=X", # Libra Esterlina/Dólar
    "USD/JPY": "USDJPY=X", # Dólar/Yen Japonés
    "USD/CAD": "USDCAD=X", # Dólar/Dólar Canadiense
    "USD/INR": "INR=X",    # Dólar/ Rupia India,
    "USD/MXN": "MXN=X",    # Dólar/Peso Mexicano
    "USD/BRL": "BRL=X",    # Dólar/Real Brasileño
    "USD/ARS": "ARS=X",    # Dólar/Peso Argentino
    "USD/PEN": "PEN=X",    # Dólar/Sol Peruano
    "USD/CLP": "CLP=X"     # Dólar/Peso Chileno    
    
    }

# Diccionario para almacenar los datos de cada divisa
datos_divisas = {}

for nombre, ticker in divisas.items():
    datos_divisas[nombre] = yf.download(ticker, start="2020-01-01", end="2025-01-01", multi_level_index=False)
    
# Mostrar los primeros 5 registros de cada divisa
for nombre, datos in datos_divisas.items():
    print(f"Datos de {nombre}:\n")
    print(datos.head(), "\n")
    print("-" * 30)
    
# Crear Instanci de Clase Ticker
ticker = yf.Ticker(ticker="EURUSD=X")
print(json.dumps(ticker.info, indent=4))

# Obtener Periodo máximo de datos
eur_usd_max = ticker.history(period="max", interval="1d")
print(eur_usd_max)

# Obtener Datos con Twelve Data

# Configurar API
api_key = "API_KEY"
td = TDClient(apikey=api_key)

# Lista de pares de divisas para obtener datos
divisas = [
    
    "EUR/USD", "GBP/USD", "USD/JPY", "USD/MXN", "USD/BRL", "USD/CNY"
    
    ]

# Datos históricos
historicos = {}
for divisa in divisas:
    historicos[divisa] = td.time_series(
        
        symbol=divisa,
        interval="1day",
        start_date="2023-01-01",
        end_date="2025-01-01",
        outputsize=None
        
        
        ).as_pandas()
    print("Datos descargados para:", divisa, "\n")
    print(historicos[divisa])
    print("-" * 60, "\n")

# Precios en Tiempo Real
for divisa in divisas:
    peticion = td.exchange_rate(symbol=divisa).as_json()
    print(f"Tipo de cambio para: {divisa} -> {peticion}")

# Convertidor de Divisas
conversion_eurusd = td.currency_conversion(symbol="EUR/USD", amount=1).as_json()
print(json.dumps(conversion_eurusd, indent=4))
                                           
conversion_usdmxn = td.currency_conversion(symbol="USD/MXN", amount=1).as_json()
print(json.dumps(conversion_usdmxn, indent=4))

conversion_mxnusd = td.currency_conversion(symbol="MXN/USD", amount=20.23).as_json()
print(json.dumps(conversion_mxnusd, indent=4))

# Obtener Datos con Alpha Vantage:
api_key = "API_KEY"
fx = foreignexchange.ForeignExchange(key=api_key, output_format="pandas")

# Datos en Tiempo Real
data, metadata = fx.get_currency_exchange_rate(from_currency="EUR", to_currency="USD")
print(data.T)

# Obtener Datos históricos
data, metadata = fx.get_currency_exchange_daily(from_symbol="EUR", to_symbol="USD", outputsize="full")
print(data[::-1])

# Recordatorio:
#   - Las divisas representan el valor relativo entre dos monedas y se negocian en el mercado de Forex,
#     el más grande y líquido del mundo, operando las 24 hors a través de redes descentralizadas.
#   - Las divisas se negocian en un mercado descentralizado (Forex), sin una bolsa que registre el volumen total,
#     ya que las transacciones ocurren entre bancos, instituciones y traders en múltiples plataformas.
