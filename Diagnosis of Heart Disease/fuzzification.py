import json
import numpy as np
import matplotlib.pyplot as plt
from utils import FuzzySet
from utils import CrispSet


def read_parameters(filename='parameters.json') -> dict: 
    
    with open(filename, 'r') as f:
        parameters = json.load(f)
    
    return parameters


def trapezoid_function(starting, maximum_point, ending):
    return lambda x: (x < ending and ((x > maximum_point and (ending - x) / (ending - maximum_point)) or (x > starting and (x - starting) / (maximum_point - starting)) or 0)) or 0


def waterfall_function(starting, ending, isAscending=True):
    return (lambda x: (x > starting and (x < ending and (x - starting) / (ending - starting) or 1)) or 0) \
           if isAscending else (lambda x: (x < ending and (x < starting and 1 or (ending - x) / (ending - starting))) or 0)


def create_fuzzy_sets(parameters: dict) -> dict:
    fuzzy_sets = {}
    fuzzy_params = {key: values for key, values in parameters.items() if values['type'] == 'fuzzy'}
    for key, values in fuzzy_params.items():
        for value in values['enum']:
            fuzzy_set = '%s_%s' % (key, value)
            fuzzy_sets[fuzzy_set] = FuzzySet(fuzzy_set)
            fuzzy_sets[fuzzy_set].set_membership(
                waterfall_function(values['enum'][value]['x1'], values['enum'][value]['x2'], values['enum'][value]['isAscending'])
                if 'isAscending' in values['enum'][value] else
                trapezoid_function(values['enum'][value]['x1'], values['enum'][value]['x2'], values['enum'][value]['x3'])
            )
    
    return fuzzy_sets


def create_crisp_sets(parameters: dict) -> dict:
    crisp_sets = {key: [CrispSet(key, values['enum'])]
                  for key, values in parameters.items() if values['type'] == 'crisp'}

    return crisp_sets   
 
params = read_parameters()
fuzzy_parameters = create_fuzzy_sets(params)
crisp_parameters = create_crisp_sets(params)