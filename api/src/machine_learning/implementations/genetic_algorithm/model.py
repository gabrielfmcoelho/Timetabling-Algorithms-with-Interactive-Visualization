from typing import List
import random

from machine_learning.implementations.genetic_algorithm.src.entities import ClassGroup, Classroom, Subject, Professor
from machine_learning.implementations.genetic_algorithm.src.chromosome import Chromosome
from machine_learning.implementations.genetic_algorithm.src.population import Population
from machine_learning.models_evaluator import MetricsEvaluator
from machine_learning.model_definition import Model


class GeneticAlgorithm(Model):
    def parameters_parser(self, data: dict, parameters: dict):
        population_size = parameters.get("population_size")
        mutation_rate = parameters.get("mutation_rate")
        crossover_rate = parameters.get("crossover_rate")
        generations = parameters.get("generations")
        fitness_threshold = parameters.get("fitness_threshold")
        course_load_one_class_threshold = parameters.get("course_load_one_class_threshold")
        if not population_size or not mutation_rate or not crossover_rate or not generations or not fitness_threshold or not course_load_one_class_threshold:
            raise Exception("Missing parameters")
        
        class_groups = [ClassGroup(class_group) for class_group in data.get("class_groups", [])]
        classrooms = [Classroom(classroom) for classroom in data.get("classrooms", [])]
        subjects = [Subject(subject) for subject in data.get("subjects", [])]
        professors = [Professor(professor) for professor in data.get("professors", [])]
        if not class_groups or not classrooms or not subjects or not professors:
            raise Exception("Missing data")
        
        return population_size, mutation_rate, crossover_rate, generations, fitness_threshold, course_load_one_class_threshold, class_groups, classrooms, subjects, professors

    def setup(self, data: dict, parameters: dict):
        population_size, mutation_rate, crossover_rate, generations, fitness_threshold, course_load_one_class_threshold, class_groups, classrooms, subjects, professors = self.parameters_parser(data, parameters)
        self.metrics_evaluator = MetricsEvaluator("Genetic Algorithm", "elite_fitness")
        population = Population()
        population.generate_population_from_data(population_size, class_groups, classrooms, subjects, professors, course_load_one_class_threshold)
        self.population = population
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.generations = generations
        self.fitness_threshold = fitness_threshold
        self.course_load_one_class_threshold = course_load_one_class_threshold
        self.class_groups = class_groups
        self.classrooms = classrooms
        self.subjects = subjects
        self.professors = professors

    @staticmethod
    def __selection(population: Population) -> Population:
        """
        Select the best individuals of the population to the matching pool
        """
        population.order_population_by_fitness()
        matching_pool: Population = Population()
        for i in range(len(population.chromosomes)):
            if random.random() < (i / len(population.chromosomes)):
                matching_pool.add_chromosome(population.chromosomes[i])
        return matching_pool
    
    @staticmethod
    def __crossover(matching_pool: Population, crossover_rate: float) -> Population:
        """
        Create a new population with the crossover of the matching pool chromosomes
        """
        new_population: Population = Population()
        for _ in range(len(matching_pool.chromosomes) // 2):
            chromosome_parent_1 = random.choice(matching_pool.chromosomes)
            chromosome_parent_2 = random.choice(matching_pool.chromosomes)
            if random.random() < crossover_rate:
                crossover_point = random.randint(1, len(chromosome_parent_1.genes) - 1)
                chromosome_child_1 = Chromosome()
                chromosome_child_2 = Chromosome()
                chromosome_child_1.genes = chromosome_parent_1.genes[:crossover_point] + chromosome_parent_2.genes[crossover_point:]
                chromosome_child_2.genes = chromosome_parent_2.genes[:crossover_point] + chromosome_parent_1.genes[crossover_point:]
                new_population.add_chromosome(chromosome_child_1)
                new_population.add_chromosome(chromosome_child_2)
            else:
                new_population.add_chromosome(chromosome_parent_1)
                new_population.add_chromosome(chromosome_parent_2)
        return new_population
    
    @staticmethod
    def __mutation(new_population: Population, mutation_rate: float, class_groups: List[ClassGroup], classrooms: List[Classroom], subjects: List[Subject], professors: List[Professor]) -> Population:
        """
        Mutate the genes of the new population with a random selection of the parameters
        """
        for chromosome in new_population.chromosomes:
            for gene in chromosome.genes:
                if random.random() < mutation_rate:
                    gene.generate_random_gene(class_groups, classrooms, subjects, professors)
        return new_population
    
    @staticmethod
    def __replace_population(population: Population, new_population: Population) -> Population:
        """
        Replace the population with the new population if the new population has better individuals
        """
        population.order_population_by_fitness()
        new_population.order_population_by_fitness(reverse=True)
        for i in range(len(new_population.chromosomes)):
            if new_population.chromosomes[i].elite_fitness > population.chromosomes[i].elite_fitness:
                population.chromosomes[i] = new_population.chromosomes[i]
        return population

    def run(self) -> MetricsEvaluator:
        """
        Run the genetic algorithm model and return the evaluation metrics
        """
        for generation in range(self.generations):
            self.metrics_evaluator.start_iteration()
            if generation > 0:
                matching_pool = self.__selection(self.population)
                new_population = self.__crossover(matching_pool, self.crossover_rate)
                new_population = self.__mutation(new_population, self.mutation_rate, self.class_groups, self.classrooms, self.subjects, self.professors)
                self.population = self.__replace_population(self.population, new_population)
            self.metrics_evaluator.finish_iteration(generation, self.population.best_chromosome, self.population.best_chromosome.avg_amount_of_conflicts, self.population.best_chromosome.elite_fitness)
            if self.population.best_chromosome.elite_fitness >= self.fitness_threshold:
                break
        self.metrics_evaluator.finish_evaluation()
        return self.metrics_evaluator