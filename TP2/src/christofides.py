import networkx as nx
import time
import cProfile
import pstats

INF = float('inf')

# Define o limite de tempo padrão global (em segundos)
LIMIT = 30 * 60 # 30 min

def christofides(distance_matrix, timeout=None, verbose=False):
    """
    Implementa o algoritmo de Christofides para resolver o problema do TSP.
    """
    if verbose == True:
        profiler = cProfile.Profile()
        profiler.enable()

        flag_erro = 0  # Declarando flag_erro

        start_time = time.time()
        timeout = timeout if timeout is not None else LIMIT

        #print("timeout christofides = ", timeout)

        def check_time():
            nonlocal flag_erro  # Acessando e modificando flag_erro da função externa
            if time.time() - start_time > timeout:
                print("Tempo limite excedido para o algoritmo Christofides")
                flag_erro = 1
                return True  # Indica que o tempo foi excedido
            return False  # Caso contrário, continua normalmente

        num_nodes = len(distance_matrix)
        graph = nx.Graph()

        # Construir o grafo a partir da matriz de distâncias
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                if distance_matrix[i][j] != INF:  # Evitar adicionar arestas desnecessárias
                    graph.add_edge(i, j, weight=distance_matrix[i][j])

        if check_time(): return [], INF, flag_erro  # Verificando logo no início

        # Construir a Árvore Geradora Mínima (MST)
        mst = nx.minimum_spanning_tree(graph)
        if check_time(): return [], INF, flag_erro  # Verificando após a criação da MST

        # Encontrar os nós com grau ímpar na MST
        odd_degree_nodes = [node for node in mst.nodes if mst.degree[node] % 2 == 1]
        if check_time(): return [], INF, flag_erro  # Verificando após encontrar nós de grau ímpar

        # Construir um subgrafo completo dos nós de grau ímpar
        odd_graph = nx.Graph()
        for i in range(len(odd_degree_nodes)):
            for j in range(i + 1, len(odd_degree_nodes)):
                u = odd_degree_nodes[i]
                v = odd_degree_nodes[j]
                odd_graph.add_edge(u, v, weight=distance_matrix[u][v])

        if check_time(): return [], INF, flag_erro  # Verificando após a construção do subgrafo

        # Encontrar o emparelhamento mínimo perfeito
        min_matching = nx.algorithms.matching.min_weight_matching(odd_graph)
        if check_time(): return [], INF, flag_erro  # Verificando após o emparelhamento

        # Adicionar as arestas do emparelhamento mínimo perfeito à MST
        multigraph = nx.MultiGraph(mst)
        for u, v in min_matching:
            multigraph.add_edge(u, v, weight=distance_matrix[u][v])

        if check_time(): return [], INF, flag_erro  # Verificando após adicionar arestas

        # Encontrar o circuito Euleriano no multigrafo
        eulerian_circuit = list(nx.eulerian_circuit(multigraph, source=0))
        if check_time(): return [], INF, flag_erro  # Verificando após o circuito Euleriano

        # Transformar o circuito Euleriano em uma solução para o TSP (Remover duplicatas)
        visited = set()
        tsp_route = []
        for u, _ in eulerian_circuit:
            if u not in visited:
                tsp_route.append(u)
                visited.add(u)
        tsp_route.append(tsp_route[0])  # Fechar o ciclo

        # Calcular o custo da rota
        total_cost = sum(
            distance_matrix[tsp_route[i]][tsp_route[i + 1]] for i in range(len(tsp_route) - 1)
        )

        if check_time(): return [], INF, flag_erro  # Verificando após o cálculo do custo

        profiler.disable()
        stats = pstats.Stats(profiler)
        stats.strip_dirs()
        stats.sort_stats(pstats.SortKey.TIME)
        stats.print_stats()

        return tsp_route, total_cost, flag_erro
    else:
        flag_erro = 0  # Declarando flag_erro

        start_time = time.time()
        timeout = timeout if timeout is not None else LIMIT

        #print("timeout christofides = ", timeout)

        def check_time():
            nonlocal flag_erro  # Acessando e modificando flag_erro da função externa
            if time.time() - start_time > timeout:
                print("Tempo limite excedido para o algoritmo Christofides")
                flag_erro = 1
                return True  # Indica que o tempo foi excedido
            return False  # Caso contrário, continua normalmente

        num_nodes = len(distance_matrix)
        graph = nx.Graph()

        # Construir o grafo a partir da matriz de distâncias
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                if distance_matrix[i][j] != INF:  # Evitar adicionar arestas desnecessárias
                    graph.add_edge(i, j, weight=distance_matrix[i][j])

        if check_time(): return [], INF, flag_erro  # Verificando logo no início

        # Construir a Árvore Geradora Mínima (MST)
        mst = nx.minimum_spanning_tree(graph)
        if check_time(): return [], INF, flag_erro  # Verificando após a criação da MST

        # Encontrar os nós com grau ímpar na MST
        odd_degree_nodes = [node for node in mst.nodes if mst.degree[node] % 2 == 1]
        if check_time(): return [], INF, flag_erro  # Verificando após encontrar nós de grau ímpar

        # Construir um subgrafo completo dos nós de grau ímpar
        odd_graph = nx.Graph()
        for i in range(len(odd_degree_nodes)):
            for j in range(i + 1, len(odd_degree_nodes)):
                u = odd_degree_nodes[i]
                v = odd_degree_nodes[j]
                odd_graph.add_edge(u, v, weight=distance_matrix[u][v])

        if check_time(): return [], INF, flag_erro  # Verificando após a construção do subgrafo

        # Encontrar o emparelhamento mínimo perfeito
        min_matching = nx.algorithms.matching.min_weight_matching(odd_graph)
        if check_time(): return [], INF, flag_erro  # Verificando após o emparelhamento

        # Adicionar as arestas do emparelhamento mínimo perfeito à MST
        multigraph = nx.MultiGraph(mst)
        for u, v in min_matching:
            multigraph.add_edge(u, v, weight=distance_matrix[u][v])

        if check_time(): return [], INF, flag_erro  # Verificando após adicionar arestas

        # Encontrar o circuito Euleriano no multigrafo
        eulerian_circuit = list(nx.eulerian_circuit(multigraph, source=0))
        if check_time(): return [], INF, flag_erro  # Verificando após o circuito Euleriano

        # Transformar o circuito Euleriano em uma solução para o TSP (Remover duplicatas)
        visited = set()
        tsp_route = []
        for u, _ in eulerian_circuit:
            if u not in visited:
                tsp_route.append(u)
                visited.add(u)
        tsp_route.append(tsp_route[0])  # Fechar o ciclo

        # Calcular o custo da rota
        total_cost = sum(
            distance_matrix[tsp_route[i]][tsp_route[i + 1]] for i in range(len(tsp_route) - 1)
        )

        if check_time(): return [], INF, flag_erro  # Verificando após o cálculo do custo

        return tsp_route, total_cost, flag_erro
