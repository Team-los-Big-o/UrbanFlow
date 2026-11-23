
from backend.simulacion.motor import ejecutar_turno

colas = {
    "norte": 12,
    "sur": 5,
    "este": 18,
    "oeste": 7
}

tiempos = {
    "norte": 0,
    "sur": 0,
    "este": 0,
    "oeste": 0
}

estado_semaforo = {
    "direccion": None,
    "tiempo_verde": 0
}

llegadas = {
    "norte": 2,
    "sur": 1,
    "este": 3,
    "oeste": 1
}

for turno in range(1, 16):

    resultado = ejecutar_turno(
        colas,
        llegadas,
        tiempos,
        estado_semaforo,
        capacidad=3,
        minimo=2,
        maximo=5
    )

    print(f"\n========== TURNO {turno} ==========")

    print("Semáforo en verde:",
          resultado["direccion_verde"].upper())

    print("Duración de luz verde:",
          resultado["tiempo_verde"], "turnos")

    print("Vehículos atendidos:",
          resultado["vehiculos_atendidos"])

    print("Colas:", resultado["colas"])

    print("Tiempos de espera:",
          resultado["tiempos_espera"])
