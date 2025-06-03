import utils.tspTestLib
from algorithms.tsp_clasico import tsp_classic
from algorithms.gspg_fc import gspg_fc_run

if __name__ == "__main__":

    fList = [
            {"name":"GSPH_FC","function":lambda x:gspg_fc_run(x)},        
            {"name":"CLASSIC_TSP","function":lambda x:tsp_classic(x)}
            ]
    utils.tspTestLib.runTest(fList)
    

    #utils.tspTestLib.searchAndReturnResults();
