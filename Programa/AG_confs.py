import numpy as np
from libs.functions import *
# ---------------------------
# Parámetros del algoritmo
# ---------------------------
POP_SIZE = 1100           # Número de individuos en la población
NUM_GENERATIONS = 1500     # Número de generaciones
NUM_RUNS = 5             # Número de ejecuciones completas (ciclos)

# Parámetros de la función de Langermann
a = np.array([3, 5, 2, 1, 7])
b = np.array([5, 2, 1, 4, 9])
c = np.array([1, 2, 5, 2, 3])

# Parámetros del torneo
TOURNAMENT_SIZE = 3  # Número de individuos participantes en cada torneo

# Parámetros del cruzamiento SBX
CROSSOVER_PROB = 0.9  # Probabilidad de aplicar cruzamiento
ETA_C = 0.001            # Índice de distribución para SBX

# Limites superiores e inferiores
LB = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
UB = np.array([0.4, 0.4, 0.4, 0.4, 0.4, 0.4])

# Parámetros de la mutación polinomial
MUTATION_PROB = 1 / (10)  # Probabilidad de mutar cada gen
ETA_MUT = 0.0001                         # Índice de distribución para mutación polinomial

# Ruta a la imagen a contrastar
# IMG_PATH = get_image_paths('imgs')

best_solutions_list = []
all_runs_history = []  # Para graficar luego

LAMBDA = 1*10e1

FUNCTIONS = {
    "Problem1": {
        "func": f_finanzas,
        "g": None,
        "h": [h1_finanzas],
        "lb": LB,
        "ub": UB,
        "name": "Problema 1",
        "num_runs": NUM_RUNS,
        "secondary_func": f_riesgos  # Función secundaria que queremos monitorear
    },
    "Problem2": {
        "func": f_riesgos,
        "g": [g1_finanzas],
        "h": [h1_finanzas],
        "lb": LB,
        "ub": UB,
        "name": "Problema 2",
        "num_runs": NUM_RUNS,
        "secondary_func": f_finanzas  # Función secundaria que queremos monitorear
    },
    "Problem3": {
        "func": f_finanzas,
        "g": [g2_finanzas],
        "h": [h1_finanzas],
        "lb": LB,
        "ub": UB,
        "name": "Problema 3",
        "num_runs": NUM_RUNS,
        "secondary_func": f_riesgos  # Función secundaria que queremos monitorear
    }
}