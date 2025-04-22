# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import numpy as np
import pytz # pip install pytz

# Descargar datos
df = yf.download(tickers="TSLA", period="1d", interval="1m", multi_level_index=False, ignore_tz="America/New_York")
print("Número de registros descargados:", df.shape[0])
print(df)

# Realizar un Resampleo a temporalidad de 2 minutos
temporalidad = "2T"
operaciones_dict = {
    
    "Open": "first",
    "High": "max",
    "Low": "min",
    "Close": "last",
    "Volume": "sum"
    
    }

df_2min = df.resample(temporalidad, closed="left").agg(operaciones_dict)
print("Número de registros descargados:", df_2min.shape[0])
print(df_2min)

# Comprobar Precios
df_new = yf.download(tickers="TSLA", period="1d", interval="2m", multi_level_index=False, ignore_tz="America/New_York")
# Ajustar columnas en el mismo orden de nuestros datos anteriores
df_new = df_new[["Open", "High", "Low", "Close", "Volume"]]

# Validar que los datos son iguales
if np.mean(df_2min.loc[df_new.index] == df_new) == 1:
    print("¡Los Datos son idénticos!")
    
# Ampliar el tiempo de descarga
df =  yf.download(tickers="TSLA", period="3d", interval="1m", multi_level_index=False, ignore_tz="America/New_York")
print("Número de registros descargados:", df.shape[0])
print(df)    

# Realizar Resampleo
temporalidad = "5T"
df_5min = df.resample(temporalidad).agg(operaciones_dict)    
print("Número de registros descargados:", df_5min.shape[0])
print(df_5min)

# Comprobar Precios
df_new = yf.download(tickers="TSLA", period="3d", interval="5m", multi_level_index=False, ignore_tz="America/New_York")
# Ajustar columnas en el mismo orden de nuestros datos anteriores
df_new = df_new[["Open", "High", "Low", "Close", "Volume"]]

# Validar longitud
if df_new.shape[0] != df_5min.shape[0]:
    print("¡La extensión de ambos DataFrames es distinta!")

# Obtener Registros con Nans
df_nans = df_5min.loc[df_5min.isna().any(axis=1)]
print(df_nans)    
    
# Eliminar Datos Nans después de realizar el resampleo
temporalidad = "5T"
df_5min = df.resample(temporalidad).agg(operaciones_dict).dropna(axis=0)  
print("Número de registros descargados:", df_5min.shape[0])
print(df_5min)  
    
# Validar
if np.mean(df_5min.loc[df_new.index] == df_new) == 1:
    print("¡Los Datos han sido cambiados exitosamente!")
    
# Resamplear con datos descargados de 5 minutos a 1 hora
temporalidad = "1H"
df_1h = df_5min.resample(temporalidad, origin="start").agg(operaciones_dict).dropna(axis=0)

# Descargar datos en un hora
df = yf.download(tickers="TSLA", period="3d", interval="1h", multi_level_index=False, ignore_tz="America/New_York")
df = df[["Open", "High", "Low", "Close", "Volume"]]

# Validar
if np.mean(df_1h == df) == 1:
    print("¡Los datos han sido cambiados exitosamente!")
    
# Explorar las zonas horarias
print("Diferentes Zonas Horarias:", pytz.all_timezones)
    
# Establecer o localizar una Zona Horari en nuestros datos
df.index = df.index.tz_localize("America/New_York")
print("Zona Horaria:", df.index.tz)
print(df)    
    
# Cambiar Zona Horaria
df.index = df.index.tz_convert("America/Mexico_City")
print("Zona Horaria:", df.index.tz)

# Recordatorio:
#   - Los datos pueden ser resampleados y agregados para cambiar su frecuencia temporal, facilitando el análisis de datos
#     temporales. El resampleo ajusta la granularidad de los datos, mientras que la agregación permite resumirlos mediante
#     funciones como promedio, suma, máximo o mínimo, proporcionando una visión más clara de tendencias o patrones.
#   - Las Zonas Horarias nos permiten ajustar los datos en base a la ubicación geográfic de los mercados, garantizando que
#     los registros temporales coincidan con las horas locales de cada activo.
