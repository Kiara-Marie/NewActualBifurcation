import numpy as np
from numpy import linalg as LA
from numpy.random import default_rng
#from readDensityDataFromFile import get_shell_vals
from dummyVals import get_shell_vals as get_dummy_vals
from mathUtils import get_dists, solve_for_foci
import constants as C


class ParticleManager():

    def __init__(self, target_shells, total_desired_num_points, 
                 check_time, c_acceleration, max_dist, temp_drop):
        # 20 m/s = 2e-8 m/ns = 2e-5 micrometers/ns
        v_0 = 2e-5                            # micrometers / ns
        self.max_dist = max_dist              # micrometers
        self.c_acceleration = c_acceleration  # micrometers / ns^2
        self.temp_drop = temp_drop
        # get_shell_vals will set the temperature, in K
        # self.e_temperature, shell_widths, num_points_by_shell, num_ions_by_shell = \
        #     get_shell_vals(target_shells,  total_desired_num_points, check_time)
        self.e_temperature, shell_widths, num_points_by_shell, num_ions_by_shell = \
            get_dummy_vals(total_desired_num_points)
        num_shells = len(num_points_by_shell)
        total_num_points = int(np.sum(num_points_by_shell))
        self.initialize_points(total_num_points, num_shells, shell_widths,
                               num_points_by_shell, num_ions_by_shell)
        self.speeds = np.zeros(total_num_points)
        self.speeds[self.which_are_ions] = np.ones(np.sum(self.which_are_ions)) * v_0
        self.update_ion_densities()

    def create_ellipsoid_shell(self, r_i, r_o, num_points):
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
        sphere_to_consider = self.max_dist
        self.local_ion_densities = np.zeros(len(self.points))
        for p_index, point in enumerate(self.points):
            dists_to_point = get_dists(point, self.points)
            # how many points are within the max sphere of this point, and are ions?
            which_are_close = dists_to_point <= sphere_to_consider
            self.local_ion_densities[p_index] = np.sum(which_are_close &
                                                       self.which_are_ions)

    def update_points(self, line):
        accelerations = np.zeros(len(self.which_are_ions))
        acceleration_val = self.e_temperature * self.c_acceleration
        num_ions = np.sum(self.which_are_ions)
        accelerations[self.which_are_ions] = [acceleration_val for i in range(num_ions)] 
        accelerations[accelerations < 0] = 0
        self.update_temp(accelerations)
        self.speeds += accelerations
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

        self.total_num_points = total_num_points
        self.points = np.zeros((total_num_points, 3))
        self.which_are_ions = [False for i in range(total_num_points)]
        shell_widths = np.insert(shell_widths, 0, 0)
        points_so_far = 0
        for shell in range(num_shells):
            shell_width = shell_widths[shell]
            num_points = num_points_by_shell[shell]
            r_i = shell_width
            r_o = shell_widths[shell+1]
            points_to_add = self.create_ellipsoid_shell(r_i, r_o, num_points)
            
            start = int(points_so_far)
            end = int(points_so_far + num_points)
            self.points[start:end, :] = points_to_add
            points_so_far += num_points

            num_ions = int(num_ions_by_shell[shell])
            ion_end = int(num_ions + start)
            self.which_are_ions[start:ion_end] = [True for i in range(num_ions)]

    def update_temp(self, accelerations):
        # delta_v = a*t (in this case, t = 1ns, a is in micrometres/ns^2)
        delta_v_sqr = accelerations ** 2
        sum_dvs = np.sum(delta_v_sqr)
        num_ions = np.sum(self.which_are_ions)
        # Should be multiplied by m_i / 3N_e K_b
        factor = C.ION_MASS / (3 * num_ions * C.BOLTZMANN)
        self.e_temperature -= self.temp_drop*(sum_dvs * factor)
