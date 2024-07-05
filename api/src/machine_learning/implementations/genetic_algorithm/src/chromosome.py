from dataclasses import dataclass
from typing import List

from machine_learning.implementations.genetic_algorithm.src.gene import Gene


@dataclass
class Chromosome:
    """
    A chromosome is a combination of genes that can represent a possible solution for the problem (the complete timetable)
    """
    genes: List[Gene]

    def __init__(self) -> None:
        self.genes = []

    def add_gene(self, gene: Gene) -> None:
        self.genes.append(gene)
        
    @property
    def amount_of_conflicts(self) -> int:
        """
        Returns the amount of conflicts in the chromosome; Evaluates the amount of internal conflicts in each gene and the amount of conflicts between the genes
        """
        conflicts = 0
        professor_timeslots_usage = {}
        classroom_timeslots_usage = {}
        for gene in self.genes:
            conflicts += gene.get_amount_of_internal_conflicts(is_valid=True, is_feasible=False) # Não checa assegura se a sala de aula comporta tem a mesma disponibilidade do professor
            
            professor_timeslots_usage_key = (gene.professor.id, gene.professor.given_availability.day_id, gene.professor.given_availability.time_id) # Checa se o professor possui timeslots duplicados em outros genes
            if professor_timeslots_usage_key in professor_timeslots_usage:
                conflicts += 1
            else:
                professor_timeslots_usage[professor_timeslots_usage_key] = 1

            classroom_timeslots_usage_key = (gene.classroom.id, gene.classroom.given_availability.day_id, gene.classroom.given_availability.time_id) # Checa se a sala de aula possui timeslots duplicados em outros genes
            if classroom_timeslots_usage_key in classroom_timeslots_usage:
                conflicts += 1
            else:
                classroom_timeslots_usage[classroom_timeslots_usage_key] = 1

        #print(f"Chromosome with total amount of {conflicts} conflicts")
        return conflicts
    
    @property
    def avg_amount_of_conflicts(self) -> float:
        avg_amount_of_conflicts = self.amount_of_conflicts / len(self.genes)
        #print(f"Chromosome with average amount of {avg_amount_of_conflicts} conflicts")
        return avg_amount_of_conflicts

    @property
    def elite_fitness(self) -> float:
        fitness = round(1 - self.amount_of_conflicts * 0.1, 2)
        if fitness < 0:
            #print(f"Chromosome with negative fitness, floored to 0 !")
            fitness = 0
        return fitness