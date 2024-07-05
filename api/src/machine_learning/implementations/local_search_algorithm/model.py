import random
from copy import deepcopy
from typing import List, Dict

from machine_learning.implementations.local_search_algorithm.src.evaluate_solution import evaluate_solution
from machine_learning.implementations.local_search_algorithm.src.generate_initial_solution import generate_initial_solution
from machine_learning.models_evaluator import MetricsEvaluator
from machine_learning.model_definition import Model


class LocalSearchAlgorithm(Model):
    def parameters_parser(self, data: dict, parameters: dict):
        max_iterations = parameters.get("max_iterations")
        if not max_iterations:
            raise Exception("Missing parameters")
        classes = data.get("classes")
        teachers = data.get("teachers")
        rooms = data.get("rooms")
        times = data.get("times")
        subjects = data.get("subjects")
        days = data.get("days")
        if not classes or not teachers or not rooms or not times or not subjects or not days:
            raise Exception("Missing data")
        return max_iterations, classes, teachers, rooms, times, subjects, days
    
    def setup(self, data: dict, parameters: dict):
        max_iterations, classes, teachers, rooms, times, subjects, days = self.parameters_parser(data, parameters)
        self.metrics_evaluator = MetricsEvaluator("Local Search Algorithm", "conflicts")
        self.max_iterations = max_iterations
        self.classes = classes
        self.teachers = teachers
        self.rooms = rooms
        self.times = times
        self.subjects = subjects
        self.days = days

    def get_available_rooms(self, day_id: int, time_id: int) -> List[Dict]:
        return [room for room in self.rooms if day_id in room['days'] and time_id in room['times']]

    def run(self) -> MetricsEvaluator:
        best_solution = generate_initial_solution(self.classes, self.teachers, self.rooms, self.times, self.subjects, self.days)
        best_score = evaluate_solution(best_solution)

        for _ in range(self.max_iterations):
            self.metrics_evaluator.start_iteration()
            candidate_solution = deepcopy(best_solution)

            for class_info in candidate_solution:
                for day_schedule in class_info['schedule']:
                    day_id = next(day['id'] for day in self.days if day['name'] == day_schedule['day'])
                    for idx, period in enumerate(day_schedule['periods']):
                        available_rooms = self.get_available_rooms(day_id, idx + 1)
                        if available_rooms:
                            random_room = random.choice(available_rooms)
                            period['room'] = random_room['name']
                        else:
                            period['room'] = "No room available"

            candidate_score = evaluate_solution(candidate_solution)
        
            if candidate_score < best_score:
                best_solution = deepcopy(candidate_solution)
                best_score = candidate_score

            self.metrics_evaluator.finish_iteration(_, candidate_solution, candidate_score)

        self.metrics_evaluator.finish_evaluation()
        return self.metrics_evaluator