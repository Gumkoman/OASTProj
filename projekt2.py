from os import link
import pathlib
import itertools as IT
import os
from classes import *
import BurteForce as bf

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
                pathList.append(path)
            # print(pathList)
            demandList.append(Demand(startNode,endNode,volume,pathList))
    for item in demandList:
        item.printSelf()
    return demandList

def createCombinations(volume,numOfPaths):
    for choice in IT.combinations(range(volume+numOfPaths-1),volume):
        # slot = [c-i for i,c in enumerate(choice)]
        slot = []
        for i,j in enumerate(choice):
            slot.append(j-i)
        result = [0] * numOfPaths
        for i in slot:
            result[i] += 1
        yield result

# def brutForce(demands,links):
#     demandGenes = []
#     for demand in demands:
#         combinations = createCombinations(demand.volume,len(demand.paths))
#         genes = []
#         for i in combinations:
#             temp = {'volume':demand.volume,'PathFlowList':i}
#             genes.append(temp)
#         demandGenes.append(genes)
    # if os.path.exists():
    #     pass
    # else:
    #     pass
    # if True:
    #     print("saving to txt")
    #     myProd = IT.product(demandGenes)
    #     print("TEST")
    #     with open("brutforceSolution.txt","w") as f:
    #         for prod in myProd:
    #             # print("prod",len(prod),prod)
    #             f.write("Solution: ")
    #             for item in prod[0]:
    #                 f.write('  ')
    #                 f.write(' '.join([str(elem) for elem in item['PathFlowList']]))
    #                 f.write(' ')
    #                 f.write(str(item['volume']))
    #             f.write("\n")


def main():
    linkList = createNetwork("net4.txt")
    demandList = createDemands("net4.txt")
    # linkList = createNetwork("net12_2.txt")
    # demandList = createDemands("net12_2.txt")
    brutForce  = bf.BruteForce(demandList,linkList)
    brutForce.run(demandList)

if __name__ == "__main__":
    main()