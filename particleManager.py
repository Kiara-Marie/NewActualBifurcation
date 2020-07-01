import numpy as np
from numpy import linalg as LA
from numpy.random import default_rng
from readDensityDataFromFile import get_shell_vals
from mathUtils import get_dists, solve_for_foci


class ParticleManager():

    def __init__(self):
        v_0 = 0.1
        # get_shell_vals will set the temperature
        self.e_temperature, shell_widths, num_points_by_shell, num_ions_by_shell = get_shell_vals()
        num_shells = len(num_points_by_shell)
        total_num_points = int(np.sum(num_points_by_shell))
        self.initialize_points(total_num_points, num_shells, shell_widths,
                               num_points_by_shell, num_ions_by_shell)
        self.speeds = np.ones(len(self.points)) * v_0
        self.update_ion_densities()

    def create_ellipsoid_shell(self, r_i, r_o, num_points=100):
        """ r_i is the inner radius of the ellipsoid shell \n
            r_o is the outer radius of the ellipsoid shell """
        A_i, B_i, s_i = solve_for_foci(r_i)
        A_o, B_o, s_o = solve_for_foci(r_o)
        rng = default_rng()
        num_points = int(num_points)

        unfiltered_points = (rng.random(size=(int(num_points*30), 3)) * r_o)
        unfiltered_points -= (r_o/2)

        dists_to_A = get_dists(A_o, unfiltered_points)
        dists_to_B = get_dists(B_o, unfiltered_points)
        total_dists = dists_to_A + dists_to_B
        filtered_points = unfiltered_points[(total_dists <= s_o), :]

        inner_dists_to_A = get_dists(A_i, unfiltered_points)
        inner_dists_to_B = get_dists(B_i, unfiltered_points)
        inner_total_dists = inner_dists_to_A + inner_dists_to_B
        filtered_points = unfiltered_points[(inner_total_dists >= s_i), :]

        if (len(filtered_points) < num_points):
            raise Exception("Not enough points found!")
        filtered_points = filtered_points[0:num_points]
        return filtered_points

    def update_ion_densities(self):
        sphere_to_consider = 0.2
        self.local_ion_densities = np.zeros(len(self.points))
        for p_index, point in enumerate(self.points):
            dists_to_point = get_dists(point, self.points)
            # how many points are within the max sphere of this point, and are ions?
            which_are_close = dists_to_point <= sphere_to_consider
            self.local_ion_densities[p_index] = np.sum(which_are_close &
                                                       self.which_are_ions)

    def update_points(self, line):
        c_acceleration = -0.01
        accelerations = self.local_ion_densities * self.e_temperature * c_acceleration
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

    def update_fun(self, num, line):
        self.update_points(line)
        self.update_ion_densities()

    def initialize_points(self, total_num_points, num_shells, shell_widths,
                          num_points_by_shell, num_ions_by_shell):

        self.points = np.zeros((total_num_points, 3))
        self.which_are_ions = [False for i in range(total_num_points)]
        for shell in range(num_shells):
            shell_width = shell_widths[shell]
            num_points = num_points_by_shell[shell]
            r_i = shell*shell_width
            r_o = (shell+1)*shell_width
            points_to_add = self.create_ellipsoid_shell(r_i, r_o, num_points)
            start = int(shell*num_points)
            end = int((shell+1)*num_points)
            self.points[start:end, :] = points_to_add

            num_ions = int(num_ions_by_shell[shell])
            ion_end = int(num_ions + start)
            self.which_are_ions[start:ion_end] = [True for i in range(num_ions)]
