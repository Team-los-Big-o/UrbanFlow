
def actualizar_tiempos_espera(tiempos, direccion_verde, colas):
    """
    Actualiza el tiempo de espera de cada dirección.

    La dirección con luz verde reinicia su espera
    si tiene vehículos. Las demás acumulan un turno.
    """

    for direccion in tiempos:

        if direccion == direccion_verde and colas[direccion] > 0:
            tiempos[direccion] = 0
        elif colas[direccion] > 0:
            tiempos[direccion] += 1
        else:
            tiempos[direccion] = 0
