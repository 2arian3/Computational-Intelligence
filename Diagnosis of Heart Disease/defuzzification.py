from scipy.integrate import quad

def centroid_defuzzification(output_membership_functions=[]):
    output_membership_function = lambda x: max(f(x) for f in output_membership_functions)
    try:
        return quad(lambda x: output_membership_function(x) * x, 0, 4)[0] / quad(output_membership_function, 0, 4)[0]
    except:
        return None

    

def defuzzification(inference_outputs, fuzzy_params, crisp_params):
    functions = []
    functions.append(lambda x: min(inference_outputs['sick_1'], fuzzy_params['output']['sick_1'].get_membership_value(x)))
    functions.append(lambda x: min(inference_outputs['sick_2'], fuzzy_params['output']['sick_2'].get_membership_value(x)))
    functions.append(lambda x: min(inference_outputs['sick_3'], fuzzy_params['output']['sick_3'].get_membership_value(x)))
    functions.append(lambda x: min(inference_outputs['sick_4'], fuzzy_params['output']['sick_4'].get_membership_value(x)))
    functions.append(lambda x: min(inference_outputs['healthy'], fuzzy_params['output']['healthy'].get_membership_value(x)))
    
    return centroid_defuzzification(functions)