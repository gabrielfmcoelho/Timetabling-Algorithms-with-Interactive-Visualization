from dataclasses import dataclass
from typing import List
import random

from machine_learning.implementations.genetic_algorithm.src.entities import ClassGroup, Classroom, Subject, Professor


@dataclass
class Gene:
    """
    A gene is a combination of a class group, a classroom, a subject and a professor (a possible timeslot entry in the timetable)
    """
    class_group: ClassGroup
    classroom: Classroom
    subject: Subject
    professor: Professor

    def __init__(self) -> None:
        pass
    
    def create_gene_with_random_availability(self, class_group: ClassGroup, classroom: Classroom, subject: Subject, professor: Professor) -> None:
        """
        Create a gene with the **given parameters** and randomly select the availability for the classroom and the professor
        """
        self.class_group = class_group
        classroom.set_random_availability()
        self.classroom = classroom
        self.subject = subject
        professor.set_random_availability()
        self.professor = professor

    def create_gene_with_given_availability(self, class_group: ClassGroup, classroom: Classroom, subject: Subject, professor: Professor) -> None:
        """
        Create a gene with the **given parameters** and the **given availability** for the classroom and the professor
        """
        self.class_group = class_group
        self.classroom = classroom
        self.subject = subject
        self.professor = professor

    def generate_random_gene(self, class_groups: List[ClassGroup], classrooms: List[Classroom], subjects: List[Subject], professors: List[Professor]) -> None:
        """
        Create a gene with complete random parameters and availability for the classroom and the professor
        """
        self.class_group = random.choice(class_groups)
        random_classroom_availability = random.choice(classrooms)
        random_classroom_availability.set_random_availability()
        self.classroom = random_classroom_availability
        self.subject = random.choice(subjects)
        random_professor_availability = random.choice(professors)
        random_professor_availability.set_random_availability()
        random_professor_availability.set_random_subject()
        self.professor = random_professor_availability

    @property
    def __is_valid(self) -> bool:
        """
        Gene is valid if the classroom capacity is greater or equal than the class group students amount
        """
        return self.class_group.students_amount <= self.classroom.capacity # Capacidade da sala de aula comporta a quantidade de alunos da turma
    
    @property
    def __is_feasible(self) -> bool:
        """
        Gene is feasible if the classroom and the professor have the same availability;
        """
        return self.classroom.given_availability == self.professor.given_availability
    
    def get_amount_of_internal_conflicts(self, is_valid: bool, is_feasible: bool) -> int:
        """
        Returns the amount of conflicts in the gene; from 0 to 2; Evaluates if the gene is valid and feasible
        """
        internal_conflicts = 0
        if is_valid:
            if not self.__is_valid:
                internal_conflicts += 1
        if is_feasible:
            if not self.__is_feasible:
                internal_conflicts += 1
        #print(f"Gene {self} has {conflicts} conflicts and is valid: {self.__is_valid} and feasible: {self.__is_feasible}")
        return internal_conflicts