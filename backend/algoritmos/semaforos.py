
def seleccionar_semaforo(vehiculos):
    """
    Selecciona la dirección con mayor cantidad
    de vehículos esperando.
    """

    direccion = max(vehiculos, key=vehiculos.get)

    return direccion
