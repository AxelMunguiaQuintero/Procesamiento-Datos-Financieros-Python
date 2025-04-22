# Importar librerías
import yfinance as yf
import wallstreet
import dash
from dash import dcc, html 
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from datetime import datetime
import webbrowser

# Definir Tickers
tickers = {
    
    "Acción: Apple": "AAPL", "Acción: Microsoft": "MSFT", "Acción: Google": "GOOGL",
    "Acción: Amazon": "AMZN", "Acción: Tesla": "TSLA", "Acción: Meta": "META",
    "Acción: Coca-Cola": "KO", "Índice: S&P 500": "^GSPC",
    "Índice: Dow Jones Industrial Average": "^DJI", "ETFs: S&P 500 ETF": "SPY",
    "ETFs: Invesco QQQ Trust": "QQQ"
    
    }

# Definir Marcos de Tiempo
marcos_de_tiempo = {
    
    "1 minuto": "1m", "2 minutos": "2m", "5 minutos": "5m", "15 minutos": "15m",
    "30 minutos": "30m", "1 hora": "1h", "90 minutos": "90m", "1 día": "1d",
    "5 días": "5d", "1 semana": "1wk", "1 mes": "1mo", "3 meses": "3mo"
    
    }

# Periodo de Descarga
periodos_descarga = {
    
    "1 día": "1d", "1 semana": "1wk", "1 mes": "1mo", "3 meses": "3mo",
    "1 año": "1y", "3 años": "3y", "5 años": "5y", "Máximo Disponible": "max"
    
    }

# Crear Aplicación Dash
app = dash.Dash(__name__)

# Definir Diseño de Nuestra Aplicación
app.layout = html.Div([
    
    # Agregar Título
    html.H1("Dashboard de Monitoreo Financiero en Tiempo Real", style={"font-size": "34px", "text-align": "center",
                                                                       "margin-top": "10px"}),
    
    # Instrucciones
    html.Div([
        html.Label("Selecciona un Ticker, un marco de tiempo y un periodo de descarga de datos:",
                   style={"font-size": "20px", "color": "darkblue", "font-weight": "bold"})
        ], style={"width": "100%", "margin-bottom": "10px"}),
    
    # Contenedor de los Dropdowns (en la misma línea)
    html.Div([
        
        dcc.Dropdown(id="tickers",
                     options=[{"label": clave, "value": valor} for clave, valor in tickers.items()],
                     value="AMZN", style={"flex": 1, "margin-right": "5px"}),
        dcc.Dropdown(id="ventanas",
                     options=[{"label": clave, "value": valor} for clave, valor in marcos_de_tiempo.items()],
                     value="1d", style={"flex": 1, "margin-right": "5px"}),
        dcc.Dropdown(id="periodo",
                     options=[{"label": clave, "value": valor} for clave, valor in periodos_descarga.items()],
                     value="1y", style={"flex": 1})
        
        ], style={"display": "flex", "width": "100%"}),
    
    # Mostrar Información para el Ticker Seleccionado
    html.H3(id="titulo_ticker", style={"text-align": "center", "margin-bottom": "5px", "margin-top": "10px"}),
    html.P(id="descripcion-ticker", style={"text-align": "center", "margin-top": "5px"}),
    
    # Tabla con el Precio, Cambio en el Precio y Cambio Porcentual
    html.Div([
        
        html.Table(id="tabla-precios", style={"margin": "auto", "text-align": "center", "border": "5px solid darkblue"},
                   children=[
                       
                       html.Tr([
                           
                           html.Th(children="Hora Actual",
                                   style={"padding": "10px", "border": "2px solid darkblue"}),
                           html.Th(children="Precio en Tiempo Real",
                                   style={"padding": "10px", "border": "2px solid darkblue"}),
                           html.Th(children="Cambio en el Precio",
                                   style={"padding": "10px", "border": "2px solid darkblue"}),
                           html.Th(children="Cambio Porcentual",
                                   style={"padding": "10px", "border": "2px solid darkblue"})
                           
                           ]),
                       
                       html.Tr([
                           
                           html.Td(id="hora", children=datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                                   style={"padding": "10px", "border": "2px solid darkblue"}),
                           html.Td(id="precio", children="0.0 USD",
                                   style={"padding": "10px", "border": "2px solid darkblue"}),
                           html.Td(id="cambio_precio", children="0.0",
                                   style={"padding": "10px", "border": "2px solid darkblue"}),
                           html.Td(id="cambio_porcentual", children="0 %",
                                   style={"padding": "10px", "border": "2px solid darkblue"})
                           
                           ])
                                             
                       ])

        ], style={"margin-top": "20px"}),
    
    # Componente Interval para actualizar la tabla cada 5 segundos
    dcc.Interval(id="intervalo", interval=60 * 1_000, n_intervals=0),
    
    # Gráfico de Precios
    dcc.Graph(id="grafico")
    
    ])


# Callback para actualizar la información
@app.callback(
    
    [Output(component_id="titulo_ticker", component_property="children"),
     Output(component_id="descripcion-ticker", component_property="children"),
     Output(component_id="hora", component_property="children"),
     Output(component_id="precio", component_property="children"),
     Output(component_id="cambio_precio", component_property="children"),
     Output(component_id="cambio_porcentual", component_property="children"),
     Output(component_id="grafico", component_property="figure")],
    
    [Input(component_id="tickers", component_property="value"),
     Input(component_id="ventanas", component_property="value"),
     Input(component_id="periodo", component_property="value"),
     Input(component_id="intervalo", component_property="n_intervals")]
    
    )
def actualizar_dashboard(ticker_seleccionado: str, marco_de_tiempo: str, periodo_descarga: str, n_intervals: int):
    
    """
    Función que actualiza el Dashboard.
    """

    # Obtener título
    titulo = f"Precio en Tiempo Real para {ticker_seleccionado}"
    
    # Obtener descripción de la empresa
    ticker = yf.Ticker(ticker=ticker_seleccionado)
    descripcion = ticker.info.get("longBusinessSummary", "Descripción no disponible")[:500] + "..."
    
    # Obtener Precio y otros datos
    precio = wallstreet.Stock(quote=ticker_seleccionado)
    precio_str = f"{precio.price} {precio.currency}"
    cambio_precio_str = f"{precio.change}"
    cambio_porcentual_str = f"{precio.cp}"
    hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    # Descargar los datos históricos con Yahoo Finance
    df = yf.download(ticker_seleccionado, period=periodo_descarga, interval=marco_de_tiempo, multi_level_index=False, progress=False)
    
    # Validar que hay datos descargados
    if df.empty:
        return titulo, descripcion, hora, precio_str, cambio_precio_str, cambio_porcentual_str, go.Figure()

    # Crear el gráfico de velas con Plotly
    fig = go.Figure(data=[
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"]
            )
        ])
    
    # Agregar una línea horizontal en el precio actual
    precio_actual = precio.price
    fig.add_shape(
        type="line",
        x0=df.index[0],
        y0=precio_actual,
        x1=df.index[-1],
        y1=precio_actual,
        line=dict(color="red", dash="dot")
        )
    
    # Títulos y diseño al gráfico
    fig.update_layout(
        
        title=f"Gráfico de Velas - {ticker_seleccionado}",
        xaxis_title="Fecha",
        yaxis_title="Precio (USD)",
        xaxis_rangeslider_visible=False
        
        )

    return titulo, descripcion, hora, precio_str, cambio_precio_str, cambio_porcentual_str, fig

# Inicializar Servidor
if __name__ == "__main__":
    host="127.0.0.1"
    port="8050"
    app.run(host=host, port=port, debug=True)
    webbrowser.open(url="http://" + host + ":" + port + "/")
