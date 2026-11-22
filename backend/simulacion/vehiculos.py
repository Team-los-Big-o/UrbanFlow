
def agregar_vehiculos(colas, llegadas):
    """
    Agrega los vehículos que llegan a cada dirección.
    """
    for direccion, cantidad in llegadas.items():
        colas[direccion] += cantidad


def avanzar_vehiculos(colas, direccion_verde, capacidad=3):
    """
    Permite el paso de vehículos por la dirección
    que tiene luz verde.
    """

    disponibles = colas[direccion_verde]

    atendidos = min(disponibles, capacidad)

    colas[direccion_verde] -= atendidos

    return atendidos
