# -*- coding: utf-8 -*-
# Importar librerías
from finvizfinance.news import News # pip install finvizfinance
from finvizfinance.quote import finvizfinance
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer # pip install vaderSentiment
import csv

# Obtener Noticias Generales:
    
# Generar Instancia de la Clase
news = News()
noticias_blogs = news.get_news()
# Desempaquetar
noticias = noticias_blogs["news"]
blogs = noticias_blogs["blogs"]

# Mostrar todas las columnas sin truncamiento
pd.set_option("display.max_columns", None)

print("\nÚltimas 10 Noticias Generales más recientes:\n")
for indice, registro in noticias.iloc[:10, :].iterrows():
    fecha, titulo, fuente, link = registro["Date"], registro["Title"], registro["Source"], registro["Link"]
    print(f"Fecha/Hora: {fecha} - Título: {titulo} - Fuente: {fuente} - Link: {link}\n")
    
print("\nÚltimas 10 Noticias/Artículos de Blogs Generales del mercado más recientes:\n")
for indice, registro in blogs.iloc[:10, :].iterrows():
    fecha, titulo, fuente, link = registro["Date"], registro["Title"], registro["Source"], registro["Link"]
    print(f"Fecha/Hora: {fecha} - Título: {titulo} - Fuente: {fuente} - Link: {link}\n")
    
# Obtener Noticias Específicas:
    
# Crear Instancia de la Clase
stock = finvizfinance(ticker="AMZN")
print("Información del Activo:", stock.ticker_description())
# Iterar en las Noticias
contador = 0
for indice, noticia in stock.ticker_news().iterrows():
    fecha, titulo, fuente, link = noticia["Date"], noticia["Title"], noticia["Source"], noticia["Link"]
    print(f"Fecha/Hora: {fecha} - Título: {titulo} - Fuente: {fuente} - Link: {link}\n")
    contador += 1
    
print("Total de Noticias:", contador)

# Realizar Análisis de Sentimiento

# Ejemplo
oracion_1 = "Apple is a good stock"
oracion_2 = "Apple is a bad stock"

# Medir Sentimiento
analizador = SentimentIntensityAnalyzer()
sentimiento_1 = analizador.polarity_scores(oracion_1)["compound"]
sentimiento_1 = "Positivo" if sentimiento_1 >= 0 else "Negativo"
print(sentimiento_1)
sentimiento_2 = analizador.polarity_scores(oracion_2)["compound"]
sentimiento_2 = "Positivo" if sentimiento_2 >= 0 else "Negativo"
print(sentimiento_2)

# Iterar en cada noticia
sentimiento_noticia = []
noticias = stock.ticker_news()
for noticia in noticias["Title"]:
    sentimiento = analizador.polarity_scores(noticia)["compound"]
    sentimiento = "Positivo" if sentimiento >= 0 else "Negativo"
    sentimiento_noticia.append(sentimiento)
    
# Agregar columna
noticias["Sentiment"] = sentimiento_noticia
print(noticias[["Title", "Sentiment"]])
    
# Guardar Datos de Manera Local
nombre_archivo = "../datos/noticias_financieras.csv"
file = open(nombre_archivo, mode="w", newline="", encoding="utf-8")
writer = csv.writer(file)
# Escribir Columnas
writer.writerow(["Fecha", "Título", "Fuente", "Link", "Sentimiento"])
# Iterar en Noticias para guardarlas
for indice, noticia in noticias.iterrows():
    noticia = noticia.to_dict()
    writer.writerow([noticia["Date"], noticia["Title"], noticia["Source"], noticia["Link"], noticia["Sentiment"]])
    
file.close()
print(f"\nNoticias han sido guardads en {nombre_archivo}\n")
    
# Leer Noticias
noticias = pd.read_csv(nombre_archivo)
print(noticias)    

# Recordatorio:
#   - Las emociones reflejadas en las noticias pueden influir directamente en los precios de los activos financieros.
#     Un análisis de Sentimiento efectivo puede identificar patrones que anticipen movimientos del mercdo o tendencias.
