
from backend.simulacion.red import crear_red
from backend.simulacion.rutas import buscar_ruta

# Crear la red
red = crear_red()

# Buscar una ruta desde I11 hasta I33
print("RUTA ORIGINAL")

resultado = buscar_ruta(
    red,
    "I11",
    "I33"
)

print(resultado)

# Registrar un accidente que bloquea la salida sur de I11
red["I11"]["estado_semaforo"]["incidente"]["sur"] = 3

# Buscar nuevamente la ruta
print("\nRUTA CON ACCIDENTE")

resultado = buscar_ruta(
    red,
    "I11",
    "I33"
)

print(resultado)
