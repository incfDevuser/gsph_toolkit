import argparse, importlib, time
from pathlib import Path

ALGORITHMS = {
    "tsp_clasico": ("tsp_clasico", "tsp_2opt", "plot_route"),
    "gsph_fc"   : ("gspg_fc",     "gsph_fc",  "plot_gsph_fc"),
}
parser = argparse.ArgumentParser(description="Prueba rápida de heurísticas TSP")
parser.add_argument("algoritmo", choices=ALGORITHMS.keys())
parser.add_argument("instancia", type=Path)
parser.add_argument("--plot", action="store_true", help="Generar PNG con el recorrido")
args = parser.parse_args()
mod_name, solver_name, plot_name = ALGORITHMS[args.algoritmo]
mod     = importlib.import_module(mod_name)
solver  = getattr(mod, solver_name)
plotter = getattr(mod, plot_name) if args.plot else None

nodes = mod.read_tsplib(args.instancia)
t0 = time.time()

if args.algoritmo == "gsph_fc":
    rutas, conns, length, xm, ym = solver(nodes)
else:
    tour   = solver(nodes)
    tour.append(tour[0])
    length = mod.total_path_length(tour)

t_exec = time.time() - t0
result_dir = Path(f"results_manual_test_{args.instancia.stem}")
result_dir.mkdir(exist_ok=True)
if plotter:
    if args.algoritmo == "gsph_fc":
        plotter(rutas, conns, xm, ym,
                save_path=result_dir / f"grafico_{args.algoritmo}.png")
    else:
        plotter(tour, title="TSP clásico (2-opt)",
                save_path=result_dir / f"grafico_{args.algoritmo}.png")
with open(result_dir / "resultado.txt", "w", encoding="utf-8") as f:
    f.write("── RESULTADO MANUAL TEST ──\n")
    f.write(f"Algoritmo : {args.algoritmo}\n")
    f.write(f"Instancia : {args.instancia.name}\n")
    f.write(f"Longitud total : {length:.2f}\n")
    f.write(f"Tiempo (s)     : {t_exec:.3f}\n")
print(f"{args.algoritmo} → Longitud total: {length:.2f} | "
      f"Tiempo: {t_exec:.3f}s | carpeta: {result_dir}")
