from typing import List
from .City import City
    
class Route:
    cityList:List[City] = []
    cost: int

    def __init__(self,cityList):
        self.cityList   = cityList
        self.cost       = 0
    
    def calculateCost(self):
        cost = 0
        for i in range(len(self.cityList)-1):
            cost += self.cityList[i].calculateDistance(self.cityList[i+1])

        self.cost = cost
             