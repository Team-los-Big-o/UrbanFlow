
from backend.algoritmos.semaforos import seleccionar_semaforo


def actualizar_semaforo(
    colas,
    direccion_actual,
    tiempo_verde,
    tiempos_espera,
    minimo=2,
    maximo=5
):
    """
    Decide si el semáforo actual debe mantenerse
    o cambiar a otra dirección.
    """

    # Si todavía no hay dirección activa
    if direccion_actual is None:
        return seleccionar_semaforo(colas, tiempos_espera)

    # Si no se ha cumplido el tiempo mínimo
    if tiempo_verde < minimo:
        return direccion_actual

    # Buscar otras direcciones con vehículos
    otras_direcciones = {
        direccion: cantidad
        for direccion, cantidad in colas.items()
        if direccion != direccion_actual and cantidad > 0
    }

    # Si se alcanzó el tiempo máximo, cambiar
    if tiempo_verde >= maximo:

        if otras_direcciones:
            tiempos_filtrados = {
                direccion: tiempos_espera[direccion]
                for direccion in otras_direcciones
            }

            return seleccionar_semaforo(
                otras_direcciones,
                tiempos_filtrados
            )

        return direccion_actual

    # Si la cola actual está vacía, cambiar si hay otra
    if colas[direccion_actual] == 0 and otras_direcciones:

        tiempos_filtrados = {
            direccion: tiempos_espera[direccion]
            for direccion in otras_direcciones
        }

        return seleccionar_semaforo(
            otras_direcciones,
            tiempos_filtrados
        )

    return direccion_actual
