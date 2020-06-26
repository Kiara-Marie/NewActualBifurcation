def solve_quadratic(a, b, c):
    discriminant = b**2 - 4*a*c
    if (discriminant < 0 or a == 0):
        return None, None
    option_1 = (-b + discriminant**(1/2)) / (2*a)
    option_2 = (-b - discriminant**(1/2)) / (2*a)
    return option_1, option_2
