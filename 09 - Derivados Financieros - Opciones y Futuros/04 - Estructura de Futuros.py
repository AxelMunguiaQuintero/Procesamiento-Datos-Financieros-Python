# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta # pip install python-dateutil

# Futuros en Yahoo Finance
futuros = {
    
    "Materias Primas": [
        
        "GC=F",  # Oro
        "SI=F",  # Plata
        "PL=F",  # Platino
        "PA=F",  # Paladio
        "CL=F",  # Petróleo Crudo WTI
        "BZ=F",  # Petróleo Crudo Brent
        "NG=F",  # Gas Natural
        "HO=F",  # Combustible de calefacción
        "RB=F",  # Gasolina
        "HG=F"   # Cobre
        
    ],
    
    "Índices Bursátiles": [
        
        "ES=F",  # S&P 500
        "NQ=F",  # Nasdaq 100
        "YM=F",  # Dow Jones
        "RTY=F"  # Russell 2000
        
    ],
    
    "Divisas": [
        
        "6E=F",  # Euro/Dólar (EUR/USD)
        "6B=F",  # Libra/Dólar (GBP/USD)
        "6J=F",  # Yen Japonés/Dólar (JPY/USD)
        "6C=F",  # Dólar Canadiense/USD
        "6A=F",  # Dólar Australiano/USD
        "6N=F",  # Dólar Neozelandés/USD
        "6S=F"   # Franco Suizo/USD
        
    ],
    
    "Bonos": [
        
        "ZB=F",  # Bonos del Tesoro a 30 años
        "ZN=F",  # Bonos del Tesoro a 10 años
        "ZF=F",  # Bonos del Tesoro a 5 años
        "ZT=F"   # Bonos del Tesoro a 2 años
        
    ], 
    
    "Agrícolas": [
        
        "ZC=F",  # Maíz
        "ZW=F",  # Trigo
        "ZS=F",  # Soya
        "ZL=F",  # Aceite de Soya
        "KC=F",  # Café
        "CT=F",  # Algodón
        "CC=F",  # Cacao
        "OJ=F"   # Jugo de Naranja
        
    ] 
}

# Descargar datos históricos
datos_futuros = {}
for categoria, tickers in futuros.items():
    print(f"\n{categoria}:")
    for ticker in tickers:
        df = yf.download(ticker, period="2y", interval="1d")
        datos_futuros[ticker] = df

# Mostrar Datos del Petróleo
print("\nDatos del Petróleo (Futuros):\n\n", datos_futuros["CL=F"])

# Definir Clase de Ticker
gold_future = yf.Ticker(ticker="GC=F")
gold_future_data = gold_future.history(period="max", interval="1d")
print(gold_future_data)

# Obtener datos de los contratos de futuros para los meses del año (meses restantes) - Petróleo (CL)
hoy = datetime.now()

# Lista de códigos de meses en futuros (Enero - Diciembre)
codigos_meses = ["F", "G", "H", "J", "K", "M", "N", "Q", "U", "V", "X", "Z"]

# Generar Tickers de los contratos (Petróleo) para los 3 siguientes meses del actual
codigo_base = "CL"
contratos_futuros_petroleo = []
for i in range(1, 4, 1):
    mes_siguiente = hoy + relativedelta(months=i)
    # Definir nombre del ticker
    ticker_contrato = codigo_base + codigos_meses[mes_siguiente.month - 1] + str(mes_siguiente.year)[-2:] + ".NYM"
    contratos_futuros_petroleo.append(ticker_contrato)
print(contratos_futuros_petroleo)

# Descargar datos
datos_futuros_petroleo = yf.download(tickers=contratos_futuros_petroleo, period="2y", interval="1d")
print(datos_futuros_petroleo)

# Lista de códigos de meses en futuros (Enero - Diciembre)
codigos_meses_bonos = ["H", "M", "U", "Z"] # Mar, Jun, Sep, Dic

# Generar Ticker del Contrato (Bonos) para el próximo vencimiento
codigo_base_bonos = "ZN"
condicion = hoy.month >= np.array([3, 6, 9, 12])
if not any(condicion):
    index = 0
    fecha_referencia = hoy
else:
    index = np.sum(condicion)
    # Validar respuesta
    if index != 4: # Todavía hay vencimientos restantes en este año
        index = index
        fecha_referencia = hoy
    else:
        index = 0
        fecha_referencia = hoy + relativedelta(years=1)
        
# Contrato Siguiente
contrato_bonos_proximo = codigo_base_bonos + codigos_meses_bonos[index] + str(fecha_referencia.year)[-2:] + ".CBT"

print("Ticker Siguiente Contrato:", contrato_bonos_proximo)

# Divisas: Contratos Trimestrales. Ejemplo de Estructura con Contrato Euro/Dólar (6EH27.CME)
# Ejemplo: 6E (Euro/Dólar) es un contrato de futuros mensual en el mercado CME.
# El formato del ticker es: [Código Activo] + [Código del Mes] + [Año] + .CME (Por ejemplo: "6EH27.CME")

# Materias Primas: Contratos Mensuales. Ejemplo de Estructura con Contrato de Petróleo Crudo WTI (CLF27.NYM)
# Ejemplo: CL (Petróleo Crudo WTI) es un contrato de futuros mensual en el mercado NYMEX.
# El formato del ticker es: [Código Activo] + [Código del Mes] + [Año] + .NYM (Por ejemplo: "CLF27.NYM")

# Índices Bursátiles: Contratos Trimestrales. Ejemplo de Estructura con Contrato S&P 500 (ESH27.CME)
# Ejemplo: ES (S&P 500) es un contrato de futuros mensual en el mercado CME.
# El formato del ticker es: [Código Activo] + [Código del Mes] + [Año] + .CME (Por ejemplo: "ESH27.CME")

# Bonos: Contratos Trimestrales. Ejemplo de Estructura con Contrato Bonos del Tesoro a 10 años (ZNM27.CBT)
# Ejemplo: ZN (Bonos del Tesoro a 10 años) es un contrato de futuros trimestral en el mercado CBOT.
# El formato del ticker es: [Código Activo] + [Código del Mes] + [Año] + .CBT (Por ejemplo: "ZNM27.CBT")

# Agrícolas: Contratos Variables. Ejemplo de Estructura con Contrato de Maíz (ZCF27.CBT). Contrato de Café (KCH27.NYB)
# Ejemplo: ZC (Maíz) es un contrato de futuros mensual en el mercado CME.
# El formato del ticker es: [Código Activo] + [Código del Mes] + [Año] + .CBT (Por ejemplo: "ZCF27.CBT")

# Recordatorio:
#   - Los Futuros son contratos financieros que obligan a comprar o vender a un precio determinado en una fecha
#     futura. Se utilizan para especular sobre la dirección de los precios o para cubrir riesgos, como fluctuaciones de precios
#     en commodities, divisas, o índices.
