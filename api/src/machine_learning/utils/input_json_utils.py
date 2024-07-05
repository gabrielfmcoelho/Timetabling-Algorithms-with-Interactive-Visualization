import json


def load_data(file_path, dataclasses_relationships) -> dict:
    """
    Load data from a json file and return a dictionary with the data loaded as dataclasses of each entity
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
        timetabling_data = {}
        for entity, values in data.items():
            print(f"Loading {entity} data")
            timetabling_data[entity] = []
            for value in values:
                entity_value = dataclasses_relationships[entity](value)
                timetabling_data[entity].append(entity_value)
            print(f"{len(timetabling_data[entity])} of {entity} loaded")
        return timetabling_data
    

def load_data_to_dict(file_path) -> dict:
    """
    Load data from a json file and return a dictionary with the data loaded as dictionaries
    """
    print(f"Loading data from {file_path}")
    with open(file_path, 'r') as file:
        data = json.load(file)
        print(data)
        return data