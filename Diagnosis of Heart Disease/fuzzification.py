import json
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
           

def step_function(axis, isAscending=True):
    return (lambda x: (x >= axis and 1) or 0) if isAscending else (lambda x: (x <= axis and 1) or 0)


def create_fuzzy_sets(parameters: dict) -> dict:
    fuzzy_sets = {}
    fuzzy_params = {key: values for key, values in parameters.items() if values['type'] == 'fuzzy'}
    for key, values in fuzzy_params.items():
        fuzzy_sets[key] = {}
        for value in values['enum']:
            fuzzy_sets[key][value] = FuzzySet(value)
            fuzzy_sets[key][value].set_membership(
                waterfall_function(values['enum'][value]['x1'], values['enum'][value]['x2'], values['enum'][value]['isAscending'])
                if 'isAscending' in values['enum'][value] and 'isStepFunction' not in values['enum'][value] else
                (trapezoid_function(values['enum'][value]['x1'], values['enum'][value]['x2'], values['enum'][value]['x3'])
                 if'isStepFunction' not in values['enum'][value] else step_function(values['enum'][value]['x'], values['enum'][value]['isAscending']))
            )
    
    return fuzzy_sets


def create_crisp_sets(parameters: dict) -> dict:
    crisp_sets = {key: CrispSet(key, values['enum'])
                  for key, values in parameters.items() if values['type'] == 'crisp'}

    return crisp_sets   
 

def get_parameters():
    params = read_parameters()
    fuzzy_parameters = create_fuzzy_sets(params)
    crisp_parameters = create_crisp_sets(params)

    return params, fuzzy_parameters, crisp_parameters


def fuzzification(input_dict: dict):
    _, fuzzy_parameters, crisp_parameters = get_parameters()
    fuzzy_values = {key1: {key2: 0 for key2, _ in value1.items()} for key1, value1 in fuzzy_parameters.items()}
    crisp_values = {key: '' for key, _ in crisp_parameters.items()}

    for key, value in input_dict.items():
        if key in fuzzy_values:
            for param in fuzzy_values[key]:
                fuzzy_values[key][param] = fuzzy_parameters[key][param].get_membership_value(float(value))
        else:
            crisp_values[key] = crisp_parameters[key].get_crisp_value(value)
    
    return fuzzy_parameters, crisp_parameters, fuzzy_values, crisp_values