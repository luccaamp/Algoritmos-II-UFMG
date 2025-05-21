import sys
import time
from utils import parse_tsplib, compute_distance_matrix
from christofides import christofides
from twice_around_tree import twice_around_tree
from branch_and_bound import bnb_tsp

def run_algorithm_with_timeout(algorithm_func, distance_matrix, timeout, algorithm_name, verbose):
    start_time = time.time()
    result = None
    if timeout is None:
        result = algorithm_func(distance_matrix, None, verbose)
    else:
        while time.time() - start_time < timeout:
            result = algorithm_func(distance_matrix, timeout, verbose)
            if result:  # Algoritmo terminou, resultado válido
                break
    elapsed_time = time.time() - start_time
    if timeout is not None and elapsed_time >= timeout:
        print(f"Algoritmo {algorithm_name} foi interrompido devido ao tempo limite de {timeout} segundos.")
        return None, float('inf'), result[2], elapsed_time
    return result[0], result[1], result[2], elapsed_time

def main(file_path, options, timeout, verbose):
    dimension, node_coords, edge_weight_type = parse_tsplib(file_path)
    distance_matrix = compute_distance_matrix(node_coords, edge_weight_type)
    
    if '-t' in options or '-all' in options:
        print("Dimensão: ", dimension)
        print("TSP Solver - Twice-Around-the-Tree")
        print("------------------------------------------------------------------------")

        tatt_route, tatt_cost, flag_erro, tatt_time = run_algorithm_with_timeout(twice_around_tree, distance_matrix, timeout, "Twice-Around-the-Tree", verbose)
        if flag_erro == 1:
            print(f"Rota Aproximada (Twice-Around-the-Tree): NA (não-disponível)")
            print(f"Custo Total Aproximado (Twice-Around-the-Tree): NA (não-disponível)")
            print(f"Tempo de execução (Twice-Around-the-Tree): NA (não-disponível) segundos")
            print("------------------------------------------------------------------------")
        else:
            print(f"Rota Aproximada (Twice-Around-the-Tree): {tatt_route}")
            print(f"Custo Total Aproximado (Twice-Around-the-Tree): {tatt_cost}")
            print(f"Tempo de execução (Twice-Around-the-Tree): {tatt_time:.4f} segundos")
            print("------------------------------------------------------------------------")

    if '-c' in options or '-all' in options:
        print("TSP Solver - Christofides")
        print("------------------------------------------------------------------------")
        ch_route, ch_cost, flag_erro, ch_time = run_algorithm_with_timeout(christofides, distance_matrix, timeout, "Christofides", verbose)
        
        if flag_erro == 1:
            print(f"Rota Aproximada (Christofides): NA (não-disponível)")
            print(f"Custo Total Aproximado (Christofides): NA (não-disponível)")
            print(f"Tempo de execução (Christofides): NA (não-disponível)")
            print("------------------------------------------------------------------------")
        else:
            print(f"Rota Aproximada (Christofides): {ch_route}")
            print(f"Custo Total Aproximado (Christofides): {ch_cost}")
            print(f"Tempo de execução (Christofides): {ch_time:.4f} segundos")
            print("------------------------------------------------------------------------")

    if '-b' in options or '-all' in options:
        print("TSP Solver - Branch-and-Bound")
        print("------------------------------------------------------------------------")
        bnb_route, bnb_cost, flag_erro, bnb_time = run_algorithm_with_timeout(bnb_tsp, distance_matrix, timeout, "Branch-and-Bound", verbose)

        if flag_erro == 1:
            print(f"Custo Total (Branch-and-Bound): NA (não-disponível)")
            print(f"Rota Ótima (Branch-and-Bound): NA (não-disponível)")
            print(f"Tempo de execução (Branch-and-Bound): NA (não-disponível)")
            print("------------------------------------------------------------------------")
        else:
            print(f"Custo Total (Branch-and-Bound): {bnb_cost}")
            print(f"Rota Ótima (Branch-and-Bound): {bnb_route}")
            print(f"Tempo de execução (Branch-and-Bound): {bnb_time:.4f} segundos")
            print("------------------------------------------------------------------------")

def erro():
    print("Uso: python3 ./src/main.py <caminho_do_arquivo_teste> <opções de algoritmos> [tempo] [verbose]")
    print("\nArgumentos opcionais para escolha de algoritmos:")
    print("-c    -> Executa o algoritmo Christofides")
    print("-t    -> Executa o algoritmo Twice-Around-the-Tree")
    print("-b    -> Executa o algoritmo Branch-and-Bound")
    print("-all  -> Executa todos os algoritmos (default)")
    print("\nObs: É possível usar até 2 opções ao mesmo tempo (combinar '-c', '-t', '-b', não importando ordem)")
    print("\nArgumento opcional para tempo:")
    print("-timeout=<tempo> -> Define o tempo máximo de execução em segundos para cada algoritmo")
    print("\nObs: Caso não for passado um valor, o tempo máximo é 30min para cada algoritmo")
    print("\nArgumento opcional para profiling:")
    print("-verbose -> Ativa a saída detalhada, profiling do código para identificar os gargalos")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Erro: Menos que 2 parâmetros passados\n")
        erro()
        sys.exit(1)
    
    if len(sys.argv) > 6:
        print("Erro: Mais que 6 parâmetros passados\n")
        erro()
        sys.exit(1)
    
    file_path = sys.argv[1]
    options = sys.argv[2:] if len(sys.argv) > 2 else []

    timeout = None  # Define None como padrão para sem limite de tempo
    verbose = False  # Define False como padrão para não verbose
    valid_options = ['-c', '-t', '-b', '-all', '-verbose']

    # Separar e validar argumentos de timeout e verbose
    for option in list(options):  # Criar uma cópia da lista para iterar e modificar
        if option.startswith("-timeout="):
            try:
                timeout = float(option.split("=")[1])
                options.remove(option)
            except ValueError:
                print("Erro: valor inválido para '-timeout'")
                erro()
                sys.exit(1)
        elif option == "-verbose":
            verbose = True
            options.remove(option)

    # Validar opções restantes
    for option in options:
        if option not in valid_options[:-1]:  # Excluir '-verbose' da validação das opções de algoritmo
            print(f"Erro: Opção inválida '{option}'\n")
            erro()
            sys.exit(1)

    if timeout is not None:
        print(f"timeout = {timeout} (tempo máximo de {timeout} segundos de execução para cada algoritmo)")
    else:
        print("timeout = default (tempo máximo de 30 min de execução para cada algoritmo)")

    if not options:
        options.append('-all')  # Se nenhuma opção de algoritmo foi passada, use '-all'

    main(file_path, options, timeout, verbose)
