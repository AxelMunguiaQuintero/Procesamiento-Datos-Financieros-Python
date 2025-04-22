# -*- coding: utf-8 -*-
# Importar librerías
import wallstreet # pip install wallstreet
import threading
import time

# Definir Parámetros
ticker = "AAPL"
stock = wallstreet.Stock(quote=ticker)

# Mostrar Precio en Tiempo Real
print(f"Precio en Tiempo Real de {stock.name}: {stock.price} en {stock.currency}")

# Obtener el cambio porcentual y el cambio en el precio desde que abrió el mercado
print(f"Cambio Porcentual desde que abrió el mercado de {stock.name}: {stock.cp:.2f}%")
print(f"Cambio en el Precio desde que abrió el mercado de {stock.name}: {stock.change:.2f}")

# Calcular el Precio de Cierre de un día anterior
precio_anterior = stock.price - stock.change
print(f"Precio de Cierre para {stock.name} el día de ayer fue: {precio_anterior:.2f}")

# Obtener y desplegar precios en segundo plano (Se mostrarán en la consola)
detenerse = False
def Obtener_Precio(tickers: list, n_segundos: float):
    
    """
    Esta función obtiene el precio en tiempo real cada n_segundos para los activos que se pasaron
    dentro de la variable de tickers.
    """
    
    while True:
        # Obtener Precios
        for ticker in tickers:
            ticker_precio = wallstreet.Stock(quote=ticker)
            print(f"Precio en Tiempo Real de {ticker_precio.name}: {ticker_precio.price} en {ticker_precio.currency}. Cambio: {ticker_precio.change}")
            
        # Revisar si se tiene que continuar
        if detenerse:
            break
        # Dormir
        time.sleep(n_segundos)
        
# Ejecutar en segundo plano
tickers = ["AMZN", "TSLA", "MSFT"]
hilo = threading.Thread(target=Obtener_Precio, args=(tickers, 10))
hilo.start()

# Cancelar Actualización de Precios
detenerse = True

# Recordatorio:
#   - El módulo de wallstreet nos permite obtener datos en tiempo real para una gran variedad de activos financieros.
#   - El módulo de threading nos permite ejecutar de manera simultánea múltiples tareas.
