
from backend.simulacion.motor import ejecutar_turno


def crear_interseccion():
    return {
        "colas": {"norte": 0, "sur": 0, "este": 0, "oeste": 0},
        "tiempos": {"norte": 0, "sur": 0, "este": 0, "oeste": 0},
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

    # Primera fase: simular todas las intersecciones
    for nombre, interseccion in red.items():
        resultado = ejecutar_turno(
            interseccion["colas"],
            llegadas.get(nombre, {}),
            interseccion["tiempos"],
            interseccion["estado_semaforo"],
            capacidad=3,
            minimo=2,
            maximo=5
        )

        resultados[nombre] = resultado

        atendidos = resultado["vehiculos_atendidos"]
        direccion = resultado["direccion_verde"]

        resultado["vehiculos_transferidos"] = 0
        resultado["vehiculos_salieron"] = 0

        if atendidos > 0:
            distribucion = distribuir_vehiculos(direccion, atendidos)

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

            direccion = resultado["direccion_emergencia"]
            destino = obtener_destino(nombre, direccion)

            if destino is not None:
                red[destino]["estado_semaforo"]["emergencia"] = {
                    "direccion": direccion,
                    "tipo": resultado["tipo_emergencia"],
                    "activo": True
                }

                resultado["emergencia_transferida"] = True
    # Actualizar resultados con las colas finales
    for nombre in red:
        resultados[nombre]["colas"] = red[nombre]["colas"].copy()

    return resultados
