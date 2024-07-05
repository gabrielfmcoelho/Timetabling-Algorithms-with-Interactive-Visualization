from machine_learning.model_definition import ModelDefinition
from machine_learning.implementations.genetic_algorithm.model import GeneticAlgorithm
from machine_learning.implementations.local_search_algorithm.model import LocalSearchAlgorithm
from machine_learning.implementations.randomized.model import RandomizedSelectionAlgorithm


# Models in stable version
LOCAL_SEARCH_ALGORITHM_DEFINITION = ModelDefinition(
    uid="local-search-algorithm",
    model=LocalSearchAlgorithm(),
    default_parameters={
        "max_iterations": 100
    }
)

GENETIC_ALGORITHM_DEFINITION = ModelDefinition(
    uid="genetic-algorithm",
    model=GeneticAlgorithm(),
    default_parameters={
        "population_size": 200,
        "mutation_rate": 0.4,
        "crossover_rate": 0.6,
        "generations": 500,
        "fitness_threshold": 0.9,
        "course_load_one_class_threshold": 36
    }
)

RANDOMIZED_SELECTION_ALGORITHM_DEFINITION = ModelDefinition(
    uid="randomized-selection-algorithm",
    model=RandomizedSelectionAlgorithm(),
    default_parameters={}
)


# Dictionary of models available
MODELS_AVAILABLE = {
    "timetabling": {
        LOCAL_SEARCH_ALGORITHM_DEFINITION.uid: LOCAL_SEARCH_ALGORITHM_DEFINITION,
        GENETIC_ALGORITHM_DEFINITION.uid: GENETIC_ALGORITHM_DEFINITION,
        RANDOMIZED_SELECTION_ALGORITHM_DEFINITION.uid: RANDOMIZED_SELECTION_ALGORITHM_DEFINITION
    }
}