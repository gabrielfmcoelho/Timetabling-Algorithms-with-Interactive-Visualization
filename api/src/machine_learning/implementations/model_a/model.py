from src.machine_learning.model import Model


class ModelA(Model):
    def setup(self, credentials_params: dict|None):
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