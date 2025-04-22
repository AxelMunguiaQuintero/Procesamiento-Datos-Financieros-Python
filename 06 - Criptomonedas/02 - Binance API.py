# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import requests
import json
from datetime import datetime
import websocket
import threading

# Definir URL a la API
base_url = "https://api.binance.com"

# Definir Endpoints 
conectividad_endpoint = "/api/v3/ping"
horario_endpoint = "/api/v3/time" 
informacion_exchange_endpoint = "/api/v3/exchangeInfo" 

# Ejemplo 1: Endpoint de Conectividad
url_conectividad_completa = base_url + conectividad_endpoint
ping_response = requests.get(url=url_conectividad_completa) 
print("Url Completa:", ping_response.url)
if ping_response.status_code == 200:
    respuesta_json = ping_response.json()
    if respuesta_json == {}:
        print("¡La conexión funciona correctamente!")
        
# Ejemplo 2: Endpoint para obtener el tiempo del servidor
url_horario_completa = base_url + horario_endpoint
horario_response = requests.get(url=url_horario_completa)
print("Url Completa:", horario_response.url)
if horario_response.status_code == 200:
    respuesta_json = horario_response.json()
    print(json.dumps(respuesta_json, indent=4))
    # Convertir respuesta a un formato más legible
    server_time_ms = respuesta_json["serverTime"] / 1000 # Retorna un Timestamp en milisegundos
    print("\nHorario:", datetime.fromtimestamp(server_time_ms))
    
# Ejemplo 3: Endpoint para obtener la información de Exchange
url_info_exchange_completa = base_url + informacion_exchange_endpoint
exchange_info_response = requests.get(url=url_info_exchange_completa)
respuesta_json = exchange_info_response.json()

# Mostrar Instrumentos
activos = []
for activo in respuesta_json["symbols"]:
    print("Símbolo:", activo["symbol"])
    activos.append(activo["symbol"])
print("Hay un total de {} activos".format(len(activos)))
    
# Ejemplo 4: Endpoint para obtener el precio de un activo en Tiempo Real
ticker_price_endpoint = "/api/v3/ticker/price"
url_ticker_price_completa = base_url + ticker_price_endpoint
# Definir parámetros de petición
params = {
    
    "symbol": "BTCUSDT"
    
    }
precio_response = requests.get(url=url_ticker_price_completa, params=params)
print(f"Precio más reciente para {params['symbol']}:\n\n", json.dumps(precio_response.json(), indent=4))

# Monitorear diferentes activos
params = {
    
    "symbols": '["ETHUSDT","SOLUSDT"]'
    
    }
precio_response = requests.get(url=url_ticker_price_completa, params=params)
print(f"Precios más recientes para {params['symbols']}:\n\n", json.dumps(precio_response.json(), indent=4))
    
# Obtener el precio de todos los activos
params = {}
precios_response = requests.get(url=url_ticker_price_completa, params=params)
precios_json = precios_response.json()  
print("Precios:\n\n", json.dumps(precios_json[:5], indent=4))
print("Total de Precios Obtenidos:", len(precios_json))
    
# Ejemplo 5: Endpoint para obtener estadísticas de las últimas 24 horas de un activo
ticker_24hr_endpoint = "/api/v3/ticker/24hr"
url_ticker_24hr_completa = base_url + ticker_24hr_endpoint
params = {
    
    "symbol": "BTCUSDT"
    
    }
stats_24hr_response = requests.get(url=url_ticker_24hr_completa, params=params)
print(f"Estadísticas de 24 hotas para {params['symbol']}:\n\n", json.dumps(stats_24hr_response.json(), indent=4))

# Ejemplo 6: Endpoint para obtener el libro de órdenes (order book)
order_book_endpoint = "/api/v3/depth"
url_order_book_completa = base_url + order_book_endpoint
params = {
    
    "symbol": "BTCUSDT",
    "limit": 5
    
    }
order_book_response = requests.get(url=url_order_book_completa, params=params)
print(f"Libro de órdenes para {params['symbol']}:\n\n", json.dumps(order_book_response.json(), indent=4))
    
# Ejemplo 7: Endpoint para obtener transacciones agregadas
agg_trades_endpoint = "/api/v3/aggTrades"
url_agg_trades_endpoint = base_url + agg_trades_endpoint
params = {
    
    "symbol": "BTCUSDT",
    "limit": 1
    
    }
agg_trades_response = requests.get(url=url_agg_trades_endpoint, params=params)
print(f"Transacciones agregadas para {params['symbol']}:\n\n", json.dumps(agg_trades_response.json(), indent=4))   
    
# Explicación de respuesta:
#   {
#    "a": -> Aggregate tradeId,
#    "p": -> Price,
#    "q": -> Quantity,
#    "f": -> First tradeId,
#    "l": -> Last tradeId,
#    "T": -> Timestamp,
#    "m": -> Was the buyer the maker?
#    "M": -> Was the trade the best price math?
#   }

# Ejemplo 8: Endpoint para obtener velas
klines_endpoint = "/api/v3/klines"
url_klines_completa = base_url + klines_endpoint
params = {
    
    "symbol": "BTCUSDT",
    "interval": "1h",
    "limit": 1_000 
    
    }
klines_response = requests.get(url=url_klines_completa, params=params)
df = pd.DataFrame(klines_response.json())

df.columns = ["open_time", "open", "high", "low", "close", "volume", "close_time",
              "quote_asset_time", "number_of_trades", "taker_buy_base_asset_volume",
              "taker_buy_quote_asset_volume", "ignore"]
print(df[["open_time", "open", "high", "low", "close", "volume"]]) 
    
# Elegir columnas de interés
sub_df = df[["open_time", "open", "high", "low", "close", "volume"]].copy()
sub_df["open_time"] = pd.to_datetime(sub_df["open_time"], unit="ms")
print(sub_df)

# Intervalos disponibles
intervalos = ["1s", "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h",
              "1d", "3d", "1w", "1M"]

# Petición con más parámetros
params = {
    
    "symbol": "BTCUSDT",
    "interval": "1d",
    "startTime": int(pd.to_datetime("2023-01-01").timestamp() * 1000),
    "endTime": int(pd.to_datetime("2025-01-01").timestamp() * 1000),
    "timeZone": "0", # Formato UTC
    "limit": 1_000
    
    }
klines_response = requests.get(url=url_klines_completa, params=params)
df = pd.DataFrame(klines_response.json())

df.columns = ["open_time", "open", "high", "low", "close", "volume", "close_time",
              "quote_asset_time", "number_of_trades", "taker_buy_base_asset_volume",
              "taker_buy_quote_asset_volume", "ignore"]
df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
print(df)
    
# Datos en Tiempo Real (Streaming)
def on_message(ws, message):
    
    """
    Función que despliega en la consola los datos recibidos.
    """
    
    data = json.loads(message)
    print(f"Precio de BTC/USDT: {data['p']}")
    
socket_url = "wss://stream.binance.com:9443/ws/btcusdt@trade"

ws = websocket.WebSocketApp(socket_url, on_message=on_message)
threading.Thread(target=ws.run_forever).start()    

# Cesar conexión
ws.close()

# Recordatorio:
#   - Binance es una platforma global de intercambio de criptomonedas que permite comprar, vender
#     y operar con una amplia variedad de activos digitales.
#   - La API de Binance nos permite automatizar operaciones de trading, acceder a datos en tiempo real,
#     gestionar balances y realizar análisis avanzados.
