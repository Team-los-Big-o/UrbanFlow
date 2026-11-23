
from backend.simulacion.red import crear_red, ejecutar_red
from backend.simulacion.emergencias import registrar_emergencia

# Crear la red
red = crear_red()

# Registrar una ambulancia en I11 que avanza hacia el este
print("REGISTRO DE EMERGENCIA")
print(registrar_emergencia(
    red,
    "I11",
    "este",
    "ambulancia"
))

# Ejecutar el primer turno
print("\nPRIMER TURNO")
resultados = ejecutar_red(red, {})

print("Emergencias atendidas en I11:",
      resultados["I11"]["vehiculos_emergencia_atendidos"])

print("Emergencia transferida:",
      resultados["I11"]["emergencia_transferida"])

# Consultar si llegó a I12
print("\nESTADO DE I12")
print(red["I12"]["estado_semaforo"].get("emergencia"))

# Ejecutar el segundo turno
print("\nSEGUNDO TURNO")
resultados = ejecutar_red(red, {})

print("Emergencias atendidas en I12:",
      resultados["I12"]["vehiculos_emergencia_atendidos"])

print("Emergencia transferida:",
      resultados["I12"]["emergencia_transferida"])

# Consultar si salió de la red
print("\nESTADO DE I13")
print(red["I13"]["estado_semaforo"].get("emergencia"))
