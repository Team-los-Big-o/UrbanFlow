
from backend.simulacion.rutas import buscar_ruta


def obtener_direccion(origen, siguiente):
    fila_origen = int(origen[1])
    columna_origen = int(origen[2])

    fila_siguiente = int(siguiente[1])
    columna_siguiente = int(siguiente[2])

    if fila_siguiente < fila_origen:
        return "norte"
    if fila_siguiente > fila_origen:
        return "sur"
    if columna_siguiente > columna_origen:
        return "este"
    if columna_siguiente < columna_origen:
        return "oeste"

    return None


def registrar_emergencia(red, origen, destino, tipo="ambulancia"):
    # Verificar que existan las intersecciones
    if origen not in red or destino not in red:
        return {"error": "Intersección inexistente"}

    tipos_validos = ["ambulancia", "policia", "bomberos"]

    if tipo not in tipos_validos:
        return {"error": "Tipo de emergencia inválido"}

    # Verificar que no exista otra emergencia en el origen
    estado = red[origen]["estado_semaforo"]

    if estado.get("emergencia", {}).get("activo"):
        return {"error": "Ya existe una emergencia activa"}

    # Calcular la ruta mediante BFS
    resultado_ruta = buscar_ruta(red, origen, destino)

    if resultado_ruta.get("ruta") is None:
        return {"error": "No existe una ruta disponible"}

    ruta = resultado_ruta["ruta"]

    if len(ruta) < 2:
        return {"error": "El origen y destino son iguales"}

    # Obtener la primera dirección de movimiento
    direccion = obtener_direccion(ruta[0], ruta[1])

    # Registrar la emergencia
    estado["emergencia"] = {
    "direccion": direccion,
    "tipo": tipo,
    "activo": True,
    "origen": origen,
    "destino": destino,
    "ruta": ruta,
    "indice": 0
}

    return {
        "mensaje": "Emergencia registrada",
        "tipo": tipo,
        "origen": origen,
        "destino": destino,
        "ruta": ruta,
        "pasos": resultado_ruta["pasos"]
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
