import networkx as nx
import time
import cProfile
import pstats

INF = float('inf')

# Define o limite de tempo padrão global (em segundos)
LIMIT = 30 * 60 # 30 min

def twice_around_tree(distance_matrix, timeout=None, verbose=False):
    """
    Implementa o algoritmo Twice-Around-the-Tree para o problema do TSP.
    """

    if verbose == True:
        profiler = cProfile.Profile()
        profiler.enable()

        flag_erro = 0  # Declarando flag_erro

        start_time = time.time()
        timeout = timeout if timeout is not None else LIMIT

        #print("timeout twice_around_tree = ", timeout)

        def check_time():
            nonlocal flag_erro  # Acessando e modificando flag_erro da função externa
            if time.time() - start_time > timeout:
                print("Tempo limite excedido para o algoritmo Twice-Around-the-Tree")
                flag_erro = 1
                return True  # Indica que o tempo foi excedido
            return False  # Caso contrário, continua normalmente

        num_nodes = len(distance_matrix)
        graph = nx.Graph()

        # Construir o grafo a partir da matriz de distâncias
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                graph.add_edge(i, j, weight=distance_matrix[i][j])
        
        if check_time(): return [], INF, flag_erro

        # Construir a Árvore Geradora Mínima (MST)
        mst = nx.minimum_spanning_tree(graph)

        if check_time(): return [], INF, flag_erro

        # Seja dfs_nodes a lista de vértices de mst em pré-ordem a partir de root
        dfs_nodes = list(nx.dfs_preorder_nodes(mst, source=0))

        if check_time(): return [], INF, flag_erro

        # Adiciona o vértice inicial no final de dfs_nodes para fechar o ciclo
        dfs_nodes.append(dfs_nodes[0])

        # Calcula o custo diretamente da matriz de distâncias
        total_cost = sum(
            distance_matrix[dfs_nodes[i]][dfs_nodes[i + 1]] for i in range(len(dfs_nodes) - 1)
        )

        if check_time(): return [], INF, flag_erro

        profiler.disable()
        stats = pstats.Stats(profiler)
        stats.strip_dirs()
        stats.sort_stats(pstats.SortKey.TIME)
        stats.print_stats()

        return dfs_nodes, total_cost, flag_erro
    else:
        
        flag_erro = 0  # Declarando flag_erro

        start_time = time.time()
        timeout = timeout if timeout is not None else LIMIT

        #print("timeout twice_around_tree = ", timeout)

        def check_time():
            nonlocal flag_erro  # Acessando e modificando flag_erro da função externa
            if time.time() - start_time > timeout:
                print("Tempo limite excedido para o algoritmo Twice-Around-the-Tree")
                flag_erro = 1
                return True  # Indica que o tempo foi excedido
            return False  # Caso contrário, continua normalmente

        num_nodes = len(distance_matrix)
        graph = nx.Graph()

        # Construir o grafo a partir da matriz de distâncias
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                graph.add_edge(i, j, weight=distance_matrix[i][j])
        
        if check_time(): return [], INF, flag_erro

        # Construir a Árvore Geradora Mínima (MST)
        mst = nx.minimum_spanning_tree(graph)

        if check_time(): return [], INF, flag_erro

        # Seja dfs_nodes a lista de vértices de mst em pré-ordem a partir de root
        dfs_nodes = list(nx.dfs_preorder_nodes(mst, source=0))

        if check_time(): return [], INF, flag_erro

        # Adiciona o vértice inicial no final de dfs_nodes para fechar o ciclo
        dfs_nodes.append(dfs_nodes[0])

        # Calcula o custo diretamente da matriz de distâncias
        total_cost = sum(
            distance_matrix[dfs_nodes[i]][dfs_nodes[i + 1]] for i in range(len(dfs_nodes) - 1)
        )

        if check_time(): return [], INF, flag_erro

        return dfs_nodes, total_cost, flag_erro
