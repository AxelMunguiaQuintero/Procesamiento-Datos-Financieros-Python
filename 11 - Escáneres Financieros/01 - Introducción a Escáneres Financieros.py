# -*- coding: utf-8 -*-
# Importar librerías
import pandas_ta as ta # pip install pandas-ta
from yahooquery import Screener, Ticker
import yfinance as yf
import matplotlib.pyplot as plt

# Obtener los screeners disponibles en Yahoo Finance
screener = Screener()
screeners_disponibles = screener.available_screeners
for n, screener_disponible in enumerate(screeners_disponibles):
    print(f"Opción No. {n}", screener_disponible)
    
# Obtener Diferentes Escáneres
screener_opciones = ["most_actives", "day_gainers", "day_losers", "undervalued_growth_stocks"]

# Extraer los 30 primeros activos de cada screener
screener_data = {s: screener.get_screeners(screen_ids=[s], count=30)[s] for s in screener_opciones}

# Mostrar Información y Activos de Cada Escáner
for clave, valores in screener_data.items():
    print(f"\nEscáner: {clave} -> {valores['description']}\n")
    for activo in valores["quotes"]:
        activo_nombre = activo["longName"] if "longName" in activo else activo["displayName"]
        precio_mercado = activo["regularMarketPrice"]
        cambio_precio = activo["regularMarketChange"]
        cambio_porcentaje = activo["regularMarketChangePercent"]
        print(f" - Activo encontrado: {activo_nombre}. Precio de Mercado: {precio_mercado:.3f}.",
              f"Cambio en el Precio: {cambio_precio:.3f}. Cambio Porcentual: {cambio_porcentaje:.3f}")
        
# Filtrar Tickers para "day_losers"
tickers_unicos = [activo["symbol"] for activo in screener_data["day_losers"]["quotes"]]
print("Tickers:", tickers_unicos)

# Generar Instancia con Tickers Seleccionados
tickers = Ticker(symbols=tickers_unicos)

# Aplicar análisis técnico con Pandas TA:
    
# Descargar datos históricos
hist_data = yf.download(tickers=tickers_unicos, period="3y", interval="1d")["Close"]

# Calcular RSI y Medias Móviles
rsi_values = hist_data.apply(lambda x: ta.rsi(x, length=14), axis=0)
ema_50 = hist_data.apply(lambda x: ta.ema(x, length=50), axis=0)
ema_200 = hist_data.apply(lambda x: ta.ema(x, length=200), axis=0)

# Seleccionar tickers con RSI <= 50 y Cruce de Medias Móviles (Tendencia Bajista Continua)
seleccionados = []
for ticker in tickers_unicos:
    if rsi_values[ticker].iloc[-1] <= 50 and ema_50[ticker].iloc[-1] < ema_200[ticker].iloc[-1]:
        seleccionados.append(ticker)
        
print("Activos Seleccionados:", seleccionados)

# Graficar los resultados
if seleccionados:
    print("\nGraficando tendencia de los activos seleccionados...")
    # Máximo 3 gráficos para mejor visualización
    num_assets = min(len(seleccionados), 3)
    fig, axes = plt.subplots(ncols=num_assets, nrows=1, figsize=(22, 8), dpi=100)
    colores = ["blue", "green", "brown"]
    if num_assets == 1:
        axes = [axes]
    # Iterar en subplots
    for i, ticker in enumerate(seleccionados[:3]):
        ax = axes[i]
        ax.plot(hist_data.index, hist_data[ticker], label=f"Precio {ticker}", color=colores[i])
        ax.plot(hist_data.index, ema_50[ticker], label="EMA 50", color="orange", linestyle="dashed")
        ax.plot(hist_data.index, ema_200[ticker], label="EMA 200", color="red", linestyle="dashed")
        
        ax.set_title(f"Evolución de {ticker}")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Precio de Cierre")
        ax.legend()
        ax.grid()
        
    plt.tight_layout()
    plt.show()
else:
    print("\nNo se encontraron activos que cumplan los criterios de selcción...")

# Recordatorio:
#   - Los escáneres permiten identificar rápidamente activos financieros que cumplen con criterios
#     específicos, como tendencias, ganancias, pérdidas o crecimiento, optimizando el proceso de análisis
#     para estrategias de trading.
