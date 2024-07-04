import random
from copy import deepcopy
from typing import List, Dict

from .evaluate_solution import evaluate_solution
from .generate_initial_solution import generate_initial_solution
from .MetricsEvaluator import metrics_evaluator

def local_search(
    classes: List[Dict], 
    teachers: List[Dict], 
    rooms: List[Dict], 
    times: List[Dict], 
    subjects: List[Dict], 
    days: List[Dict], 
    max_iterations: int = 1000
) -> List[Dict]:
    
    best_solution = generate_initial_solution(classes, teachers, rooms, times, subjects, days)
    best_score = evaluate_solution(best_solution)
    metrics_evaluator.update_metrics(best_solution, best_score)

    for _ in range(max_iterations):
        metrics_evaluator.start_iteration_timer()
        candidate_solution = deepcopy(best_solution)

        # Perturbação: Troca aleatória de alguns horários
        for class_info in candidate_solution:
            for day_schedule in class_info['schedule']:
                day_id = next(day['id'] for day in days if day['name'] == day_schedule['day'])
                for idx, period in enumerate(day_schedule['periods'], start=1):
                    available_rooms = get_available_rooms(rooms, day_id, idx)
                    if available_rooms:
                        random_room = random.choice(available_rooms)
                        period['room'] = random_room['name']
                    else:
                        period['room'] = "No room available"

        candidate_score = evaluate_solution(candidate_solution)

        if candidate_score < best_score:
            best_solution = deepcopy(candidate_solution)
            best_score = candidate_score
            metrics_evaluator.update_metrics(best_solution, best_score)
        
        metrics_evaluator.update_best_metric(candidate_solution, candidate_score)
        metrics_evaluator.stop_iteration_timer()

    metrics_evaluator.stop_timer()

    return best_solution, metrics_evaluator

def get_available_rooms(rooms: List[Dict], day_id: int, time_id: int) -> List[Dict]:
    return [room for room in rooms if day_id in room['days'] and time_id in room['times']]