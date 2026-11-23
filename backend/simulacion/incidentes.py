
def crear_incidente(red, interseccion, direccion, reduccion=1):
    if interseccion not in red:
        return {"error": "Intersección inexistente"}

    if direccion not in red[interseccion]["colas"]:
        return {"error": "Dirección inválida"}

    if "incidentes" not in red[interseccion]:
        red[interseccion]["incidentes"] = {}

    if direccion in red[interseccion]["incidentes"]:
        return {"error": "Ya existe un incidente en esa dirección"}

    if reduccion < 1:
        return {"error": "La reducción debe ser mayor que cero"}

    red[interseccion]["incidentes"][direccion] = {
        "carriles_reducidos": reduccion,
        "activo": True
    }

    return {
        "mensaje": "Incidente registrado",
        "interseccion": interseccion,
        "direccion": direccion,
        "carriles_reducidos": reduccion
    }


def eliminar_incidente(red, interseccion, direccion):
    incidentes = red[interseccion].get("incidentes", {})

    if direccion not in incidentes:
        return {"error": "No existe un incidente en esa dirección"}

    del incidentes[direccion]

    return {"mensaje": "Incidente eliminado"}
