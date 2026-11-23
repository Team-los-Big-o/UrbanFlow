
from backend.algoritmos.semaforos import seleccionar_semaforo


def actualizar_semaforo(
    colas,
    direccion_actual,
    tiempo_verde,
    tiempos_espera,
    minimo=2,
    maximo=5,
    emergencia=None
):

    # Prioridad absoluta para vehículos de emergencia
    if emergencia and emergencia.get("activo"):
        return emergencia["direccion"]

    # Seleccionar la primera dirección
    if direccion_actual is None:
        return seleccionar_semaforo(colas, tiempos_espera)

    # Respetar el tiempo mínimo de luz verde
    if tiempo_verde < minimo:
        return direccion_actual

    # Identificar otras direcciones con vehículos
    otras_direcciones = {
        direccion: cantidad
        for direccion, cantidad in colas.items()
        if direccion != direccion_actual and cantidad > 0
    }

    # Si no hay vehículos en otras direcciones
    if not otras_direcciones:
        if colas[direccion_actual] > 0:
            return direccion_actual

        return seleccionar_semaforo(colas, tiempos_espera)

    # Encontrar la dirección con mayor prioridad
    tiempos_filtrados = {
        direccion: tiempos_espera[direccion]
        for direccion in otras_direcciones
    }

    mejor_direccion = seleccionar_semaforo(
        otras_direcciones,
        tiempos_filtrados
    )

    # Calcular prioridad de la dirección actual
    puntuacion_actual = (
        colas[direccion_actual]
        + tiempos_espera[direccion_actual] * 2
    )

    # Calcular prioridad de la mejor dirección alternativa
    puntuacion_alternativa = (
        colas[mejor_direccion]
        + tiempos_espera[mejor_direccion] * 2
    )

    # Respetar el tiempo máximo de luz verde
    if tiempo_verde >= maximo:
        return mejor_direccion

    # Cambiar si la alternativa tiene mayor prioridad
    if puntuacion_alternativa > puntuacion_actual:
        return mejor_direccion

    return direccion_actual
