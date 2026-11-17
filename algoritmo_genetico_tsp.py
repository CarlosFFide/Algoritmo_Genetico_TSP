import itertools
import math
import random


CIUDADES = {
    "A": (0, 0),
    "B": (2, 6),
    "C": (5, 3),
    "D": (7, 8),
    "E": (9, 1),
    "F": (12, 5),
}

CIUDAD_ORIGEN = "A"
TAMANO_POBLACION = 60
GENERACIONES = 150
TAMANO_TORNEO = 3
ELITES = 2
PROBABILIDAD_MUTACION = 0.20
SEMILLA = 42


def distancia(ciudad_1, ciudad_2):
    x1, y1 = CIUDADES[ciudad_1]
    x2, y2 = CIUDADES[ciudad_2]
    return math.hypot(x2 - x1, y2 - y1)


def distancia_total(cromosoma):
    ruta = (CIUDAD_ORIGEN, *cromosoma, CIUDAD_ORIGEN)
    return sum(distancia(ruta[i], ruta[i + 1]) for i in range(len(ruta) - 1))


def aptitud(cromosoma):
    return 1.0 / distancia_total(cromosoma)


def crear_poblacion(ciudades):
    return [tuple(random.sample(ciudades, len(ciudades))) for _ in range(TAMANO_POBLACION)]


def seleccionar_por_torneo(poblacion):
    candidatos = random.sample(poblacion, TAMANO_TORNEO)
    return max(candidatos, key=aptitud)


def cruce_ordenado(padre_1, padre_2):
    longitud = len(padre_1)
    inicio, fin = sorted(random.sample(range(longitud), 2))
    hijo = [None] * longitud
    hijo[inicio : fin + 1] = padre_1[inicio : fin + 1]

    orden = list(range(fin + 1, longitud)) + list(range(0, fin + 1))
    restantes = [padre_2[posicion] for posicion in orden if padre_2[posicion] not in hijo]
    posiciones_libres = [posicion for posicion in orden if hijo[posicion] is None]
    for posicion, ciudad in zip(posiciones_libres, restantes):
        hijo[posicion] = ciudad

    return tuple(hijo)


def mutar(cromosoma):
    hijo = list(cromosoma)
    if random.random() < PROBABILIDAD_MUTACION:
        posicion_1, posicion_2 = random.sample(range(len(hijo)), 2)
        hijo[posicion_1], hijo[posicion_2] = hijo[posicion_2], hijo[posicion_1]
    return tuple(hijo)


def algoritmo_genetico():
    ciudades = tuple(ciudad for ciudad in CIUDADES if ciudad != CIUDAD_ORIGEN)
    poblacion = crear_poblacion(ciudades)
    mejor_inicial = min(poblacion, key=distancia_total)
    historial = [distancia_total(mejor_inicial)]

    for _ in range(GENERACIONES):
        poblacion.sort(key=distancia_total)
        siguiente_generacion = poblacion[:ELITES]

        while len(siguiente_generacion) < TAMANO_POBLACION:
            padre_1 = seleccionar_por_torneo(poblacion)
            padre_2 = seleccionar_por_torneo(poblacion)
            hijo = cruce_ordenado(padre_1, padre_2)
            siguiente_generacion.append(mutar(hijo))

        poblacion = siguiente_generacion
        historial.append(min(distancia_total(ruta) for ruta in poblacion))

    mejor_final = min(poblacion, key=distancia_total)
    return mejor_inicial, mejor_final, historial


def busqueda_exhaustiva():
    ciudades = tuple(ciudad for ciudad in CIUDADES if ciudad != CIUDAD_ORIGEN)
    return min(itertools.permutations(ciudades), key=distancia_total)


def mostrar_ruta(cromosoma):
    return " -> ".join((CIUDAD_ORIGEN, *cromosoma, CIUDAD_ORIGEN))


def main():
    random.seed(SEMILLA)
    inicial, final, historial = algoritmo_genetico()
    optima = busqueda_exhaustiva()
    distancia_inicial = distancia_total(inicial)
    distancia_final = distancia_total(final)
    distancia_optima = distancia_total(optima)
    mejora_porcentual = (distancia_inicial - distancia_final) / distancia_inicial * 100
    diferencia_optima = distancia_final - distancia_optima

    print("Problema del viajero - Algoritmo genético")
    print(f"Ciudades: {', '.join(CIUDADES)}")
    print(f"Población: {TAMANO_POBLACION} rutas | Generaciones: {GENERACIONES}")
    print(f"Mutación: {PROBABILIDAD_MUTACION:.0%} | Rutas conservadas: {ELITES} | Semilla: {SEMILLA}")
    print()
    print("Resultados del algoritmo")
    print(f"  Mejor ruta inicial: {mostrar_ruta(inicial)}")
    print(f"  Distancia inicial: {distancia_inicial:.4f} unidades")
    print(f"  Mejor ruta final: {mostrar_ruta(final)}")
    print(f"  Distancia final: {distancia_final:.4f} unidades")
    print(f"  Reducción de distancia: {mejora_porcentual:.2f}%")
    print()
    print("Comprobación con búsqueda exhaustiva")
    print(f"  Ruta más corta: {mostrar_ruta(optima)}")
    print(f"  Distancia mínima: {distancia_optima:.4f} unidades")
    print(f"  Diferencia respecto al mínimo: {diferencia_optima:.4f} unidades")
    if math.isclose(distancia_final, distancia_optima, abs_tol=1e-9):
        print("  El algoritmo encontró una ruta óptima.")
    else:
        print("  El algoritmo no alcanzó la distancia mínima.")
    print()
    print("Evolución de la mejor distancia por generación")
    for generacion in (0, 1, 5, 10, 25, 50, 75, 100, 125, 150):
        print(f"  Generación {generacion:>3}: {historial[generacion]:.4f} unidades")

if __name__ == "__main__":
    main()
