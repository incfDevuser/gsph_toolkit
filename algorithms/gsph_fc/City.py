import numpy as np

class City:
    x: float
    y: float

    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y

    def calculateDistance(self,otherCity):
        dist = np.sqrt((self.x- otherCity.x)**2 + (self.y-otherCity.y)**2)
        return int(dist + 0.5)