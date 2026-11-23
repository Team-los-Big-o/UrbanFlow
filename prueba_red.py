from backend.simulacion.red import crear_red, ejecutar_red
from backend.simulacion.red import distribuir_vehiculos

print(distribuir_vehiculos("norte", 10))

red = crear_red()

llegadas = {
    "I11": {"este": 2, "sur": 1},
    "I12": {"sur": 2},
    "I13": {"sur": 1, "oeste": 2},

    "I21": {"este": 2},
    "I22": {},
    "I23": {"oeste": 2},

    "I31": {"este": 1, "norte": 2},
    "I32": {"norte": 1},
    "I33": {"norte": 2, "oeste": 1}
}

for turno in range(1, 6):

    resultados = ejecutar_red(red, llegadas)

    print(f"\n========== TURNO {turno} ==========")

    for nombre, resultado in resultados.items():

        print(f"\nIntersección {nombre}")
        print("Semáforo:", resultado["direccion_verde"])
        print("Atendidos:", resultado["vehiculos_atendidos"])
        print("Transferidos:", resultado["vehiculos_transferidos"])
        print("Salieron de la red:", resultado["vehiculos_salieron"])
        print("Colas:", resultado["colas"])