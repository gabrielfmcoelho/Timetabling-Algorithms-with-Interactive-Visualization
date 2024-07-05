from dataclasses import dataclass, Field


class Model:
    def setup(self, data, parameters):
        """
        This method initializes and setup credentials (in case of third party) for the model instance.
        """
        raise NotImplementedError
    
    def run(self):
        """
        This method runs the model with the given data.
        """
        raise NotImplementedError
    
@dataclass
class ModelDefinition:
    """
    This class is used to define a model and its configuration parameters for instantiation and usage.
    """
    uid: str
    model: Model
    default_parameters: dict