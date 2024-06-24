import random
from copy import deepcopy
from typing import List, Dict

from generate_initial_solution import generate_initial_solution
from evaluate_solution import evaluate_solution

""" Algoritmo de busca local para timetabling """

def local_search(
    classes: List[Dict], 
    teachers: List[Dict], 
    rooms: List[Dict], 
    times: List[Dict], 
    subjects: List[Dict], 
    max_iterations: int = 1000
) -> List[Dict]:

    best_solution = generate_initial_solution(classes, teachers, rooms, times, subjects)
    best_score = evaluate_solution(best_solution)

    for _ in range(max_iterations):
        candidate_solution = deepcopy(best_solution)

        # Perturbação: Troca aleatória de alguns horários
        for class_info in candidate_solution:
            for day_schedule in class_info['schedule']:
                random_time_index = random.randint(0, len(times) - 1)
                random_teacher = random.choice(teachers)
                random_room = random.choice(rooms)
                subject = random.choice(random_teacher['subjects'])
                teacher_name = random_teacher['name']
                room_name = random_room['name']
                day_schedule['periods'][random_time_index] = {
                    "day": day_schedule['day'],
                    "times": f"{times[random_time_index]['start']} - {times[random_time_index]['end']}",
                    "subject": next((sub['name'] for sub in subjects if sub['id'] == subject), None),
                    "teacher": teacher_name,
                    "room": room_name
                }

        candidate_score = evaluate_solution(candidate_solution)  

        if candidate_score < best_score:
            best_solution = deepcopy(candidate_solution)
            best_score = candidate_score

    return best_solution