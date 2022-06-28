from fuzzification import fuzzification
from inference import inference
from defuzzification import defuzzification

class ProvideResult(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ProvideResult, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def get_final_result(input_dict: dict) -> str:
        fuzzy_params, crisp_params, fuzzy_values, crisp_values = fuzzification(input_dict)
        inference_outputs = inference(fuzzy_params, crisp_params, fuzzy_values, crisp_values)
        defuzzification_result = defuzzification(inference_outputs, fuzzy_params, crisp_params)
        
        results = []
        print(defuzzification_result)
        if defuzzification_result < 1.78:
            results.append('healthy')
        if 2.51 >= defuzzification_result >= 1:
            results.append('sick_1')
        if 3.25 >= defuzzification_result >= 1.78:
            results.append('sick_2')
        if 4.5 >= defuzzification_result >= 1.5:
            results.append('sick_3')
        if defuzzification_result > 3.25:
            results.append('sick_4')
        
        return ' & '.join(results)
