# -*- coding: utf-8 -*-
# Importar librerías
import requests
from fake_useragent import UserAgent # pip install fake-useragent
import pandas as pd
import json
from warnings import filterwarnings
filterwarnings("ignore")

# URL de Trading Economics con las tasas de interés de los bonos a 10 años
url_bonds = "https://tradingeconomics.com/bonds"

# Generar un Usuario de Web Random
headers = {
    "User-Agent": UserAgent().chrome
    }
print(json.dumps(headers, indent=4))

# Realizar Petición
response = requests.get(url=url_bonds, headers=headers)

# Validar que la respuesta sea correcta
if response.status_code == 200:
    print("¡La Extracción de datos ha sido exitosa!")
    
# Extraer las tablas con pandas
tablas = pd.read_html(response.text)
print("Tablas Encontradas:\n", tablas)

# Dar formato a tablas
tablas = {tabla.columns[1]:tabla.iloc[:, 1:] for tabla in tablas}
for clave, tabla in tablas.items():
    print(f"\nTabla Estructurada para {clave}:\n", tabla)
    
# Extraer Datos dentro de la Tabla No. 1 (Major10Y)
df = tablas["Major10Y"]

# Filtrar las filas para obtener las tasas de los bonos de los países de estudio: Estados Unidos y México
tasa_eeuu = float(df.loc[df["Major10Y"] == "United States", "Yield"].values[0]) / 100
tasa_mexico = float(df.loc[df["Major10Y"] == "Mexico", "Yield"].values[0]) / 100

# Diferencial de Tasas
diferencial_tasas = tasa_mexico - tasa_eeuu
print(f"Diferencial de Tasas entre México y Estados Unidos: {diferencial_tasas:.4f}")

# Monto Inicial en USD
monto_inicial_usd = 1_000

# Cálculos de la inversión:
    
# Cálculos de pagos diarios, semanales, mensuales y anuales
dias_por_año = 365
semanas_por_año = 52
meses_por_año = 12

# Obtener Cantidad a favor o en contra por diferencial de tasas
interes_diario = monto_inicial_usd * (diferencial_tasas / dias_por_año)
interes_semanal = monto_inicial_usd * (diferencial_tasas / semanas_por_año)
interes_mensual = monto_inicial_usd * (diferencial_tasas / meses_por_año)

print(f"\nInterés ganado/pagado por día: ${interes_diario:.4f} USD")
print(f"\nInterés ganado/pagado por semana: ${interes_semanal:.4f} USD")
print(f"\nInterés ganado/pagado por mensual: ${interes_mensual:.4f} USD")
print(f"\nInterés ganado/pagado por año: ${monto_inicial_usd * diferencial_tasas:.2f} USD")

# Extraer Tablas de Pronósticos:
url_pronosticos_divisas = "https://tradingeconomics.com/forecast/currency"
# Realizar Petición
response = requests.get(url=url_pronosticos_divisas, headers=headers)
# Validar Respuesta
if response.status_code == 200:
    print("¡La Extracción ha sido exitosa!")
    
# Extraer tablas encontradas
tablas = pd.read_html(response.text)
print("Tablas de Pronósticos Encontradas:\n", tablas)

# Dar Formato y Estructura
tablas_pronosticos = {tabla.columns[1]: tabla.iloc[:, 1:] for tabla in tablas}
print("Tablas de Pronósticos Formateadas:\n\n", tablas_pronosticos)

# Extraer Principales Divisas
tabla_major = tablas_pronosticos["Major"].copy()
tendencia = (tabla_major["Price"] < tabla_major[tabla_major.columns[3]]).replace({False: -1,
                                                                                  True: 1})

tabla_major["Signal"] = tendencia
print(tabla_major)

# Recordatorio:
#   - Recuerda que al invertir en una paridad de divisas, las tasas de interés determinan si ganas o pagas
#     intereses. Si tienes una posición larga (compras una divisa con tasa alta) y corta (vendes la divisa
#     con tasa baja), recibirás la diferencia de tasas. Si la situación es opuesta, pagarás la diferencia.
