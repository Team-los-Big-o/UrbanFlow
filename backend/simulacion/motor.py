
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
    if (sum(colas.values()) == 0 and not estado_semaforo.get("emergencia", {}).get("activo")):
        estado_semaforo["direccion"] = None
        estado_semaforo["tiempo_verde"] = 0

        return {
            "direccion_verde": None,
            "tiempo_verde": 0,
            "vehiculos_atendidos": 0,
            "colas": colas.copy(),
            "tiempos_espera": tiempos.copy(),
            "vehiculos_emergencia_atendidos": 0,
            "tipo_emergencia": None,
            "direccion_emergencia": None,
            "emergencia_transferida": False,
            "datos_emergencia": None
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
    maximo,
    estado_semaforo.get("emergencia")
)

    # 4. Actualizar contador de luz verde
    if direccion_nueva != direccion_anterior:
        estado_semaforo["direccion"] = direccion_nueva
        estado_semaforo["tiempo_verde"] = 1
    else:
        estado_semaforo["tiempo_verde"] += 1

    
    # 5. Permitir el paso de vehículos
    incidente = estado_semaforo.get("incidente", {}).get(direccion_nueva, 0)

    # Calcular la capacidad disponible
    capacidad_actual = max(0, capacidad - incidente)

    # Verificar si hay un vehículo de emergencia
    emergencia = estado_semaforo.get("emergencia")
    emergencia_atendida = False
    tipo_emergencia = None

    datos_emergencia = None

    if (
        emergencia
        and emergencia.get("activo")
        and emergencia.get("direccion") == direccion_nueva
        and capacidad_actual > 0
    ):
        emergencia_atendida = True
        tipo_emergencia = emergencia.get("tipo")

        # Conservar los datos del recorrido
        datos_emergencia = emergencia.copy()

        estado_semaforo.pop("emergencia", None)

    # La emergencia ocupa una unidad de capacidad
    capacidad_normal = max(
        0,
        capacidad_actual - int(emergencia_atendida)
    )

    # Atender vehículos normales con la capacidad restante
    atendidos = avanzar_vehiculos(
        colas,
        direccion_nueva,
        capacidad_normal
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
        "tiempos_espera": tiempos.copy(),
        "vehiculos_emergencia_atendidos": int(emergencia_atendida),
        "tipo_emergencia": tipo_emergencia,
        "direccion_emergencia": direccion_nueva if emergencia_atendida else None,
        "emergencia_transferida": False,
        "datos_emergencia": datos_emergencia
    }
