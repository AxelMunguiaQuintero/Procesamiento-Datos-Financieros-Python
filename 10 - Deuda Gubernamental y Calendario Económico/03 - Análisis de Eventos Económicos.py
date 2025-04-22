# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from fredapi import Fred

# Configurar la API
api_key = "API_TOKEN"
fred = Fred(api_key=api_key)

# Descargar los datos de la Tasa de Desempleo (UNRATE)
tasa_desempleo_data = fred.get_series(series_id="UNRATE")

# Descargar datos del S&P 500 utilizando Yahoo Finance
sp500_data = yf.download("^GSPC", period="max", multi_level_index=False)["Close"]

# Unir ambos datasets en una única tabla (se alinean por fecha)
data = pd.DataFrame({
    
    "Tasa de Desempleo": tasa_desempleo_data,
    "S&P500": sp500_data
    
    }).dropna()
print(data)

# Gráfica de la Tasa de Desempleo y el S&P 500
fig, ax1 = plt.subplots(figsize=(22, 6))

# Gráfico de la Tasa de Desempleo en el primer eje y
ax1.set_xlabel("Fecha")
ax1.set_ylabel("Tasa de Desempleo (%)", color="blue")
ax1.plot(data.index, data["Tasa de Desempleo"], color="blue", label="Tasa de Desempleo", linewidth=2)
ax1.tick_params(axis="y", labelcolor="blue")

# Crear un segundo eje para el S&P 500
ax2 = ax1.twinx()
ax2.set_ylabel("Precio S&P 500", color="red")
ax2.plot(data.index, data["S&P500"], color="red", label="S&P 500", linewidth=2)
ax2.tick_params(axis="y", labelcolor="red")

plt.title("Análisis de la Tas de Desempleo y S&P 500")
fig.legend(loc="upper left", bbox_to_anchor=(0.03, 0.93))
plt.grid()
fig.tight_layout()
plt.show()

# Descargar indicadores económicos importantes desde FRED
indicator_codes = {
    
    "Índice de Confianza al Consumidor": "UMCSENT",
    "PIB": "GDP",
    "Índice de Precios Al Consumidor": "CPIAUCSL",
    "Producto Interno Bruto Real": "A191RL1Q225SBEA"
    
    }

# Descargar los datos de todos los indicadores
economic_data = {name: fred.get_series(series_id=code) for name, code in indicator_codes.items()}

# Crear subplots para los indicadores económicos
fig, axes = plt.subplots(2, 2, figsize=(22, 10), sharex=False)
axes = axes.flatten()

# Graficar cada indicador
colors = ["blue", "green", "red", "orange"]
for idx, (name, data) in enumerate(economic_data.items()):
    data = data.copy().dropna()
    axes[idx].plot(data.index, data, color=colors[idx], linewidth=2)
    axes[idx].set_title(name)
    axes[idx].set_xlabel("Fecha")
    axes[idx].set_ylabel("Valor")
    axes[idx].grid(True)
    
plt.tight_layout()
plt.show()

# Recordatorio:
#   - Los indicadores económicos como la tasa de desempleo, el PIB y la inflación, ofrecen información relevante sobre la salud
#     macroeconómica, permitiendo anticipar movimientos en los mercados y detectar posibles cambios en la tendencia económica.
