import gzip
import numpy as np

def parse_tsplib(file_path):
    """
    Lê um arquivo .tsp da TSPLIB (compactado ou não) e retorna a dimensão, 
    as coordenadas dos nós e o tipo de peso das arestas.
    """

    if file_path.endswith('.gz'):
        open_func = gzip.open
    else:
        open_func = open

    with open_func(file_path, 'rt') as file: 
        lines = file.readlines()

    dimension = None
    node_coords = []
    edge_weight_type = "EUC_2D"  # Valor padrão
    reading_nodes = False

    for line in lines:
        line = line.strip()
        if line.startswith("DIMENSION"):
            dimension = int(line.split(":")[1].strip())
        elif line.startswith("EDGE_WEIGHT_TYPE"):
            edge_weight_type = line.split(":")[1].strip()
        elif line.startswith("NODE_COORD_SECTION"):
            reading_nodes = True
        elif line.startswith("EOF"):
            break
        elif reading_nodes:
            parts = line.split()
            node_coords.append((int(parts[0]), float(parts[1]), float(parts[2])))

    if dimension is None:
        raise ValueError("DIMENSION não encontrada no arquivo.")

    return dimension, node_coords, edge_weight_type

def compute_distance_matrix(node_coords, edge_weight_type="EUC_2D"):
    """
    Calcula a matriz de distâncias a partir das coordenadas dos nós.
    """
    num_nodes = len(node_coords)
    dist_matrix = np.zeros((num_nodes, num_nodes))

    for i in range(num_nodes):
        x1, y1 = node_coords[i][1], node_coords[i][2]
        for j in range(i + 1, num_nodes):  
            x2, y2 = node_coords[j][1], node_coords[j][2]

            if edge_weight_type == "EUC_2D":
                # Distância Euclidiana padrão
                dist = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            elif edge_weight_type == "CEIL_2D":
                # Distância Euclidiana com arredondamento para cima
                dist = np.ceil(np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
            else:
                raise ValueError(f"Tipo de distância inválido: {edge_weight_type}")

            dist_matrix[i, j] = dist
            dist_matrix[j, i] = dist 

    return dist_matrix
