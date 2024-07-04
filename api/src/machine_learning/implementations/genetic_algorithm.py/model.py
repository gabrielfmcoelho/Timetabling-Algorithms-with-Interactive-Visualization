from dataclasses import dataclass, Field
from typing import List, Dict, Set, Tuple
import time
import random
import json

from icecream import ic


@dataclass
class Professor:
    id: int
    name: str
    time_available: dict

    def __init__(self, professor_name: str, professor_data: dict) -> None:
        self.id = professor_data["id"]
        self.name = professor_name
        self.time_available = professor_data["time_available"]

    @property
    def availability(self) -> List[Set[str]]:
        availability = []
        for day, times in self.time_available.items():
            for time in times:
                availability.append((day, time))
        return availability
    
@dataclass
class ClassGroup:
    id: int
    name: str
    students: int

    def __init__(self, class_group_name: str, class_group_data: dict) -> None:
        self.id = class_group_data["id"]
        self.name = class_group_name
        self.students = class_group_data["students"]

@dataclass
class Subject:
    id: int
    name: str
    professors: List[str]
    course_load: int

    def __init__(self, subject_name: str, subject_data: dict) -> None:
        self.id = subject_data["id"]
        self.name = subject_name
        self.professors = subject_data["professors"]
        self.course_load = subject_data["course_load"]


@dataclass
class Classroom:
    id: int
    name: str
    time_available: Dict[str, List[int]]
    capacity: int
    def __init__(self, classroom_name: str, classroom_data: dict) -> None:
        self.id = classroom_data["id"]
        self.name = classroom_name
        self.time_available = classroom_data["time_available"]

    @property
    def availability(self) -> List[Set[str]]:
        availability = []
        for day, times in self.time_available.items():
            for time in times:
                availability.append((day, time))
        return availability
    

@dataclass
class Gene:
    professor: Professor
    subject: Subject
    day: str
    time: int

    def __init__(self, professor: Professor, subject: Subject, day: str, time: int) -> None:
        self.professor = professor
        self.subject = subject
        self.day = day
        self.time = time


@dataclass
class Chromosome:
    genes: List[Gene]

    def __init__(self) -> None:
        self.genes = []

    def add_gene(self, gene: Gene) -> None:
        self.genes.append(gene)


@dataclass
class Population:
    chromosomes: List[Chromosome]

    def __init__(self) -> None:
        self.chromosomes = []

    def add_chromosome(self, chromosome: Chromosome) -> None:
        self.chromosomes.append(chromosome)


class MetricsEvaluator:
    def __init__(self, model: str) -> None:
        self.model = model
        self.metrics = {
            "time_to_converge": 0,
            "best_fitness": 0,
            "best_chromosome": None
        }

    def __repr__(self) -> str:
        return f"MetricsEvaluator({self.model})"
    
    def __str__(self) -> str:
        return f"MetricsEvaluator of Model: {self.model} with Metrics: {self.metrics}"

    def start_timer(self):
        self.start_time = time.time()

    def stop_timer(self):
        self.metrics["time_to_converge"] = time.time() - self.start_time // 60

    def update_metrics(self, best_chromosome: Chromosome, best_fitness: float):
        self.metrics["best_fitness"] = best_fitness
        self.metrics["best_chromosome"] = best_chromosome
        

class GeneticAlgorithm:
    def __init__(self, population_size: int, mutation_rate: float, crossover_rate: float, generations: int, fitness_threshold: float, subjects: Dict[str, Subject], professors: Dict[str, Professor], classrooms: Dict[str, Classroom]) -> None:
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.generations = generations
        self.fitness_threshold = fitness_threshold
        self.subjects = subjects
        self.professors = professors
        self.classrooms = classrooms

    def generate_initial_population(self) -> Population:
        print(f"Creating population with {self.population_size} chromosomes, {len(self.subjects)} subjects, {len(self.professors)} professors and {len(self.classrooms)} classrooms")
        population = Population()
        for _ in range(self.population_size):
            chromosome = Chromosome()
            for subject, subject_data in self.subjects.items():
                for professor in subject_data.professors:
                    for _ in range((subject_data.course_load // 36)):
                        for classroom, classroom_data in self.classrooms.items():
                            day, time = random.choice(list(set(self.professors[professor].availability) & set(classroom_data.availability)))
                            gene = Gene(self.professors[professor], subject_data, day, time)
                            chromosome.add_gene(gene)
            population.add_chromosome(chromosome)
        return population
    
    def calculate_chromosome_fitness(self, chromosome: Chromosome) -> float:
        fitness = 1.0
        conflicts = 0
        timeslot_count = {}
        room_usage = {}
        for gene in chromosome.genes:
            # Contar uso de horários por professor
            if (gene.professor.name, gene.day, gene.time) in timeslot_count:
                timeslot_count[(gene.professor.name, gene.day, gene.time)] += 1
            else:
                timeslot_count[(gene.professor.name, gene.day, gene.time)] = 1
            # Contar uso de salas
            if (gene.subject.name, gene.day, gene.time) in room_usage:
                room_usage[(gene.subject.name, gene.day, gene.time)] += 1
            else:
                room_usage[(gene.subject.name, gene.day, gene.time)] = 1
        for count in timeslot_count.values():
            if count > 1:
                conflicts += (count - 1)
        for count in room_usage.values():
            if count > 1:
                conflicts += (count - 1)
        # CHECAR QUANTIDADE DE ALUNOS
        # Reduzir a fitness por conflito
        fitness -= conflicts * 0.1
        if fitness < 0:
            fitness = 0
        return fitness
    
    def selection(self, population: Population) -> List[Chromosome]:
        mating_pool = []
        population_fitness = [(chromosome, self.calculate_chromosome_fitness(chromosome)) for chromosome in population.chromosomes]
        population_fitness.sort(key=lambda x: x[1], reverse=True)
        for i in range(len(population_fitness)):
            if random.random() < (i / len(population_fitness)):
                mating_pool.append(population_fitness[i][0])
        return mating_pool
    
    def crossover(self, mating_pool: List[Chromosome]) -> List[Chromosome]:
        offspring = []
        for _ in range(len(mating_pool) // 2):
            parent1 = random.choice(mating_pool)
            parent2 = random.choice(mating_pool)
            if random.random() < self.crossover_rate:
                point = random.randint(1, len(parent1.genes) - 1)
                child1 = Chromosome()
                child2 = Chromosome()
                child1.genes = parent1.genes[:point] + parent2.genes[point:]
                child2.genes = parent2.genes[:point] + parent1.genes[point:]
                offspring.extend([child1, child2])
            else:
                offspring.extend([parent1, parent2])
        return offspring
    
    def mutate(self, mating_pool: List[Chromosome]) -> List[Chromosome]:
        for chromosome in mating_pool:
            for gene in chromosome.genes:
                if random.random() < self.mutation_rate:
                    available_times = list(set(self.professors[gene.professor.name].time_available) & set(self.classrooms))
                    day, time = random.choice(available_times)
                    gene.day = day
                    gene.time = time
        return mating_pool
    
    def replace_population(self, population: Population, mating_pool: List[Chromosome]) -> List[Chromosome]:
        population_fitness = [(chromosome, self.calculate_chromosome_fitness(chromosome)) for chromosome in population.chromosomes]
        population_fitness.sort(key=lambda x: x[1])
        mating_pool_fitness = [(chromosome, self.calculate_chromosome_fitness(chromosome)) for chromosome in mating_pool]
        mating_pool_fitness.sort(key=lambda x: x[1], reverse=True)
        for i in range(len(mating_pool_fitness)):
            if mating_pool_fitness[i][1] > population_fitness[i][1]:
                population_fitness[i] = mating_pool_fitness[i]
        return [chromosome for chromosome, fitness in population_fitness]

    def run(self) -> Tuple[Chromosome, MetricsEvaluator]:
        metrics_evaluator = MetricsEvaluator("Genetic Algorithm")
        metrics_evaluator.start_timer()
        population = generate_initial_population(self.population_size, self.subjects, self.professors, self.classrooms)
        best_chromosome = None
        for generation in range(0, self.generations):
            print(f"Evaluating generation: {generation}")

            # Calcula a "nota" (fitness) de cada conjunto de horários
            population_fitness = [calculate_chromosome_fitness(chromosome) for chromosome in population.chromosomes]

            # Encontra a melhor "nota" atual
            best_fitness = max(population_fitness)

            if best_fitness >= self.fitness_threshold:
                print(f"Fitness threshold reached in generation {generation}")
                best_chromosome = population.chromosomes[population_fitness.index(best_fitness)]
                break

            mating_pool = selection(population)
            mating_pool = crossover(mating_pool, self.crossover_rate)
            mating_pool = mutate(mating_pool, self.mutation_rate, self.professors, self.subjects, self.classrooms)
            population = replace_population(population, mating_pool)

        if best_chromosome is None:
            best_chromosome = population.chromosomes[population_fitness.index(max(population_fitness))]
        metrics_evaluator.stop_timer()
        metrics_evaluator.update_metrics(best_chromosome, best_fitness)
        print(f"Best chromosome: {best_chromosome}, Fitness: {best_fitness}")
        return best_chromosome, metrics_evaluator