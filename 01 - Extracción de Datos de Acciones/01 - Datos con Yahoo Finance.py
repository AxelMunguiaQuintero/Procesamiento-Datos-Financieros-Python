# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf # pip install yfinance
import pandas as pd
import time
import matplotlib.pyplot as plt

# Definir Parámetros
ticker = "AMZN"
fecha_inicio = "2023-01-01"
fecha_final = "2025-01-01"
intervalo = "1d"

# Ejemplo 1: Descargar datos históricos con rangos de fechas e intervalo diario
df = yf.download(tickers=ticker, start=fecha_inicio, end=fecha_final, interval=intervalo)
print(df)

# Ejemplo 2: Descargar datos para el último mes con intervalo de 15 minutos
df = yf.download(tickers=ticker, period="1mo", interval="15m")
print(df)

# Ejemplo 3: Descargar datos de los últimos 2 días con pre y post mercado en intervalo de 1 minuto
df = yf.download(tickers=ticker, period="2d", interval="1m", prepost=True, progress=False)
print("Cantidad de datos descargados:", df.shape[0])

# Separar Datos del Horario Regular y del Horario Extendido:
    
# Convertir el Índice del DataFrame a la Zona Horario de Nueva York
print("Timezone Actual:", df.index.tz)
if df.index.tz is None:
    df.index = pd.to_datetime(df.index).tz_localize("UTC").tz_convert("America/New_York")
else:
    df.index = df.index.tz_convert("America/New_York")
    
# Definir el rango del horario normal, pre-market y post-market
horario_pre_mercado_inicio = "04:00:00"
horario_pre_mercado_final = "09:30:00"
horario_normal_inicio = "09:30:00"
horario_normal_final = "16:00:00"
horario_post_mercado_inicio = "16:00:00"
horario_post_mercado_final = "20:00:00"

# Separar los datos según el horario
datos_pre_mercado = df.between_time(start_time=horario_pre_mercado_inicio, end_time=horario_pre_mercado_final).iloc[:-1]
datos_horario_normal = df.between_time(start_time=horario_normal_inicio, end_time=horario_normal_final)
datos_post_mercado = df.between_time(start_time=horario_post_mercado_inicio, end_time=horario_post_mercado_final).iloc[1:]

# Mostrar los datos
print("Datos del horario normal:")
print(datos_horario_normal)

print("\nDatos del pre mercado:")
print(datos_pre_mercado)

print("\nDatos del post mercado:")
print(datos_post_mercado)

# Ejemplo 4: Descargar Datos para múltiples activos (Descarga Concurrente)
tickers = ["AMZN", "AAPL", "MSFT", "TSLA", "NFLX", "META", "XYZ", "NVDA", "PYPL", "QCOM"]

tiempo_inicio = time.time()
df_activos = yf.download(tickers=tickers, start=fecha_inicio, end=fecha_final, interval=intervalo, threads=True)
tiempo_final = time.time()
print("La descarga tomó {} segundos".format(tiempo_final - tiempo_inicio))
print(df_activos)

# Ejemplo 5: Descargar Datos para múltiples activos (Descarga Secuencial)
tiempo_inicio = time.time()
df_activos = yf.download(tickers=tickers, start=fecha_inicio, end=fecha_final, interval=intervalo, threads=False)
tiempo_final = time.time()
print("La descarga tomó {} segundos".format(tiempo_final - tiempo_inicio))
print(df_activos)

# Ejemplo 6: Descargar el máximo histórico de datos sin multi nivel
df = yf.download(tickers=ticker, period="max", interval=intervalo, multi_level_index=False)
print(df)

# Intervalos disponibles en yfinance y sus limitaciones de tiempo:
#
# | Intervalo | Descripción            | Limitación de tiempo     |
# |-----------|------------------------|--------------------------|
# | 1m        | Datos por minuto       | Limitado a 8 días        |
# | 2m        | Datos cada 2 minutos   | Limitado a 60 días       |
# | 5m        | Datos cada 5 minutos   | Limitado a 60 días       |
# | 15m       | Datos cada 15 minutos  | Limitado a 60 días       |
# | 30m       | Datos cada 30 minutos  | Limitado a 60 días       |
# | 60m       | Datos cada 60 minutos  | Limitado a 730 días      |
# | 90m       | Datos cada 90 minutos  | Limitado a 60 días       |
# | 1h        | Datos cada 1 hora      | Limitado a 730 días      |
# | 1d        | Datos por día          | Sin limitación           |
# | 5d        | Datos por 5 días       | Sin limitación           |
# | 1wk       | Datos por semana       | Sin limitación           |
# | 1mo       | Datos por mes          | Sin limitación           |
# | 3mo       | Datos por 3 meses      | Sin limitación           |


# Graficar Datos
df = yf.download(tickers="TSLA", start="2024-01-01", end="2025-01-01", interval="1d", multi_level_index=False)
plt.figure(figsize=(22, 6))
plt.plot(df.index, df["Close"], label="Precios de Cierre")
plt.title("Precio de Tesla", fontsize=20)
plt.xlabel("Fecha", fontsize=18)
plt.ylabel("Precios de la Acción", fontsize=18)
plt.legend()
plt.grid()
plt.show()

# Recordatorio:
#   - Yahoo Finance nos permite obtener datos históricos en diversos intervalos, desde 1 minuto hasta 3 meses.
#   - La disponibilidad de los datos varía en función del intervalo utilizado.
#   - Podemos extraear datos Pre y Post mercado, lo que puede ser útil para el análisis de precios fuera del 
#     horario regular de trading.
