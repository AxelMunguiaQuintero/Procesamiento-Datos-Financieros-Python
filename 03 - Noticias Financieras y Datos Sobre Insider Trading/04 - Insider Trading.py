# -*- coding: utf-8 -*-
# Importar librerías
from finvizfinance.insider import Insider
from finvizfinance.quote import finvizfinance
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Cambiar Opción 
pd.set_option("display.max_columns", None)

# Obtener transacciones más recientes
insider_trader_latest = Insider(option="latest")
latest_df = insider_trader_latest.get_insider()

# Opción -> latest: Obtiene la información más reciente sobre las transacciones internas.
# Opción -> latest buys: Obtiene las compras internas más recientes.
# Opción -> latest sales: Obtiene las ventas internas más recientes.
# Opción -> top week: Muestra las transacciones internas más importantes de la última semana.
# Opción -> top week buys: Muestra las compras internas más importantes de la última semana.
# Opción -> top week sales: Muestra las ventas internas más importantes de la última semana.
# Opción -> top owner trade: Muestra las transacciones internas más importantes por los propietarios principales.
# Opción -> top owner buys: Muestra las transacciones de compra internas más importantes por los propietarios principales.
# Opción -> top owner sales: Muestra las transacciones de ventas internas más importantes por los propietarios principales.
# Opción -> insider_id: Permite obtener información basada en un ID específico de un interno.

# Realizar nueva petición
insider_trader_twb = Insider(option="top week buys")
latest_df = insider_trader_twb.get_insider()

# Analizar si los activos involucrados de compra tuvieron una mayor volatilidad en los últimos días
buys_df = latest_df[latest_df["Transaction"] == "Buy"]
tickers = buys_df["Ticker"].drop_duplicates().values.tolist()

# Descargar Datos
df = yf.download(tickers=tickers, period="1y", interval="1d")

# Eliminar Tickers con información incompleta
df = df.dropna(axis=1)
# Guardar los Precios de Cierre y Volumen para los primeros 6 activos
close = df["Close"].iloc[:, :6]
volume = df["Volume"][close.columns]
tickers = close.columns

# Crear subgráficos para cada tickers
fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(22, 15), dpi=300)

# Graficar el cierre de cada tickers
colores = ["g", "r", "b", "gold", "purple", "brown"]
for i, ticker in enumerate(tickers):
    row, col = divmod(i, 2)
    axes[row, col].plot(close[ticker], label=ticker, color=colores[i])
    axes[row, col].set_title(f"Precio de Cierre de {ticker}")
    axes[row, col].set_xlabel("Fecha")
    axes[row, col].set_ylabel("Precio de Cierre")
    axes[row, col].legend()
    
plt.suptitle("Precios de Cierre", fontsize=18)
fig.tight_layout()
plt.show()

# Calcular el volumen promedio diario de cada activo
volumen_promedio_diario = volume.mean(axis=0)

# Calcular el volumen diario promedio de los últimos 7 días de cada activo
volumen_promedio_7dias = volume.tail(7).mean(axis=0)

# Crear un DataFrame combinado
df_combined = pd.DataFrame({
    
    "Volumen Promedio Diario": volumen_promedio_diario,
    "Volumen Promedio Últimos 7 Días": volumen_promedio_7dias
    
    })

# Crear un gráfico de barras laterales para comparar los volúmenes
fig, ax = plt.subplots(figsize=(28, 6), dpi=300)

# índice de barras
ind = np.arange(len(df_combined.index))
width = 0.35

# Graficar barras de volumen promedio diario
bar1 = ax.bar(x=ind - width / 2, height=df_combined["Volumen Promedio Diario"], width=width,
              label="Volumen Promedio Diario", color="red")
# Graficar barras de volumen promedio de los últimos 7 días
bar2 = ax.bar(x=ind + width / 2, height=df_combined["Volumen Promedio Últimos 7 Días"], width=width,
              label="Volumen Promedio Últimos 7 Días", color="green")

ax.set_xlabel("Ticker")
ax.set_ylabel("Volumen Promedio")
ax.set_title("Comparación de Volumen Promedio Diario Anual y Volumen Promedio Últimos 7 Días")
ax.set_xticks(ind)
ax.set_xticklabels(df_combined.index)
ax.legend()

fig.tight_layout()
plt.show()

# Obtener Actividad de Insider Trading para Tickers Específicos:
    
# Generar Instancia
stock = finvizfinance(ticker="AAPL")
# Tabla con Insiders
insider_trader_df = stock.ticker_inside_trader()

# Recordatorio:
#   - El Insider Trading ocurre cuando una persona usa información no pública y material sobre una empresa para tomar
#     decisiones de inversión antes de que esa información sea divulgada al público.
#   - Los informes públicos sobre transacciones de insiders pueden afectar significativamente los precios de los activos,
#     ya que los inversionistas reaccionan a estas compras o ventas, interpretándolas como señales de la salud futura
#     de la empresa.
