from dataclasses import dataclass, Field
from typing import List, Dict, Set, Tuple, Any
from datetime import datetime
import time
import json


@dataclass
class IterationEvaluationMetrics:
    """
    A set of partial indicators about a iteration of the genetic algorithm;
    With those indicators, it is possible to analyze the performance of the model through execution time and the quality of the solutions;
    * Conflicts are the hard constraints that are not satisfied in the timetable;
    * Elite fitness is a metric that represents the quality of the best solution found in the population given some fitness function;
    """
    iteration: int
    chromosome: Any
    avg_conflicts: float
    elite_fitness: float|None
    time_elapsed: float
    
@dataclass
class EvaluationMetrics:
    """
    A data structure to store the evaluation metrics of genetic algorithms models;
    It tracks partial indicators about each iteration and the best indicators of the model;
    """
    iteration_history: List[IterationEvaluationMetrics]
    best_iteration: IterationEvaluationMetrics
    total_time_elapsed: float

    def __init__(self, main_metric_of_evaluation: str) -> None:
        if main_metric_of_evaluation not in ["conflicts", "elite_fitness"]:
            raise ValueError("The main metric of evaluation must be 'conflicts' or 'elite_fitness'")
        self.main_metric_of_evaluation = main_metric_of_evaluation
        self.iteration_history = []
        self.best_iteration = IterationEvaluationMetrics(0, None, 0, 0, 0)

    def __compare_conflicts(self, iteration_evaluation_metrics: IterationEvaluationMetrics) -> None:
        """
        Compare the conflicts of the iteration with the best iteration found so far;
        """
        if iteration_evaluation_metrics.avg_conflicts < self.best_iteration.avg_conflicts:
            print(f"New best iteration found with {iteration_evaluation_metrics.avg_conflicts} conflicts !")
            self.best_iteration = iteration_evaluation_metrics

    def __compare_elite_fitness(self, iteration_evaluation_metrics: IterationEvaluationMetrics) -> None:
        """
        Compare the elite fitness of the iteration with the best iteration found so far;
        """
        if iteration_evaluation_metrics.elite_fitness > self.best_iteration.elite_fitness:
            print(f"New best iteration found with {iteration_evaluation_metrics.elite_fitness} elite fitness !")
            self.best_iteration = iteration_evaluation_metrics

    def add_iteration_evaluation_metrics(self, iteration_evaluation_metrics: IterationEvaluationMetrics) -> None:
        """
        Add a new iteration evaluation metrics to the evaluation metrics data structure;
        The main metric to compare the quality of the solution is the average of conflicts in the timetable (the N number of hard constraints not satisfied);
        """
        print(f"Iteration {iteration_evaluation_metrics.iteration} - Conflicts: {iteration_evaluation_metrics.avg_conflicts} - Elite Fitness: {iteration_evaluation_metrics.elite_fitness} - Time Elapsed: {iteration_evaluation_metrics.time_elapsed}")
        self.iteration_history.append(iteration_evaluation_metrics)
        if self.main_metric_of_evaluation == "conflicts":
            self.__compare_conflicts(iteration_evaluation_metrics)
        elif self.main_metric_of_evaluation == "elite_fitness":
            self.__compare_elite_fitness(iteration_evaluation_metrics)

    def calculate_total_time_elapsed(self, start_time: float) -> None:
        """
        Calculate the total time elapsed in the execution of the genetic algorithm model;
        """
        self.total_time_elapsed = time.time() - start_time


class MetricsEvaluator:
    """
    A class to manage the workflow of the evaluation metrics of genetic algorithms models;
    It tracks the performance of the model through the evaluation of the quality of the solutions and the execution time;
    """
    def __init__(self, model: str, main_metric_of_evaluation: str) -> None:
        print(f"Creating MetricsEvaluator of Model: {model}, starting evaluation")
        self.model: str = model
        self.metrics: EvaluationMetrics = EvaluationMetrics(main_metric_of_evaluation)
        self.start_time = time.time()

    def __repr__(self) -> str:
        return f"MetricsEvaluator({self.model})"
    
    def __str__(self) -> str:
        return f"MetricsEvaluator of Model: {self.model} with Metrics: {self.metrics}"

    def start_iteration(self) -> None:
        """
        Start the timer of the iteration to evaluate the execution time of the genetic
        """
        self.iteration_start_time: float = time.time()
        print(f"Starting iteration {len(self.metrics.iteration_history) + 1}")

    def finish_iteration(self, iteration: int, chromosome: Any, avg_conflicts: float, elite_fitness: float|None = None) -> None:
        """
        Finish the iteration, save it's partial metrics and calculate the time elapsed
        """
        iteration_time_elapsed: float = time.time() - self.iteration_start_time
        self.metrics.add_iteration_evaluation_metrics(IterationEvaluationMetrics(iteration, chromosome, avg_conflicts, elite_fitness, iteration_time_elapsed))
        print(f"Iteration {iteration} finished")

    def __save_evaluation(self) -> None:
        """
        Save the evaluation metrics of the genetic algorithm model in a json file
        """
        print(f"Saving evaluation metrics of the model {self.model}")
        with open(f"../../../data/{self.model}_evaluation_metrics_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json", 'w') as file:
            json.dump(self.metrics, file, default=lambda x: x.__dict__)
        print(f"Metrics of the model saved")

    def finish_evaluation(self) -> None:
        """
        Finish the evaluation of the genetic algorithm model therefore calculating the total time elapsed and saving the evaluation metrics
        """
        self.metrics.calculate_total_time_elapsed(self.start_time)
        print(f"With a total time elapsed of {self.metrics.total_time_elapsed} seconds and {len(self.metrics.iteration_history)} iterations, the best iteration found was {self.metrics.best_iteration} which is the best solution found by the model with {self.metrics.best_iteration.avg_conflicts} conflicts and {self.metrics.best_iteration.elite_fitness} elite fitness")
        self.__save_evaluation()
    