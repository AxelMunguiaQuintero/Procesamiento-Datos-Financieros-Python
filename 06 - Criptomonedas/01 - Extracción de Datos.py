# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
from twelvedata import TDClient
from alpha_vantage import cryptocurrencies
import pandas as pd
import json
from datetime import datetime

# Configurar API Key
api_key = "API_KEY"
td = TDClient(apikey=api_key)

# Definir criptomoneda y el intervalo de tiempo
symbol = "BTC/USD"
interval = "1min"

# Obtener Datos
data = td.time_series(
    
    symbol=symbol,
    interval=interval,
    end_date=datetime.now(),
    outputsize=10,
    order="asc"
    
    ).as_pandas()
print(data)

# Extraer múltiples tickers en una sola petición
symbols = ["BTC/USD", "ETH/USD", "ADA/USD"]

symbols = ", ".join(symbols)
print("Símbolos a descargar:", symbols)
interval = "5min"

data = td.time_series(
    
    symbol=symbols,
    interval=interval,
    end_date=datetime.now(),
    outputsize=10
    
    ).as_pandas()
print(data)
print("BTC/USD:\n", data.loc["BTC/USD"])

# Obtener lista de Criptomonedas disponibles en TwelveData
df_criptos = pd.DataFrame(td.get_cryptocurrencies_list().as_json())
print(df_criptos)

# Obtener los Exchanges Disponibles
df_exchanges = pd.DataFrame(td.get_cryptocurrency_exchanges_list().as_json())
print(df_exchanges)

# Obtener Exchanges donde se puede solicitar el precio de Bitcoin
exchanges = df_criptos[df_criptos["symbol"] == "BTC/USD"]["available_exchanges"].iloc[0]
print(exchanges)

# Obtener el precio de Bitcoin desde diferentes Exchanges
for exchange in exchanges:
    data = td.time_series(
        
        symbol="BTC/USD",
        interval="1min",
        exchange=exchange,
        end_date=datetime.now(),
        outputsize=10
        
        ).as_pandas()
    print(f"\nDatos descargados con {exchange}:\n\n", data)

# Descargar Datos con Yahoo Finance
symbols = ["BTC-USD", "ETH-USD", "XRP-USD"]
df = yf.download(tickers=symbols, interval="1d", period="3mo")
print(df)

# Cambiar Niveles de Columnas
df = df.swaplevel(axis=1)
print(df["BTC-USD"])

# Obtener Información General de Bitcoin
bitcoin = yf.Ticker(ticker="BTC-USD")
print(json.dumps(bitcoin.info, indent=4))

# Descargar datos con Alpha Vantage
api_key = "API_KEY"
cc = cryptocurrencies.CryptoCurrencies(key=api_key, output_format="pandas")

# Datos Históricos de Bitcoin en USD
data, metadata = cc.get_digital_currency_daily(symbol="BTC", market="USD")
print(data)

# Datos Históricos de Bitcoin en EUR
data, metadata = cc.get_digital_currency_daily(symbol="BTC", market="EUR")
print(data)

# Precio de Bitcoin en Tiempo Real
exchange_rate = cc.get_digital_currency_exchange_rate(from_currency="BTC", to_currency="USD")
print(exchange_rate[0].T)

# Recordatorio:
#   - Las criptomonedas son monedas digitales que utilizan la criptografía para asegurar las transacciones,
#     sin necesidad de intermediarios como bancos. Operan en redes descentralizadas como blockchain, garantizando
#     seguridad y transparencia.
#   - Las criptomonedas son conocidas por su alta volatilidad, lo que las convierte en activos especulativos.
