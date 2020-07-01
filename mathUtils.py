import numpy as np
from numpy import linalg as LA


def solve_quadratic(a, b, c):
    discriminant = b**2 - 4*a*c
    if (discriminant < 0 or a == 0):
        return None, None
    option_1 = (-b + discriminant**(1/2)) / (2*a)
    option_2 = (-b - discriminant**(1/2)) / (2*a)
    return option_1, option_2


def solve_for_foci(a):
    coeff_a = -3
    coeff_b = -12*a
    coeff_c = 8*a*a
    d_1, d_2 = solve_quadratic(coeff_a, coeff_b, coeff_c)
    d = d_1 if d_1 > d_2 else d_2
    A = [-d/2, 0, 0]
    B = [d/2, 0, 0]
    s = (a*a + d*d)**(1/2)
    return A, B, s


def get_dists(point, mat):
    def minus_point_func(vec):
        return vec - point
    mat_minus_point = np.apply_along_axis(minus_point_func, 1, mat)
    dist_to_point = LA.norm(mat_minus_point, axis=1)
    return dist_to_point
