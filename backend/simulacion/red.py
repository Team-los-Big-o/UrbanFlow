
from backend.simulacion.motor import ejecutar_turno
from backend.simulacion.rutas import buscar_ruta
from backend.simulacion.emergencias import obtener_direccion


def crear_interseccion():
    return {
        "colas": {
            "norte": 0,
            "sur": 0,
            "este": 0,
            "oeste": 0
        },
        "tiempos": {
            "norte": 0,
            "sur": 0,
            "este": 0,
            "oeste": 0
        },
        "estado_semaforo": {
            "direccion": None,
            "tiempo_verde": 0,
            "incidente": {}
        }
    }


def crear_red():
    return {
        f"I{fila}{columna}": crear_interseccion()
        for fila in range(1, 4)
        for columna in range(1, 4)
    }


def obtener_destino(nombre, direccion):
    fila = int(nombre[1])
    columna = int(nombre[2])

    if direccion == "norte":
        fila -= 1
    elif direccion == "sur":
        fila += 1
    elif direccion == "este":
        columna += 1
    elif direccion == "oeste":
        columna -= 1

    if 1 <= fila <= 3 and 1 <= columna <= 3:
        return f"I{fila}{columna}"

    return None


def distribuir_vehiculos(direccion, cantidad):
    derecho = round(cantidad * 0.60)
    izquierda = round(cantidad * 0.20)
    derecha = cantidad - derecho - izquierda

    movimientos = {
        "norte": {
            "derecho": "norte",
            "izquierda": "oeste",
            "derecha": "este"
        },
        "sur": {
            "derecho": "sur",
            "izquierda": "este",
            "derecha": "oeste"
        },
        "este": {
            "derecho": "este",
            "izquierda": "norte",
            "derecha": "sur"
        },
        "oeste": {
            "derecho": "oeste",
            "izquierda": "sur",
            "derecha": "norte"
        }
    }

    distribucion = movimientos[direccion]

    return [
        (distribucion["derecho"], derecho),
        (distribucion["izquierda"], izquierda),
        (distribucion["derecha"], derecha)
    ]


def ejecutar_red(red, llegadas):
    resultados = {}
    movimientos = []

    # Primera fase: revisar y simular las intersecciones
    for nombre, interseccion in red.items():

        estado = interseccion["estado_semaforo"]
        emergencia = estado.get("emergencia")
        reencaminada = False

        # Revisar si existe una emergencia activa
        if emergencia and emergencia.get("activo"):

            destino = emergencia.get("destino")
            ruta_actual = emergencia.get("ruta", [])
            indice = emergencia.get("indice", 0)

            # Obtener el tramo de ruta que falta recorrer
            ruta_restante = ruta_actual[indice:]

            # Buscar una ruta actualizada
            nueva_ruta = buscar_ruta(
                red,
                nombre,
                destino
            )

            if nueva_ruta.get("ruta"):

                ruta_calculada = nueva_ruta["ruta"]

                # Actualizar solamente si cambió el recorrido
                if ruta_calculada != ruta_restante and len(ruta_calculada) >= 2:

                    emergencia["ruta"] = ruta_calculada
                    emergencia["indice"] = 0

                    emergencia["direccion"] = obtener_direccion(
                        ruta_calculada[0],
                        ruta_calculada[1]
                    )

                    reencaminada = True

        # Ejecutar el turno de la intersección
        resultado = ejecutar_turno(
            interseccion["colas"],
            llegadas.get(nombre, {}),
            interseccion["tiempos"],
            estado,
            capacidad=3,
            minimo=2,
            maximo=5
        )

        resultados[nombre] = resultado

        resultado["emergencia_reencaminada"] = reencaminada

        if emergencia and emergencia.get("activo"):
            resultado["ruta_emergencia"] = emergencia.get("ruta")

        atendidos = resultado["vehiculos_atendidos"]
        direccion = resultado["direccion_verde"]

        resultado["vehiculos_transferidos"] = 0
        resultado["vehiculos_salieron"] = 0

        # Distribuir vehículos normales
        if atendidos > 0:

            distribucion = distribuir_vehiculos(
                direccion,
                atendidos
            )

            for movimiento, cantidad in distribucion:

                if cantidad == 0:
                    continue

                destino = obtener_destino(nombre, movimiento)

                if destino is None:
                    resultado["vehiculos_salieron"] += cantidad

                else:
                    movimientos.append(
                        (nombre, destino, movimiento, cantidad)
                    )

                    resultado["vehiculos_transferidos"] += cantidad

    # Segunda fase: transferir vehículos normales
    for origen, destino, direccion, cantidad in movimientos:
        red[destino]["colas"][direccion] += cantidad

    # Tercera fase: transferir vehículos de emergencia
    for nombre, resultado in resultados.items():

        if resultado["vehiculos_emergencia_atendidos"] > 0:

            emergencia = resultado["datos_emergencia"]

            ruta = emergencia["ruta"]
            indice = emergencia["indice"]

            nuevo_indice = indice + 1

            # Verificar si llegó al destino
            if nuevo_indice >= len(ruta) - 1:

                resultado["emergencia_llego_destino"] = True
                continue

            # Obtener la siguiente intersección
            siguiente = ruta[nuevo_indice]
            despues = ruta[nuevo_indice + 1]

            direccion = obtener_direccion(
                siguiente,
                despues
            )

            # Registrar la emergencia en la siguiente intersección
            red[siguiente]["estado_semaforo"]["emergencia"] = {
                **emergencia,
                "direccion": direccion,
                "indice": nuevo_indice
            }

            resultado["emergencia_transferida"] = True
            resultado["siguiente_interseccion"] = siguiente

    # Actualizar las colas finales
    for nombre in red:
        resultados[nombre]["colas"] = red[nombre]["colas"].copy()

    return resultados
