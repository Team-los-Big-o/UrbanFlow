
from time import perf_counter

from backend.simulacion.vehiculos import (
    agregar_vehiculos,
    avanzar_vehiculos
)

from backend.simulacion.tiempos import actualizar_tiempos_espera
from backend.simulacion.controlador import actualizar_semaforo


DIRECCIONES = ["norte", "sur", "este", "oeste"]


def generar_llegadas():
    patrones = {
        "norte": [5, 0, 3, 1, 4, 0, 2, 6, 0, 3, 1, 4],
        "sur":   [0, 4, 1, 5, 0, 3, 2, 0, 6, 1, 4, 0],
        "este":  [2, 1, 0, 4, 3, 2, 0, 5, 1, 0, 4, 2],
        "oeste": [1, 3, 5, 0, 2, 4, 1, 0, 3, 5, 0, 2]
    }

    llegadas = []

    for turno in range(24):
        indice = turno % 12

        llegadas.append({
            direccion: patrones[direccion][indice]
            for direccion in DIRECCIONES
        })

    return llegadas


def simular_algoritmo(
    nombre,
    llegadas,
    capacidad=3,
    duracion_fija=3,
    minimo=2,
    maximo=5
):
    colas = {direccion: 0 for direccion in DIRECCIONES}
    tiempos = {direccion: 0 for direccion in DIRECCIONES}

    direccion_actual = None
    tiempo_verde = 0

    vehiculos_atendidos = 0
    vehiculos_llegaron = 0
    cola_maxima = 0

    suma_esperas = 0
    muestras_espera = 0

    inicio = perf_counter()

    for turno, nuevas_llegadas in enumerate(llegadas, start=1):

        # Incorporar nuevas llegadas
        agregar_vehiculos(colas, nuevas_llegadas)

        vehiculos_llegaron += sum(nuevas_llegadas.values())

        # Seleccionar el semáforo
        if nombre == "fijo":

            fase = ((turno - 1) // duracion_fija) % len(DIRECCIONES)
            direccion_nueva = DIRECCIONES[fase]

        else:

            direccion_nueva = actualizar_semaforo(
                colas,
                direccion_actual,
                tiempo_verde,
                tiempos,
                minimo,
                maximo
            )

        # Actualizar duración de la luz verde
        if direccion_nueva != direccion_actual:
            direccion_actual = direccion_nueva
            tiempo_verde = 1
        else:
            tiempo_verde += 1

        # Atender vehículos
        atendidos = avanzar_vehiculos(
            colas,
            direccion_actual,
            capacidad
        )

        vehiculos_atendidos += atendidos

        # Actualizar tiempos de espera
        actualizar_tiempos_espera(
            tiempos,
            direccion_actual,
            colas
        )

        # Registrar espera de las direcciones con vehículos
        for direccion in DIRECCIONES:

            if colas[direccion] > 0:
                suma_esperas += tiempos[direccion]
                muestras_espera += 1

        # Registrar cola máxima
        total_cola = sum(colas.values())

        cola_maxima = max(
            cola_maxima,
            total_cola
        )

    tiempo_ejecucion = (perf_counter() - inicio) * 1000

    espera_promedio = (
        suma_esperas / muestras_espera
        if muestras_espera > 0 else 0
    )

    return {
        "algoritmo": nombre,
        "turnos": len(llegadas),
        "vehiculos_llegaron": vehiculos_llegaron,
        "vehiculos_atendidos": vehiculos_atendidos,
        "vehiculos_pendientes": sum(colas.values()),
        "tiempo_espera_promedio": round(espera_promedio, 2),
        "cola_maxima": cola_maxima,
        "tiempo_ejecucion_ms": round(tiempo_ejecucion, 4)
    }


def comparar_algoritmos():

    llegadas = generar_llegadas()

    resultado_fijo = simular_algoritmo(
        "fijo",
        llegadas
    )

    resultado_adaptativo = simular_algoritmo(
        "adaptativo",
        llegadas
    )

    # Calcular mejoras porcentuales
    espera_fija = resultado_fijo["tiempo_espera_promedio"]
    espera_adaptativa = resultado_adaptativo["tiempo_espera_promedio"]

    cola_fija = resultado_fijo["cola_maxima"]
    cola_adaptativa = resultado_adaptativo["cola_maxima"]

    if espera_fija > 0:
        mejora_espera = (
            (espera_fija - espera_adaptativa) / espera_fija
        ) * 100
    else:
        mejora_espera = 0

    if cola_fija > 0:
        mejora_cola = (
            (cola_fija - cola_adaptativa) / cola_fija
        ) * 100
    else:
        mejora_cola = 0

    return {
        "condiciones": {
            "turnos": len(llegadas),
            "capacidad_por_turno": 3,
            "duracion_ciclo_fijo": 3,
            "orden_ciclo_fijo": DIRECCIONES
        },
        "ciclo_fijo": resultado_fijo,
        "adaptativo": resultado_adaptativo,
        "mejoras_porcentuales": {
            "reduccion_espera": round(mejora_espera, 2),
            "reduccion_cola_maxima": round(mejora_cola, 2)
        }
    }
