
def seleccionar_semaforo(vehiculos, tiempos_espera):
    """
    Selecciona la dirección con mayor puntuación.

    Considera tanto la cantidad de vehículos
    como el tiempo que llevan esperando.
    """

    puntuaciones = {}

    for direccion in vehiculos:

        puntuacion = (
            vehiculos[direccion]
            + tiempos_espera[direccion] * 2
        )

        puntuaciones[direccion] = puntuacion

    direccion = max(puntuaciones, key=puntuaciones.get)

    return direccion
