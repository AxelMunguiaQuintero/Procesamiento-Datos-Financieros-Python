# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
from finvizfinance import quote
import emoji # pip install emoji
import json
import matplotlib.pyplot as plt

# Definir el Ticker
ticker = "NVDA"
stock = yf.Ticker(ticker=ticker)

# 1. Obtener Información General de la Empresa
info = stock.info
caracter_categoria = emoji.emojize(":small_blue_diamond:")
print("\n" + caracter_categoria + "Información General de la Empresa:\n")
print(f"Nombre: {info.get('longName', 'N/A')}") 
print(f"Sector: {info.get('sector', 'N/A')}")
print(f"Industria: {info.get('industry', 'N/A')}")
print(f"Capitalización de Mercado: {info.get('marketCap', 'N/A')}")
print(f"Beta: {info.get('beta', 'N/A')}")
print(f"Rendimiento por Dividendo: {info.get('dividendYield', 'N/A')}")
print("Total de Valores devueltos:", len(info))

# 2. Extraer Estado de Resultados (Income Statement)
income_stmt = stock.income_stmt
caracter_categoria = emoji.emojize(":bar_chart:")
print("\n" + caracter_categoria + " Estado de Resultados (Últimos Años):\n")
print(income_stmt)

# Graficar Ingresos Netos
plt.figure(figsize=(22, 6))
income_stmt.loc["Total Revenue"].plot(kind="bar", color="royalblue", alpha=0.7)
plt.title(f"Ingresos Totales por Año ({ticker})")
plt.xlabel("Fecha")
plt.ylabel("Ingresos Totales (USD)")
plt.xticks(rotation=45)
plt.grid()
plt.show()

# 3. Extraer Balance General
balance_sheet = stock.balance_sheet
caracter_categoria = emoji.emojize(":chart_increasing:")
print("\n" + caracter_categoria + " Balance General:\n")
print(balance_sheet)

# Graficar Activos Totales vs Pasivos Totales
balance_sheet.loc[["Total Assets", "Total Liabilities Net Minority Interest"]].T.plot(kind="bar",
                                                                                      figsize=(22, 6))
plt.title("Activos Totales vs Pasivos Totales")
plt.xlabel("Fecha")
plt.ylabel("USD")
plt.xticks(rotation=45)
plt.legend(["Activos Totales", "Pasivos Totales"])
plt.grid()
plt.show()

# 4. Extraer Flujo de Efectivo (Cashflow)
cashflow = stock.cashflow
caracter_categoria = emoji.emojize(":money_bag:")
print("\n" + caracter_categoria + " Flujo de Efectivo:\n")
print(cashflow)

plt.figure(figsize=(22, 6))
cashflow.loc["Operating Cash Flow"].plot(kind="bar", color="green", alpha=0.7)
plt.title(f"Flujo de Efectivo Operativo de {ticker}")
plt.xlabel("Fecha")
plt.ylabel("USD")
plt.xticks(rotation=45)
plt.grid()
plt.show()

# 5. Extraer Fechas de Reportes de Ganancias
earnings_dates = stock.earnings_dates
caracter_categoria = emoji.emojize(":calendar:")
print("\n" + caracter_categoria + " Fechas de Reportes de Ganancias:\n")
print(earnings_dates) 

# 6. Datos Trimestriales
caracter_categoria = emoji.emojize(":chart_decreasing:")
print("\n" + caracter_categoria + " Reportes Trimestrales:\n")

# Estado de Resultados Trimestral
quarterly_income = stock.quarterly_income_stmt
print("\nEstado de Resultados Trimestral:\n")
print(quarterly_income.head())

# Balance Trimestral
quarterly_balance = stock.quarterly_balance_sheet
print("\nBalance General Trimestral:\n")
print(quarterly_balance)

# Flujo de Efectivo Trimestral
quarterly_cashflow = stock.quarterly_cash_flow
print("\nFlujo de Efectivo Trimestral:\n")
print(quarterly_income.head())

# 7. Obtener Historial de Acciones en Circulación
shares = stock.get_shares_full(start="2023-01-01", end="2025-01-01")
caracter_categoria = emoji.emojize(":pushpin:")
print("\n" + caracter_categoria + " Acciones en Circulación en el Tiempo Seleccionado:\n")
print(shares)

plt.figure(figsize=(22, 6))
shares.plot(kind="line", color="purple", marker="o", linestyle="-")
plt.title(f"Acciones en Circulación de {ticker}")
plt.xlabel("Fecha")
plt.ylabel("Número de Acciones")
plt.xticks(rotation=45)
plt.grid()
plt.show()

ultimo_split = stock.splits
print(ultimo_split)

# Información Fundamental con Finviz
stock = quote.finvizfinance(ticker=ticker)
stock_fundament = stock.ticker_fundament()
print(json.dumps(stock_fundament, indent=4))

# Recordatorio:
#   - Los Datos Fundamentales nos permiten evaluar la estabilidad de una empresa, entender su desempeño
#     financiero y prever posibles oportunidades de inversión.
