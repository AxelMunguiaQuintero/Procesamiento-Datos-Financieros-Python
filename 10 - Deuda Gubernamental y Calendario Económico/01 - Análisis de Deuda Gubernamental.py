# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fredapi import Fred # pip install fredapi

# Inicializar conexión con FRED
API_KEY = "API_TOKEN"
fred = Fred(api_key=API_KEY)

# Deuda Total del Gobierno de EE.UU (GFDEBTN)
deuda_total = fred.get_series("GFDEBTN", observation_start="01/01/2015", observation_end="01/01/2025")

# Deuda como Porcentaje del PIB (GFDEGDQ188S)
deuda_pib = fred.get_series(series_id="GFDEGDQ188S", observation_start="01/01/2015", observation_end="01/01/2025")

# Rendimientos de Bonos del Tesoro de EE.UU:
    
# Bonos a 2 años: Reflejan las expectativas a corto plazo
rendimiento_2y = fred.get_series("DGS2", observation_start="01/01/2015", observation_end="01/01/2025")
# Bonos a 10 años: Se utilizan para ver las expectativas de crecimiento y de inflación
rendimiento_10y = fred.get_series("DGS10", observation_start="01/01/2015", observation_end="01/01/2025")
# Bonos a 30 años: Muestran las expectativas a largo plazo
rendimiento_30y = fred.get_series("DGS30", observation_start="01/01/2015", observation_end="01/01/2025")
# Índice S&P 500
sp500 = fred.get_series(series_id="SP500", observation_start="01/01/2015", observation_end="01/01/2025")

# Agrupar Información
df = pd.DataFrame({
    
    "Deuda_Total": deuda_total,
    "Deuda_PIB": deuda_pib,
    "Rendimiento_2Y": rendimiento_2y,
    "Rendimiento_10Y": rendimiento_10y,
    "Rendimiento_30Y": rendimiento_30y,
    "SP500": sp500
    
    }).dropna()
print(df)

# Crear subplots (3 filas y 2 columnas)
fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(22, 10))

colores = ["blue", "green", "red", "orange", "purple", "black"]
# Iterar sobre las columnas y graficar
for i, (col, ax) in enumerate(zip(df.columns, axs.ravel())):
    ax.plot(df.index, df[col], color=colores[i])
    ax.set_title(col)
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Valor")
    ax.grid()
    
plt.tight_layout(pad=3.0)
plt.show()

# Calcular Spread entre los rendimientos de los bonos a 10 años y 2 años
df["Spread_10Y_2Y"] = df["Rendimiento_10Y"] - df["Rendimiento_2Y"]

# Generar Plot
plt.figure(figsize=(22, 8))

# Gráfico 1: Deuda total del gobierno a lo largo del tiempo
plt.subplot(2, 1, 1)
plt.plot(df["Deuda_Total"], label="Deuda Total (Trillones USD)", color="blue")
plt.title("Evolucion de la Deuda Total del Gobierno de EE.UU.")
plt.xlabel("Año")
plt.ylabel("Deuda (USD)")
plt.legend()
plt.grid()

# Gráfico 2: Spread de la Curva de Rendimientos
plt.subplot(2, 1, 2)
plt.plot(df["Spread_10Y_2Y"], label="Spread 10Y - 2Y", color="red")
plt.axhline(0, linestyle="--", color="black", alpha=0.7)
plt.title("Curva de Rendimientos (Spread 10Y - 2Y)")
plt.xlabel("Año")
plt.ylabel("Diferencia (%)")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()

# Calcular Matriz de Correlación
correlation_matrix = df.corr()
# Graficar
plt.figure(figsize=(14, 14))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Matriz de Correlación entre Variables")
plt.show()

# Indicador de Recesión (True si el spread es negativo)
df["Recesión"] = df["Spread_10Y_2Y"] < 0

# Filtramos los periodos en los que la curva estuvo invertida
recesiones = df[df["Recesión"]]

# Generar Plot
plt.plot(df["Spread_10Y_2Y"], label="Spread 10Y - 2Y", color="red")
plt.scatter(recesiones.index, recesiones["Spread_10Y_2Y"], color="black", label="Posibles Recisiones", marker="o")
plt.axhline(0, linestyle="--", color="black", alpha=0.7)
plt.legend()
plt.title("Inversión de la Curva de Rendimientos (Posibles Recesiones)")
plt.xlabel("Año")
plt.ylabel("Diferencial (%)")
plt.grid()
plt.show()

# Recordatorio:
#   - El análisis del diferencial entre los rendimientos de los bonos a 10 y 2 años es fundamental para evaluar
#     las expectativs económicas. Un spread negativo, que indica una inversión en la curva de rendimientos, históricamente
#     precede a recesiones económicas, señalando posibles dificultades en el crecimiento.
