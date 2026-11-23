
def crear_estadisticas():
    return {
        "turnos": 0,
        "vehiculos_atendidos": 0,
        "vehiculos_transferidos": 0,
        "vehiculos_salieron": 0,
        "movimientos_emergencia": 0,
        "emergencias_completadas": 0,
        "tiempo_total_emergencias": 0,
        "turnos_emergencia_actuales": 0,
        "emergencias_reencaminadas": 0,
        "suma_tiempos_espera": 0,
        "muestras_tiempos_espera": 0,
        "cola_maxima": 0,
        "intersecciones": {}
    }


def actualizar_estadisticas(estadisticas, resultados):

    estadisticas["turnos"] += 1

    for nombre, resultado in resultados.items():

        estadisticas["vehiculos_atendidos"] += resultado.get(
            "vehiculos_atendidos", 0
        )

        estadisticas["vehiculos_transferidos"] += resultado.get(
            "vehiculos_transferidos", 0
        )

        estadisticas["vehiculos_salieron"] += resultado.get(
            "vehiculos_salieron", 0
        )

        movimientos = resultado.get(
            "vehiculos_emergencia_atendidos", 0
        )

        estadisticas["movimientos_emergencia"] += movimientos

        if movimientos > 0:
            estadisticas["turnos_emergencia_actuales"] += 1

        if resultado.get("emergencia_llego_destino"):

            estadisticas["emergencias_completadas"] += 1

            estadisticas["tiempo_total_emergencias"] += (
                estadisticas["turnos_emergencia_actuales"]
            )

            estadisticas["turnos_emergencia_actuales"] = 0

        if resultado.get("emergencia_reencaminada"):
            estadisticas["emergencias_reencaminadas"] += 1

        colas = resultado.get("colas", {})
        tiempos = resultado.get("tiempos_espera", {})

        for direccion, cantidad in colas.items():

            if cantidad > 0:
                estadisticas["suma_tiempos_espera"] += tiempos.get(
                    direccion, 0
                )

                estadisticas["muestras_tiempos_espera"] += 1

        total_cola = sum(colas.values())

        estadisticas["cola_maxima"] = max(
            estadisticas["cola_maxima"],
            total_cola
        )

        if nombre not in estadisticas["intersecciones"]:
            estadisticas["intersecciones"][nombre] = {
                "cola_maxima": 0,
                "acumulado_cola": 0,
                "turnos_medidos": 0
            }

        datos = estadisticas["intersecciones"][nombre]

        datos["cola_maxima"] = max(
            datos["cola_maxima"],
            total_cola
        )

        datos["acumulado_cola"] += total_cola
        datos["turnos_medidos"] += 1


def obtener_estadisticas(estadisticas):

    muestras = estadisticas["muestras_tiempos_espera"]

    espera_promedio = (
        estadisticas["suma_tiempos_espera"] / muestras
        if muestras > 0 else 0
    )

    completadas = estadisticas["emergencias_completadas"]

    tiempo_emergencia_promedio = (
        estadisticas["tiempo_total_emergencias"] / completadas
        if completadas > 0 else 0
    )

    intersecciones = {}

    for nombre, datos in estadisticas["intersecciones"].items():

        cola_promedio = (
            datos["acumulado_cola"] / datos["turnos_medidos"]
            if datos["turnos_medidos"] > 0 else 0
        )

        intersecciones[nombre] = {
            "cola_maxima": datos["cola_maxima"],
            "cola_promedio": round(cola_promedio, 2)
        }

    if intersecciones:
        mayor_congestion = max(
            intersecciones,
            key=lambda nombre: intersecciones[nombre]["cola_promedio"]
        )
    else:
        mayor_congestion = None

    return {
        "turnos": estadisticas["turnos"],
        "vehiculos_atendidos": estadisticas["vehiculos_atendidos"],
        "vehiculos_transferidos": estadisticas["vehiculos_transferidos"],
        "vehiculos_salieron": estadisticas["vehiculos_salieron"],
        "tiempo_espera_promedio": round(espera_promedio, 2),
        "cola_maxima": estadisticas["cola_maxima"],
        "movimientos_emergencia": estadisticas["movimientos_emergencia"],
        "emergencias_completadas": completadas,
        "tiempo_promedio_emergencia": round(
            tiempo_emergencia_promedio, 2
        ),
        "emergencias_reencaminadas": estadisticas[
            "emergencias_reencaminadas"
        ],
        "interseccion_mayor_congestion": mayor_congestion,
        "congestion_por_interseccion": intersecciones
    }
