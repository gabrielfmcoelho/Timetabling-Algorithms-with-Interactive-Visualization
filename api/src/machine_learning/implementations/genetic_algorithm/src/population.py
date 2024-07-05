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
            for class_group in class_groups: # Para cada TURMA
                for classroom in classrooms: # Para cada SALA DE AULA
                    for professor in professors: # Para cada PROFESSOR
                        for taughtble_subject_id in professor.taughtble_subjects_ids: # Para cada DISCIPLINA....
                            for subject in subjects:
                                if subject.id == taughtble_subject_id: # ...que o PROFESSOR pode lecionar
                                    for class_slot in range(subject.course_load // course_load_per_month): # Para cada SLOT DE AULA
                                        gene: Gene = Gene()
                                        gene.create_gene_with_random_availability(class_group, classroom, subject, professor) # Seleciona DIA e HORARIO aleatório para a SALA DE AULA e DIA e HORARIO aleatório para o PROFESSOR.
                                        chromosome.add_gene(gene)
            self.add_chromosome(chromosome)
        print(f"Population generated with {len(self.chromosomes)} chromosomes")

    def generate_population_from_data_safe_solution(self, population_size: int, class_groups: List[ClassGroup], classrooms: List[Classroom], subjects: List[Subject], professors: List[Professor]) -> None:
        """
        Generate a initial population with more safe chromosomes (timetables) with genes (timeslots) with the combinatorial selection of class groups, classrooms, subjects and professors ensuring that the professor can teach the subject and the classroom is available in the professor's availability only randomly selecting the day of the week for the professor and the time of the day for the classroom.
        """
        print(f"Generating population of size {population_size} with {len(class_groups)} class groups, {len(classrooms)} classrooms, {len(subjects)} subjects and {len(professors)} professors")
        for _ in range(population_size):
            chromosome: Chromosome = Chromosome()
            for subject in subjects: # Para cada DISCIPLINA
                for class_group in class_groups: # Para cada TURMA
                    for professor in professors: # Para cada PROFESSOR...
                        if subject.id in professor.taughtble_subjects_ids: # ...que pode lecionar a DISCIPLINA (Reduz consideravelmente o tamanho da população e conflitos ao selecionar apenas professores que podem lecionar a disciplina)
                            for classroom in classrooms: # Para cada SALA DE AULA
                                gene: Gene = Gene()
                                professor_random_available_day_id = professor.random_available_day # !!! Seleciona DIA aleatório para o PROFESSOR
                                if professor_random_available_day_id in classroom.available_days_ids: # APENA SE a SALA DE AULA estiver disponível no DIA selecionado para o PROFESSOR (Reduz consideravelmente o tamanho da população e conflitos ao selecionar apenas salas de aula disponíveis no dia do professor)
                                    classroom_random_available_time_id = classroom.random_available_time # !!! Seleciona HORARIO aleatório para a SALA DE AULA
                                    professor.set_availability(professor_random_available_day_id, classroom_random_available_time_id) # !!! Define o DIA e HORARIO para o PROFESSOR
                                    classroom.set_availability(professor_random_available_day_id, classroom_random_available_time_id) # !!! Define o DIA e HORARIO para a SALA DE AULA O MESMO DO PROFESSOR
                                    gene.create_gene_with_given_availability(class_group, classroom, subject, professor)
                                    chromosome.add_gene(gene)
            self.add_chromosome(chromosome)
        print(f"Population generated with {len(self.chromosomes)} chromosomes")
                                
    @property
    def best_chromosome(self) -> Chromosome:
        best_chromosome = max(self.chromosomes, key=lambda chromosome: chromosome.elite_fitness)
        #print(f"Best chromosome with fitness of {best_chromosome.elite_fitness}")
        return best_chromosome
    
    @property
    def sum_of_total_fitness(self) -> float:
        sum_of_total_fitness = sum(chromosome.elite_fitness for chromosome in self.chromosomes)
        #print(f"Sum of total fitness of {sum_of_total_fitness}")
        return sum_of_total_fitness
    
    def order_population_by_fitness(self, reverse: bool = False) -> None:
        """
        Order the chromosomes by fitness and select the best individuals **(elitism)**
        """
        self.chromosomes.sort(key=lambda chromosome: chromosome.elite_fitness, reverse=reverse)

    def order_population_by_conflicts(self, reverse: bool = False) -> None:
        """
        Order the chromosomes by conflicts and select the best individuals **(elitism)**
        """
        self.chromosomes.sort(key=lambda chromosome: chromosome.amount_of_conflicts, reverse=reverse)
