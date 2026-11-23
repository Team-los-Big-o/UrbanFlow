
from collections import deque


def buscar_ruta(red, origen, destino, capacidad=3):
    # Verificar que existan las intersecciones
    if origen not in red or destino not in red:
        return {"error": "Intersección inexistente"}

    if origen == destino:
        return {
            "ruta": [origen],
            "pasos": 0
        }

    # Movimientos posibles dentro de la cuadrícula
    movimientos = {
        "norte": (-1, 0),
        "sur": (1, 0),
        "este": (0, 1),
        "oeste": (0, -1)
    }

    # Cola de búsqueda BFS
    cola = deque([origen])

    # Registrar los nodos visitados y sus anteriores
    visitados = {origen}
    anteriores = {}

    while cola:
        actual = cola.popleft()

        fila = int(actual[1])
        columna = int(actual[2])

        for direccion, (df, dc) in movimientos.items():
            nueva_fila = fila + df
            nueva_columna = columna + dc

            vecino = f"I{nueva_fila}{nueva_columna}"

            # Verificar que exista la intersección vecina
            if vecino not in red or vecino in visitados:
                continue

            # Consultar si la dirección está completamente bloqueada
            incidentes = red[actual]["estado_semaforo"].get(
                "incidente", {}
            )

            carriles_reducidos = incidentes.get(direccion, 0)

            if capacidad - carriles_reducidos <= 0:
                continue

            # Registrar el recorrido
            visitados.add(vecino)
            anteriores[vecino] = actual

            if vecino == destino:
                # Reconstruir la ruta
                ruta = [destino]

                while ruta[-1] != origen:
                    ruta.append(anteriores[ruta[-1]])

                ruta.reverse()

                return {
                    "ruta": ruta,
                    "pasos": len(ruta) - 1
                }

            cola.append(vecino)

    return {
        "ruta": None,
        "mensaje": "No existe una ruta disponible"
    }
