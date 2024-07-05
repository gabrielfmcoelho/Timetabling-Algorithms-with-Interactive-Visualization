from machine_learning.implementations.genetic_algorithm.src.entities import ClassGroup, Classroom, Subject, Professor, Day, Time
from machine_learning.implementations.genetic_algorithm.src.gene import Gene
from machine_learning.implementations.genetic_algorithm.src.chromosome import Chromosome
from machine_learning.models_evaluator import MetricsEvaluator
from machine_learning.model_definition import Model


class RandomizedSelectionAlgorithm(Model):
    def parameters_parser(self, data: dict, parameters: dict):
        class_groups = [ClassGroup(class_group) for class_group in data.get("class_groups", [])]
        classrooms = [Classroom(classroom) for classroom in data.get("classrooms", [])]
        subjects = [Subject(subject) for subject in data.get("subjects", [])]
        professors = [Professor(professor) for professor in data.get("professors", [])]
        days = [Day(day) for day in data.get("days", [])]
        times = [Time(time) for time in data.get("times", [])]
        if not class_groups or not classrooms or not subjects or not professors or not days or not times:
            raise Exception("Missing data")
        return class_groups, classrooms, subjects, professors, days, times

    def setup(self, data: dict, parameters: dict):
        class_groups, classrooms, subjects, professors, days, times = self.parameters_parser(data, parameters)
        self.metrics_evaluator = MetricsEvaluator("Randomized Selection Model", "conflicts")
        self.class_groups = class_groups
        self.classrooms = classrooms
        self.subjects = subjects
        self.professors = professors
        self.days = days
        self.times = times

    def run(self) -> MetricsEvaluator:
        self.metrics_evaluator.start_iteration()
        chromosome = Chromosome()
        for _ in range(CLASSES_NEED_TO_BE_SCHEDULED):
            gene = Gene()
            gene.generate_random_gene(self.class_groups, self.classrooms, self.subjects, self.professors)
            chromosome.add_gene(gene)
        self.metrics_evaluator.finish_iteration(0, chromosome, chromosome.amount_of_conflicts, chromosome.elite_fitness)
        self.metrics_evaluator.finish_evaluation()
        return self.metrics_evaluator
        