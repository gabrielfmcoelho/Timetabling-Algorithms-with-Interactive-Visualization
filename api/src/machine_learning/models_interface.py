from machine_learning.model_definition import Model
from machine_learning.models_available import MODELS_AVAILABLE


class ModelsInterface:
    @staticmethod
    def instantiate(uid: str, model_type: str, data: dict, parameters: dict|None = None) -> Model:
        """
        This method returns the model instance for the given uid and model_type.
        """
        for model_type_available in MODELS_AVAILABLE:
            if model_type is not None and model_type_available != model_type:
                continue
            if uid in MODELS_AVAILABLE[model_type_available]:
                model_definition = MODELS_AVAILABLE[model_type_available][uid]
        if not model_definition:
            raise ValueError(f"Model {uid} not found.")
        if not parameters:
            parameters = model_definition.default_parameters
        return model_definition.model.setup(data, parameters)
        
    @staticmethod
    def run(uid: str, model_type: str, data: dict, parameters: dict|None = None):
        """
        This method instantiate the model and calls the run method for the given data.
        """
        model = ModelsInterface.instantiate(uid, model_type, data, parameters)
        return model.run()