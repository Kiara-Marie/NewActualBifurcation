import numpy as np
from loadFromBinary import load_from_binary


def read_density_from_file(filename, time_to_consider, target_shells):
    # densities are expressed as a percentage of the total particles

    mat = load_from_binary(filename)
    times, ryd, deac, electrons, temperatures, volumes = parse_matrix(mat)

    time_index = find_time(times, time_to_consider)

    ryd = ryd[time_index, :] 
    deac = deac[time_index, :]
    electrons = electrons[time_index, :] 
    volumes = volumes[time_index, :]
    temperature = temperatures[time_index]

    volumes = volumes / np.max(volumes)

    ryd, deac, electrons, volumes = reduce_shells(ryd, deac, electrons, volumes, target_shells)

    check_sum(ryd, deac, electrons)

    return ryd, electrons, volumes, temperature


def get_shell_vals(target_shells, total_desired_num_points, check_time):
    file_path = ""
    file_name = "All_Fractions_vs_timepqn_50Density_0p5_shells_100_t_max_200.bin"
    file_to_read = file_path + file_name
    ryds, electrons, volumes, temperature = read_density_from_file(file_to_read, check_time, target_shells)
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
    ryd_sum = np.sum(ryd)
    deac_sum = np.sum(deac)
    electrons_sum = np.sum(electrons)
    total_sum = ryd_sum + deac_sum + electrons_sum
    if np.abs(total_sum - 1) > 0.01:
        raise Exception("incorrect file format!")


def find_time(times, time_to_consider):
    time_index = np.searchsorted(times, time_to_consider, side='left')
    d_time_l = np.abs(times[time_index] - time_to_consider)
    d_time_r = np.abs(times[time_index + 1] - time_to_consider)
    time_index = time_index if d_time_l < d_time_r else time_index + 1
    return time_index


def parse_matrix(mat):
    # matrix is organized [times,totalRyd,totaldeac,totalE,Te,vol]
    #                      1        N         N       N    1   N
    num_shells = int((mat.shape[1] - 2) / 4)
    
    times = mat[:, 0]
    ryd = mat[:, 1:num_shells+1]
    deac = mat[:, num_shells+1:2*num_shells+1]
    electrons = mat[:, 2*num_shells+1:3*num_shells+1]
    temperatures = mat[:, 3*num_shells+1]
    volumes = mat[:, 3*num_shells + 2: 4*num_shells + 2]

    return times, ryd, deac, electrons, temperatures, volumes


def reduce_shells(ryd, deac, electrons, volumes, target_shells):
    total_particles = np.sum(ryd[0:target_shells]) 
    total_particles += np.sum(electrons[0:target_shells]) 
    total_particles += np.sum(deac[0:target_shells]) 

    ryd = ryd[0:target_shells] / total_particles
    deac = deac[0:target_shells] / total_particles
    electrons = electrons[0:target_shells] / total_particles
    volumes = volumes[0:target_shells]

    return ryd, deac, electrons, volumes
