# -*- coding: utf-8 -*-
# Importar librerías
import requests
import pandas as pd
from fake_useragent import UserAgent
import yfinance as yf
import json
from warnings import filterwarnings
filterwarnings("ignore")

# Definir Urls
commodities_precios = "https://tradingeconomics.com/commodities"
commodities_pronosticos = "https://tradingeconomics.com/forecast/commodity"

# Realizar Petición
headers = {"User-Agent": UserAgent().chrome}
response = requests.get(url=commodities_precios, headers=headers)

# Leer datos
dfs = pd.read_html(response.text)
print(dfs)

# Extraer las diferentes tablas encontradas
tablas_commodities = {tabla.columns[0]: tabla for tabla in dfs}
total_activos = 0
for clave, valor in tablas_commodities.items():
    print(f"Datos para {clave}:\n\n", valor)
    print("-" * 60, "\n")
    total_activos += valor.shape[0]
print("Total de Instrumentos:", total_activos)
print("Grupos de Commodities:", list(tablas_commodities.keys()))

# Obtener Pronósticos del Movimiento del Precio
response = requests.get(url=commodities_pronosticos, headers=headers)
dfs_pronosticos = pd.read_html(response.text)
print(dfs_pronosticos)

# Extraer nuevas tablas
tablas_commodities_pronosticos = {tabla.columns[1]: tabla.iloc[:, 1:] for tabla in dfs_pronosticos}
for clave, valor in tablas_commodities_pronosticos.items():
    print(f"Pronósticos para {clave}:\n\n", valor)
    print("-" * 60, "\n")
    
# Ajustar Tendencias de Corto Plazo
metales = tablas_commodities_pronosticos["Metals"].copy()
columnas = metales.columns
print(columnas)
metales["Signal"] = metales["Price"] < metales[columnas[3]]
metales["Signal"] = metales["Signal"].replace({False: -1, True: 1})
print(metales) 
    
# Encontrar activos para invertir basados en industrias
sector = "basic-materials"
sector_yf = yf.Sector(key=sector)    
print("Info General:\n\n", json.dumps(sector_yf.overview, indent=4))

# Obtener Industrias Dentro del Sector
industrias = sector_yf.industries    
print(f"Industrias dentro del Sector: {sector}\n\n", industrias)

# Empresas más relevantes del Sector
top_companies = sector_yf.top_companies
print("Empresas Top:\n\n", top_companies)

# ETFs más relevantes del Sector
top_etfs = sector_yf.top_etfs    
print("Top ETFs:\n\n", json.dumps(top_etfs, indent=4))    

# Desplegar Fondos Mutuos con Mayor Exposición a este Sector
top_mutual_funds = sector_yf.top_mutual_funds    
print(f"Fondos Mutuos ({sector}):\n\n", json.dumps(top_mutual_funds, indent=4))
    
# Descargar Datos de Fondos Mutuos
df_mutual_funds = yf.download(tickers=list(top_mutual_funds.keys()), period="1y", interval="1d")
print(df_mutual_funds["Close"])

# Diferentes Sectores Disponibles
sectores_disponibles = ["communication-services", "consumer-cyclical", "consumer-defensive",
                        "energy", "financial-services", "healthcare", "industrials",
                        "real-state", "technology", "utilities"]
    
# Probar con "energy"
index_energy = sectores_disponibles.index("energy")
print("Index:", index_energy)    
sector_yf = yf.Sector(key=sectores_disponibles[index_energy])    
print("Industrias dentro del Sector de Energía:\n\n", sector_yf.industries)    

# Recordatorio:
#   - Recuerda que existen fondos y ETFs que proporcionan acceso a commodities sin la necesidad de tenerlos
#     directamente. Estos fondos permiten diversificar el riesgo y mitigar la volatilidad de los precios 
#     de los productos, lo que puede ser atractivo para los inversionistas que buscan una exposición más
#     estable.
