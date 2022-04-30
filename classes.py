class Link:
    def __init__(self,startNode,endNode,fibersInCable,fiberCost,numOfLambdas):
        self.startNode = int(startNode)
        self.endNode = int(endNode)
        self.fibersInCable = int(fibersInCable)
        self.fiberCost = int(fiberCost)
        self.numOfLambdas = int(numOfLambdas)
    def printSelf(self):
        print("startNode:",self.startNode,"endNode:",self.endNode,"fibersInCable:",self.fibersInCable,"fiberCost:",self.fiberCost,"numOfLambdas:",self.numOfLambdas)

class Demand:
    def __init__(self,startNode,endNode,volume,paths):
        self.startNode = int(startNode)
        self.endNode = int(endNode)
        self.volume = int(volume)
        self.demandPaths = paths
    def printSelf(self):
        print(self.startNode,self.endNode,self.volume,self.demandPaths)

class DemandPath:
    def __init__(self, id_demand_path, link_list):
        self.id_demand_path = id_demand_path
        self.link_list = [int(i) for i in link_list]