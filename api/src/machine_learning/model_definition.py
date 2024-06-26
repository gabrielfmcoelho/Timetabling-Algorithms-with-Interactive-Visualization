from dataclasses import dataclass, Field


@dataclass
class ModelCredentials:
    """
    This class is used to define the credentials required to access some third party models.
    """
    credentials: dict|None = None
    credentials_path: str|None = None

class Model:
    def setup(self, credentials_params: ModelCredentials|None):
        """
        This method initializes and setup credentials (in case of third party) for the model instance.
        """
        if credentials_params:
            raise NotImplementedError
        return self
    
    def run(self, data: dict, **kwargs):
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
    credentials_params: ModelCredentials|None = None