from typing import List
import tsplib95
import os
from datetime import datetime
import shutil

def getTspFiles(path="input") -> List[tsplib95.models.StandardProblem]:
    fileList = [f for f in os.listdir(path) if f.endswith(".tsp")]

    problemList = []

    for tspFile in fileList:
        with open(os.path.join(path,tspFile)) as file:
            problem = tsplib95.parse(file.read())
            problemList.append(problem)

    return problemList

def generateOutput(OUTPUT_FOLDER,INSTANCE_NAME,ALGORITHM_NAME,RESULTS,RESULTS_FILENAME = "results.txt",PLOT_FILENAME="plot.png"):
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    currTime = datetime.now()
    year = currTime.year
    month = currTime.month
    day = currTime.day
    hour = currTime.hour
    minute = currTime.minute
    second = currTime.second

    title = f"{INSTANCE_NAME}_{ALGORITHM_NAME}_{year}_{month}_{day}_{hour}_{minute}_{second}"

    outputPath = os.path.join(OUTPUT_FOLDER,title)
    os.mkdir(outputPath)

    results_string = f"distance;duration;path\n{RESULTS.get('distance')};{RESULTS.get('duration')};{RESULTS.get('tours')}\n"
    results_path = os.path.join(outputPath,RESULTS_FILENAME)
    with open(results_path,'w') as file:
        file.write(results_string)


    #SavePlot
    plotImage = RESULTS.get('plot')
    print(plotImage)
    if(plotImage != None):
        plot_image_path = os.path.join(outputPath,PLOT_FILENAME)
        with open(plot_image_path,'wb') as file:
            shutil.copyfileobj(plotImage, file)

def tsplib95ToNodeList(problem:tsplib95.models.StandardProblem) -> List:
    nodes = []
    for i in problem.get_nodes():
        nodes.append(problem.node_coords[i])
    return nodes

def runTest(functionList,OUTPUT_FOLDER="output",RESULTS_FILENAME="results.txt"):
    problemList = getTspFiles()
    for problem in problemList:
        print(f"[*]Ejecutando test con {problem.name}")
        for function in functionList:
            print(f"[*]Ejecutando función {function["name"]}")
            nodes = tsplib95ToNodeList(problem)
            results = function["function"](nodes)
            print(f"[+]Proceso finalizado, almacenando salidas")
            generateOutput(OUTPUT_FOLDER,
                           INSTANCE_NAME=problem.name.upper(),
                           ALGORITHM_NAME=function["name"],
                           RESULTS=results,
                           RESULTS_FILENAME=RESULTS_FILENAME
                           )
            print(f"[+]Salida almacenada correctamente.")


