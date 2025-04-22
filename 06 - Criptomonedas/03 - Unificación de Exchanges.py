# Importar librerías
import ccxt # pip install ccxt
import json
import pandas as pd
import threading

# Mostrar todos los exchanges disponibles en CCXT
print("Exchanges disponibles:\n\n", ccxt.exchanges)
print("Hay un total {} de diferentes exchanges".format(len(ccxt.exchanges)))

# Trabajar con Binance
exchange = ccxt.binance()

# Obtener todos los pares de trading disponibles en Binnce
markets = exchange.load_markets()
print("Primeros 10 Instrumentos:", list(markets.keys())[:10])

# Obtener el precio actual de Bitcoin
ticker = exchange.fetch_ticker("BTC/USDT")
print(json.dumps(ticker, indent=4))

# Consultar el libro de órdenes (order book)
order_book = exchange.fetch_order_book("BTC/USDT", limit=10)

# Mostrar las 5 mejores ofertas de compra y de venta
print("Mejores ofertas de compra:", order_book["bids"][:5])
print("Mejores ofertas de venta:", order_book["asks"][:5])

# Obtener precios desde múltiples exchanges
exchanges = [ccxt.binance(), ccxt.kraken(), ccxt.coinbase()]
# Iterar en cada Exchange
for ex in exchanges:
    ticker = json.dumps(ex.fetch_ticker("BTC/USDT"), indent=4)
    if ticker:
        print(f"Precio en {ex.id}: \n\n {ticker}")
        
# Obtener Datos históricos (Binance)
ohlcv = exchange.fetch_ohlcv("BTC/USDT", timeframe="1d", limit=5)

# Convertir a DataFrame
df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
print(df)

# Extraer información de todos los instrumentos disponibles
tickers = exchange.fetch_tickers()
print(json.dumps(tickers["ETH/USDT"], indent=4))

# Comparar precios entre distintos exchanges para arbitraje
exchanges = {"binance": ccxt.binance(), "kraken": ccxt.kraken(), "coinbase": ccxt.coinbase()}

def descargar_datos(exchange, symbol, dictionary):
    
    """
    Función que descarga el precio más reciente de un exchange y los almacena
    """
    
    last_price = exchange.fetch_ticker(symbol)["last"]
    dictionary[symbol + "_" + exchange.id] = last_price
    print(exchange, "ha terminado")
    
prices = {}
threads = []
for ex in exchanges.values():
    t = threading.Thread(target=descargar_datos, args=(ex, "BTC/USDT", prices))
    threads.append(t)
    t.start()
    
# Esperar a que terminen los Hilos de obtener los datos
for thread in threads:
    thread.join()
    
print(json.dumps(prices, indent=4))

# Recordatorio:
#   - La librería de CCXT (Cryptocurrency Trading Library) es una biblioteca de Python que proporciona una interfaz
#     para interactuar con diferentes plataformas de intercambio de criptomonedas (exchanges).
