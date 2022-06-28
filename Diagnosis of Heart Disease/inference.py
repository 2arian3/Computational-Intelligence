import re
from utils.Rule import Rule

def read_rules(filename='rules.fcl') -> list:
    with open(filename, 'r') as f:
        rules = f.readlines()
    for i in range(len(rules)):
        rules[i] = rules[i].strip()
        rules[i] = rules[i][0:-1]
        rules[i] = re.sub('RULE [0-9]+: ', '', rules[i])  
    return [Rule(rule) for rule in rules]


def inference(fuzzy_params: dict, crisp_params: dict,
              fuzzy_values: dict, crisp_values: dict) -> dict:
    rules = read_rules()
    outputs = {key: 0 for key, _ in fuzzy_params['output'].items()}
    
    for rule in rules:
        print(rule)
        for logic_input in rule.inputs:
            input_parameter = rule.inputs[logic_input]
            if logic_input in crisp_params:
                input_parameter.set_fuzzy_value(
                    1 if crisp_values[logic_input] == input_parameter.name or crisp_values[logic_input] == 'exercise' else 0
                )
            elif logic_input in fuzzy_params:
                input_parameter.set_fuzzy_value(fuzzy_values[logic_input][input_parameter.name])
                
            print(input_parameter.value)
        output_name = rule.output[list(rule.output.keys())[0]].name
        outputs[output_name] = max(outputs[output_name], rule.get_fuzzy_output())
        print('OUT: ', rule.get_fuzzy_output())
    return outputs
    