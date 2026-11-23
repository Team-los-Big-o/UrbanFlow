
from time import perf_counter

from backend.simulacion.vehiculos import (
    agregar_vehiculos,
    avanzar_vehiculos
)

from backend.simulacion.tiempos import actualizar_tiempos_espera
from backend.simulacion.controlador import actualizar_semaforo


DIRECCIONES = ["norte", "sur", "este", "oeste"]

DURACION_SIMULACION = 36
REPETICIONES = 10


def generar_escenarios():
    escenarios = {
        "bajo": [1, 0, 0, 0],
        "medio": [1, 1, 0, 0],
        "alto": [1, 1, 1, 0]
    }

    resultado = {}

    for nombre, patron in escenarios.items():
        llegadas = []

        for turno in range(DURACION_SIMULACION):
            nuevas_llegadas = {}

            for indice, direccion in enumerate(DIRECCIONES):
                posicion = (turno + indice) % len(patron)
                nuevas_llegadas[direccion] = patron[posicion]

            llegadas.append(nuevas_llegadas)

        resultado[nombre] = llegadas

    return resultado


def simular_algoritmo(
    nombre,
    llegadas,
    capacidad=3,
    duracion_fija=3,
    minimo=2,
    maximo=5
):
    colas = {
        direccion: 0
        for direccion in DIRECCIONES
    }

    tiempos = {
        direccion: 0
        for direccion in DIRECCIONES
    }

    # Guarda el turno en que llegó cada vehículo.
    llegadas_por_direccion = {
        direccion: []
        for direccion in DIRECCIONES
    }

    direccion_actual = None
    tiempo_verde = 0

    vehiculos_llegaron = 0
    vehiculos_atendidos = 0
    suma_esperas = 0
    cola_maxima = 0

    inicio = perf_counter()

    for turno, nuevas_llegadas in enumerate(llegadas, start=1):

        # 1. Registrar las nuevas llegadas.
        agregar_vehiculos(colas, nuevas_llegadas)

        for direccion, cantidad in nuevas_llegadas.items():
            vehiculos_llegaron += cantidad

            llegadas_por_direccion[direccion].extend(
                [turno] * cantidad
            )

        # 2. Seleccionar el semáforo.
        if nombre == "fijo":
            fase = (
                (turno - 1) // duracion_fija
            ) % len(DIRECCIONES)

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

        # 3. Actualizar el tiempo de luz verde.
        if direccion_nueva != direccion_actual:
            direccion_actual = direccion_nueva
            tiempo_verde = 1
        else:
            tiempo_verde += 1

        # 4. Atender vehículos.
        atendidos = avanzar_vehiculos(
            colas,
            direccion_actual,
            capacidad
        )

        vehiculos_atendidos += atendidos

        # 5. Calcular la espera de los vehículos atendidos.
        for _ in range(atendidos):
            turno_llegada = llegadas_por_direccion[
                direccion_actual
            ].pop(0)

            suma_esperas += turno - turno_llegada

        # 6. Actualizar los tiempos usados por el controlador.
        actualizar_tiempos_espera(
            tiempos,
            direccion_actual,
            colas
        )

        # 7. Registrar la cola máxima.
        total_cola = sum(colas.values())

        cola_maxima = max(
            cola_maxima,
            total_cola
        )

    # 8. Calcular la espera acumulada de vehículos pendientes.
    for direccion in DIRECCIONES:
        for turno_llegada in llegadas_por_direccion[direccion]:
            suma_esperas += DURACION_SIMULACION - turno_llegada

    tiempo_ejecucion = (
        perf_counter() - inicio
    ) * 1000

    espera_promedio = (
        suma_esperas / vehiculos_llegaron
        if vehiculos_llegaron > 0
        else 0
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


def promediar_resultados(resultados):
    campos = [
        "vehiculos_llegaron",
        "vehiculos_atendidos",
        "vehiculos_pendientes",
        "tiempo_espera_promedio",
        "cola_maxima",
        "tiempo_ejecucion_ms"
    ]

    promedio = {}

    for campo in campos:
        promedio[campo] = round(
            sum(resultado[campo] for resultado in resultados)
            / len(resultados),
            4
        )

    promedio["turnos"] = resultados[0]["turnos"]

    return promedio


def comparar_escenario(nombre, llegadas):
    resultados_fijos = []
    resultados_adaptativos = []

    for _ in range(REPETICIONES):
        resultados_fijos.append(
            simular_algoritmo("fijo", llegadas)
        )

        resultados_adaptativos.append(
            simular_algoritmo("adaptativo", llegadas)
        )

    fijo = promediar_resultados(resultados_fijos)
    adaptativo = promediar_resultados(resultados_adaptativos)

    espera_fija = fijo["tiempo_espera_promedio"]
    espera_adaptativa = adaptativo["tiempo_espera_promedio"]

    cola_fija = fijo["cola_maxima"]
    cola_adaptativa = adaptativo["cola_maxima"]

    mejora_espera = (
        (espera_fija - espera_adaptativa) / espera_fija * 100
        if espera_fija > 0
        else 0
    )

    mejora_cola = (
        (cola_fija - cola_adaptativa) / cola_fija * 100
        if cola_fija > 0
        else 0
    )

    return {
        "escenario": nombre,
        "repeticiones": REPETICIONES,
        "ciclo_fijo": fijo,
        "adaptativo": adaptativo,
        "mejoras_porcentuales": {
            "reduccion_espera": round(mejora_espera, 2),
            "reduccion_cola_maxima": round(mejora_cola, 2)
        }
    }


def comparar_algoritmos():
    escenarios = generar_escenarios()
    resultados = {}

    for nombre, llegadas in escenarios.items():
        resultados[nombre] = comparar_escenario(
            nombre,
            llegadas
        )

    return {
        "condiciones": {
            "turnos_por_simulacion": DURACION_SIMULACION,
            "repeticiones": REPETICIONES,
            "capacidad_por_turno": 3,
            "duracion_ciclo_fijo": 3,
            "tiempo_minimo_adaptativo": 2,
            "tiempo_maximo_adaptativo": 5,
            "orden_ciclo_fijo": DIRECCIONES
        },
        "escenarios": resultados
    }
