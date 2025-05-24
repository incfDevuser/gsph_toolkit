from typing import List
import tsplib95
import os
from datetime import datetime

def getTspFiles(path="input") -> List[tsplib95.models.StandardProblem]:
    fileList = [f for f in os.listdir(path) if f.endswith(".tsp")]

    problemList = []

    for tspFile in fileList:
        with open(os.path.join(path,tspFile)) as file:
            problem = tsplib95.parse(file.read())
            problemList.append(problem)

    return problemList

def generateOutput(OUTPUT_FOLDER,INSTANCE_NAME,ALGORITHM_NAME,RESULTS,RESULTS_FILENAME = "results.txt"):
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

    results_string = f"distance;duration;path\n{RESULTS.get('distance')};{RESULTS.get('duration')};{RESULTS.get('path')}\n"
    results_path = os.path.join(outputPath,RESULTS_FILENAME)
    with open(results_path,'w') as file:
        file.write(results_string)

def runTest(functionList):
    problemList = getTspFiles()
    for problem in problemList:
        for function in functionList:
            results = function(problem)
