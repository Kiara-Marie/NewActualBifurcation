import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from numpy import linalg as LA
from numpy.random import default_rng
from readDensityDataFromFile import read_density_from_file
from solveQuadratic import solve_quadratic

class ParticleManager():

    def __init__(self, num_shells=20):
        v_0 = 0.1
        # get_shell_vals will set the temperature
        shell_widths, num_points_by_shell = self.get_shell_vals()
        total_num_points = np.sum(num_points_by_shell) * num_shells
        self.points = np.zeros((total_num_points, 3))
        for shell in range(num_shells):
            shell_width = shell_widths[shell]
            num_points = num_points_by_shell[shell]
            r_i = shell*shell_width
            r_o = (shell+1)*shell_width
            points_to_add = self.create_ellipsoid_shell(r_i, r_o, num_points)
            start = shell*num_points
            end = (shell+1)*num_points
            self.points[start:end, :] = points_to_add

        self.speeds = np.ones(len(self.points)) * v_0
        self.initialize_which_are_ions()
        self.update_ion_densities()

    def create_ellipsoid_shell(self, r_i, r_o, num_points=100):
        """ r_i is the inner radius of the ellipsoid shell \n
            r_o is the outer radius of the ellipsoid shell """

        # x = 2 ;  y, z = 1
        A_i, B_i, s_i = self.solve_for_foci(r_i)
        A_o, B_o, s_o = self.solve_for_foci(r_o) 
        rng = default_rng()

        unfiltered_points = (rng.random(size=(int(num_points*30), 3)) * r_o)
        unfiltered_points -= (r_o/2)

        dists_to_A = self.get_dists(A_o, unfiltered_points)
        dists_to_B = self.get_dists(B_o, unfiltered_points)
        total_dists = dists_to_A + dists_to_B
        filtered_points = unfiltered_points[(total_dists <= s_o), :]
        
        inner_dists_to_A = self.get_dists(A_i, unfiltered_points)
        inner_dists_to_B = self.get_dists(B_i, unfiltered_points)
        inner_total_dists = inner_dists_to_A + inner_dists_to_B
        filtered_points = unfiltered_points[(inner_total_dists >= s_i), :]

        if (len(filtered_points) < num_points):
            raise Exception("Not enough points found!")
        filtered_points = filtered_points[0:num_points]
        return filtered_points

    def initialize_which_are_ions(self):
        initial_ion_proportion = 0.3
        num_ions = int(initial_ion_proportion * len(self.points))
        self.which_are_ions = [False for i in range(len(self.points))]
        self.which_are_ions[0:num_ions] = [True for i in range(num_ions)]

    def update_ion_densities(self):
        sphere_to_consider = 0.2
        self.local_ion_densities = np.zeros(len(self.points))
        for p_index, point in enumerate(self.points):
            dists_to_point = self.get_dists(point, self.points)
            # how many points are within the max sphere of this point, and are ions?
            which_are_close = dists_to_point <= sphere_to_consider
            self.local_ion_densities[p_index] = np.sum(which_are_close &
                                                       self.which_are_ions)

    def get_dists(self, point, mat):
        def minus_point_func(vec):
            return vec - point
        mat_minus_point = np.apply_along_axis(minus_point_func, 1, mat)
        dist_to_point = LA.norm(mat_minus_point, axis=1)
        return dist_to_point

    def update_points(self, line):
        c_acceleration = -0.01
        accelerations = self.local_ion_densities * self.temperature_e * c_acceleration
        accelerations[accelerations > 0] = 0
        self.speeds += accelerations
        self.speeds[self.speeds < 0] = 0.05
        speeds_to_use = np.transpose(np.array([self.speeds, self.speeds, self.speeds]))
        def n_f(v): return v / LA.norm(v)
        norm_points = np.apply_along_axis(n_f, 1, self.points)
        self.points += (np.multiply(speeds_to_use, norm_points))
        line.set_data(np.transpose(self.points[:, 0:2]))
        line.set_3d_properties(np.transpose(self.points[:, 2]))
        return line,

    def solve_for_foci(self, a):
        coeff_a = -3
        coeff_b = -12*a
        coeff_c = 8*a*a
        d_1, d_2 = solve_quadratic(coeff_a, coeff_b, coeff_c)
        d = np.max(d_1, d_2)
        A = [-d/2, 0, 0]
        B = [d/2, 0, 0]
        s = (a*a + d*d)**(1/2)
        return A, B, s

    def update_fun(self, num, line):
        self.update_points(line)
        self.update_ion_densities()

    def get_shell_vals(self):
        file_to_read = "C:/Users/Kiara/Documents/glw/CleanBifurcation/Results/AllShellsCalcs_den_0p5/All_Fractions_vs_timepqn_50Density_0p5_shells_100_t_max_200.csv"
        ryds, electrons, volumes, temperature = read_density_from_file(file_to_read, 20)
        self.temperature_e = temperature



