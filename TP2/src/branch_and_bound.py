import math
import time
import cProfile
import pstats
from heapq import heappush, heappop

INF = float('inf')

# Define o limite de tempo padrão global (em segundos)
LIMIT = 30 * 60 # 30 min

class Node:
    def __init__(self, bound, cost, level, path):
        self.bound = bound
        self.cost = cost
        self.level = level
        self.path = path

    def __lt__(self, other):
        return self.bound < other.bound

    def __str__(self):
        return f"Bound: {self.bound}, Cost: {self.cost}, Level: {self.level}, Path: {self.path}"

def two_min_edge(adj, i):
    """
    Retorna as duas menores arestas conectadas ao nó i em O(n).
    """
    first_min, second_min = INF, INF
    for j in range(len(adj)):
        if j != i:
            weight = adj[i][j]
            if weight < first_min:
                second_min = first_min
                first_min = weight
            elif weight < second_min:
                second_min = weight
    return first_min, second_min

def bound(adj, path, current_cost):
    """
    Calcula o limite inferior (bound) do caminho atual de forma incremental.
    """
    N = len(adj)
    bound = current_cost
    unvisited = set(range(N)) - set(path)

    # Soma as menores arestas para nós não visitados
    for i in unvisited:
        first, second = two_min_edge(adj, i)
        bound += (first + second) / 2

    # Adiciona a aresta do último nó no caminho ao próximo não visitado
    if len(path) > 1:
        last_node = path[-1]
        first_unvisited = next(iter(unvisited), None)
        if first_unvisited is not None:
            bound += adj[last_node][first_unvisited]

    return math.ceil(bound)

def greedy_tsp(adj):
    """
    Algoritmo guloso para obter uma solução inicial.
    """
    N = len(adj)
    visited = [False] * N
    path = [0]
    visited[0] = True
    cost = 0

    while len(path) < N:
        last = path[-1]
        next_city = min((adj[last][j], j) for j in range(N) if not visited[j])[1]
        cost += adj[last][next_city]
        path.append(next_city)
        visited[next_city] = True

    cost += adj[path[-1]][0]
    path.append(0)
    return path, cost

def bnb_tsp(adj, timeout=None, verbose=False):
    """
    Resolve o TSP usando o algoritmo otimizado de Branch-and-Bound.
    Interrompe se o tempo de execução exceder o limite (timeout).
    """

    if verbose == True:
        profiler = cProfile.Profile()
        profiler.enable()

        flag_erro = 0

        timeout = timeout if timeout is not None else LIMIT
        #print("timeout branch_and_bound = ", timeout)

        N = len(adj)
        pq = []
        
        # Inicia a contagem do tempo
        start_time = time.time()
        
        best_path, best_cost = greedy_tsp(adj)
        root = Node(bound(adj, [0], 0), 0, 0, [0])
        heappush(pq, root)

        while pq:
            # Verifica o tempo decorrido
            if time.time() - start_time > timeout:
                print("Tempo limite excedido para o algoritmo Branch-and-Bound")
                flag_erro = 1
                return [], INF, flag_erro # Retorna uma solução inválida

            node = heappop(pq)

            # Apenas explora nós com bound menor que o melhor custo
            if node.bound < best_cost:
                if node.level == N - 1:
                    last_to_start = adj[node.path[-1]][0]
                    current_cost = node.cost + last_to_start
                    if current_cost < best_cost:
                        best_cost = current_cost
                        best_path = node.path + [0]
                else:
                    for i in range(N):
                        if i not in node.path:
                            new_path = node.path + [i]
                            new_cost = node.cost + adj[node.path[-1]][i]
                            if new_cost < best_cost:  # Poda imediata
                                new_bound = bound(adj, new_path, new_cost)
                                if new_bound < best_cost:
                                    child_node = Node(new_bound, new_cost, node.level + 1, new_path)
                                    heappush(pq, child_node)

        profiler.disable()
        stats = pstats.Stats(profiler)
        stats.strip_dirs()
        stats.sort_stats(pstats.SortKey.TIME)
        stats.print_stats()

        return best_path, best_cost, flag_erro
    else:
        
        flag_erro = 0

        timeout = timeout if timeout is not None else LIMIT
        #print("timeout branch_and_bound = ", timeout)

        N = len(adj)
        pq = []
        
        # Inicia a contagem do tempo
        start_time = time.time()
        
        best_path, best_cost = greedy_tsp(adj)
        root = Node(bound(adj, [0], 0), 0, 0, [0])
        heappush(pq, root)

        while pq:
            # Verifica o tempo decorrido
            if time.time() - start_time > timeout:
                print("Tempo limite excedido para o algoritmo Branch-and-Bound")
                flag_erro = 1
                return [], INF, flag_erro # Retorna uma solução inválida

            node = heappop(pq)

            # Apenas explora nós com bound menor que o melhor custo
            if node.bound < best_cost:
                if node.level == N - 1:
                    last_to_start = adj[node.path[-1]][0]
                    current_cost = node.cost + last_to_start
                    if current_cost < best_cost:
                        best_cost = current_cost
                        best_path = node.path + [0]
                else:
                    for i in range(N):
                        if i not in node.path:
                            new_path = node.path + [i]
                            new_cost = node.cost + adj[node.path[-1]][i]
                            if new_cost < best_cost:  # Poda imediata
                                new_bound = bound(adj, new_path, new_cost)
                                if new_bound < best_cost:
                                    child_node = Node(new_bound, new_cost, node.level + 1, new_path)
                                    heappush(pq, child_node)

        return best_path, best_cost, flag_erro
