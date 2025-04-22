# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
from twelvedata import TDClient
from alpha_vantage import commodities
import investpy
import pandas as pd

# Obtener Datos con API de Investing:
    
# Grupos de Commodities
grupos_commodities = investpy.get_commodity_groups()
print(grupos_commodities)

# Lista de Activos
dict_commodities = investpy.get_commodities_dict()
df_commodities = pd.DataFrame(dict_commodities) 
print(df_commodities.iloc[:, 1:])

# Filtrar por tipos de Commodities
for grupo in grupos_commodities:
    sub_df = df_commodities[df_commodities["group"] == grupo]
    print("Commodity:", grupo, "\n")
    print(sub_df.iloc[:, 1:])
    print("-" * 60, "\n")
    
# Obtener Datos con Twelve Data:
    
# Configurar API
api_key = "API_KEY"
td = TDClient(apikey=api_key)

# Petición Datos Históricos de Oro (XAU/USD)
try:
    data_gold = td.time_series(symbol="XAU/USD", interval="1day", outputsize=100).as_pandas()
    print(data_gold)
except Exception as error:
    print(error)
    
# Obtener Datos con Yahoo Finance:
    
# Definir tickers para commodities (Oro, Petróleo, Gas Natural, Plata)
commodities_tickers = ["GC=F", "CL=F", "NG=F", "SI=F"]

# Descargar Datos
df_commodities = yf.download(tickers=commodities_tickers, period="1y", interval="1d")
print(df_commodities.head())

# Obtener Datos con API de Alpha Vantage: "monthly", "quarterly", "annual"

# Configurar API
api_key = "API_KEY"
cmt = commodities.Commodities(key=api_key)

# Descargar datos de Aluminio
aluminum, _ = cmt.get_aluminum(interval="monthly")
print("Datos de Aluminio:\n\n", aluminum[::-1])

print(aluminum[aluminum["value"] != "."].dropna()[::-1])

# Obtener datos del Petróleo (BRENT)
oil, _ = cmt.get_brent(interval="monthly")
print("Datos de Petróleo:\n\n", oil)

# Obtener el precio del Global Price Index of All Commodities
gpi, _ = cmt.get_price_index()
gpi = gpi[gpi["value"] != "."]
print("Global Price Index of All Commodities:\n\n", gpi[::-1])

# Conocer todos los métodos disponibles para descargar datos de commodities
metodos_disponibles = [metodo_atributo for metodo_atributo in dir(cmt) if ("get" in metodo_atributo) and
                                                                          (not metodo_atributo.startswith("_"))]
print("Métodos disponibles:", metodos_disponibles)

# Recordatorio:
#   - Los commodities ofrecen una excelente forma de diversificar riesgos en un portafolio de inversión,
#     ya que su valor generalmente no está correlacionado con acciones o bonos, protegiendo contra las
#     volatilidades del mercado.
