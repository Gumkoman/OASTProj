from classes import *

def createNetwork(path):
    with open(path) as f:
        # print('st1art')
        # print(f.readlines())
        print(" ",f.readline().replace("\n",''))
        listOfLinks = []
        for line in f.readlines():
            if "-1" in line: break
            items = line.replace("\n",'').split(" ")
            listOfLinks.append(Link(items[0],items[1],items[2],items[3],items[4]))
        
        for item in listOfLinks:
            item.printSelf()
        return listOfLinks

def createDemands(path):
    print('demands')
    demandList = []
    with open(path) as f:
        demandsText = f.read().split("-1\n")[1]
        demands = demandsText.split("\n\n")
        for i in range(1,len(demands)):
            demandsparameters = demands[i].split("\n")
            if len(demandsparameters[0].split(' ')) != 3:
                continue
            startNode = demandsparameters[0].split(' ')[0]
            endNode = demandsparameters[0].split(' ')[1]
            volume = demandsparameters[0].split(' ')[2]
            numberOfPaths = int(demandsparameters[1])
            pathList = []
            for j in range(numberOfPaths):
                path = demandsparameters[2+j].strip().split(" ")
                pathId = path[0]
                path = path [1:]
                # print("Path id:",pathId,"path",path)
                pathList.append(DemandPath(pathId,path))
            # print(pathList)
            demandList.append(Demand(startNode,endNode,volume,pathList))
    for item in demandList:
        item.printSelf()
    return demandList
