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
    
    def create_gene(self, class_group: ClassGroup, classroom: Classroom, subject: Subject, professor: Professor) -> None:
        """
        Create a gene with the **given parameters** and randomly select the availability for the classroom and the professor
        """
        self.class_group = class_group
        classroom.set_random_availability()
        self.classroom = classroom
        self.subject = subject
        professor.set_random_availability()
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
        return self.class_group.students_amount <= self.classroom.capacity
    
    @property
    def __is_feasible(self) -> bool:
        """
        Gene is feasible if the classroom and the professor have the same availability
        """
        return self.classroom.given_availability == self.professor.given_availability
    
    @property
    def amount_of_internal_conflicts(self) -> int:
        """
        Returns the amount of conflicts in the gene; from 0 to 2; Evaluates if the gene is valid and feasible
        """
        conflicts = 0
        if not self.__is_valid:
            conflicts += 1
        if not self.__is_feasible:
            conflicts += 1
        #print(f"Gene {self} has {conflicts} conflicts and is valid: {self.__is_valid} and feasible: {self.__is_feasible}")
        return conflicts