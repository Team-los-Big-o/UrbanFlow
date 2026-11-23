
import json

from backend.estadisticas.comparacion import comparar_algoritmos


resultados = comparar_algoritmos()

print("\n========== COMPARACIÓN DE ALGORITMOS ==========\n")

print(json.dumps(
    resultados,
    indent=4,
    ensure_ascii=False
))
