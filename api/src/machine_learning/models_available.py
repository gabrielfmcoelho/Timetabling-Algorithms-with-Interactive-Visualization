from machine_learning.model_definition import ModelCredentials, ModelDefinition
from machine_learning.implementations.model_a.model import ModelA


# Models in stable version
LOCAL_SEARCH_ALGORITHM_DEFINITION = ModelDefinition(
    uid="local-search-algorithm",
    model=ModelA(),
    credentials_params=ModelCredentials()
)

GENETIC_ALGORITHM_DEFINITION = ModelDefinition(
    uid="genetic-algorithm",
    model=ModelA(),
    credentials_params=ModelCredentials()
)


# Dictionary of models available
MODELS_AVAILABLE = {
    "timetabling": {
        LOCAL_SEARCH_ALGORITHM_DEFINITION.uid: LOCAL_SEARCH_ALGORITHM_DEFINITION,
        GENETIC_ALGORITHM_DEFINITION.uid: GENETIC_ALGORITHM_DEFINITION
    }
}