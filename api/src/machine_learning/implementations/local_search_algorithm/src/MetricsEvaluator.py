import json
import time

from typing import Any

class MetricsEvaluator:
    def __init__(self, model: str) -> None:
        self.model = model
        self.metrics = {
            "time_to_converge": 0,
            "best_conflicts": 0,
            "best_elite_fitness": 0,
            "best_chromosome": None,
            "iterations": 0,
            "avg_conflicts_history": [], # Pure fitness conflicts 
            "avg_elite_fitness_history": [], # Fitness with conflicts resolved
            "time_to_evaluate": [],
        }

    def __repr__(self) -> str:
        return f"MetricsEvaluator({self.model})"
    
    def __str__(self) -> str:
        return f"MetricsEvaluator of Model: {self.model} with Metrics: {self.metrics}"
    
    def start_timer(self) -> None:
        self.start_time = time.time()
    
    def stop_timer(self):
        self.metrics["time_to_converge"] = (time.time() - self.start_time) / 60

    def start_iteration_timer(self) -> None:
        self.iteration_start_time = time.time()

    def stop_iteration_timer(self) -> None:
        self.metrics["time_to_evaluate"].append((time.time() - self.iteration_start_time) / 60)

    def update_metrics(self, iteration: int, avg_conflicts: float, avg_elite_fitness: float|None = None) -> None:
        self.metrics["iterations"] = iteration
        self.metrics["avg_conflicts_history"].append(avg_conflicts)
        if avg_elite_fitness is not None:
            self.metrics["avg_elite_fitness_history"].append(avg_elite_fitness)

    def update_best_metric(self, best_timetable: Any, best_conflicts: float, best_elite_fitness: float|None = None) -> None:
        self.metrics["best_timetable"] = best_timetable
        self.metrics["best_conflicts"] = best_conflicts
        if best_elite_fitness is not None:
            self.metrics["best_elite_fitness"] = best_elite_fitness

    def save_metrics(self, file_path: str) -> None:
        with open(file_path, "w") as file:
            json.dump(self.metrics, file, indent=4)


metrics_evaluator = MetricsEvaluator("Local Search Algorithm")