# -*- coding: utf-8 -*-
# Importar librerías
import requests
import gradio as gr # pip install gradio
import json

# Convertir 1 Dólar Americano a todas las divisas disponibles
url = "https://open.er-api.com/v6/latest/USD"
response = requests.get(url)
data = response.json()
print(json.dumps(data, indent=4))

# Función para convertir divisas
def convert_currency(from_currency: str, to_currency: str = "USD", amount: float = 1):
    
    """
    Función para obtener tasas de cambio desde la API.
    """
    
    # Realizar Petición
    url = "https://open.er-api.com/v6/latest/"
    response = requests.get(url + from_currency)
    rates = response.json()["rates"]
    # Validar que exista la divisa de conversión
    if to_currency in rates.keys():
        converted_amount = amount * rates[to_currency]
        return f"{amount} {from_currency} = {converted_amount:.5f} {to_currency}"
    
    return "Error al obtener la tasa de cambio."

# Lista de monedas disponibles
currencies = sorted(list(data["rates"].keys()))

# Crear Interfaz en Gradio
iface = gr.Interface(
    
    fn=convert_currency,
    inputs=[
        gr.Dropdown(choices=currencies, label="Moneda de Origen", value="USD"),
        gr.Dropdown(choices=currencies, label="Moneda de Destino", value="EUR"),
        gr.Number(value=1, label="Cantidad")
        ], 
    outputs=gr.Textbox(label="Resultado"),
    title="Conversor de Divisas en Tiempo Real",
    description="Convierte dinero entre distintas monedas utilizando tasas de cambio en vivo"
    
    )

# Ejecutar aplicación
iface.launch(inbrowser=True)

# Recordatorio:
#   - La conversión de divisas permite transformar una moneda a otra según la tasa de cambio, facilitando
#     transacciones internacionales y la diversificación de inversiones en mercados globales en tiempo real.
