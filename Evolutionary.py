from classes import Gene, Chromosome
import random
from math import ceil
import numpy
import time



class Evelutionary:
    def __init__(self,demandList,linkList,stop_input,max_number_of_seconds,max_number_of_generations,max_number_of_mutations,max_unimproved_generations,seed,deafultPopulationSize):
        self.DEFAULT_POPULATION_SIZE = 10
        self.DEFAULT_MUTATION_PROBABILITY = 0.01
        self.OFFSPRING_FROM_PARENT_PROBABILITY = 0.5
        self.not_improved_in_N_generations = 100
        self.default_population_size = 3000
        self.mutation_probability = 0.01
        self.crossover_probability_mul = 0.9
        self.stop_input = stop_input
        self.max_number_of_seconds = max_number_of_seconds
        self.max_number_of_generations = max_number_of_generations
        self.max_number_of_mutations = max_number_of_mutations
        self.max_unimproved_generations = max_unimproved_generations
        self.deafultPopulationSize = deafultPopulationSize
        self.seed=seed
        self.problem_to_solve = ""  # DAP or DDAP
        self.demandList = demandList
        self.linkList = linkList

    def evolutionarySimulation(self):
        currentPopulation = self.generate_first_population(self.demandList,self.deafultPopulationSize)
        self.calculate_fitness(self.linkList,self.demandList,currentPopulation)

        current_population.sort(key=lambda x: x.fitness, reverse=False)
        current_population=current_population[:200]

        best_fitness = numpy.inf
        best_chromosome = current_population[0]  # best chromosome is first one in  sorted by fitness population
        best_chromosomes_list = list()  # Trajectory
        best_chromosomes_list.append(best_chromosome)

        best_fitness_list = list()
        best_generation_ids = list()  # X values for graph

        time_elapsed = 0
        generations_counter = 0
        mutations_counter = 0
        not_improved_counter = 0

        self.start_time = time.time()

        while self.stop_condition(time_elapsed, generations_counter, mutations_counter, not_improved_counter):

            # Pick which fitness to prioritise based on chosen algorithm, then recalculate the relevant parameters
            current_fitness = current_population[0].fitness

            if current_fitness < best_fitness:
                best_chromosome = current_population[0]
                best_fitness = current_fitness
                best_chromosomes_list.append(best_chromosome)
                # Store trajectory
                best_generation_ids.append(generations_counter)
                best_fitness_list.append(best_fitness)
            else:
                pass

            # Crossover and recalculate fitness
            new_population = self.crossover_chromosomes(
                current_population,
                best_fitness,  
                self.crossover_probability_mul)
            self.calculate_fitness(self.links_list, self.demands_list, new_population)

            new_population.sort(key=lambda x: x.fitness, reverse=False)

            # Mutate and recalculate fitness
            for chromosome in new_population:
                self.mutate_chromosome(chromosome, self.mutation_probability)
                mutations_counter += 1
            self.calculate_fitness(self.links_list, self.demands_list, new_population)
            # print(f"Mutations: {mutations_counter}")

            # Sort population

            new_population.sort(key=lambda x: x.fitness, reverse=False)

            # Calculate the remaining counters:
            if new_population[0].fitness < best_fitness:
                not_improved_counter = 0
                print(f"Actual fitness: {new_population[0].fitness}")
            else:
                not_improved_counter += 1
                # print(f"n impr: {not_improved_counter}")

            generations_counter += 1
            time_elapsed = time.time() - self.start_time

            # Keep n=initial_population_size best chromosomes, discard rest
            #current_population = new_population[:default_population_size]
            current_population = new_population[:60]

            link_loads = self.get_link_loads(best_chromosome, self.links_list, self.demands_list)
            link_sizes = self.get_link_sizes(link_loads, self.links_list)


    def generate_chromosome(self,list_of_demands):
        list_of_genes = list()  # Empty list for appending Genes

        # Generate genes for each demand
        for demand in list_of_demands:
            demand_volume = demand.demand_volume  # Get demand volume for the gene
            number_of_demand_paths = demand.number_of_demand_paths  # Length of the gene

            path_flow_list = [0] * number_of_demand_paths  # Init with zeros

            # Randomly distribute the demand_volume across path flows
            # Sum of path flows must equal demand volume
            for i in range(int(demand_volume)):
                
                picked_path_flow = random.randint(0, number_of_demand_paths - 1)
                path_flow_list[picked_path_flow] += 1

            new_gene = Gene(path_flow_list, demand_volume)
            list_of_genes.append(new_gene)

        chromosome = Chromosome(list_of_genes, 0)  # Fitness is updated manually in the main script
        return chromosome


    def generate_first_population(self,list_of_demands: list, population_size: int):
        # Check if first population size is > 0
        if population_size <= 0:
            population_size = self.DEFAULT_POPULATION_SIZE

        first_population_list = list()
        for i in range(population_size):
            first_population_list.append(self.generate_chromosome(list_of_demands))
        return first_population_list


    # Mutation perturbs the values of the chromosome genes with a certain low probability
    def mutate_chromosome(self,chromosome: Chromosome, mutation_probability: float):
        if not 0 <= mutation_probability <= 1:
            mutation_probability = self.DEFAULT_MUTATION_PROBABILITY

        for gene in chromosome.list_of_genes:

            # For each gene on the list, decide if mutation will be performed
            # Mutation = move 1 unit between 2 path flows in a gene
            if self.get_random_bool(mutation_probability):
                number_of_path_flows = len(gene.path_flow_list)

                if number_of_path_flows == 1:
                    # Avoids a soft-lock (can't mutate a path flow with itself)
                    continue

                # Randomly select 2 path flows to mutate
                first_path_flow_id = random.randint(0, number_of_path_flows - 1)
                second_path_flow_id = random.randint(0, number_of_path_flows - 1)
                
                # Check if 2nd path flow won't be smaller than 0 after decrementing it
                # and check if the same path flow wasn't chosen for both operations;
                # Get a new 2nd one until the conditions are met
                iterations = 0
                while gene.path_flow_list[second_path_flow_id] < 1 or first_path_flow_id == second_path_flow_id:
                    second_path_flow_id = random.randint(0, number_of_path_flows - 1)

                    iterations += 1
                    if iterations > number_of_path_flows:
                        # We've looped over the whole gene and found no solution; the loop is now soft-locked
                        # Try again with a new first_path_flow_id
                        first_path_flow_id = random.randint(0, number_of_path_flows - 1)
                        # WARNING: THIS CAN STILL SOFT-LOCK

                gene.path_flow_list[first_path_flow_id] += 1
                gene.path_flow_list[second_path_flow_id] -= 1


    # Crossover exchanges genes between two parent chromosomes to produce two offspring
    # A new population is generated; it includes the old population and all offspring.
    def crossover_chromosomes(self,original_population, best_fitness: float, crossover_probability_mul: float):
        # Firstly, list is filled with parent chromosomes
        new_population = list(original_population)
        population_size = len(original_population)

        #fitness_list = list()
        # abs_list = list()
        # for i in range(population_size):
        #     fitness_list.append(original_population[i].fitness)
        #     abs_list.append( 1/(abs(original_population[i].fitness - original_population[0].fitness) + 1))
        #print(fitness_list)
        #norm = numpy.linalg.norm(fitness_list)
        #norm_list = fitness_list / norm

        for j in range(0, population_size):
            
            #first_parent_id, second_parent_id = random.choices(range(population_size), abs_list, k=2)
            first_parent_id = random.randint(0, population_size - 1)
            second_parent_id = random.randint(0, population_size - 1)

            while first_parent_id == second_parent_id:
                #second_parent_id = random.choices(range(population_size), abs_list, k=1)
                second_parent_id = random.randint(0, population_size - 1)

            first_parent = original_population[first_parent_id]
            second_parent = original_population[second_parent_id]

            if first_parent.fitness != 0 and second_parent.fitness != 0:
                first_parent_score = numpy.abs(best_fitness / first_parent.fitness)
                second_parent_score = numpy.abs(best_fitness / second_parent.fitness)
            else:
                first_parent_score = 0.5
                second_parent_score = 0.5

            # Crossover prob. is determined by parents' fitness
            crossover_probability = crossover_probability_mul * (second_parent_score + first_parent_score) / 2
            if crossover_probability > 1.0:
                crossover_probability = 1.0

            if self.get_random_bool(crossover_probability):
                first_parent_genes = first_parent.list_of_genes
                second_parent_genes = second_parent.list_of_genes

                first_offspring_genes = list()
                second_offspring_genes = list()

                # Create offspring from parent genes:
                # For each gene in the parent chromosome...
                for i in range(0, len(first_parent_genes)):
                    # First offspring gets gene from first parent, second offspring from second parent
                    if self.get_random_bool(self.OFFSPRING_FROM_PARENT_PROBABILITY):
                        first_offspring_genes.append(first_parent_genes[i])
                        second_offspring_genes.append(second_parent_genes[i])
                    # vice versa as the above:
                    else:
                        first_offspring_genes.append(second_parent_genes[i])
                        second_offspring_genes.append(first_parent_genes[i])

                # Add offsprings to the whole list
                first_offspring = Chromosome(first_offspring_genes)
                second_offspring = Chromosome(second_offspring_genes)
                new_population.append(first_offspring)
                new_population.append(second_offspring)
                
        return new_population


    # Calculate fitness for all chromosomes in the passed population (list of chromosomes)
    def calculate_fitness(self,links, demands, population):
        for chromosome in population:
            number_of_links = len(links)
            # Init lists with zeros
            l = [0] * number_of_links  # Link loads
            y = [0] * number_of_links  # Link size (for DDAP)
            f = [0] * number_of_links  # Link overloads (for DAP)
            chromosome.fitness = 0
            for d in range(len(chromosome.list_of_genes)):
                for p in range(len(chromosome.list_of_genes[d].path_flow_list)):
                    for e in range(len(links)):
                        # Path flow if the edge partakes in the given demand path; else a zero takes the place
                        if self.check_link_in_demand(e + 1, demands[d], p):
                            l[e] += chromosome.list_of_genes[d].path_flow_list[p]

            if self.problem_to_solve == "DAP":
                for e in range(len(links)):
                    f[e] = l[e] - links[e].number_of_modules * links[e].link_module  # Calc link overloads
                chromosome.fitness = max(f)

            else:  # DDAP
                for e in range(len(links)):
                    y[e] = ceil(l[e] / links[e].link_module)  # Calc link sizes
                    chromosome.fitness += y[e] * links[e].unit_cost


    # Calculate link loads for the given chromosome
    def get_link_loads(self,chromosome, links, demands):
        number_of_links = len(links)
        l = [0] * number_of_links  # Init link load list with zeros

        for d in range(len(chromosome.list_of_genes)):
            for p in range(len(chromosome.list_of_genes[d].path_flow_list)):
                for e in range(len(links)):
                    # Path flow if the edge partakes in the given demand path; else a zero takes the place
                    if self.check_link_in_demand(e + 1, demands[d], p):
                        l[e] += chromosome.list_of_genes[d].path_flow_list[p]
        return l


    # Calculate link sizes from link loads
    def get_link_sizes(self,link_loads, links):
        number_of_links = len(links)
        y = [0] * number_of_links  # Init link sizes list with zeros
        for e in range(len(links)):
            y[e] = ceil(link_loads[e] / links[e].link_module)
        return y


    # Check if given link is in a given demand path
    def check_link_in_demand(self,link, demand, path_num):
        demand_path = demand.list_of_demand_paths[path_num]
        return str(link) in demand_path.link_id_list


    def get_random_bool(self,probability: float):
        return random.random() < probability
