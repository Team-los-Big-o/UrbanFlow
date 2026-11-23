
def registrar_emergencia(red, interseccion, direccion, tipo="ambulancia"):
    # Verificar que exista la intersección
    if interseccion not in red:
        return {"error": "Intersección inexistente"}

    # Verificar que la dirección sea válida
    if direccion not in red[interseccion]["colas"]:
        return {"error": "Dirección inválida"}

    tipos_validos = ["ambulancia", "policia", "bomberos"]

    if tipo not in tipos_validos:
        return {"error": "Tipo de emergencia inválido"}

    estado = red[interseccion]["estado_semaforo"]

    # Registrar el vehículo prioritario
    estado["emergencia"] = {
        "direccion": direccion,
        "tipo": tipo,
        "activo": True
    }

    return {
        "mensaje": "Emergencia registrada",
        "interseccion": interseccion,
        "direccion": direccion,
        "tipo": tipo
    }


def eliminar_emergencia(red, interseccion):
    if interseccion not in red:
        return {"error": "Intersección inexistente"}

    estado = red[interseccion]["estado_semaforo"]

    if "emergencia" not in estado:
        return {"error": "No existe una emergencia activa"}

    del estado["emergencia"]

    return {
        "mensaje": "Emergencia eliminada",
        "interseccion": interseccion
    }
