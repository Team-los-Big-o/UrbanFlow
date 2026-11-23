
def crear_incidente(red, interseccion, direccion, reduccion=1):
    # Verificar que exista la intersección
    if interseccion not in red:
        return {"error": "Intersección inexistente"}

    # Verificar que la dirección sea válida
    if direccion not in red[interseccion]["colas"]:
        return {"error": "Dirección inválida"}

    # Verificar que la reducción sea un número entero positivo
    if not isinstance(reduccion, int) or isinstance(reduccion, bool) or reduccion < 1:
        return {"error": "La reducción debe ser un entero mayor que cero"}

    # Crear el registro de incidentes si no existe
    if "incidentes" not in red[interseccion]:
        red[interseccion]["incidentes"] = {}

    # Evitar duplicar incidentes en la misma dirección
    if direccion in red[interseccion]["incidentes"]:
        return {"error": "Ya existe un incidente en esa dirección"}

    # Registrar el incidente
    red[interseccion]["incidentes"][direccion] = {
        "carriles_reducidos": reduccion,
        "activo": True
    }

    # Conectar el incidente con el motor de simulación
    red[interseccion]["estado_semaforo"]["incidente"][direccion] = reduccion

    return {
        "mensaje": "Incidente registrado",
        "interseccion": interseccion,
        "direccion": direccion,
        "carriles_reducidos": reduccion
    }


def eliminar_incidente(red, interseccion, direccion):
    # Verificar que exista la intersección
    if interseccion not in red:
        return {"error": "Intersección inexistente"}

    incidentes = red[interseccion].get("incidentes", {})

    # Verificar que exista el incidente
    if direccion not in incidentes:
        return {"error": "No existe un incidente en esa dirección"}

    # Eliminar el incidente del registro
    del incidentes[direccion]

    # Eliminar también su efecto sobre el motor
    red[interseccion]["estado_semaforo"]["incidente"].pop(direccion, None)

    return {
        "mensaje": "Incidente eliminado",
        "interseccion": interseccion,
        "direccion": direccion
    }
