
from backend.simulacion.vehiculos import (
    agregar_vehiculos,
    avanzar_vehiculos

)

from backend.simulacion.tiempos import actualizar_tiempos_espera

from backend.simulacion.controlador import actualizar_semaforo


def ejecutar_turno(
    colas,
    llegadas,
    tiempos,
    estado_semaforo,
    capacidad=3,
    minimo=2,
    maximo=5
):

    # 1. Llegada de vehículos
    agregar_vehiculos(colas, llegadas)
    
    # Verificar si hay vehículos en la intersección
    if sum(colas.values()) == 0:
        estado_semaforo["direccion"] = None
        estado_semaforo["tiempo_verde"] = 0

        return {
            "direccion_verde": None,
            "tiempo_verde": 0,
            "vehiculos_atendidos": 0,
            "colas": colas.copy(),
            "tiempos_espera": tiempos.copy()
        }

    # 2. Consultar estado del semáforo
    direccion_anterior = estado_semaforo["direccion"]
    tiempo_anterior = estado_semaforo["tiempo_verde"]

    # 3. Decidir si mantener o cambiar el semáforo
    direccion_nueva = actualizar_semaforo(
        colas,
        direccion_anterior,
        tiempo_anterior,
        tiempos,
        minimo,
        maximo
    )

    # 4. Actualizar contador de luz verde
    if direccion_nueva != direccion_anterior:
        estado_semaforo["direccion"] = direccion_nueva
        estado_semaforo["tiempo_verde"] = 1
    else:
        estado_semaforo["tiempo_verde"] += 1

    # 5. Permitir el paso de vehículos
    atendidos = avanzar_vehiculos(
        colas,
        direccion_nueva,
        capacidad
    )

    # 6. Actualizar tiempos de espera
    actualizar_tiempos_espera(
        tiempos,
        direccion_nueva,
        colas
    )

    return {
        "direccion_verde": direccion_nueva,
        "tiempo_verde": estado_semaforo["tiempo_verde"],
        "vehiculos_atendidos": atendidos,
        "colas": colas.copy(),
        "tiempos_espera": tiempos.copy()
    }
