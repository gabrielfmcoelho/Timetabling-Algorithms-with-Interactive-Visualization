from dataclasses import dataclass
from typing import List

from machine_learning.implementations.genetic_algorithm.src.entities import ClassGroup, Classroom, Subject, Professor
from machine_learning.implementations.genetic_algorithm.src.gene import Gene
from machine_learning.implementations.genetic_algorithm.src.chromosome import Chromosome


@dataclass
class Population:
    """
    A population is a collection of chromosomes that can represent a set of possible solutions for the problem
    """
    chromosomes: List[Chromosome]

    def __init__(self) -> None:
        self.chromosomes = []

    def add_chromosome(self, chromosome: Chromosome) -> None:
        self.chromosomes.append(chromosome)

    def generate_population_from_data(self, population_size: int, class_groups: List[ClassGroup], classrooms: List[Classroom], subjects: List[Subject], professors: List[Professor], course_load_per_month: int = 36) -> None:
        """
        Generate a initial population of chromosomes (timetables) with genes (timeslots) with the combinatorial selection of class groups, classrooms, subjects and professors and the random selection of availabilities (day and time) for the classroom and the professor
        """
        print(f"Generating population of size {population_size} with {len(class_groups)} class groups, {len(classrooms)} classrooms, {len(subjects)} subjects and {len(professors)} professors and a course load threshold of {course_load_per_month} hours")
        for _ in range(population_size):
            chromosome: Chromosome = Chromosome()
            for class_group in class_groups:
                for classroom in classrooms:
                    for professor in professors:
                        for taughtble_subject_id in professor.taughtble_subjects_ids:
                            for subject in subjects:
                                if subject.id == taughtble_subject_id:
                                    for class_slot in range(subject.course_load // course_load_per_month):
                                        gene: Gene = Gene()
                                        gene.create_gene(class_group, classroom, subject, professor)
                                        chromosome.add_gene(gene)
            self.add_chromosome(chromosome)
        print(f"Population generated with {len(self.chromosomes)} chromosomes")

    @property
    def best_chromosome(self) -> Chromosome:
        best_chromosome = max(self.chromosomes, key=lambda chromosome: chromosome.elite_fitness)
        #print(f"Best chromosome with fitness of {best_chromosome.elite_fitness}")
        return best_chromosome
    
    def order_population_by_fitness(self, reverse: bool = False) -> None:
        """
        Order the chromosomes by fitness and select the best individuals **(elitism)**
        """
        self.chromosomes.sort(key=lambda chromosome: chromosome.elite_fitness, reverse=reverse)
