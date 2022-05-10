from classes import *
import copy
from math import ceil
class BruteForce:
    def __init__(self, demands, links,problemToSolve):
        self.res_list = []
        self.solutions = {}
        self.solution = []
        self.all = []
        self.links = links
        self.demands = demands
        self.dap = []
        self.ddap = []
        self.problemToSolve = problemToSolve

        self.best_cost_function = float('inf')
        for i in range(0, len(demands)):
            self.solutions[i+1] = []

    def run(self, demands):
        # print("Uruchomiono algorytm BruteForce:")
        k = list(self.solutions.keys())
        i = 0
        for demand in demands:
            self.rec(int(demand.volume), int(demand.volume), 0, len(demand.demandPaths)-1, [])
            self.solutions[k[i]] = copy.deepcopy(self.solution)
            del self.solution[:]
            i += 1
        self.allSolutions()

    def rec(self, volume, max_volume, level, max_level, trace):
        volumes = list(range(int(volume), -1, -1))
        for i in volumes:
            t = copy.deepcopy(trace)
            t.append(i)
            if level < max_level:
                self.rec(volume-i, max_volume, level+1, max_level, t)
            elif sum(t) == max_volume:
                self.solution.append(t)

    def allSolutions(self):
        print("Rozpoczęto tworzenie pełnej przestrzeni rozwiązań")
        d_keys = list(self.solutions.keys())
        self.all = copy.deepcopy(self.solutions[d_keys[0]])
        l = []
        i = 0
        f = open("debug.txt","w+")
        f.close()
        for d in d_keys[1:]:
            for e in self.all:
                for u in self.solutions[d]:
                    if (len(l)+1>81000):
                        break
                    # f = open("debug.txt","a+")
                    # f.write(str(len(l))+"\n")
                    # f.close()
                    try:
                        if i==0:
                            l.append([e] + [u])
                        else:
                            l.append(e + [u])
                    except:
                        break
            del self.all[:]
            i = 1
            for e in l:
                try:
                    self.all.append(e)
                except:
                    break
            del l[:]
        for z in self.all:
            self.Solution(z)
        self.findBestSolution()

    def Solution(self, z):
        load = []
        numOfLinks = len(self.links)
        tempResult = [0] * numOfLinks
        tempDDAPResult = [0] * numOfLinks
        resultDAP = [0] * numOfLinks
        resultDDAP = [0] * numOfLinks
        for i in range(len(z)):
            # print(z)
            for j in range(len(z[i])):
                for l in range(len(self.links)):
                    # print(self.demands[i])
                    # print(self.demands[i].demandPaths[j])
                    if(l+1 in self.demands[i].demandPaths[j].link_list):
                        tempResult[l] += z[i][j]

        ##DAP
        if self.problemToSolve == "DAP":
            for e in range(len(self.links)):
                resultDAP[e] = tempResult[e]-self.links[e].fibersInCable * self.links[e].numOfLambdas
            self.dap.append(max(resultDAP))
        else:
            
        #DDAP
            cost = 0
            for e in range(len(self.links)):
                # resultDDAP[e] = int(tempResult[e]/self.links[e].numOfLambdas)
                cost += ceil(tempResult[e]/self.links[e].numOfLambdas) * self.links[e].fiberCost
            self.ddap.append(cost)

            
    def findBestSolution(self):
        
        if self.problemToSolve == "DAP":
            f = open("Bf_results_DAP.txt","w+")
            maximum = min(self.dap)
            f.write("Uzyskano najlepszy wynik: "+ str(maximum) + "dla następujących kombinacji\n")
            for i in range(len(self.dap)):
                if self.dap[i] == maximum:
                    # print(self.dap[i],"tab",i,"asd",self.all[i])
                    f.write("ID:"+str(i)+" "+str(self.all[i])+'\n')
            f.close()

        else:
            f = open("Bf_results_DDAP.txt","w+")
            maximum = min(self.ddap)
            f.write("Uzyskano najlepszy wynik: "+ str(maximum) + "dla następujących kombinacji\n")
            for i in range(len(self.ddap)):
                if self.ddap[i] == maximum:
                    # print(self.ddap[i],"tab",i,"asd",self.all[i])
                    f.write("ID:"+str(i)+" "+str(self.all[i])+'\n')
            f.close()
        print("Zakończono działanie algorytmu dla Brute Force")

    # def SolutionDDAP(self, z):
    #     cost = 0
    #     for i in range(len(z)):
    #         for path in self.demands[i].demandPaths:
    #             for j in range(len(path.link_list)):
    #                 cost += (self.links[path.link_list[j] - 1].fiberCost * z[i][int(path.id_demand_path) - 1])
    #     self.ddap.append(cost)

    # def WriteAllSolution(self):
    #     file_all = open("testwynik.txt","w+")
    #     i = 1
    #     t = 0
    #     for a in self.all:
    #         line = str(a)
    #         file_all.write(line+'\n')
    #         line = 'Id: ' + str(i) + ' DAP: ' + str(self.dap[t]) + ' DDAP: ' + str(self.ddap[t])
    #         file_all.write(line+'\n')
    #         i += 1
    #         t += 1
    #     file_all.close()

    # def BestSolution(self):
    #     print("Szukanie najlepszego rozwiązania")
    #     costs = []
    #     best_cost = []
    #     id_costs = []
    #     id_best_costs = []
    #     i = 1

    #     for c in self.ddap:
    #         costs.append(c)
    #         id_costs.append(i)
    #         i += 1

    #     i = 0
    #     bestcost = min(costs)
    #     for co in costs:
    #         if co == bestcost:
    #             best_cost.append(co)
    #             id_best_costs.append(id_costs[i])
    #         i += 1

    #     load = []
    #     for i in id_best_costs:
    #         load.append(self.dap[i-1])

    #     bestload = max(load)

    #     id_best_solution = []
    #     cost_best_solution = []
    #     load_best_solution = []
    #     i = 0
    #     for l in load:
    #         if l == bestload:
    #             id_best_solution.append(id_best_costs[i])
    #             cost_best_solution.append(best_cost[i])
    #             load_best_solution.append(l)
    #         i += 1

    #     best_solution = []
    #     for z in id_best_solution:
    #         best_solution.append(self.all[z])

    #     file_all = open("testwynik123.txt","w+")
    #     k = 0
    #     print("Zanaleziono najlepsze rozwiązanie:")
    #     for a in best_solution:
    #         line = str(a)
    #         print(line)
    #         file_all.write(line+'\n')
    #         line = 'Id: ' + str(id_best_solution[k]) + ' DAP: ' + str(load_best_solution[k]) + ' DDAP: ' + str(cost_best_solution[k])
    #         file_all.write(line+'\n')
    #         print(line)
    #         k += 1
    #     file_all.close()
    #     print("Algorytm Brute Force zakończył działanie")