import numpy as np


def read_density_from_file(filename, time_to_consider):
    # densities are expressed as a percentage of the total particles

    # matrix is organized [times,totalRyd,totaldeac,totalE,Te,vol]
    #                      1        N         N       N    1   N

    mat = np.loadtxt(filename, delimiter=",")

    num_shells = 100
    times = mat[:, 0]
    ryd = mat[:, 1:num_shells+1]
    deac = mat[:, num_shells+1:2*num_shells+1]
    electrons = mat[:, 2*num_shells+1:3*num_shells+1]
    temperatures = mat[:, 3*num_shells+1]
    volumes = mat[:, 3*num_shells + 2: 4*num_shells + 2]

    volumes = volumes / np.max(volumes)
    
    ryd_sum = np.sum(ryd, axis=1)
    deac_sum = np.sum(deac, axis=1)
    electrons_sum = np.sum(electrons, axis=1)
    total_sum = ryd_sum + deac_sum + electrons_sum
    if any(np.abs(total_sum - 100) > 0.01):
        raise Exception("incorrect file format!")
    
    time_index = np.searchsorted(times, time_to_consider, side='left')
    d_time_l = np.abs(times[time_index] - time_to_consider)
    d_time_r = np.abs(times[time_index + 1] - time_to_consider)
    time_index = time_index if d_time_l < d_time_r else time_index + 1
    return ryd[time_index, :], electrons[time_index, :], volumes[time_index, :], temperatures[time_index]


def get_shell_vals():
    file_path = "C:/Users/Kiara/Documents/glw/CleanBifurcation/Results/AllShellsCalcs_den_0p5/"
    file_name = "All_Fractions_vs_timepqn_50Density_0p5_shells_100_t_max_200.csv"
    file_to_read = file_path + file_name
    check_time = 20
    total_desired_num_points = 300
    ryds, electrons, volumes, temperature = read_density_from_file(file_to_read, check_time)
    self.temperature_e = temperature
    return temperature, find_widths_and_nums(ryds,
                                             electrons,
                                             volumes,
                                             total_desired_num_points)


def find_widths_and_nums(ryds, electrons, volumes, total_desired_num_points):    
    # a = b/2 = c/2
    # V = 4pi/3abc = pi/3 * a^3 -> (3V/pi)**(1/3) = a
    shell_widths = (3*volumes/np.pi)**(1/3)
    num_points_by_shell = (ryds + electrons) * total_desired_num_points
    return shell_widths, num_points_by_shell
