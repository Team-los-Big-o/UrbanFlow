
from backend.simulacion.red import crear_red
from backend.simulacion.incidentes import crear_incidente, eliminar_incidente
from backend.simulacion.motor import ejecutar_turno

# 1. Crear la red
red = crear_red()

# 2. Seleccionar la intersección I11
interseccion = red["I11"]

# 3. Agregar 10 vehículos hacia el este
interseccion["colas"]["este"] = 10

# 4. Configurar el semáforo en verde hacia el este
interseccion["estado_semaforo"]["direccion"] = "este"
interseccion["estado_semaforo"]["tiempo_verde"] = 1

# 5. Registrar un accidente que reduce un carril
resultado_incidente = crear_incidente(
    red,
    "I11",
    "este",
    reduccion=3
)

print("REGISTRO DEL INCIDENTE")
print(resultado_incidente)
print("Incidentes en el semáforo:", interseccion["estado_semaforo"]["incidente"])

# 6. Ejecutar un turno de simulación
resultado = ejecutar_turno(
    interseccion["colas"],
    {},
    interseccion["tiempos"],
    interseccion["estado_semaforo"],
    capacidad=3
)

print("\nRESULTADO DE LA SIMULACIÓN")
print("Vehículos atendidos:", resultado["vehiculos_atendidos"])
print("Vehículos restantes:", resultado["colas"]["este"])

# 7. Eliminar el accidente
print("\nELIMINACIÓN DEL INCIDENTE")
print(eliminar_incidente(red, "I11", "este"))
