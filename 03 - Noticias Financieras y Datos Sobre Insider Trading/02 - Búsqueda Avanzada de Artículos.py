# -*- coding: utf-8 -*-
# Importar librerías
from newsapi import NewsApiClient, const # pip install newsapi-python
from datetime import datetime, timedelta
import requests
import json

# API Key
apiKey = "API_KEY"
# Generar Instancia de la Clase
newsapi = NewsApiClient(api_key=apiKey)

# URL Base de la API
url = "https://newsapi.org/v2/everything"

# Ejemplo 1: Obtener los 5 artículos más recientes con respecto a Bitcoin
articulos_top = newsapi.get_everything(q="bitcoin", language="en", page_size=5, sort_by="publishedAt")

# Mostrar Artículos
print("Total de Artículos:", len(articulos_top["articles"]))
print(json.dumps(articulos_top["articles"][0], indent=3))

# Ejemplo 2: Obtener Artículos más relevantes con respecto a Bitcoin (Manualmente)
params = {
    
    "q": "bitcoin",
    "apiKey": apiKey,
    "pageSize": 5,
    "language": "es",
    "sortBy": "relevance"
    
    }
# Hacer la solicitud Get
response = requests.get(url, params=params)

# Validar que se han recibido los datos
if response.status_code == 200: 
    # Extraer Datos
    data = response.json()
    # Iterar en cada una de ellas
    for resultado in data["articles"]:
        print("\n" + "- -" * 60)
        print("Nuevo Artículo:\n")
        print("Título:", resultado["title"])
        print("Descripción:", resultado["description"])
        print("Url:", resultado["url"])
        print("Fuente:", resultado["source"]["name"])
        print("- -" * 60 + "\n")
        
# Ejemplo 3: Obtener Artículos y Filtrar por Fuentes en un Rango de fechas para un tema específico "economy"
fecha_hoy = datetime.now()
# Establecer la Fecha Inicial una semana atrás
fecha_pasada = fecha_hoy - timedelta(days=7)
print(f"Fecha Inicial: {fecha_pasada} - Fecha Final: {fecha_hoy}")    
        
# Mostrar la cantidad de Fuentes Disponibles
print("Total de Fuentes Disponibles:", len(newsapi.get_sources()["sources"]))

fuentes = ""
for fuente in newsapi.get_sources()["sources"]:
    print("Nombre:", fuente["name"], "- Id:", fuente["id"])
    fuentes += fuente["id"] + ","
# Eliminar última coma
fuentes = fuentes[:-1]
articulos_filtrados = newsapi.get_everything(q="economy", sources=fuentes, from_param=fecha_pasada, to=fecha_hoy,
                                             page_size=7, page=1, sort_by="popularity")
        
for articulo in articulos_filtrados["articles"]:    
    print("\n" + "- -" * 60)
    print("Nuevo Artículo:\n")
    print("Título:", articulo["title"])
    print("Descripción:", articulo["description"])
    print("Url:", articulo["url"])
    print("Fuente:", articulo["source"]["name"])
    print("- -" * 60 + "\n")
        
print("Lenguajes Disponibles:", const.languages)

# Recordatorio:
#   - NewsApi nos permite extraer noticias de cualquier fuente de información, ya sea global o local,
#     permitiéndonos acceder a artículos de divdersos medios de comunicación, blogs, foros y redes sociales.
#   - El poder filtrar noticias por fuentes específicas nos permite selccionar medios de comunicación confiables
#     y relevantes, asegurando la calidad y la veracidad de la información que utilizamos.
