class CrispSet:

    def __init__(self, name, values=None):
        if values is None:
            values = []
        self.name = name
        self.values = values

    def __str__(self):
        return 'Crisp set for %s' % self.name

    def __repr__(self):
        return 'Crisp set for %s' % self.name

    def get_crisp_value(self, value) -> str:
        return self.values[value]
