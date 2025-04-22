# -*- coding: utf-8 -*-
# Importar librerías
import pandas_datareader as pdr # pip install pandas-datareader
import datetime
import mplfinance as mpf # pip install mplfinance
import matplotlib.pyplot as plt

# Definir el rango de fechas para los datos históricos
start_date = datetime.datetime(2020, 1, 1)
end_date = datetime.datetime(2025, 1, 1)

# Obtener datos históricos de acciones:
    
print("------- Obtener Datos Históricos. Fuente: Stooq -------")
df_stooq = pdr.get_data_stooq(symbols=["AMZN"], start=start_date, end=end_date)
print("Datos \n\n", df_stooq)

# Extraer Datos. Fuente: Stooq
stooq_df = pdr.stooq.StooqDailyReader(symbols=["AMZN"], start="2020-01-01", end="2025-01-01")
df = stooq_df.read()
df = df[::-1]
print(df)

# Eliminar Nivel de Columnas
df.columns = df.columns.droplevel(level=1)
print("Datos con un solo nivel en columnas:\n\n", df)

# Opciones dentro de Pandas DataReader para descargar datos
opciones = [i for i in dir(pdr) if "get_data" in i]
for opcion in opciones:
    print("Opción:", opcion)
    
# Graficar Datos en formato de Velas
mpf.plot(data=df, style="yahoo", type="candle", volume=True, title="Precio de Amazon", figsize=(22, 6),
         warn_too_much_data=df.shape[0], figscale=3.0, panel_ratios=(7, 3))
plt.show()

# Recordatorio:
#   - Pandas DataReader es una alternativa viable para obtener datos de mercado. Sin embargo, su tiempo de descarga
#     puede tomar más tiempo si se compara con librerías más fiables (ejemplo: Yahoo Finance).
