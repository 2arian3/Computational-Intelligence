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

rules = read_rules()
print(*rules)