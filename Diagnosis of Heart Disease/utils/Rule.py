import re

class Parameter:
    def __init__(self, name) -> None:
        self.name = name
        self.value = None
    
    def __str__(self):
        return 'Fuzzy value for %s is %s' % self.name, self.value

    def __repr__(self):
        return 'Fuzzy value for %s is %s' % self.name, self.value
    
    def set_fuzzy_value(self, value):
        self.value = value

    
class Rule:
    OPERANDS = {
        'and': min,
        'or': max
    }
    
    def __init__(self, string) -> None:
        self.string = string
        self.string = re.sub('IF ', '', self.string)
        inputs_strings, output_strings = self.string.split(' THEN ')
        self.operands = []
        self.inputs, self.output = dict(), dict()
        for expression in re.findall('\[[^\]]*\]|\([^\)]*\)|\"[^\"]*\"|\S+',inputs_strings):
            expression = expression.lower()
            if expression in Rule.OPERANDS:
                self.operands.append(expression)
            else:
                expression = expression[1:-1].split()
                self.inputs[expression[0]] = Parameter(expression[-1])
        expression = output_strings.lower().split()
        self.output[expression[0]] = Parameter(expression[-1])
    
    def __str__(self):
        inputs_params = ['({} IS {})'.format(input_param, self.inputs[input_param].name) for input_param in self.inputs]
        inputs = inputs_params[0]
        for i in range(len(self.operands)):
            inputs += ' {} {}'.format(self.operands[i].upper(), inputs_params[i+1])
        output_param = list(self.output.keys())[0]
        return 'IF {} THEN ({} IS {})'.format(inputs, output_param, self.output[output_param].name)

    def __repr__(self):
        inputs_params = ['({} IS {})'.format(input_param, self.inputs[input_param].name) for input_param in self.inputs]
        inputs = inputs_params[0]
        for i in range(len(self.operands)):
            inputs += ' {} {}'.format(self.operands[i].upper(), inputs_params[i+1])
        output_param = list(self.output.keys())[0]
        return 'IF {} THEN ({} IS {})'.format(inputs, output_param, self.output[output_param].name)
      
    def set_fuzzy_value(self, name, value):
        self.inputs[name].set_fuzzy_value(value)
        
    def get_fuzzy_output(self):
        if len(self.operands) != len(self.inputs) - 1:
            return None
        for input_parameter in self.inputs:
            if self.inputs[input_parameter].value == None:
                return None
        input_parameters = list(self.inputs.keys())
        output = self.inputs[input_parameters[0]].value
        for i in range(1, len(input_parameters)):
            output = Rule.OPERANDS[self.operands[i-1]](output, self.inputs[input_parameters[i]].value)
        self.output[list(self.output.keys())[0]].value = output
        return output
            
        