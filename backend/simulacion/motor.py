
from backend.algoritmos.semaforos import seleccionar_semaforo
from backend.simulacion.vehiculos import (
    agregar_vehiculos,
    avanzar_vehiculos
)


def ejecutar_turno(colas, llegadas, capacidad=3):
    """
    Ejecuta un turno completo de simulación.
    """

    # 1. Llegan nuevos vehículos
    agregar_vehiculos(colas, llegadas)

    # 2. Seleccionar dirección para luz verde
    direccion_verde = seleccionar_semaforo(colas)

    # 3. Permitir el paso de vehículos
    atendidos = avanzar_vehiculos(
        colas,
        direccion_verde,
        capacidad
    )

    # 4. Devolver los resultados del turno
    return {
        "direccion_verde": direccion_verde,
        "vehiculos_atendidos": atendidos,
        "colas": colas.copy()
    }
