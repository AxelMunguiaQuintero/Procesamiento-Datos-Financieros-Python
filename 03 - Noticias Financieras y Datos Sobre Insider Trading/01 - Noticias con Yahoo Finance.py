# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
from datetime import datetime

# Ejemplo 1: Obtener una lista de activos financieros relacionados con "AMZN"
quotes = yf.Search(query="AMZN", max_results=10).quotes
print(quotes[0])

# Mostrar las cotizaciones encontradas
for quote in quotes:
    print(f"Activo: {quote['symbol']}. Nombre Corto: {quote['shortname']}. Tipo de Activo: {quote['quoteType']}")
    
# Ejemplo 2: Obtener una lista de noticias relacionadas con "AAPL"
news = yf.Search(query="Apple", news_count=5).news
print(news[0])

# Mostrar las noticias
for noticia in news:
    print("\n" + "- -" * 60)
    print("Nueva Noticia:\n")
    print("Título:", noticia["title"])
    print("Link:", noticia["link"])
    print("Fecha de Publicación:", datetime.fromtimestamp(noticia["providerPublishTime"]))
    print("Tipo de Noticia:", noticia["type"])
    print("- -" * 60 + "\n")
    
# Ejemplo 3: Buscar activos y noticias financieras relacionadas con el Oro/Gold
quotes_news = yf.Search(query="Gold", max_results=10, news_count=5)

# Iterar en las noticias
for noticia in quotes_news.news:
    print("\n" + "- -" * 60)
    print("Nueva Noticia:\n")
    print("Título:", noticia["title"])
    print("Link:", noticia["link"])
    print("Fecha de Publicación:", datetime.fromtimestamp(noticia["providerPublishTime"]))
    print("Tipo de Noticia:", noticia["type"])
    print("- -" * 60 + "\n")
    
# Iterar en los Instrumentos Financieros Encontrados
for quote in quotes_news.quotes:
    print(f"Activo: {quote['symbol']}. Nombre Corto: {quote['shortname']}. Tipo de Activo: {quote['quoteType']}")

# Recordatorio:
#   - Las noticias nos pueden proporcionar información importante sobre el sentimiento del mercado,
#     y además nos pueden informar sobre eventos relevantes que afecten el comportamiento de los activos
#     financieros.
