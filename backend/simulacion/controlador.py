
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
    # Dar prioridad a una emergencia activa
    if emergencia and emergencia.get("activo"):
        return emergencia["direccion"]

    if direccion_actual is None:
        return seleccionar_semaforo(colas, tiempos_espera)

    if tiempo_verde < minimo:
        return direccion_actual

    otras_direcciones = {
        direccion: cantidad
        for direccion, cantidad in colas.items()
        if direccion != direccion_actual and cantidad > 0
    }

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
