from dataclasses import dataclass
from typing import List
import random


@dataclass
class Time:
    id: int
    start: str
    end: str

    def __init__(self, time_data: dict) -> None:
        self.id = time_data["id"]
        self.start = time_data["start"]
        self.end = time_data["end"]

@dataclass
class Day:
    id: int
    name: str

    def __init__(self, day_data: dict) -> None:
        self.id = day_data["id"]
        self.name = day_data["name"]

@dataclass
class Availability:
    day_id: int
    time_id: int

@dataclass
class ClassGroup:
    id: int
    students_amount: int

    def __init__(self, class_group_data: dict) -> None:
        self.id = class_group_data["id"]
        self.students_amount = class_group_data["studentsAmount"]

@dataclass
class Classroom:
    id: int
    capacity: int
    available_days_ids: List[int]
    available_time_ids: List[int]
    given_availability: Availability|None = None
    
    def __init__(self, classroom_data: dict) -> None:
        self.id = classroom_data["id"]
        self.capacity = classroom_data["capacity"]
        self.available_days_ids = classroom_data["days"]
        self.available_time_ids = classroom_data["times"]
        
    @property
    def availabilities(self) -> List[Availability]:
        """
        Returns a list of all possible availabilities for the professor
        """
        availabilities = []
        for day_id in self.available_days_ids:
            for time_id in self.available_time_ids:
                availabilities.append(Availability(day_id, time_id))
        return availabilities
    
    def set_random_availability(self) -> None:
        """
        Sets a random availability for the professor
        """
        self.given_availability = random.choice(self.availabilities)

@dataclass
class Subject:
    id: int
    course_load: int

    def __init__(self, subject_data: dict) -> None:
        self.id = subject_data["id"]
        self.course_load = subject_data["hours"]

@dataclass
class Professor:
    id: int
    available_days_ids: List[int]
    available_time_ids: List[int]
    taughtble_subjects_ids: List[int]
    given_subject_id: int|None = None
    given_availability: Availability|None = None

    def __init__(self, professor_data: dict) -> None:
        self.id = professor_data["id"]
        self.available_days_ids = professor_data["days"]
        self.available_time_ids = professor_data["times"]
        self.taughtble_subjects_ids = professor_data["subjects"]

    @property
    def availabilities(self) -> List[Availability]:
        """
        Returns a list of all possible availabilities for the professor
        """
        availabilities = []
        for day_id in self.available_days_ids:
            for time_id in self.available_time_ids:
                availabilities.append(Availability(day_id, time_id))
        return availabilities
    
    def set_random_availability(self) -> None:
        """
        Sets a random availability for the professor
        """
        self.given_availability = random.choice(self.availabilities)

    def set_random_subject(self) -> None:
        """
        Sets a random subject for the professor
        """
        self.given_subject_id = random.choice(self.taughtble_subjects_ids)