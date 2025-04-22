# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import matplotlib.pyplot as plt

# Definir Ticker
ticker = "JNJ" # Johnson & Johnson

# Definir Instancia
stock = yf.Ticker(ticker=ticker)

# Obtener el código ISIN (International Securities Identification Number)
identificador_internacional = stock.get_isin()
print("Identificador Internacional:", identificador_internacional)

# Obtener Dividendos Históricos
dividendos = stock.get_dividends()
dividendos = dividendos.reset_index()
print("Dividendos:\n\n", dividendos)

# Obtener el promedio de tiempo que toma JNJ para pagar un nuevo dividendo
dias_frecuencia = (dividendos["Date"] - dividendos["Date"].shift(periods=1)).mean().days
print(f"La empresa {ticker} paga un dividendo cada {dias_frecuencia} días")

# Obtener Splits
splits = stock.get_splits()
print(splits)

# Datos Históricos junto con los Dividendos y Splits
df = stock.history(period="max", interval="1d")
print("Datos Completos:\n\n", df)

# Calcular el porcentaje del dividendo con respecto al precio de la acción cuando fue emitido
df_dividendos = df[df["Dividends"] != 0].copy()
print(df_dividendos)

df_dividendos["Dividend_Perc"] = (df_dividendos["Dividends"] / df_dividendos["Close"]) * 100

# Graficar Dividendos y el porcentaje en relación al precio
fig, axes = plt.subplots(ncols=2, nrows=1, figsize=(22, 6), dpi=100)

# Graficar los dividendos distribuidos en relación al precio
axes[0].plot(df_dividendos["Dividends"], marker="o", color="g", label="Dividendos")
axes[0].set_title(f"Dividendos Pagados a lo largo del Tiempo ({ticker})")
axes[0].set_xlabel("Fecha")
axes[0].set_ylabel("Monto del Dividendo")
axes[0].grid()
axes[0].legend()

# Graficar el porcentaje de dividendo en relación al precio de la acción
axes[1].plot(df_dividendos["Dividend_Perc"], marker="o", color="b", label="Porcentaje de Dividendo")
axes[1].set_title(f"Porcentaje de Dividendo sobre el Precio de la Acción ({ticker})")
axes[1].set_xlabel("Fecha")
axes[1].set_ylabel("Porcentaje de Dividendo (%)")
axes[1].grid()
axes[1].legend()

plt.tight_layout()
plt.show()

# Mostrar Precio 10 días antes y después de un split
fechas_split = df[df["Stock Splits"] != 0].index
# Obtener Datos en Rangos de Fechas
rangos = []
for fecha_split in fechas_split: 
    # Recuperar Fechas
    fechas_10_antes = df.loc[:fecha_split].index[-11:].tolist()
    fechas_10_despues = df.loc[fecha_split:].index[1:11].tolist()
    todas_fechas = fechas_10_antes + fechas_10_despues
    rangos.append(df.loc[todas_fechas]["Close"])

# Graficar Precios para cada Split en Subplots
ncols = 3
nrows = divmod(len(rangos), ncols)
nrows = nrows[0] + 1 if nrows[1] > 0 else nrows[0]

# Generar Plots
fig, axes = plt.subplots(ncols=ncols, nrows=nrows, figsize=(22, 12), dpi=300)

# Iterar en cada subplot
for n, ax in enumerate(axes.flatten()):
    # Graficar solo la cantidad exacta de datos que tenemos
    if n < len(rangos):
        ax.plot(rangos[n])
        # Marcar el punto cuando sucedió el split
        ax.plot(rangos[n].index[10], rangos[n].iloc[10], color="red", marker="o")
        ax.set_title(f"Split para la fecha: {fechas_split[n]}")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Precio ($)")
        
plt.tight_layout()
plt.show()

# Obtener el Calendario de Eventos
calendario = stock.calendar
print("Calendario de Eventos:\n")
for clave, valor in calendario.items():
    print(f"Evento: {clave} - {valor}")

# Recordatorio:
#   - Un Dividendo es una parte de las ganancias de una empresa distribuida a sus accionistas como recompensa
#     por su inversión, generalmente pagado en efectivo o acciones, de forma periódica.
#   - Un split es una acción corporativa en la que una empresa divide sus acciones en una proporción determinada
#     reduciendo el precio por acción, pero sin cambiar el valor total de la inversión del accionista.
