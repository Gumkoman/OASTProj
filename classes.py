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


class Gene:

    def __init__(self, path_flow_list, demand_volume):
        self.path_flow_list = path_flow_list  # list of int
        # Sum of all values on list of path flows should be the same as demand_volume
        self.demand_volume = demand_volume  # int


# A chromosome holds genes, one for each given demand
# It encodes a complete feasible solution
class Chromosome:

    def __init__(self, list_of_genes, fitness=0):
        self.list_of_genes = list_of_genes  # as list of Int
        self.fitness = fitness
        # # Fitness function = the objective function

class Result:

    def __init__(self,
                 seed: int,
                 generations: int,
                 time: float,
                 population: int,
                 mutation_prob: float,
                 crossover_prob: float,
                 best_fitness: int,
                 best_chromosome: Chromosome,
                 link_load_list,
                 link_size_list,
                 network):
        self.seed = seed
        self.generations = generations
        self.time = time
        self.population = population
        self.mutation_prob = mutation_prob
        self.crossover_prob = crossover_prob
        self.best_fitness = best_fitness
        self.best_chromosome = best_chromosome
        self.link_load_list = link_load_list
        self.link_size_list = link_size_list
        self.network = network

    def get_strings(self):
        strings = [
            "Network:\t\t\t\t\t{}".format(self.network),
            "Seed:\t\t\t\t\t\t{}".format(self.seed),
            "Generations:\t\t\t\t{}".format(self.generations),
            "Time elapsed:\t\t\t\t{}".format(self.time),
            "Initial population size:\t{}".format(self.population),
            "Mutation probability:\t\t{}".format(self.mutation_prob),
            "Crossover prob. mult.:\t\t{}".format(self.crossover_prob),
            "Best fitness:\t\t\t\t{}".format(self.best_fitness),
            "\nBest chromosome:"
        ]
        d = 0
        for gene in self.best_chromosome.list_of_genes:
            d += 1
            strings.append("Demand {}: {}".format(d, str(gene.path_flow_list)))
        strings.append("Link loads (\"number of signals\"):")
        strings.append(str(self.link_load_list))
        strings.append("Link sizes (\"number of fibers\"):")
        strings.append(str(self.link_size_list))
        return strings

    def print(self):
        for line in self.get_strings():
            print(line)

    def file_write(self, problem_to_solve):
        result_file = open("results_" + problem_to_solve + ".txt", "w")
        for line in self.get_strings():
            result_file.write(line+"\n")
        result_file.close()



class Result:

    def __init__(self,
                 seed: int,
                 generations: int,
                 time: float,
                 population: int,
                 mutation_prob: float,
                 crossover_prob: float,
                 best_fitness: int,
                 best_chromosome: Chromosome,
                 link_load_list,
                 link_size_list,
                 network):
        self.seed = seed
        self.generations = generations
        self.time = time
        self.population = population
        self.mutation_prob = mutation_prob
        self.crossover_prob = crossover_prob
        self.best_fitness = best_fitness
        self.best_chromosome = best_chromosome
        self.link_load_list = link_load_list
        self.link_size_list = link_size_list
        self.network = network

    def get_strings(self):
        strings = [
            "Network:\t\t\t\t\t{}".format(self.network),
            "Seed:\t\t\t\t\t\t{}".format(self.seed),
            "Generations:\t\t\t\t{}".format(self.generations),
            "Time elapsed:\t\t\t\t{}".format(self.time),
            "Initial population size:\t{}".format(self.population),
            "Mutation probability:\t\t{}".format(self.mutation_prob),
            "Crossover prob. mult.:\t\t{}".format(self.crossover_prob),
            "Best fitness:\t\t\t\t{}".format(self.best_fitness),
            "\nBest chromosome:"
        ]
        d = 0
        for gene in self.best_chromosome.list_of_genes:
            d += 1
            strings.append("Demand {}: {}".format(d, str(gene.path_flow_list)))
        strings.append("Link loads (\"number of signals\"):")
        strings.append(str(self.link_load_list))
        strings.append("Link sizes (\"number of fibers\"):")
        strings.append(str(self.link_size_list))
        return strings

    def print(self):
        for line in self.get_strings():
            print(line)

    def file_write(self, problem_to_solve):
        result_file = open("results_" + problem_to_solve + ".txt", "w")
        for line in self.get_strings():
            result_file.write(line+"\n")
        result_file.close()
