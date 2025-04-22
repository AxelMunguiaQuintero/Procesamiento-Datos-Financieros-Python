# -*- coding: utf-8 -*-
# Importar librerías
from alpha_vantage.timeseries import TimeSeries # pip install alpha-vantage
import json
import dash # pip install dash
from dash import dcc, html
import plotly.graph_objects as go
import webbrowser

# Clave API
api_key = "TOKEN"

# Crear un objeto de TimeSeries
ts = TimeSeries(key=api_key, output_format="pandas")

# Obtener datos de una acción específica
datos, metadata = ts.get_daily(symbol="AAPL", outputsize="compact")

# Mostrar resultados
print("Metadata:\n\n", json.dumps(metadata, indent=4))
print("Datos descargados:\n\n", datos)

# Descargar todos los datos disponibles
datos, metadata = ts.get_daily(symbol="AAPL", outputsize="full")

# Mostrar resultados
print("Metadata:\n\n", json.dumps(metadata, indent=4))
print("Datos descargados:\n\n", datos)

# Descargar datos intradía
datos, metadata = ts.get_intraday(symbol="TSLA", interval="1min", outputsize="compact")
# Intervalos disponibles: "1min", "5min", "30min", "60min"

# Mostrar resultados
print("Metadata:\n\n", json.dumps(metadata, indent=4))
print("Datos descargados:\n\n", datos)

# Datos Intradía para un mes en particular
datos, metadata = ts.get_intraday(symbol="TSLA", interval="1min", outputsize="full", extended_hours=True, month="2020-01")

# Mostrar resultados
print("Metadata:\n\n", json.dumps(metadata, indent=4))
print("Datos descargados:\n\n", datos)

# Datos en Ventanas Temporales más amplias
datos, metadata = ts.get_monthly(symbol="AAPL")

# Mostrar resultados
print("Metadata:\n\n", json.dumps(metadata, indent=4))
print("Datos descargados:\n\n", datos)

# Generar visualización más avanzada
datos = datos.rename(columns={
    
    "1. open": "Open",
    "2. high": "High",
    "3. low": "Low",
    "4. close": "Close",
    "5. volume": "Volume"
    
    })
datos = datos[::-1]

# Crear la aplicación de Dash
app = dash.Dash(__name__)

# Definir el diseño de la aplicación
app.layout = html.Div([
    html.H1("Gráfico de Velas de AAPL", style={"textAlign": "center"}),
    dcc.Graph(id="grafico-velas",
              figure={
                  "data": [
                      
                      go.Candlestick(
                          x=datos.index,
                          open=datos["Open"],
                          high=datos["High"],
                          low=datos["Low"],
                          close=datos["Close"],
                          name="AAPL"
                          
                          )
                      
                      ],
                  "layout": go.Layout(
                      
                      title="Gráfico de Velas",
                      xaxis={"title": "Fecha"},
                      yaxis={"title": "Precio ($)"},
                      template="plotly_dark"
                      
                      )
                  
                  })
    
    ])

# Ejecutar el servidor Dash
host = "127.0.0.1"
puerto = "8050"
app.run(debug=True, host=host, port=puerto)
url_completa = "http://" + host + ":" + puerto + "/"
webbrowser.open(url=url_completa)

# Recordatorio:
#   - Alpha Vantage es una platforma que proporciona datos financieros gratuitos y de pago. Su plan gratuito
#     incluye únicamente 25 peticiones por día.
#   - Dash es un framework útil para crear aplicaciones web interactivas en Python, especialmente orientado
#     a visualizaciones de datos.
