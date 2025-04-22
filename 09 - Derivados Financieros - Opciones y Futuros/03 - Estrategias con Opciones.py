# -*- coding: utf-8 -*-
# Importar librerías
import numpy as np
import matplotlib.pyplot as plt

# Función para calcular el payoff de una opción Call
def call_payoff(strike: float, premium: float, stock_prices: np.array):
    
    """
    Calcula la ganancia o pérdida de una opción de Call al vencimiento.
    
    Recordatorio:
        - El payoff del Call es la diferencia entre el precio del activo y el strike, menos 
        la prima pagada.
    """
    
    return np.maximum(stock_prices - strike, 0) - premium

# Función para calcular el payoff de una opción Put
def put_payoff(strike: float, premium: float, stock_prices: np.array):
    
    """
    Calcula la ganancia o pérdida de una opción de Put al vencimiento.
    
    Recordatorio:
        - El payoff del Put es la diferencia entre el strike y el precio del activo,
        menos la prima pagada.
    """
    
    return np.maximum(strike - stock_prices, 0) - premium


# Definir los preios del activo subyacente al vencimiento
stock_prices = np.linspace(start=70, stop=130, num=100)
strike = 100      # Precio de ejercicio/strike
premium_call = 5  # Costo/Prima de la opción Call
premium_put = 5   # Costo/Prima de la opción Put

# Calcular los payoffs individuales para la estrategia de Long Call
call_payoffs = call_payoff(strike=strike, premium=premium_call, stock_prices=stock_prices)

# Puntos de equilibrio del Long Call
breakeven_call = strike + premium_call

# Visualizción del Long Call
plt.figure(figsize=(10, 5))
plt.plot(stock_prices, call_payoffs, label="Long Call", color="blue")
plt.axhline(0, color="black", linestyle="--", linewidth=1.2)
plt.axvline(strike, color="red", linestyle="--", label="Strike Price")
plt.axvline(breakeven_call, color="green", linestyle="--", label="Breakeven")

# Colorear la zona de pérdidas en rojo y la de ganancias en verde
plt.fill_between(x=stock_prices, y1=call_payoffs, y2=0, where=(call_payoffs >= 0), color="green", alpha=0.3)
plt.fill_between(x=stock_prices, y1=call_payoffs, y2=0, where=(call_payoffs < 0), color="red", alpha=0.3)

plt.xlabel("Precio del Activo al Vencimiento")
plt.ylabel("Profit/Loss")
plt.title("Long Call Payoff")
plt.legend()
plt.grid()
plt.show()

# Calcular los payoffs individuales para la estrategia de Long Put
put_payoffs = put_payoff(strike=strike, premium=premium_put, stock_prices=stock_prices)

# Puntos de equilibrio del Long Put
breakeven_put = strike - premium_put

# Visualizción del Long Put
plt.figure(figsize=(10, 5))
plt.plot(stock_prices, put_payoffs, label="Long Put", color="purple")
plt.axhline(0, color="black", linestyle="--", linewidth=1.2)
plt.axvline(strike, color="red", linestyle="--", label="Strike Price")
plt.axvline(breakeven_put, color="green", linestyle="--", label="Breakeven")

# Colorear la zona de pérdidas en rojo y la de ganancias en verde
plt.fill_between(x=stock_prices, y1=put_payoffs, y2=0, where=(put_payoffs >= 0), color="green", alpha=0.3)
plt.fill_between(x=stock_prices, y1=put_payoffs, y2=0, where=(put_payoffs < 0), color="red", alpha=0.3)

plt.xlabel("Precio del Activo al Vencimiento")
plt.ylabel("Profit/Loss")
plt.title("Long Put Payoff")
plt.legend()
plt.grid()
plt.show()

# Recordatorio:
#   - La estrategia Long Call involucra comprar una opción call, esperando que el precio del activo suba por encima
#     del precio de ejercicio más la prima pagada.
#   - La estrategia Long Put involucra comprar una opción put, esperando que el precio del activo caiga por debajo
#     del precio de ejercicio menos la prima pagada.
#   - Em ambas estrategias, el máximo riesgo es la prima pagada por las opciones, mientras que el beneficio potencial
#     es ilimitado para Long Call y limitado para el Long Put.
