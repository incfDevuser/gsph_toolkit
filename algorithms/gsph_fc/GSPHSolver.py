from typing import List
from .Map import Map
from .City import City
from .Route import Route
from time import process_time
import numpy as np

class GSPHSolver:
    EPS_FRONTIER :int
    MAX_ITER_LOCAL: int

    tspMap:Map

    def __init__(self,nodes,EPS_FRONTIER=5,MAX_ITER_LOCAL=800):
        self.EPS_FRONTIER = EPS_FRONTIER
        self.MAX_ITER_LOCAL = MAX_ITER_LOCAL

        #Load Map
        tmpMap = Map()
        tmpMap.loadNodeList(nodes)
        self.tspMap = tmpMap
        pass

    def tsp_2opt(self,pts,max_iter = 800):
        def two_opt_swap(r, i, k):
            return r[:i] + r[i:k+1][::-1] + r[k+1:]
        
        mapSize = len(self.tspMap.cityList)
        best = self.tspMap.cityList[:]
        tmpRoute = Route(best)
        tmpRoute.calculateCost()

        best_dist = tmpRoute.cost

        changed, it = True, 0
        while changed and it < max_iter:
            changed = False
            for i in range(1, mapSize-2):
                for k in range(i+1, mapSize):
                    new = two_opt_swap(best, i, k)

                    newRoute = Route(new)
                    newRoute.calculateCost
                    
                    new_dist = newRoute.cost
                    if new_dist < best_dist:
                        best, best_dist, changed = new, new_dist, True
            it += 1
        return best
    
    def euclidean_distance(self,p1, p2):
        dist = np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
        return int(dist + 0.5)

    def total_path_length(self,path):
        return sum(self.euclidean_distance(path[i], path[i+1]) for i in range(len(path)-1))
    
    def subdivide_quadrants(self):
        pts = self.tspMap.getPoints()
        xs, ys = zip(*pts)
        xmid, ymid = (min(xs)+max(xs))/2, (min(ys)+max(ys))/2
        quads = {'Q1':[], 'Q2':[], 'Q3':[], 'Q4':[]}
        for p in pts:
            x, y = p
            if x <= xmid and y >  ymid: quads['Q1'].append(p)
            elif x >  xmid and y >  ymid: quads['Q2'].append(p)
            elif x <= xmid and y <= ymid: quads['Q3'].append(p)
            else: quads['Q4'].append(p)
        return quads, xmid, ymid

    def best_frontier_pair(self,A, B, direction, mid, eps):
        filt = (lambda p: abs(p[0]-mid)<eps) if direction=='vertical' else (lambda p: abs(p[1]-mid)<eps)
        candA = [p for p in A if filt(p)]
        candB = [p for p in B if filt(p)]
        best, best_d = (None,None), float('inf')
        for a in candA:
            for b in candB:
                d = self.euclidean_distance(a,b)
                if d < best_d:
                    best, best_d = (a,b), d
        return best, best_d
    
    def resolve(self):

        quads, xmid, ymid = self.subdivide_quadrants()
        routes = {}
        for q, pts in quads.items():
            #print(pts)
            if len(pts) > 1:
                rt = self.tsp_2opt(pts,self.MAX_ITER_LOCAL)
                routes[q] = rt
            else:
                routes[q] = pts
        neighbor_pairs = [
            ('Q1','Q2','vertical',  xmid),
            ('Q1','Q3','horizontal',ymid),
            ('Q2','Q4','horizontal',ymid),
            ('Q3','Q4','vertical',  xmid)
        ]
        connections = []
        inter_len   = 0
        for q1,q2,dirc,mid in neighbor_pairs:
            (a,b), d = self.best_frontier_pair(quads[q1], quads[q2], dirc, mid, self.EPS_FRONTIER)
            if a and b:
                connections.append((a,b))
                inter_len += d
                
        #sub_len = sum(self.total_path_length(r) for r in routes.values())
        sub_len  = 0
        print(len(routes['Q2']))
        for r in routes.values():
            tmpRoute = Route(r)
            tmpRoute.calculateCost()
            sub_len += tmpRoute.cost
        
        return routes, connections, sub_len+inter_len, xmid, ymid


# Code for tspTestLib, NO PLOT!
def gsph_fc_test_run(nodes,plot):
    solver = GSPHSolver(nodes)
    t0      = process_time()
    routes, conns, total_length, xm, ym = solver.resolve()
    t_heur  = process_time() - t0
    
    if plot:
        #plotImage   = plot_gsph_fc(routes,conns,xm,ym,None,save_on_memory=True)
        pass
    else:
        plotImage = None

    return {"duration": t_heur,
            "distance": total_length,
            "tours":routes,
            "conns":conns,
            "xm":xm,
            "ym":ym,
            "plotImage":plotImage}


    
"""
    def plot_result(self,routes, conns, xmid, ymid, save_path=None,save_on_memory=False):
        plt.figure(figsize=(8,8))
        colors = ['blue', 'green', 'red', 'orange']
        for idx, (q, r) in enumerate(routes.items()):
            if len(r) > 1:
                x, y = zip(*r)
                plt.plot(x, y, marker='o', color=colors[idx])
            else:
                plt.scatter(*r[0], color='black', marker='x')
        subroutes = list(routes.values())
        for i in range(len(subroutes)-1):
            last_point = subroutes[i][-1]
            next_point = subroutes[i+1][0]
            plt.plot([last_point[0], next_point[0]], [last_point[1], next_point[1]],
                    linestyle='--', color='black', linewidth=2)
        last_to_first = (subroutes[-1][-1], subroutes[0][0])
        plt.plot([last_to_first[0][0], last_to_first[1][0]],
                [last_to_first[0][1], last_to_first[1][1]],
                linestyle='--', color='black', linewidth=2)
        plt.axvline(xmid, linestyle='--', color='blue')
        plt.axhline(ymid, linestyle='--', color='blue')
        plt.title("GSPH–FC aplicado a instancia TSPLIB")
        plt.grid(True)
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        
        # Save on Buffer
        if save_on_memory:
            buf = io.BytesIO()
            plt.savefig(buf, bbox_inches='tight')
            buf.seek(0)  # Rewind the buffer to the beginning
            plt.close()
            return buf
        else:
            plt.close()
"""