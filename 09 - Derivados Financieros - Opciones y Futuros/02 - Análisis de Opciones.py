# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
from alpha_vantage import options
import pandas as pd
import matplotlib.pyplot as plt

# Definir el activo a analizar
ticker = "SPY"
stock = yf.Ticker(ticker=ticker)

# Obtener las fechas de vencimiento
dates_exp = stock.options
print(dates_exp)
print("Total de Fechas de Vencimiento:", len(dates_exp))

# Obtener Todas las Opciones Disponibles
opciones_disponibles = [stock.option_chain(date=expiration) for expiration in dates_exp]
opciones_extraer = [[opciones.calls, opciones.puts] for opciones in opciones_disponibles]
# Agregar Fecha de Vencimiento y Tipo de Opción a cada Contrato
df_opciones = pd.DataFrame()
for opciones, expiration in zip(opciones_extraer, dates_exp):
    # Extraer Opciones
    calls, puts = opciones
    calls["Tipo"] = "call"
    puts["Tipo"] = "put"
    # Concatenar
    opciones_totales = pd.concat([calls, puts], axis=0)
    # Agregar Vencimiento
    opciones_totales["expirationDate"] = pd.to_datetime(expiration)
    # Concatenar al Principal
    df_opciones = pd.concat([df_opciones, opciones_totales], axis=0)
    
# Mostrar Opciones
print(df_opciones)

# Visualizar la relación entre el precio de ejercicio y el último precio (Call y Put)
seleccionar_fecha = dates_exp[1]
calls = df_opciones[(df_opciones["expirationDate"] == seleccionar_fecha) & (df_opciones["Tipo"] == "call")]
puts = df_opciones[(df_opciones["expirationDate"] == seleccionar_fecha) & (df_opciones["Tipo"] == "put")]
precio_actual_ticker = stock.info["regularMarketPrice"]
# Generar Plot
plt.figure(figsize=(22, 5))
plt.plot(calls["strike"], calls["lastPrice"], label="Call", marker="o")
plt.plot(puts["strike"], puts["lastPrice"], label="Put", marker="s")
plt.xlabel("Precio de Ejercicio")
plt.ylabel("Último Precio")
plt.legend()
plt.title(f"Cadenas de Opciones para {ticker} ({seleccionar_fecha}) con Precio: {precio_actual_ticker}")
plt.grid()
plt.show()

# Visualizar cómo varía la volatilidad implícita en diferentes precios de ejercicio
plt.figure(figsize=(22, 5))
plt.plot(calls["strike"], calls["impliedVolatility"], label="Call", marker="o")
plt.plot(puts["strike"], puts["impliedVolatility"], label="Put", marker="s")
plt.xlabel("Precio de Ejercicio")
plt.ylabel("Volatilidad Implícita")
plt.legend()
plt.title(f"Volatilidad Implícita de Opciones para {ticker} ({seleccionar_fecha})")
plt.grid()
plt.show()

# Comparar Volatilidad Implícita para el mismo Strike en diferentes fechas de vencimiento
strikes = [400, 500, 600]
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(22, 6))
for n, strike in enumerate(strikes):
    contratos_strike = df_opciones[df_opciones["strike"] == strike]
    calls_strike = contratos_strike[contratos_strike["Tipo"] == "call"]
    puts_strike = contratos_strike[contratos_strike["Tipo"] == "put"]
    # Generar plot
    axes[n].plot(calls_strike["expirationDate"], calls_strike["impliedVolatility"],
                 marker="o", linestyle="--", label="Call")
    axes[n].plot(puts_strike["expirationDate"], puts_strike["impliedVolatility"],
                 marker="s", linestyle="--", label="Put")
    axes[n].set_xlabel("Fecha de Vencimiento")
    axes[n].set_ylabel("Volatilidad Implícita")
    axes[n].legend()
    axes[n].set_title(f"Comparación de Volatilidad Implícita para Strike {strike} \nen Diferentes Vencimientos \
                      ({ticker})")
    axes[n].grid()
    axes[n].tick_params(axis="x", rotation=45)
    
plt.subplots_adjust()
plt.show()

# Realizar Análisis de Griegas con Alpha Vantage:
    
# Configurar conexión
api_key = "API_KEY"
opt = options.Options(key=api_key)

# Obtener todas las opciones disponibles
opt_historical, _ = opt.get_historical_options(symbol=ticker, date=None)

# Análisis de las Griegas
griegas = ["delta", "gamma", "theta", "vega"]
colores = ["blue", "green", "red", "purple"]
titulos = ["Delta vs Strike", "Gamma vs Strike", "Theta vs Strike", "Vega vs Strike"]
df_vencimiento = opt_historical[(opt_historical["expiration"] == seleccionar_fecha)]
calls = df_vencimiento[df_vencimiento["type"] == "call"]
puts = df_vencimiento[df_vencimiento["type"] == "put"]
# Realizar Plot
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(22, 10))
for ax, griega, color, titulo in zip(axes.flatten(), griegas, colores, titulos):
    ax.plot(calls["strike"].astype(float), calls[griega].astype(float), color=color, alpha=0.6, label="Call")
    ax.plot(puts["strike"].astype(float), puts[griega].astype(float), color=color, alpha=0.6, linestyle="dashed",
            label="Put")
    ax.set_xlabel("Strike Price")
    ax.set_ylabel(griega.capitalize())
    ax.set_title(titulo)
    ax.legend()
    ax.grid()
    
plt.tight_layout()
plt.show()

# Recordatorio:
#   - La prima de una opción depende de la volatilidad implícita y el precio de ejercicio. Analizar esta relación
#     ayuda a prever cambios en el valor de la opción.
#   - El análisis de las griegas ayuda a gestionar riesgos, ajustando las estrategias de cobertura según cómo el
#     precio del activo subyacente, el tiempo o la volatilidad afecten las opciones.
