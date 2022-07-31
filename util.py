import json

def load_json(path:str) -> dict:
    
    f = open(path)
    
    data = json.load(f)
    
    return data