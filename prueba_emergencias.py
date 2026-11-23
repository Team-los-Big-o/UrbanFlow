
from backend.simulacion.red import crear_red
from backend.simulacion.emergencias import (
    registrar_emergencia,
    eliminar_emergencia
)
from backend.simulacion.motor import ejecutar_turno

# Crear la red
red = crear_red()
interseccion = red["I11"]

# Agregar vehículos normales al norte
interseccion["colas"]["norte"] = 5

# Configurar el semáforo actual
interseccion["estado_semaforo"]["direccion"] = "norte"
interseccion["estado_semaforo"]["tiempo_verde"] = 3

# Registrar una ambulancia que necesita avanzar al este
print(registrar_emergencia(
    red,
    "I11",
    "este",
    "ambulancia"
))

# Ejecutar un turno
resultado = ejecutar_turno(
    interseccion["colas"],
    {},
    interseccion["tiempos"],
    interseccion["estado_semaforo"],
    capacidad=3
)

print("\nRESULTADO")
print("Semáforo en verde:", resultado["direccion_verde"])
print("Vehículos atendidos:", resultado["vehiculos_atendidos"])
print("Vehículos de emergencia atendidos:", resultado["vehiculos_emergencia_atendidos"])
print("Tipo de emergencia:", resultado["tipo_emergencia"])
print("Colas:", resultado["colas"])

# Eliminar la emergencia
print("\n", eliminar_emergencia(red, "I11"))


