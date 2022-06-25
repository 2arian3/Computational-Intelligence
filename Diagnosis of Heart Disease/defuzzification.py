from scipy.integrate import quad


def centroid_defuzzification(output_membership_functions=[]):
    output_membership_function = lambda x: max(f(x) for f in output_membership_functions)
    try:
        return quad(lambda x: output_membership_function(x) * x, 0, 5)[0] / quad(output_membership_function, 0, 5)[0]
    except:
        return None