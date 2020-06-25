import numpy as np


def read_density_from_file(filename, time_to_consider):
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
