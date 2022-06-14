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
    
    fuzzy_sets['bloodsugar_veryhigh'].set_membership(
        lambda x: (x > 105 and (x < 120 and (x - 105) / 15 or 1)) or 0
    )
    
    fuzzy_sets['cholesterol_low'].set_membership(
        lambda x: (x < 197 and (x < 151 and 1 or (197 - x) / 46)) or 0
    )
    fuzzy_sets['cholesterol_medium'].set_membership(
        lambda x: (x < 250 and ((x > 215 and (250 - x) / 35) or (x > 188 and (x - 188) / 27) or 0)) or 0
    )
    fuzzy_sets['cholesterol_high'].set_membership(
        lambda x: (x < 307 and ((x > 263 and (307 - x) / 44) or (x > 217 and (x - 217) / 46) or 0)) or 0
    )
    fuzzy_sets['cholesterol_veryhigh'].set_membership(
        lambda x: (x > 281 and (x < 347 and (x - 281) / 66 or 1)) or 0
    )
    
    fuzzy_sets['heartrate_low'].set_membership(
        lambda x: (x < 141 and (x < 100 and 1 or (141 - x) / 41)) or 0
    )
    fuzzy_sets['heartrate_medium'].set_membership(
        lambda x: (x < 194 and ((x > 152 and (194 - x) / 42) or (x > 111 and (x - 111) / 41) or 0)) or 0
    )
    fuzzy_sets['heartrate_high'].set_membership(
        lambda x: (x > 152 and (x < 210 and (x - 152) / 58 or 1)) or 0
    )
    
    fuzzy_sets['ecg_normal'].set_membership(
        lambda x: (x < 0.4 and (x < 0 and 1 or (0.4 - x) / 0.4)) or 0
    )
    fuzzy_sets['ecg_abnormal'].set_membership(
        lambda x: (x < 1.8 and ((x > 1 and (1.8 - x) / 0.8) or (x > 0.2 and (x - 0.2) / 0.8) or 0)) or 0
    )
    fuzzy_sets['ecg_hypertrophy'].set_membership(
        lambda x: (x > 1.4 and (x < 1.9 and (x - 1.4) / 0.5 or 1)) or 0
    )
    
    fuzzy_sets['oldpeak_low'].set_membership(
        lambda x: (x < 2 and (x < 1 and 1 or 2 - x)) or 0
    )
    fuzzy_sets['oldpeak_risk'].set_membership(
        lambda x: (x < 4.2 and ((x > 2.8 and (4.2 - x) / 1.4) or (x > 1.5 and (x - 1.5) / 1.3) or 0)) or 0
    )
    fuzzy_sets['oldpeak_terrible'].set_membership(
        lambda x: (x > 2.5 and (x < 4 and (x - 2.5) / 1.5 or 1)) or 0
    )
    
    fuzzy_sets['output_healthy'].set_membership(
        lambda x: (x < 1 and (x < 0.25 and 1 or (1 - x) / 0.75)) or 0
    )
    fuzzy_sets['output_sick1'].set_membership(
        lambda x: (x < 2 and ((x > 1 and 2 - x) or (x > 0 and x) or 0)) or 0
    )
    fuzzy_sets['output_sick2'].set_membership(
        lambda x: (x < 3 and ((x > 2 and 3 - x) or (x > 1 and x - 1) or 0)) or 0
    )
    fuzzy_sets['output_sick3'].set_membership(
        lambda x: (x < 4 and ((x > 3 and 4 - x) or (x > 2 and x - 2) or 0)) or 0
    )
    fuzzy_sets['output_sick4'].set_membership(
        lambda x: (x > 3 and (x < 3.75 and (x - 3) / 0.75 or 1)) or 0
    )
    
    return fuzzy_sets
    
 
params = read_parameters()
fuzzy_parameters = create_fuzzy_sets(params)
crisp_parameters = create_crisp_sets(params)

fuzzy_sets = updating_membership_functions(fuzzy_parameters)

