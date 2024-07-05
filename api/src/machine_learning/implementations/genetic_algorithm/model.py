from typing import List
import random

from machine_learning.implementations.genetic_algorithm.src.entities import ClassGroup, Classroom, Subject, Professor
from machine_learning.implementations.genetic_algorithm.src.chromosome import Chromosome
from machine_learning.implementations.genetic_algorithm.src.population import Population
from machine_learning.models_evaluator import MetricsEvaluator
from machine_learning.model_definition import Model


class GeneticAlgorithm(Model):
    def setup(self, data: dict, parameters: dict):
        self.population_size = parameters.get("population_size", 200)
        self.mutation_rate = parameters.get("mutation_rate", 0.4)
        self.crossover_rate = parameters.get("crossover_rate", 0.6)
        self.generations = parameters.get("generations", 500)
        self.fitness_threshold = parameters.get("fitness_threshold", 0.9)
        self.course_load_one_class_threshold = parameters.get("course_load_one_class_threshold", 36)
        self.class_groups = data.get("classes", [])
        self.classrooms = data.get("rooms", [])
        self.subjects = data.get("subjects", [])
        self.professors = data.get("teachers", [])
        self.metrics_evaluator = MetricsEvaluator("Genetic Algorithm", "conflicts")
        population = Population()
        population.generate_population_from_data_safe_solution(self.population_size, self.class_groups, self.classrooms, self.subjects, self.professors)
        self.population = population

    @staticmethod
    def __selection(population: Population) -> Population:
        """
        Select the best individuals of the population to the matching pool
        """
        matching_pool: Population = Population()

        population.order_population_by_fitness(reverse=True)
        sum_of_total_fitness = population.sum_of_total_fitness
        if sum_of_total_fitness == 0:
            for chromosome in population.chromosomes:
                matching_pool.add_chromosome(chromosome)
            return matching_pool
        
        for chromosome in population.chromosomes:
            probability = chromosome.elite_fitness / sum_of_total_fitness
            if random.random() < probability:
                matching_pool.add_chromosome(chromosome)

        return matching_pool
    
    @staticmethod
    def __crossover(matching_pool: Population, crossover_rate: float) -> Population:
        """
        Create a new population with the crossover of the matching pool chromosomes
        """
        new_population: Population = Population()

        for _ in range((len(matching_pool.chromosomes) // 2)):
            if random.random() < crossover_rate:
                parent_chromosomes = random.sample(matching_pool.chromosomes, 2)
                parent_chromosome_1, parent_chromosome_2 = parent_chromosomes[0], parent_chromosomes[1]

                if len(parent_chromosome_1.genes) > 1 and len(parent_chromosome_2.genes) > 1:
                    crossover_point = random.randint(1, min(len(parent_chromosome_1.genes), len(parent_chromosome_2.genes)) - 1)
                    child_chromosome_1 = Chromosome()
                    child_chromosome_2 = Chromosome()

                    child_chromosome_1.genes = parent_chromosome_1.genes[:crossover_point] + parent_chromosome_2.genes[crossover_point:]
                    child_chromosome_2.genes = parent_chromosome_2.genes[:crossover_point] + parent_chromosome_1.genes[crossover_point:]

                    new_population.add_chromosome(child_chromosome_1)
                    new_population.add_chromosome(child_chromosome_2)
                else:
                    new_population.add_chromosome(parent_chromosome_1)
                    new_population.add_chromosome(parent_chromosome_2)
        return new_population

    
    @staticmethod
    def __mutation(matching_pool: Population, mutation_rate: float, professors: List[Professor]) -> Population:
        """
        Mutate the genes of the new population with a random selection of the parameters
        """
        for chromosome in matching_pool.chromosomes:
            for gene in chromosome.genes:
                if random.random() < mutation_rate:
                    professor_id = gene.professor.id
                    for professor in professors:
                        if professor.id == professor_id:
                            professor_available_days_ids = professor.available_days_ids
                            if professor_available_days_ids:
                                professor_random_available_day_id = random.choice(professor_available_days_ids)
                                professor_random_available_time_id = random.choice(professor.available_time_ids)
                                professor.set_availability(professor_random_available_day_id, professor_random_available_time_id)
        return matching_pool
    
    @staticmethod
    def __replace_population(population: Population, matching_pool: Population) -> Population:
        """
        Replace the population with the new population if the new population has better individuals
        """
        new_population = Population()

        matching_pool.order_population_by_conflicts()
        population.order_population_by_conflicts()

        for i in range(len(population.chromosomes)):
            if i < len(matching_pool.chromosomes):
                new_population.add_chromosome(matching_pool.chromosomes[i])
            else:
                new_population.add_chromosome(population.chromosomes[i])
        return population

    def run(self) -> MetricsEvaluator:
        """
        Run the genetic algorithm model and return the evaluation metrics
        """
        for generation in range(self.generations):
            self.metrics_evaluator.start_iteration()
            if generation > 0:
                matching_pool = self.__selection(self.population)
                matching_pool = self.__crossover(matching_pool, self.crossover_rate)
                matching_pool = self.__mutation(matching_pool, self.mutation_rate, self.professors)
                self.population = self.__replace_population(self.population, matching_pool)
            self.metrics_evaluator.finish_iteration(generation, self.population.best_chromosome, self.population.best_chromosome.amount_of_conflicts, self.population.best_chromosome.elite_fitness)
            if self.population.best_chromosome.elite_fitness >= self.fitness_threshold:
                break
        self.metrics_evaluator.finish_evaluation()
        return self.metrics_evaluator