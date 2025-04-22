# -*- coding: utf-8 -*-
# Importar librerías
from finvizfinance.quote import finvizfinance
import finvizfinance.screener as screener
from PIL import Image
import matplotlib.pyplot as plt
from warnings import filterwarnings
filterwarnings("ignore")

# Obtener Filtros Disponibles
filtros_disponibles = screener.get_filters()
for n, filtro in enumerate(filtros_disponibles):
    print(f"Filtro No. {n + 1}: {filtro}")
    
# Desplegar Valores que se pueden pasar a los Filtros
seleccion_filtro = "RSI (14)"
opciones_filtro = screener.get_filter_options(screen_filter=seleccion_filtro)
for n, opcion in enumerate(opciones_filtro):
    print(f"Opción Disponible No. {n + 1}: {opcion}")
    
# Realizar Ejemplo: Seleccionar acciones con RSI Sobrevendido (Menor a 30)
filtro_rsi = {
    
    "RSI (14)": "Oversold (30)"
    
    }
# Crear objeto de screener
screener_rsi = screener.overview.Overview()
screener_rsi.set_filter(filters_dict=filtro_rsi)
screener_response = screener_rsi.screener_view()
print(screener_response)

# Siguiente Ejemplo: Aplicar Múltiples Filtros (Filtros para Indentificar Activos con Tendencia Alcista)
filtros_multiples = {
    
    "Exchange": "NASDAQ",
    "Sector": "Any",
    "Country": "USA",
    "Beta": "Over 1",
    "Price": "Over $1",
    "Gap": "Up 3%"
    
    }
screener_multiple = screener.overview.Overview()
screener_multiple.set_filter(filters_dict=filtros_multiples)
screener_response = screener_multiple.screener_view(order="Change from Open", select_page=1, ascend=False)
print(screener_response[["Ticker", "Company", "Price", "Change"]])

# Siguiente Ejemplo: Top Gainers (Acciones con mayor incremento porcentual en el precio)
screener_top_gainers = screener.overview.Overview()
screener_top_gainers.set_filter(signal="Top Gainers")
screener_response = screener_top_gainers.screener_view(order="Change", ascend=False, limit=20)
print(screener_response[["Ticker", "Company", "Price", "Change"]])

# Mostrar todas las Señales Disponibles
signals = screener.get_signal()
for n, sig in enumerate(signals):
    print(f"Señal No. {n}: {sig}")

# Mostrar todas las maneras en que puedes Ordenar la respuesta
ordenar_valores = screener.get_orders()
for n, order in enumerate(ordenar_valores):
    print(f"Tipo de Ordenamiento No. {n}: {order}")

# Siguiente Ejemplo: Múltiples parámetros y Señales
screener_avanzado = screener.overview.Overview()
filtros = {
    
    "Industry": "Any",
    "Volatility": "Week - Over 3%",
    "Market Cap.": "Any", # Otro ejemplo: "Large ($10bln to $200bln)"
    "Target Price": "5% Above Price"
    
    }
screener_avanzado.set_filter(signal="Most Active", filters_dict=filtros)
screener_response = screener_avanzado.screener_view(order="Performance (Week)", select_page=1, ascend=False)
print(screener_response[["Ticker", "Company", "Price", "Change"]])

# Siguiente Ejemplo: Extracción de Datos Financieros
screener_financiero = screener.financial.Financial()
screener_financiero.set_filter(signal="Channel Up")
screener_response = screener_financiero.screener_view(order="Performance (Year)", ascend=False, select_page=1)
print(screener_response)

# Mostrar Gráfico de un Activo
ticker_channel_up = screener_response["Ticker"].iloc[0]
finviz_quote = finvizfinance(ticker=ticker_channel_up)
# Descargar Gráfico
finviz_quote.ticker_charts()
# Cargar a nuestra imagen
img = Image.open(ticker_channel_up + ".jpg")

# Visualizar
plt.figure(figsize=(22, 6), dpi=300)
plt.imshow(img)
plt.axis("off")
plt.title(f"Gráfico de {ticker_channel_up}")
plt.show()

# Siguiente Ejemplo: Peticiones con Extracción de Datos de Indicadores Técnicos
screener_tecnico = screener.technical.Technical()
screener_tecnico.set_filter(signal="TL Support")
screener_response = screener_tecnico.screener_view(order="Market Cap.", ascend=False, select_page=1)
print(screener_response)

# Graficar
ticker_tl_support = screener_response["Ticker"].iloc[0]
finviz_quote = finvizfinance(ticker=ticker_tl_support)
# Descargar Gráfico
finviz_quote.ticker_charts()
# Cargar a nuestra imagen
img = Image.open(ticker_tl_support + ".jpg")

# Visualizar
plt.figure(figsize=(22, 6), dpi=300)
plt.imshow(img)
plt.axis("off")
plt.title(f"Gráfico de {ticker_tl_support}")
plt.show()

# Opciones para extraer peticiones con información adicional
opciones_disponibles = [
    screener.overview.Overview(),  # Muestra una visión general del stock.
    screener.financial.Financial(), # Extrae datos financieros como ingresos, márgenes y ratios financieros.
    screener.technical.Technical(), # Proporciona información técnica como indicadores y tendencias del precio.
    screener.performance.Performance(), # Ofrece el rendimiento histórico de una acción en diferentes plazos.
    screener.valuation.Valuation(), # Evalúa la valoración de la acción mediante múltiplos como el P/E.
    screener.ownership.Ownership() # Muestra la distribución de la propiedad de la acción (institucional, insider)
    ]

# Recordatorio:
#   - El escáner de Finviz permite filtrar activos según diversos criterios, como volatidad, sector, capitalización,
#     precio objetivo y rendimiento, para encontrar oportunidades de inversión específicas. Puedes personalizar las
#     búsquedas con señales avanzadas y ordenar resultados según métricas clave de desempeño.
