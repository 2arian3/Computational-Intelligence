class FuzzySet:

    def __init__(self, name):
        self.name = name
        self.membership = None

    def __str__(self):
        return 'Fuzzy set for %s' % self.name

    def __repr__(self):
        return 'Fuzzy set for %s' % self.name

    def set_membership(self, membership):
        self.membership = membership

    def get_membership_value(self, x) -> float:
        return self.membership(x)
