import json


def load_data_as_json(path:str):
    movies_json = json.load(path)
    return movies_json