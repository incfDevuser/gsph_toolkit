from typing import List
import tsplib95
import os
from datetime import datetime
import shutil
import io
import csv

DEFAULT_INPUT_FOLDER    = "input"
DEFAULT_EXPORT_FOLDER   = "output"
DEFAULT_RESULTS_FILENAME= "results.txt"
DEFAULT_PLOT_FILENAME   = "plot"

def getTspFiles(path="input") -> List[tsplib95.models.StandardProblem]:
    fileList = [f for f in os.listdir(path) if f.endswith(".tsp")]

    problemList = []

    for tspFile in fileList:
        with open(os.path.join(path,tspFile)) as file:
            problem = tsplib95.parse(file.read())
            problemList.append(problem)

    return problemList

def getBKS(tspName):
    path = os.path.join(DEFAULT_INPUT_FOLDER,"bks.txt")
    with open(path) as file:
        for line in file:
            fileLine = line.split(":")
            name = fileLine[0].strip().upper()
            bks = fileLine[1].strip()
            #print(name,bks)
            if tspName == name:
                return int(bks)

def getGapBKS(distance,bks):
    return ((distance-bks)/bks)*100

def generateTourFileString(instance,dimension,distance,optimal=False) -> io.BytesIO:

    tourFile =  f"NAME : {instance}{".opt.tour" if optimal else ".tour"}\n"
    tourFile += f"TYPE : TOUR\n"
    tourFile += f"COMMENT : {"Optimal solution of" if optimal else "Solution of"} {instance} ({distance})\n"
    tourFile += f"DIMENSION : {dimension}\n"
    tourFile += f"TOUR_SECTION\n"

    #REVISAR COMO TRANSFORMAR A TOUR...

    return tourFile

def searchAndReturnResults(OUTPUT_FOLDER=DEFAULT_EXPORT_FOLDER,RESULTS_FILENAME=DEFAULT_RESULTS_FILENAME):
    #Get All results.
    resultsInFolder = os.listdir(OUTPUT_FOLDER)
    #print(resultsInFolder)

    #get All Results files
    results = []

    for resultsF in resultsInFolder:
        path = os.path.join(OUTPUT_FOLDER,resultsF)
        fileList = [f for f in os.listdir(path) if f.startswith(RESULTS_FILENAME)]
        for resultFile in fileList:
            resultPath = os.path.join(path,resultFile)
            with open(resultPath) as file:
                csvReader = csv.DictReader(file,delimiter=";")
                for row in csvReader:
                    print(row['distance'])
                    results.append(row["distance"])



def generateOutput(OUTPUT_FOLDER,INSTANCE_NAME,ALGORITHM_NAME,RESULTS,RESULTS_FILENAME = DEFAULT_RESULTS_FILENAME,PLOT_FILENAME=f"{DEFAULT_PLOT_FILENAME}.png",INSTANCE_DIMENSION=0):
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    currTime = datetime.now()
    year = currTime.year
    month = currTime.month
    day = currTime.day
    hour = currTime.hour
    minute = currTime.minute
    second = currTime.second

    bks = getBKS(INSTANCE_NAME)

    distance = RESULTS.get('distance')
    gapbks = getGapBKS(distance,bks)

    gapbks = round(gapbks,2)

    title = f"{INSTANCE_NAME}_{ALGORITHM_NAME}_{year}_{month}_{day}_{hour}_{minute}_{second}"
    
    outputPath = os.path.join(OUTPUT_FOLDER,title)
    os.mkdir(outputPath)

    results_string = f"distance;gap;bks;duration;path\n{RESULTS.get('distance')};{gapbks};{bks};{RESULTS.get('duration')};{RESULTS.get('tours')}\n"
    results_path = os.path.join(outputPath,RESULTS_FILENAME)
    with open(results_path,'w') as file:
        file.write(results_string)

    
    """
    #SavePlot
    plotImage = RESULTS.get('plot')

    if(plotImage != None):
        plot_image_path = os.path.join(outputPath,PLOT_FILENAME)
        with open(plot_image_path,'wb') as file:
            shutil.copyfileobj(plotImage, file)
    """
    #SaveTourFile
    tourFileString = generateTourFileString(INSTANCE_NAME.lower(),INSTANCE_DIMENSION,RESULTS.get('distance'))
    tourFilePath = os.path.join(outputPath,f"{INSTANCE_NAME}.tour")
    with open(tourFilePath, 'w') as file:
        file.write(tourFileString)

def tsplib95ToNodeList(problem:tsplib95.models.StandardProblem) -> List:
    nodes = []
    for i in problem.get_nodes():
        nodes.append(problem.node_coords[i])
    return nodes

def runTest(functionList,OUTPUT_FOLDER="output",RESULTS_FILENAME="results.txt"):

    problemList = getTspFiles()
    
    resultList = []

    for problem in problemList:
        #print(f"[*]Ejecutando test con {problem.name}")

        for function in functionList:
            #print(f"[*]Ejecutando función {function["name"]}")
            nodes = tsplib95ToNodeList(problem)
            results = function["function"](nodes)

            resultList.append({
                'algorithm':function["name"],
                "name": problem.name.upper(),
                'results':results,
                'dimension':problem.dimension
            })


            #print(f"[+]Proceso finalizado, almacenando salidas")
            generateOutput(OUTPUT_FOLDER,
                           INSTANCE_NAME=problem.name.upper(),
                           ALGORITHM_NAME=function["name"],
                           RESULTS=results,
                           RESULTS_FILENAME=RESULTS_FILENAME,
                           INSTANCE_DIMENSION=problem.dimension
                           )
            #print(f"[+]Salida almacenada correctamente.")
    

    print(resultList)