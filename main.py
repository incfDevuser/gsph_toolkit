#Arguments
import argparse, importlib, time
from pathlib import Path

import utils.tspTestLib
from algorithms.tsp_clasico import tsp_classic
from algorithms.gsph_fc.GSPHSolver import gsph_fc_test_run


parser = argparse.ArgumentParser(description="Try and Export TSP Heuristics")
parser.add_argument("-r","--run-test", action="store_true", help="Run and export tests")
parser.add_argument("-p","--plot", action="store_true", help="Allow the algorithms to export a PNG of the tours")
parser.add_argument("-t","--table-export",action="store_const",const=utils.tspTestLib.DEFAULT_TABLE_RESULTS_FILENAME, help="Search results and export a comparison table")


fList = [{"name":"GSPH_FC","function":lambda x,y:gsph_fc_test_run(x,y)},        
            #{"name":"CLASSIC_TSP","function":lambda x,y:tsp_classic(x,y)}
        ]
            
if __name__ == "__main__":
    args = parser.parse_args()
    
    if args.run_test:
        utils.tspTestLib.runTest(fList,
                                EXPORT_PLOT = args.plot)
    if args.table_export:
        print("Exporting Table")
        utils.tspTestLib.searchAndReturnResults(TABLE_RESULTS_FILENAME=f"{args.table_export}.csv");
