from typing import List
from .City import City

class Map:
    cityList: List[City]
    distanceMatrix: List[List[int]]

    def __init__(self):
        self.cityList = []
        self.distanceMatrix = []
    

    def loadTspLib(self,filename):
        cityList: List[City] = []

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
                        tmpCity = City(x,y)
                        cityList.append(tmpCity)
            self.cityList = cityList
    
    def loadNodeList(self,nodes):
        tmpCityList = []
        for i in range(len(nodes)):
            node = nodes[i]
            tmpCity = City(node[0],node[1])
            tmpCityList.append(tmpCity)
        self.cityList = tmpCityList
            

    def calculateMatrix(self):
        for i in range( len(self.cityList)-1 ):
            tmpCityDistances=[]
            for j in range( len(self.cityList)-1):
                distance = self.cityList[i].calculateDistance(self.cityList[j])
                tmpCityDistances.append(distance)
            self.distanceMatrix.append(tmpCityDistances)
        
        print(self.distanceMatrix)
    
    def getPoints(self):
        points = []
        for i in self.cityList:
            points.append([i.x,i.y])
        return points