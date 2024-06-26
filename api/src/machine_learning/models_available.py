from src.machine_learning.model import ModelCredentials, ModelDefinition
from src.machine_learning.implementations.model_a.model import ModelA


# Models in stable version
model_a_definition = ModelDefinition(
    uid="local_search",
    model=ModelA(),
    credentials_params=ModelCredentials()
)

# Dictionary of models available
MODELS_AVAILABLE = {
    "timetabling": {
        model_a_definition.uid: model_a_definition
    }
}