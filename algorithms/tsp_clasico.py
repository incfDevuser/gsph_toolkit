import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean
import time
import io
def read_tsplib(filename):
    nodes = []
    with open(filename, 'r') as f:
        reading_nodes = False
        for line in f:
            line = line.strip()
            if line == "NODE_COORD_SECTION":
                reading_nodes = True
                continue
            if line == "EOF":
                break
            if reading_nodes:
                parts = line.split()
                if len(parts) >= 3:
                    x, y = float(parts[1]), float(parts[2])
                    nodes.append((x, y))
    return nodes
def euclidean_distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))
def total_path_length(path):
    return sum(euclidean_distance(path[i], path[i+1]) for i in range(len(path)-1))
def tsp_2opt(points, max_iter=2000):
    def two_opt_swap(route, i, k):
        return route[:i] + route[i:k+1][::-1] + route[k+1:]
    best = points[:]
    best_distance = total_path_length(best)
    improved = True
    iter_count = 0
    while improved and iter_count < max_iter:
        improved = False
        for i in range(1, len(points) - 2):
            for k in range(i + 1, len(points)):
                new_route = two_opt_swap(best, i, k)
                new_distance = total_path_length(new_route)
                if new_distance < best_distance:
                    best = new_route
                    best_distance = new_distance
                    improved = True
        iter_count += 1
    return best
def plot_route(path, title="Recorrido",save_on_memory=False):
    x, y = zip(*path)
    plt.figure(figsize=(8,8))
    plt.plot(x + (x[0],), y + (y[0],), marker='o')
    plt.title(title)
    plt.grid(True)

    # Save on Buffer
    if save_on_memory:
        buf = io.BytesIO()
        plt.savefig(buf, bbox_inches='tight')
        buf.seek(0)  # Rewind the buffer to the beginning
        plt.close()
        return buf    
    else:
        plt.show()


# Code for tspTestLib
def tsp_classic(nodes,plot):
    start_2opt  = time.process_time()
    tsp_path    = tsp_2opt(nodes)

    tsp_path.append(tsp_path[0])

    tsp_len     = total_path_length(tsp_path)
    end_2opt    = time.process_time()
    
    if plot:
        plotImage  = plot_route(tsp_path, title="TSP clásico (2-opt) recorrido",save_on_memory=True)
    else:
        plotImage = None
    
    return {"duration": end_2opt-start_2opt,
            "distance": tsp_len,
            "tours":[tsp_path],
            "plotImage":plotImage}

"""
if __name__ == "__main__":
    nodes = read_tsplib('a280.tsp')
    start_2opt = time.time()
    tsp_path = tsp_2opt(nodes)
    tsp_path.append(tsp_path[0])
    tsp_len = total_path_length(tsp_path)
    end_2opt = time.time()
    print(f"2-OPT Global - Longitud total: {round(tsp_len,2)}")
    print(f"2-OPT Global - Tiempo: {round(end_2opt-start_2opt,2)}s")
    plot_route(tsp_path, title="TSP clásico (2-opt) recorrido")

"""
