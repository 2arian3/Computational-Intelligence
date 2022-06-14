import json
import numpy as np
from utils.FuzzySet import FuzzySet
from utils.CrispSet import CrispSet


def read_parameters(filename='parameters.json') -> dict: 
    
    with open(filename, 'r') as f:
        parameters = json.load(f)
    
    return parameters


def create_fuzzy_sets(parameters: dict) -> dict:
    fuzzy_sets = {key: [FuzzySet('%s_%s' % (key, values['enum']))]
                  for key, values in parameters.items() if values['type'] == 'fuzzy'}

    return fuzzy_sets


def create_crisp_sets(parameters: dict) -> dict:
    crisp_sets = {key: [CrispSet(key, values['enum'])]
                  for key, values in parameters.items() if values['type'] == 'crisp'}

    return crisp_sets
   
 
params = read_parameters()
print(create_crisp_sets(params))