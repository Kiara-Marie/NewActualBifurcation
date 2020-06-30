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

    check_sum(ryd, deac, electrons)
    time_index = find_time(times, time_to_consider)

    # divide by 100 to convert from percentage to decimal
    ryd_ret = ryd[time_index, :] / 100
    e_ret = electrons[time_index, :] / 100
    volume_ret = volumes[time_index, :]
    temp_ret = temperatures[time_index]

    return ryd_ret, e_ret, volume_ret, temp_ret


def get_shell_vals():
    file_path = "C:/Users/Kiara/Documents/glw/CleanBifurcation/Results/AllShellsCalcs_den_0p5/"
    file_name = "All_Fractions_vs_timepqn_50Density_0p5_shells_100_t_max_200.csv"
    file_to_read = file_path + file_name
    check_time = 20
    total_desired_num_points = 500
    ryds, electrons, volumes, temperature = read_density_from_file(file_to_read, check_time)
    shell_widths, num_points_by_shell, num_ions_by_shell = find_widths_and_nums(ryds,
                                                                                electrons,
                                                                                volumes,
                                                                                total_desired_num_points)
    return temperature, shell_widths, num_points_by_shell, num_ions_by_shell


def find_widths_and_nums(ryds, electrons, volumes, total_desired_num_points):
    # a = b/2 = c/2
    # V = 4pi/3abc = pi/3 * a^3 -> (3V/pi)**(1/3) = a
    shell_widths = np.zeros(len(volumes))
    prev_vol = 0
    for index in range(len(volumes)):
        desired_volume = prev_vol + volumes[index]
        shell_widths[index] = (3*desired_volume/np.pi)**(1/3)
        prev_vol = ((np.pi) / 3) * (shell_widths[index] ** 3)
    num_points_by_shell = (ryds + electrons) * total_desired_num_points
    np.fix(num_points_by_shell, out=num_points_by_shell)
    num_ions_by_shell = electrons * total_desired_num_points
    return shell_widths, num_points_by_shell, num_ions_by_shell


def check_sum(ryd, deac, electrons):
    ryd_sum = np.sum(ryd, axis=1)
    deac_sum = np.sum(deac, axis=1)
    electrons_sum = np.sum(electrons, axis=1)
    total_sum = ryd_sum + deac_sum + electrons_sum
    if any(np.abs(total_sum - 100) > 0.01):
        raise Exception("incorrect file format!")


def find_time(times, time_to_consider):
    time_index = np.searchsorted(times, time_to_consider, side='left')
    d_time_l = np.abs(times[time_index] - time_to_consider)
    d_time_r = np.abs(times[time_index + 1] - time_to_consider)
    time_index = time_index if d_time_l < d_time_r else time_index + 1
    return time_index
