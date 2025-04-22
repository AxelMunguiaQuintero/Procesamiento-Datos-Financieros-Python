# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import os

# Diccionario de índices segmentado por categoría
indices = {
    
    "acciones": {
        
        "^GSPC": "Índice S&P 500, que mide el rendimiento de 500 grandes empresas cotizadas en EE.UU.",
        "^DJI": "Índice Dow Jones Industrial Average, compuesto por 30 importantes empresas industriales EE.UU.",
        "^IXIC": "Índice Nasdaq Composite, que incluye todas las acciones que cotizan en la Bolsa de Valores Nasdaq"
        
        },
    
    "sectoriales": {
        
        "^IXF": "Índice S&P 500 Financiero: Mide el desempeño del sector financiero dentro del S&P 500"
        
        },
    
    "bonos": {
        
        "^IRX": "Índice de rendimiento de los bonos del Tesoro de Estados Unidos a 13 semanas"
        
        },
    
    "materias_primas": {
        
        "^SPGSCI": "Índice S&P GSCI: Amplio referente del rendimiento de las materias primas a nivel mundial",
        "^BCOM": "Índice Bloomber Commodity: Mide el desempeño de una amplia gama de futuros de materias primas"
        
        },
    
    "criptomonedas": {
        
        "^CMC200": "Índice CMC Crypto 200: Rastrea el rendimiento de las 200 principales criptomonedas por capitalización de mercado"
        
        },
    
    "volatilidad": {
        
        "^VIX": "Índice de Volatilidad CBOE (VIX): Conocido como el 'índice del miedo', mide la volatilidad esperada del S&P 500",
        "^VXN": "Índice de Volatilidad Nasdaq 100: Mide la volatilidad esperada Nasdaq 100"
        
        },
    
    "divisas": {
        
        "DX-Y.NYB": "Índice del Dólar de EE.UU: Mide el valor del dólar estadounidense frente a una cesta de monedas extranjeras",
        "^XDE": "Índice del Euro: Refleja el valor del euro frente a una cesta de otras monedas"
        
        }
    
    }

# Descargar datos históricos de los índices
historical_indices = {}
for categoria, tickers in indices.items():
    for ticker, descripcion in tickers.items():
        try:
            # Descargar el último año de información
            datos = yf.download(ticker, period="1y", interval="1d")
            historical_indices[ticker] = datos
        except Exception as e:
            print(f"Error al descargar {ticker}: {e}")

# Graficar Datos
fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(22, 15), dpi=500)
axes = axes.flatten()

# Definir una lista de colores y un iterador cíclico
colores = itertools.cycle(["b", "g", "r", "c", "m", "y", "k"])

for ax, (ticker, df) in zip(axes, historical_indices.items()):
    if not df.empty:
        # Seleccionar el siguiente color en el ciclo
        color = next(colores)
        ax.plot(df.index, df["Close"], label=ticker, color=color)
        ax.set_title(f"{ticker}")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Precio de Cierre")
        ax.legend()
    else:
        ax.set_visible(False)
        
plt.tight_layout()
plt.show()

# Guardar los datos en un archivo csv por índice
if not os.path.isdir("../datos"):
    os.mkdir("../datos")
for ticker, df in historical_indices.items():
    df.to_csv(f"../datos/{ticker}.csv")
    print(f"Datos guardados en ../datos/{ticker}.csv")

# Guardar datos un Excel
writer = pd.ExcelWriter("../datos/indices_historicos.xlsx")

# Iterar sobre los datos históricos y escribir cada DataFrame en una hoja separada
for ticker, df in historical_indices.items():
    df.to_excel(writer, sheet_name=ticker)
    
writer.close()

print("Datos combinados han sido guardados")

# Comprobar que los datos se han guardado en diferentes pestañas
datos_cargados = {}
for indice in historical_indices.keys():
    datos_cargados[indice] = pd.read_excel("../datos/indices_historicos.xlsx", sheet_name=indice)
    print(f"\nDatos para {indice}:\n\n", datos_cargados[indice])

# Recordatorio:
#   - Los Índices permiten acceder a diferentes sectores o activos, como acciones, bonos o materias primas,
#     ofreciendo diversificación y exposición específica. Esto ayuda a los inversionistas, traders e instituciones
#     a reducir riesgos y ajustar carteras.
