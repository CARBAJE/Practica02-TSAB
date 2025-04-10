import os
import pandas as pd
from AG_confs import *

from AG import genetic_algorithm
from libs.plot import *
from libs.functions import ImgRGB2Gray, apply_sigmoid

def main():
    # Crear carpetas de salida generales
    os.makedirs("outputs", exist_ok=True)
    
    for func_key, func_data in FUNCTIONS.items():
        f_obj = func_data["func"]
        g = func_data["g"]
        h = func_data["h"]
        lb = func_data["lb"]
        ub = func_data["ub"]
        func_name = func_data["name"]
        num_runs = func_data["num_runs"]
        
        # Carpetas específicas de cada función
        func_folder = f"outputs/{func_key}"
        os.makedirs(func_folder, exist_ok=True)
        hist_folder = os.path.join(func_folder, "historiales")
        res_folder = os.path.join(func_folder, "resumenes")
        os.makedirs(hist_folder, exist_ok=True)
        os.makedirs(res_folder, exist_ok=True)
        
        print(f"\n==============================================")
        print(f"  FUNCIÓN: {func_name}")
        print(f"==============================================")
        
        all_runs_history = []
        all_violations_history = []  # Nuevo: para almacenar violaciones de todas las corridas
        best_solutions_all_runs = []  # Guardaremos los mejores individuos (x1, x2) de cada corrida
        best_values_across_runs = []  # Guardaremos el best_val (fitness) de cada corrida
        
        for run in range(num_runs):
            print(f"\nEjecución {run+1}/{num_runs}")
            
            (best_sol, best_val,
             worst_sol, worst_val,
             avg_sol,  avg_val,
             std_val,
             best_fitness_history,
             best_x1_history,
             best_x2_history,
             constraint_violations_history,  # Nuevo: recibir historial de violaciones
             population_final,
             fitness_final,
             best_solutions_over_time) = genetic_algorithm(
                 f_obj, g, h, lb, ub,
                 pop_size=POP_SIZE,
                 num_generations=NUM_GENERATIONS,
                 tournament_size=TOURNAMENT_SIZE,
                 crossover_prob=CROSSOVER_PROB,
                 eta_c=ETA_C,
                 mutation_prob=MUTATION_PROB,
                 eta_mut=ETA_MUT,
                 lam = LAMBDA
             )
            
            # 1) Guardar historial
            df_historial = pd.DataFrame({
                "Generacion": np.arange(1, NUM_GENERATIONS + 1),
                "Mejor alpha": best_x1_history,
                "Mejor delta": best_x2_history,
                "Mejor Fitness": best_fitness_history
            })
            # Añadir columna de violaciones si existe
            if constraint_violations_history:
                df_historial["Violaciones"] = constraint_violations_history
                
            historial_filename = os.path.join(hist_folder, f"historial_run_{run+1}.csv")
            df_historial.to_csv(historial_filename, index=False)
            
            # 2) Guardar resumen de la corrida
            data_resumen = [
                ["Mejor", best_sol[0], best_sol[1], best_val],
                ["Media", avg_sol[0], avg_sol[1], avg_val],
                ["Peor", worst_sol[0], worst_sol[1], worst_val],
                ["Desv. estándar", np.nan, np.nan, std_val]
            ]
            df_resumen = pd.DataFrame(data_resumen, columns=["Indicador", "x1", "x2", "Fitness"])
            resumen_filename = os.path.join(res_folder, f"resumen_run_{run+1}.csv")
            df_resumen.to_csv(resumen_filename, index=False)
            
            print(df_resumen.to_string(index=False))
            
            all_runs_history.append(best_fitness_history)
            if constraint_violations_history:
                all_violations_history.append(constraint_violations_history)
            best_solutions_all_runs.append(best_sol)
            best_values_across_runs.append(best_val)
        
        # ===========================================
        #       RESUMEN GLOBAL DE LAS CORRIDAS
        # ===========================================
        best_values_arr = np.array(best_values_across_runs)
        solutions_arr = np.array(best_solutions_all_runs)  # Cada fila: [x1, x2] del mejor individuo de cada corrida
        
        # Para el "Mejor" y "Peor", buscamos el índice de la corrida con mínimo y máximo fitness
        min_index = np.argmin(best_values_arr)
        max_index = np.argmax(best_values_arr)
        
        data_global = [
            ["Mejor (Fitness)", solutions_arr[min_index, 0], solutions_arr[min_index, 1], best_values_arr[min_index]],
            ["Peor (Fitness)", solutions_arr[max_index, 0], solutions_arr[max_index, 1], best_values_arr[max_index]],
            ["Media", np.mean(solutions_arr[:, 0]), np.mean(solutions_arr[:, 1]), np.mean(best_values_arr)],
            ["Desv. Estándar", np.std(solutions_arr[:, 0]), np.std(solutions_arr[:, 1]), np.std(best_values_arr)]
        ]
        df_global = pd.DataFrame(data_global, columns=["Indicador", "alpha", "delta", "Fitness"])
        
        global_filename = os.path.join(res_folder, "resumen_global_corridas.csv")
        df_global.to_csv(global_filename, index=False)
        
        # Graficar evolución del fitness y violaciones
        plot_evolucion_fitness_with_violations(all_runs_history, all_violations_history, func_key, func_name)
        
        # Graficar superficie 3D con restricciones si la función es de 2 variables
        if len(lb) == 2 and g:
            plot_surface_3d_with_constraints(f_obj, g, lb, ub, best_solutions_all_runs, func_key, func_name)
        # Si no hay restricciones, usar la función original
        elif len(lb) == 2:
            plot_surface_3d(f_obj, lb, ub, best_solutions_all_runs, func_key, func_name)

if __name__ == "__main__":
    main()
