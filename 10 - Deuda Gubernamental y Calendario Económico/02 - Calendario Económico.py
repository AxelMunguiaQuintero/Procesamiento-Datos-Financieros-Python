# -*- coding: utf-8 -*-
# Importar librerías
from selenium import webdriver # pip install selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager # pip install webdriver-manager
import pandas as pd

# Configurar Selenium con Chrome
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled") # Evita detección de bot
# options.add_argument("--headless") # Ejecuta en segundo plano

# Configurar Driver
ruta_instalacion = ChromeDriverManager().install()
service = Service(executable_path=ruta_instalacion)
driver = webdriver.Chrome(service=service, options=options)

# URL del Calendario Económico
URL = "https://www.investing.com/economic-calendar"

# Definir función para extraer Calendario Económico
def obtener_calendario(url: str):
    
    """
    Función que extrae el calendario económico de Investing.com y devuelve un DataFrame con la información.
    """
    
    # Dirigirse al Sitio de Investing
    driver.get(url)
    # Esperar hasta 10 segundos para que la tabla se cargue
    wait = WebDriverWait(driver, 10)
    
    # Localizar Tabla
    try:
        tabla = wait.until(EC.presence_of_element_located(("id", "economicCalendarData")))
    except:
        print("No se pudo cargar la tabla")
        driver.quit()
        return None
    
    # Obtener todas las filas de eventos económicos
    filas = tabla.find_elements("class name", "js-event-item")
    
    # Iterar en cada evento para extraer la información
    eventos = []
    for fila in filas:
        columnas = fila.find_elements("tag name", "td")
        # Validar que la información está completa
        if len(columnas) < 7:
            continue
        
        # Extraer columnas para cada evento
        hora = columnas[0].text.strip()
        moneda = columnas[1].text.strip()
        impacto = columnas[2].get_attribute("title")
        evento = columnas[3].text.strip()
        actual = columnas[4].text.strip()
        esperado = columnas[5].text.strip()
        previo = columnas[6].text.strip()
        
        eventos.append([hora, moneda, impacto, evento, actual, esperado, previo])
        
    # Cerrar Navegador
    driver.quit()
    
    # Convertir los datos en un DataFrame
    df = pd.DataFrame(eventos, columns=["Hora", "Moneda", "Impacto", "Evento", "Actual", "Esperado", "Previo"])
    
    return df

# Ejecutar y mostrar los resultados
df_calendario = obtener_calendario(url=URL)
if df_calendario is not None:
    print(df_calendario)
else:
    print("No se pudo obtener el calendario económico.")
    
# Recordatorio:
#   - El Calendario Económico es una herramienta que lista eventos macroeconómicos programados, como anuncios
#     de políticas monetarias y datos clave de economía. En el trading, permite evaluar la volatilidad esperada
#     y gestionar riesgos al anticipar movimientos de mercado impulsados por dichos eventos.
