# -*- coding: utf-8 -*-
# Importar librerías
from yahooquery import Ticker # pip install yahooquery
import json

# Definir el ticker de la acción
ticker = "AAPL"

# Crear Instancia
stock = Ticker(symbols=ticker)
print(json.dumps(stock.summary_profile, indent=4))

# Historial de Transacciones de Insiders
insider_transactions = stock.insider_transactions
print(insider_transactions)

# Accionistas Internos (Insider Holders)
insider_holders = stock.insider_holders
print(insider_holders)

# Desglose de Mayores Poseedores (Major Holders Breakdown)
holders_breakdown = stock.major_holders
print(json.dumps(holders_breakdown, indent=4))

# Propiedad Institucional
instituion_ownsership = stock.institution_ownership
print(instituion_ownsership.loc["AAPL"])

# Mayores Fondos Poseedores
fund_holders = stock.fund_ownership
print(fund_holders)

# Obtener Resuen de los Precios de la Acción
print("Precios:\n\n", json.dumps(stock.price, indent=4))

# Recordatorio:
#   - Conocer quiénes son los mayores poseedores de una acción nos permite evaluar la confianza de inversores clave en la empresa.
#   - Detectar cambios en la participación de instituciones y fondos puede anticipar tendencias alcistas o bajistas en el mercado.
