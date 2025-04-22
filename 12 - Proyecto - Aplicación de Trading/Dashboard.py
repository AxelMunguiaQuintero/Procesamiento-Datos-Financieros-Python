# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas_ta as ta
from datetime import datetime
import finvizfinance.screener as screener
from finvizfinance.insider import Insider
import plotly.graph_objects as go
import webbrowser

# Definir Indicadores Técnicos Válidos
indicadores = [
    
    "Media Móvil - 14 Periodos", "Media Móvil - 21 Periodos", "Media Móvil - 50 Periodos", "Media Móvil - 200 Periodos",
    "Bandas de Bollinger - 14 Periodos", "Bandas de Bollinger - 20 Periodos", "Bandas de Bollinger - 50 Periodos"
    
    ]

# Definir Lista de Seguimiento de Activos
activos = ["AAPL", "MSFT", "AMZN", "TSLA", "GOOGL", "META", "WMT", "NVDA", "JNJ", "PYPL", "NFLX", "QCOM", "AMD",
           "EURUSD=X", "GBPUSD=X", "USDJPY=X", "USDCAD=X"]

# Definir Ticker Inicial
ticker = "AAPL"

# Funciones auxiliares
def obtener_escaner():
    
    """
    Obtiene el escáner de los instrumentos más activos y los más volatiles desde Finviz.
    """
    
    # Most Active
    most_active = screener.overview.Overview()
    most_active.set_filter(signal="Most Active")
    most_active = most_active.screener_view(order="Change", ascend=False, limit=40)
    most_active[["Volume", "Market Cap"]] = most_active[["Volume", "Market Cap"]].fillna(0)
    # Mejorar Estructura de Datos
    for col in ["Volume", "Market Cap", "Price", "Change", "P/E"]:
        try:
            most_active[col] = most_active[col].apply(lambda x: round(x, 4 if col in ["Price", "Change", "P/E"] else 0))
        except:
            continue
        
    # Most Volatile
    most_volatile = screener.overview.Overview()
    most_volatile.set_filter(signal="Most Volatile")
    most_volatile = most_volatile.screener_view(order="Change", ascend=False, limit=40)
    most_volatile[["Volume", "Market Cap"]] = most_volatile[["Volume", "Market Cap"]].fillna(0)
    # Mejorar Estructura de Datos
    for col in ["Volume", "Market Cap", "Price", "Change", "P/E"]:
        try:
            most_volatile[col] = most_volatile[col].apply(lambda x: round(x, 4 if col in ["Price", "Change", "P/E"] else 0))
        except:
            continue
    
    return most_active, most_volatile
    

def obtener_info_activo(ticker: str):

    """
    Obtiene la información general de un activo.
    """    

    # Obtener Información
    info = yf.Ticker(ticker).info
    try:
        holders = yf.Ticker(ticker).major_holders
        insiders_prop = round(float(holders.loc["insidersPercentHeld"].iloc[0]) * 100, 3)
        inst_prop = round(float(holders.loc["institutionsPercentHeld"].iloc[0]) * 100, 3)
    except:
        insiders_prop = "N/A"
        inst_prop = "N/A"
        
    return {
        
        "nombre": info.get("longName") or info.get("displayName"),
        "precio_actual": info.get("currentPrice") or info.get("regularMarketPrice"),
        "volumen_promedio": info.get("averageVolume", "N/A"),
        "beta": info.get("beta", "N/A"),
        "estimacion_alta": info.get("targetHighPrice", "N/A"),
        "estimacion_media": info.get("targetMeanPrice", "N/A"),
        "estimacion_baja": info.get("targetLowPrice", "N/A"),
        "recomendacion": info.get("recommendationKey", "N/A"),
        "insiders_prop": insiders_prop,
        "inst_prop": inst_prop
        
        }
    
        
def insider_latest():
    
    """
    Función que obtiene la actividad más reciente de los Insiders.
    """
    
    # Realizar Petición
    insider_trader_latest = Insider(option="latest")
    latest_df = insider_trader_latest.get_insider()[["Ticker", "Transaction", "Date"]]
    
    return latest_df


def precios_recientes(activos: list):
    
    """
    Función que obtiene los datos más recientes para una lista de activos.
    """
    
    # Descargar datos
    valores_activos = yf.download(tickers=activos, period="1d", interval="1m", progress=False,
                                  prepost=True)["Close"].ffill().iloc[-1].apply(lambda x: round(x, 5))
    valores_activos = valores_activos.to_frame(name="Precio").reset_index()
    
    return valores_activos


def grafico_analisis(ticker: str):
    
    """
    Función que obtiene el gráfico de análisis para un instrumento.
    """
    
    # Definir URL
    url = "https://finviz.com/chart.ashx?t={}&ty=c&ta=1&p=d".format(ticker)
    
    return url


def generar_grafico(ticker: str, lista_indicadores: list = []):
    
    """
    Función que genera un gráfico y añade indicadores en el mismo plot.
    """
    
    # Generar Gráfico
    df = yf.download(tickers=ticker, period="2y", interval="1d", progress=False, multi_level_index=False)
    calculos = {}
    # Revisar si hay indicadores
    if lista_indicadores:
        # Iterar en cada uno para determinar los cálculos a realizar
        bb_calculo = False
        for indicador in lista_indicadores:
            if "Media" in indicador:
                length = indicador.split(" ")[3]
                # Ejemplo: "Media Móvil - 14 Periodos" -> ["Media", "Móvil", "-", "14", "Periodos"]
                nombre_indicador = f"SMA_{length}"
                # Realizar Calculo
                calc = ta.sma(close=df["Close"], length=int(length))
                calculos[nombre_indicador] = calc
            elif "Bandas" in indicador:
                if not bb_calculo:
                    length = indicador.split(" ")[4]
                    # Ejemplo: "Bandas de Bollinger - 20 Periodos" -> ["Bandas", "de", "Bollinger", "-", "20", "Periodos"]
                    nombre_indicador = f"BB_{length}"
                    # Realizar Cálculo
                    bb = ta.bbands(close=df["Close"], length=int(length)).iloc[:, [0, 2]] # Banda Inferior y Banda Superior
                    calculos[nombre_indicador] = bb
                    bb_calculo = True
    # Realizar Gráfico de Velas
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name=f"Gráfico de Velas {ticker}"
        )])
    # Agregar Media Móviles y Bandas de Bollinger
    colores_sma = ["red", "green", "blue", "white"]
    contador = 0
    for clave, calculo in calculos.items():
        if "SMA" in clave:
            # Agregar la media móvil
            fig.add_trace(go.Scatter(
                
                x=calculo.index,
                y=calculo,
                mode="lines",
                name=clave.replace("_", " "),
                line=dict(color=colores_sma[contador], width=1.5)
                
                ))
            contador += 1
        elif "BB" in clave:
            # Agregar Bandas de Bollinger
            fig.add_trace(go.Scatter(
                
                x=calculo.index,
                y=calculo.iloc[:, 0],
                mode="lines",
                line=dict(color="purple", width=1),
                showlegend=False
                
                ))
            fig.add_trace(go.Scatter(
                
                x=calculo.index,
                y=calculo.iloc[:, 1],
                mode="lines",
                line=dict(color="purple", width=1),
                showlegend=False,
                fill="tonexty",
                fillcolor="rgba(128, 0, 128, 0.2)"
                
                ))
            
    # Añadir detalles al gráfico
    fig.update_layout(
        
        title=f"Gráfico de {ticker}",
        xaxis_title="Fecha",
        yaxis_title="Precio",
        template="plotly_dark",
        margin=dict(l=25, r=25, t=45, b=25),
        xaxis=dict(rangeslider=dict(visible=False)),
        legend=dict(
            
            x=0.02,
            y=0.98,
            bgcolor="rgba(255, 255, 255, 0.5)",
            bordercolor="black",
            borderwidth=1
            
            )
        )
            
    return fig


# Inicialización de datos
most_active, most_volatile = obtener_escaner()
info_activo = obtener_info_activo(ticker=ticker)
ruta_imagen = grafico_analisis(ticker=ticker)

# Descargar Precios más recientes
valores_activos = precios_recientes(activos=activos)

# Obtener Actividad de Insiders Trading
latest_df = insider_latest()

# Generar Gráfico
indicadores_default = ["Media Móvil - 50 Periodos", "Media Móvil - 200 Periodos",
                       "Bandas de Bollinger - 20 Periodos"]
fig = generar_grafico(ticker=ticker, lista_indicadores=indicadores_default)


# Crear la aplicación Dash
app = dash.Dash(__name__)

# Definir Interfaz
app.layout = html.Div(
    
    # Definir Estilo de Todo el Contenedor
    style={"display": "flex", "flex-direction": "row", "position": "absolute", "left": "0px", "top": "0px",
           "width": "100vw", "height": "100vh", "overflow": "hidden"},
    
    children=[
        
        # Sección 1: Generar Menú del lado izquierdo con opciones de Configuración (22% de la Pantalla)
        html.Div(style={"width": "22vw", "height": "100vh", "background-color": "#e0e0e0", "padding": "5px",
                        "overflow-y": "auto"},
                 children=[
                     # Agregar Título al Menú
                     html.H3(children="Menú de Configuración del Gráfico", style={"text-align": "center", "color": "black"}),
                     
                     # Contenedor con parámetros de configuración y Datos del Activo
                     html.Div(style={"display": "flex", "flexDirection": "column", "alignItems": "center", "width": "100%",
                                     "max-width": "100%", "overflow": "hidden"},
                              
                              children = [
                                  
                                  # Campo de entrada para que el usuario escriba el activo
                                  dcc.Input(id="input-activo", type="text", debounce=True, value=ticker,
                                            placeholder="Escribe el Activo (Ej. AAPL, BTC-USD)...", list="activos-list",
                                            style={"width": "90%", "padding": "10px", "font-size": "14px", "font-weight": "bold",
                                                   "border-radius": "8px", "font-family": "'Poppins', Arial, Helvetica, sans-serif",
                                                   "box-shadow": "0 2px 8px rgba(0, 0, 0, 0.1)"}),
                                  
                                  # Lista de Activos (Es un recordatorio al usuario de como debe de ingresar la información)
                                  html.Datalist(id="activos-list",
                                                children=[html.Option(value=activo) for activo in ["AAPL", "EURUSD=X", "BTC-USD"]]),
                                  
                                  # Instrucciones para agregar Indicadores Técnicos
                                  html.Label(children="Selecciona los Indicadores Técnicos:",
                                             style={"font-size": "20px", "color": "darkblue", "font-weight": "bold",
                                                    "padding-top": "10px", "padding-bottom": "5px"}),
                                  # Dropdown para seleccionar múltiples indicadores (Se agregarán al plot de precios)
                                  dcc.Dropdown(id="dropdown-indicadores", multi=True, value=indicadores_default,
                                               options=[{"label": indicador, "value": indicador} for indicador in indicadores],
                                               style={"width": "97%", "font-size": "14px", "padding": "5px 0px 5px 5px",  
                                                      "font-family": "'Poppins', Arial, Helvetica, sans-serif", 
                                                      "border-radius": "8px", "box-shadow": "0 2px 8px rgba(0, 0, 0, 0.1)"}),
                                  # Botón para actualizar la información
                                  html.Button(children="Actualizar Información", id="boton-actualizar", type="submit",
                                              n_clicks=0,  style={"width": "90%", "padding": "10px", "background-color": "#007BFF", 
                                                                  "color": "white", "font-size": "16px", "border-radius": "8px",
                                                                  "font-family": "'Poppins', Arial, Helvetica, sans-serif",
                                                                  "border": "none", "cursor": "pointer", "margin-top": "20px",
                                                                  "box-shadow": "0 2px 8px rgba(0, 0, 0, 0.1)"}),
                                  # Título de la Tabla con Información General del Activo
                                  html.H4(children="Datos Generales del Activo",
                                          style={"font-size": "20px", "color": "darkblue", "font-weight": "bold", 
                                            "text-align": "center", "margin-top": "10px", "margin-bottom": "5px"}),
                                  # Definir Tabla con Información
                                  html.Div(id="tabla-informacion", 
                                           
                                           children=[
                                               
                                               html.Tr([
                                                   html.Th(t.replace("_", " ").title(),
                                                           style={"padding": "10px", "border": "2px solid black", "max-width": "95%",
                                                                  "background-color": "#f2f2f2", "font-size": "15px"}),
                                                   html.Td(id=t, children=v,
                                                           style={"padding": "10px", "border": "2px solid black", "font-size": "15px",
                                                                  "max-width": "95%", "background-color": "#f2f2f2"})])
                                               
                                               for t, v in info_activo.items()]),
                                  # Mostrar Título del Gráfico de Análisis Visual
                                  html.H4(children="Análisis Visual",
                                          style={"font-size": "20px", "color": "darkblue", "font-weight": "bold", 
                                                 "text-align": "center", "margin-top": "15px", "margin-bottom": "5px"}),
                                  # Desplegar Imagen de Finviz
                                  html.Img(id="img-activo", src=ruta_imagen,
                                           style={"width": "90%", "margin": "5px auto", "border-radius": "10px"})])
                     
                     ]), # ----------> Fin del Menú de Configuración (Sección 1)
        
        # Sección 2: Generar Gráfico del Activo y Escáneres Financieros (55% de la Pantalla)
        html.Div(
            # Definir Estilo del Segundo Contenedor
            style={"width": "55vw", "height": "100vh", "background-color": "#ffffff", "padding": "5px",
                   "display": "flex", "flex-direction": "column", "alignItems": "center", "overflow": "hidden",
                   "overflow-y": "auto"},
            
            children=[
                
                # Agregar Título a Sección Principal
                html.H3(children="Dashboard: Monitoreo e Investigación de Activos",
                        style={"text-align": "center", "font-size": "25px", "margin-top": "10px"}),
                
                # Gráfico de Precios
                html.Div(
                    children=[dcc.Graph(id="grafico", figure=fig, style={"width": "100%", "height": "30vh",
                                                                        "margin-bottom": "10px", "padding": "0px"})],
                    style={"max-width": "95%", "margin": "0 auto", "width": "100%", "overflow": "hidden"}),
                
                # Generar Escáner Financiero (Most Active)
                html.H4(id="titulo-escaner1", children="Escáner Financiero: Most Active (Actualización:" \
                                                       f" {datetime.now().strftime('%H:%M')})",
                        style={"font-size": "20px", "color": "#17a2b8", "text-align": "center", "margin-bottom": "0px",
                               "margin-top":"0px", "padding": "0px"}),
                html.Div(style={"max-width": "95%",  "margin": "0 auto",  "width": "100%", "overflow": "hidden"},
                    children=[
                        
                        dash_table.DataTable(id="escaner-financiero-1", data=most_active.to_dict("records"),
                                             columns=[{"name": i, "id": i} for i in most_active.columns],
                                             page_size=20,
                                             style_table={"overflowX": "auto", "width": "100%", "height": "25vh", 
                                                          "maxWidth": "100%"}, style_cell={"textAlign": "center"},
                                             style_header={"backgroundColor": "#17a2b8", "color": "white",
                                                           "fontWeight": "bold", "textAlign": "center",
                                                           "border": "1px solid white"})
                        ]),
                
                # Agregar un Intervalo de Actualización (Actualizará Escáneres, Tabla de Insiders y Listo de Activos)
                dcc.Interval(id="intervalo-actualizacion", interval=60 * 3 * 1_000, n_intervals=0),
                
                # Generar Escáner Financiero (Most Volatile)
                html.H4(id="titulo-escaner2", children="Escáner Financiero: Most Volatile (Actualización:" \
                                                       f" {datetime.now().strftime('%H:%M')})",
                        style={"font-size": "20px", "color": "#17a2b8", "text-align": "center", "margin-bottom": "0px", 
                               "margin-top":"0px", "padding": "0px"}),
                html.Div(style={"max-width": "95%", "margin": "0 auto", "width": "100%", "overflow": "hidden"},
                    children=[
                        
                        dash_table.DataTable(id="escaner-financiero-2", data=most_volatile.to_dict("records"),
                                             columns=[{"name": i, "id": i} for i in most_volatile.columns],
                                             page_size=20,
                                             style_table={"overflowX": "auto", "width": "100%", "height": "25vh", 
                                                          "maxWidth": "100%"}, style_cell={"textAlign": "center"},
                                             style_header={"backgroundColor": "#17a2b8", "color": "white", 
                                                           "fontWeight": "bold", "textAlign": "center", 
                                                           "border": "1px solid white"})
                        
                        ])
                
                ]), # ----------> Fin del Monitoreo de Activos (Sección 2)
        
        # Sección 3: Lista de Seguimiento de Activos y Actividad más reciente de Insiders (23% de Pantalla)
        html.Div(style={"width": "23vw", "height": "100vh", "background-color": "#e0e0e0", "padding": "5px",
               "overflow": "hidden", "overflow-y": "auto"},
                 
                 children=[
                     
                     # Agregar Título
                     html.H3(children="Lista de Seguimiento", style={"text-align": "center", "color": "black"}),
                     
                     # Generar Tabla con Precios para la lista de Seguimiento
                     html.Div(
                         children=[
                             
                             dash_table.DataTable(id="lista-seguimiento", data=valores_activos.to_dict("records"),
                                                  columns=[{"name": col, "id": col} for col in valores_activos.columns],
                                                  style_table={"width": "90%", "margin": "auto", "overflow": "hidden"},
                                                  style_header={"backgroundColor": "#007BFF", "color": "white", "fontWeight": "bold",
                                                                "textAlign": "center", "border": "1px solid white"},
                                                  style_cell={"textAlign": "center", "border": "1px solid #ddd", "fontSize": "16px"},
                                                  style_data_conditional=[{"if": {"row_index": "odd"},"backgroundColor": "#f9f9f9"},
                                                                          {"if": {"row_index": "even"}, "backgroundColor": "#ffffff"}])
                             
                             ]
                         ),
                     
                     # Desplegar Información de los Insiders
                     html.H4(children="Actividad de Insiders", style={"font-size": "20px", "color": "#333", "text-align": "center", 
                                                       "margin-bottom": "0px"}),
                     html.Div(
                         children=[
                             
                             dash_table.DataTable(id="insiders", data=latest_df.to_dict("records"),
                                                  columns=[{"name": col, "id": col} for col in latest_df.columns],
                                                  page_size=8, style_table={"width": "90%", "margin": "auto", "overflow": "hidden"},
                                                  style_header={"backgroundColor": "#007BFF", "color": "white", "fontWeight": "bold",
                                                                "textAlign": "center", "border": "1px solid white"},
                                                  style_cell={"textAlign": "center", "border": "1px solid #ddd", "fontSize": "16px"},
                                                  style_data_conditional=[{"if": {"row_index": "odd"}, "backgroundColor": "#f1faff"},
                                                                          {"if": {"row_index": "even"}, "backgroundColor": "#ffffff"}])
                             
                             ]
                         )
                     
                     ]), # ----------> Fin de la Sección No. 3
                     
        ]
    )


# Callback para actualizar los escáneres, la lista de seguimiento y la tabla de insiders cada 3 minutos
@app.callback(
    
    [
     Output(component_id="escaner-financiero-1", component_property="data"),
     Output(component_id="titulo-escaner1", component_property="children"),
     Output(component_id="escaner-financiero-2", component_property="data"),
     Output(component_id="titulo-escaner2", component_property="children"),
     Output(component_id="insiders", component_property="data"),
     Output(component_id="lista-seguimiento", component_property="data")
     ],
    [
     Input(component_id="intervalo-actualizacion", component_property="n_intervals")
     ]

    )
def actualizar_info(n_intervals: int):
    
    """
    Callback para actualizar escáneres y la tabla de insiders.
    """
    
    # Evitar actualizar tan pronto se corre el script
    if n_intervals == 0:
        raise dash.exceptions.PreventUpdate
        
    # Escáneres
    most_active, most_volatile = obtener_escaner()
    titulo1 = f"Escáner Financiero: Most Active (Actualización: {datetime.now().strftime('%H:%M')})"
    titulo2 = f"Escáner Financiero: Most Volatile (Actualización: {datetime.now().strftime('%H:%M')})"
    # Tabla de Insiders
    latest_df = insider_latest()
    # Precios más recientes
    valores_activos = precios_recientes(activos=activos)
    
    return (most_active.to_dict("records"), titulo1, most_volatile.to_dict("records"), titulo2,
            latest_df.to_dict("records"), valores_activos.to_dict("records"))

# Callback para actualizar la información general del activo, el gráfico y la imagen
@app.callback(
    [
     Output(component_id="tabla-informacion", component_property="children"),
     Output(component_id="grafico", component_property="figure"),
     Output(component_id="img-activo", component_property="src")
     ],
    [
     Input(component_id="boton-actualizar", component_property="n_clicks"),
     Input(component_id="input-activo", component_property="value"),
     Input(component_id="dropdown-indicadores", component_property="value")
     ]
    )
def actualizar_informacion(n_clicks: int, ticker: str, lista_indicadores: list):
    
    """
    Callback para actualizar la información general, el gráfico y la imagen.
    """
    
    # Evitar actualizaciones no deseadas
    if (n_clicks is None) or (n_clicks == 0):
        raise dash.exceptions.PreventUpdate
        
    # Generar Gráfico
    fig = generar_grafico(ticker=ticker, lista_indicadores=lista_indicadores)
    # Obtener Gráfico de Análisis
    ruta = grafico_analisis(ticker)
    # Información General del Activo
    info_activo = obtener_info_activo(ticker)
    
    # Actualizar Tabla
    tabla_actualizada = [
        
        html.Tr([
            html.Th(t.replace("_", " ").title(),
                    style={"padding": "10px", "border": "2px solid black", "max-width": "95%",
                           "background-color": "#f2f2f2", "font-size": "15px"}),
            html.Td(id=t, children=v,
                    style={"padding": "10px", "border": "2px solid black", "font-size": "15px",
                           "max-width": "95%", "background-color": "#f2f2f2"})])
        
        for t, v in info_activo.items()]
    
    return tabla_actualizada, fig, ruta
    

# Ejecutar Aplicación
if __name__ == "__main__":
    app.run(port="8050", debug=False)
    webbrowser.open(url="http://127.0.0.1:8050/")
