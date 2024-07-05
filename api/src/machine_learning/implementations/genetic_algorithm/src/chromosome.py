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
    def amount_of_conflicts_between_genes(self) -> int:
        """
        Returns the amount of conflicts between the genes in the chromosome; For each pair of genes, evaluates if the classroom and the professor have the same availability; Therefore evaluating if the genes are feasible or if they occupy the same timeslot in the timetable.
        """
        conflicts_between_genes = 0
        # For each pair of genes
        for i in range(len(self.genes)):
            for j in range(i + 1, len(self.genes)):
                # Evaluate if the classroom are the same and have the same availability
                if self.genes[i].classroom == self.genes[j].classroom and self.genes[i].classroom.given_availability == self.genes[j].classroom.given_availability:
                    conflicts_between_genes += 1
                # Evaluate if the professor are the same and have the same availability
                if self.genes[i].professor == self.genes[j].professor and self.genes[i].professor.given_availability == self.genes[j].professor.given_availability:
                    conflicts_between_genes += 1
        #print(f"Chromosome with total amount of {conflicts_between_genes} conflicts between genes")
        return conflicts_between_genes
        
    @property
    def amount_of_conflicts(self) -> int:
        """
        Returns the amount of conflicts in the chromosome; Evaluates the amount of internal conflicts in each gene and the amount of conflicts between the genes
        """
        conflicts = 0
        for gene in self.genes:
            conflicts += gene.amount_of_internal_conflicts
        conflicts += self.amount_of_conflicts_between_genes
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
