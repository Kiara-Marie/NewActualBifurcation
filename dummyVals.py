import numpy as np


def get_shell_vals(total_desired_num_points):
    ion_proportion = 0.2
    num_ions = total_desired_num_points * ion_proportion
    num_ryds = total_desired_num_points * (1-ion_proportion)
    num_points_by_shell = np.array([num_ions, num_ryds])
    num_ions_by_shell = np.array([num_ions, 0])
    shell_widths = np.array([3, 10])
    temperature = 20 # K
    return temperature, shell_widths, num_points_by_shell, num_ions_by_shell
