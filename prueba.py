
from pprint import pprint

from backend.estadisticas.comparacion import comparar_algoritmos


print("==========================================")
print("       COMPARACIÓN DE ALGORITMOS")
print("==========================================")

resultados = comparar_algoritmos()

print("\n========== CONDICIONES DE PRUEBA ==========")
pprint(resultados["condiciones"], sort_dicts=False)

print("\n========== SEMÁFOROS DE CICLO FIJO ==========")
pprint(resultados["ciclo_fijo"], sort_dicts=False)

print("\n========== SEMÁFOROS ADAPTATIVOS ==========")
pprint(resultados["adaptativo"], sort_dicts=False)

print("\n========== MEJORAS DEL SISTEMA ADAPTATIVO ==========")
pprint(resultados["mejoras_porcentuales"], sort_dicts=False)

print("\n========== FIN DE LA COMPARACIÓN ==========")
