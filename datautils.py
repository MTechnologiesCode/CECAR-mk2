import json
import os

def save_data(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return {}
