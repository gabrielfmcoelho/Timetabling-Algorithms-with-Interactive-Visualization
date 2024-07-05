from typing import List

from machine_learning.implementations.genetic_algorithm.src.entities import Classroom, Subject


def calculate_quantity_of_classes_needed(subjects: List[Subject], classrooms: List[Classroom]) -> float:
    print(f"Calculating quantity of classes needed for {len(subjects)} subjects and {len(classrooms)} classrooms")
    quantity_of_classes: float = 0
    for subject in subjects:
        quantity_of_classes += subject.course_load // 1.5
    quantity_of_classes = quantity_of_classes * len(classrooms)
    print(f"Quantity of classes needed: {quantity_of_classes}")
    return quantity_of_classes