import json
import numpy as np
import matplotlib.pyplot as plt
from utils.FuzzySet import FuzzySet
from utils.CrispSet import CrispSet


def read_parameters(filename='parameters.json') -> dict: 
    
    with open(filename, 'r') as f:
        parameters = json.load(f)
    
    return parameters


def create_fuzzy_sets(parameters: dict) -> dict:
    fuzzy_sets = {}
    fuzzy_params = {key: values for key, values in parameters.items() if values['type'] == 'fuzzy'}
    for key, values in fuzzy_params.items():
        for value in values['enum']:
            fuzzy_set = '%s_%s' % (key, value)
            fuzzy_sets[fuzzy_set] = FuzzySet(fuzzy_set)
    
    return fuzzy_sets


def create_crisp_sets(parameters: dict) -> dict:
    crisp_sets = {key: [CrispSet(key, values['enum'])]
                  for key, values in parameters.items() if values['type'] == 'crisp'}

    return crisp_sets


def updating_membership_functions(fuzzy_sets: dict) -> dict:
    fuzzy_sets['age_young'].set_membership(
        lambda x: (x < 38 and (x < 29 and 1 or (38 - x) / 9)) or 0
    )
    fuzzy_sets['age_mild'].set_membership(
        lambda x: (x < 45 and ((x > 38 and (45 - x) / 7) or (x > 33 and (x - 33) / 5) or 0)) or 0
    )
    fuzzy_sets['age_old'].set_membership(
        lambda x: (x < 58 and ((x > 48 and (58 - x) / 10) or (x > 40 and (x - 40) / 8) or 0)) or 0
    )
    fuzzy_sets['age_veryold'].set_membership(
        lambda x: (x > 52 and (x < 60 and (x - 52) / 8 or 1)) or 0
    )
    
    fuzzy_sets['bloodpressure_low'].set_membership(
        lambda x: (x < 134 and (x < 111 and 1 or (134 - x) / 23)) or 0
    )
    fuzzy_sets['bloodpressure_medium'].set_membership(
        lambda x: (x < 153 and ((x > 139 and (153 - x) / 14) or (x > 127 and (x - 127) / 12) or 0)) or 0
    )
    fuzzy_sets['bloodpressure_high'].set_membership(
        lambda x: (x < 172 and ((x > 157 and (172 - x) / 15) or (x > 142 and (x - 142) / 15) or 0)) or 0
    )
    fuzzy_sets['bloodpressure_veryhigh'].set_membership(
        lambda x: (x > 154 and (x < 171 and (x - 154) / 17 or 1)) or 0
    )
    
    x = np.arange(0, 200, 0.1)
    plt.plot(x, [fuzzy_sets['bloodpressure_veryhigh'].get_membership_value(i) for i in x])
    plt.show()
    
 
params = read_parameters()
fuzzy_parameters = create_fuzzy_sets(params)
crisp_parameters = create_crisp_sets(params)
updating_membership_functions(fuzzy_parameters)

