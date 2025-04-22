# -*- coding: utf-8 -*-
# Importar librerías
import schedule # pip install schedule
from datetime import datetime, timedelta
import time

# Ejemplo 1: Ejecutar una función cada 5 segundos
def tarea_cada_5_seg():
    print("Ejecutando cada 5 segundos...")
    
schedule.every(interval=5).seconds.do(tarea_cada_5_seg)

# Ejemplo 2: Ejecutar función cada minuto
def tarea_cada_minuto():
    print("Ejecutando cada minuto...")
    
schedule.every(interval=1).minutes.do(tarea_cada_minuto)

# Ejemplo 3: Ejecutar función a una hora específica
def tarea_a_una_hora():
    print("Ejecutando tarea programada cada día...")
    
# Ejecutar 20 segundos después de correr el script
tiempo_ejecucion = (datetime.now() + timedelta(seconds=20)).strftime("%H:%M:%S")
schedule.every().day.at(tiempo_ejecucion).do(tarea_a_una_hora)

# Ejemplo 4: Ejecutar solo los Lunes a las 10:00 a.m.
def tarea_lunes():
    print("Ejecutando solo los Lunes...")
    
schedule.every().monday.at("10:00").do(tarea_lunes)

# Revisar tareas pendientes
print("Tareas ha ejecutar:\n")
for tarea in schedule.get_jobs():
    print(tarea)
    
# Ejecutar continuamente
while True:
    # Ejecutar Tareas
    schedule.run_pending()
    
    # Calcular cuanto tiempo falta para la próxima ejecución
    tiempo_espera = schedule.idle_seconds()
    print("Tiempo de Espera:", tiempo_espera)
    # Dormir solo hasta la próxima tarea
    if (tiempo_espera is not None) and (tiempo_espera > 0):
        time.sleep(tiempo_espera)
        
# Recordatorio:
#   - La librería "schedule" es una herramienta para automatizar tareas repetitivas en Python.
#   - Es importante planificar cuidadosamente las tareas para evitar sobrecargar el sistema o ejecutar tareas innecesarias.
    