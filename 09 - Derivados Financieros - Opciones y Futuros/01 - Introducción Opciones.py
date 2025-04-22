# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
from alpha_vantage import options
import wallstreet
import pandas as pd
from datetime import datetime
import json
from warnings import filterwarnings
filterwarnings("ignore")

# Extraer Opciones de un Activo
ticker = "AMZN"
stock = yf.Ticker(ticker=ticker)

# Obtener las fechas de vencimientos de las Opciones
fechas_vencimiento = stock.options
print(fechas_vencimiento)
print("Total de Fechas de Vencimiento:", len(fechas_vencimiento))

# Seleccionar una fecha de vencimiento (por ejemplo, la segunda disponible)
fecha = fechas_vencimiento[1]
# Obtener la Cadena de Opciones
opciones = stock.option_chain(date=fecha)
print(type(opciones))

# Desplegar información del activo (Amazon)
underlying_info = opciones.underlying
print(json.dumps(underlying_info, indent=4))

# Separar Calls y Puts
calls = opciones.calls
print(calls)

puts = opciones.puts
print(puts)

# Obtener Todas las Opcioens disponibles para todos los vencimientos y precios de ejercicio
total_opciones_df = pd.DataFrame()
for exp in fechas_vencimiento:
    # Extraer Contratos
    opciones_disponibles = stock.option_chain(date=exp)
    # Calls
    calls = opciones_disponibles.calls
    # Puts
    puts = opciones_disponibles.puts
    # Crear una nueva columna indicando el tipo de Opción
    calls["Tipo"] = "call"
    puts["Tipo"] = "put"
    # Concatenar Opciones Disponibles
    total_opciones = pd.concat([calls, puts], axis=0)
    # Agregar Fecha de Vencimiento
    total_opciones["expirationDate"] = pd.to_datetime(exp)
    # Calcular los días faltantes para el vencimiento
    hoy = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    total_opciones["daysToExpiration"] = (total_opciones["expirationDate"] - hoy)
    # Unir a DataFrame Inicial
    total_opciones_df = pd.concat([total_opciones_df, total_opciones])
    
# Mostrar un resumen de los datos recopilados
print("\nTotal de Contratos de Opciones Recopilados:", len(total_opciones_df), "\n")
print(total_opciones_df)
    
# Obtener Todas las Opciones Disponibles con Alpha Vantage:
    
# Configurar Conexión
api_key = "API_KEY"
opt = options.Options(key=api_key)

opt_historical, _ = opt.get_historical_options(symbol=ticker)
print(opt_historical)    
    
# Precio en Tiempo Real con wallstreet (Seleccionar una Opción):
primer_registro = total_opciones_df.iloc[0]
expiration_date = primer_registro["expirationDate"]
day, month, year = expiration_date.day, expiration_date.month, expiration_date.year
strike = primer_registro["strike"]
if primer_registro["Tipo"] == "call":
    precio = wallstreet.Call(quote=ticker, d=day, m=month, y=year, strike=strike)
    print(precio.price)
else:
    precio = wallstreet.Put(quote=ticker, d=day, m=month, y=year, strike=strike)
    print(precio.price)
    
# Recordatorio:
#   - Las Opciones son contratos financieros que dan el derecho, pero no la obligación, de comprar o vender
#     un activo subyacente a un precio determinado dentro de un plazo específico.
#   - Las Opciones Call otorgan al titular el derecho a comprar el activo subyacente a un precio específico.
#     Son beneficiosas cuando se espera que el precio del activo subyacente aumente.
#   - Las Opciones Put dan al titular el derecho de vender el activo subyacente a un precio determinado.
#     Son útiles cuando se espera que el precio del activo disminuya.
