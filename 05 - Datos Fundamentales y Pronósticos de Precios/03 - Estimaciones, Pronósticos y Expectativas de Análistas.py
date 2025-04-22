# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
from finvizfinance.quote import finvizfinance
import json
import datetime
import itertools
import matplotlib.pyplot as plt
from PIL import Image # pip install pillow 
import os

# Definir el ticker de la acción
symbol = "AAPL"
stock = yf.Ticker(symbol)

# Obtener información general del activo
info = stock.info

# 1. Obtener los precios objetivo de los analistas
precio_actual = info.get("currentPrice", "No disponible")
precio_objetivo_medio = info.get("targetMeanPrice", "No disponible")
precio_objetivo_bajo = info.get("targetLowPrice", "No disponible")
precio_objetivo_alto = info.get("targetHighPrice", "No disponible")

print("\nPrecios objetivo de los analistas:\n")
print(f" - Precio Actual del Activo: {precio_actual:.2f}")
print(f" - Precio Objetivo Medio: {precio_objetivo_medio:.2f}. En Porcentaje: {(precio_objetivo_medio / precio_actual -1) * 100:.2f}%")
print(f" - Precio Objetivo Bajo: {precio_objetivo_bajo:.2f}. En Porcentaje: {(precio_objetivo_bajo / precio_actual -1) * 100:.2f}%")
print(f" - Precio Objetivo Alto: {precio_objetivo_alto:.2f}. En Porcentaje: {(precio_objetivo_alto / precio_actual -1) * 100:.2f}%")

# Precios Objetivos de los Analistas
precios_objetivos = stock.analyst_price_targets
print(json.dumps(precios_objetivos, indent=4))

# 2. Obtener recomendaciones de analistas
clave_recomendacion = info.get("recommendationKey", "No disponible")
opiniones_analistas = info.get("numberOfAnalystOpinions", "No disponible")

print("Recomendaciones de los analistas:")
print(f"  - Clave de Recomendación: {clave_recomendacion}")
print(f"  - Número de Opiniones de Analistas: {opiniones_analistas}\n")

# Mostrar resumen de recomendaciones
resumen_recomendaciones = stock.recommendations_summary
print("Resumen de Recomendaciones:\n\n", resumen_recomendaciones)

# 3. Obtener mejoras y degradaciones en la calificación de la acción
mejoras_degradaciones = stock.upgrades_downgrades
print(mejoras_degradaciones)

# Realizar un Breve análisis de las calificaciones
diferentes_años = mejoras_degradaciones.index.year.drop_duplicates().tolist()
diferentes_años = sorted(diferentes_años)
print("Diferentes años con calificaciones:", diferentes_años)

# Obtener la calificación más repetida por año
periodos_calificaciones = {}
indice = mejoras_degradaciones.index.year
for n in range(1, len(diferentes_años)):
    periodo_inicio = diferentes_años[n - 1]
    periodo_final = diferentes_años[n]
    indice_filtrado = (indice >= periodo_inicio) & (indice < periodo_final)
    sub_mejoras_degradaciones = mejoras_degradaciones.loc[indice_filtrado]
    calificacion_ganadora = sub_mejoras_degradaciones["ToGrade"].value_counts(ascending=False).index[0]
    periodos_calificaciones[periodo_inicio] = calificacion_ganadora
    
# Realizar el análisis para el último periodo
indice_filtrado = indice >= diferentes_años[-1]
sub_mejoras_degradaciones = mejoras_degradaciones.loc[indice_filtrado]
calificacion_conteo = sub_mejoras_degradaciones["ToGrade"].value_counts(ascending=False)
print(calificacion_conteo)
calificacion_ganadora = calificacion_conteo.index[0]
periodos_calificaciones[diferentes_años[-1]] = calificacion_ganadora
print("Calificaciones Ganadoras por año:\n", json.dumps(periodos_calificaciones, indent=3))

# Graficar
ncols = 3
nrows = divmod(len(diferentes_años), ncols)
nrows = nrows[0] + 1 if nrows[1] > 0 else nrows[0]

# Lista de colores
colores = ["#FF5733", "#33FF57", "#3357FF", "#F0FF33", "#FF33A1"]
ciclo_colores = itertools.cycle(colores)

# Generar Subplots
fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(23, 16))
for n, ax in enumerate(axes.flatten()):
    if n < len(diferentes_años):
        # Descargar Datos
        fecha_inicio = datetime.datetime(diferentes_años[n], 1, 1).strftime("%Y-%m-%d")
        fecha_final = datetime.datetime(diferentes_años[n] + 1, 1, 1).strftime("%Y-%m-%d")
        df = yf.download(tickers=symbol, start=fecha_inicio, end=fecha_final, interval="1d", multi_level_index=False)["Close"]
        ax.plot(df, label="Año " + str(diferentes_años[n]), color=next(ciclo_colores), lw=2)
        recomendacion = periodos_calificaciones[diferentes_años[n]]
        ax.set_title("Recomendación por Firmas Calificadoras: " + recomendacion)
        
plt.tight_layout()
plt.show()

# 4. Obtener Estimaciones de Ingresos
estimaciones_ingresos = stock.get_revenue_estimate()
print("Expectativa de Ingresos:\n\n", estimaciones_ingresos.T)

# Obtener Ratings con Finviz
accion = finvizfinance(ticker=symbol)
ratings = accion.ticker_outer_ratings()
print(ratings)

# Obtener análisis del gráfico del activo
ruta_actual = os.getcwd()
accion.ticker_charts(out_dir=ruta_actual)

# Abrir la imagen usando PIL
ruta_imagen = ruta_actual + "/" + symbol + ".jpg"
img = Image.open(ruta_imagen)

plt.figure(figsize=(22, 12), dpi=300)
plt.imshow(img)
plt.axis("off")
plt.show()

# Recordatorio:
#   - Las Estimaciones y Expectativas de los analistas proporcionan una visión del posible desempeño futuro
#     de un activo. Estas proyecciones incluyen precios objetivo, recomendaciones y previsiones de ingresos,
#     basads en modelos financieros y datos de mercado.
