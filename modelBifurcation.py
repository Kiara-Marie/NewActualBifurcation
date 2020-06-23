import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
from numpy import linalg as LA
from numpy.random import default_rng


def runSim():
    small_border = -10
    big_border = 10
    fig = plt.figure()
    ax = p3.Axes3D(fig)
    line, = ax.plot(xs=points[:, 0], ys=points[:, 1],
                    zs=points[:, 2], ls='', marker='.')
    # Creating the Animation object
    line_anim = animation.FuncAnimation(fig, update_fun, frames=100,
                                        fargs=(line,), repeat=False,
                                        interval=10, blit=False)
    ax.set_xlim3d([small_border, big_border])
    ax.set_ylim3d([small_border, big_border])
    ax.set_zlim3d([small_border, big_border])

    # Set up formatting for the movie files
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=15, metadata=dict(artist='Kiara'), bitrate=1800)

    line_anim.save('drifting_lobes.mp4', writer=writer)
    plt.show()


def create_ellipsoid_shell(r_i, r_o, num_points=100):
    """ r_i is the inner radius of the ellipsoid shell \n
        r_o is the outer radius of the ellipsoid shell """
    A = np.array([-1, 0, 0])
    B = np.array([1, 0, 0])
    rng = default_rng()
    unfiltered_points = (rng.random(size=(int(num_points*10), 3)) * r_o)
    unfiltered_points -= (r_o/2)
    dists_to_A = get_dists(A, unfiltered_points)
    dists_to_B = get_dists(B, unfiltered_points)
    total_dists = dists_to_A + dists_to_B
    filtered_points = unfiltered_points[(total_dists <= r_o), :]
    return filtered_points


def initialize_which_are_ions():
    initial_ion_proportion = 0.3
    num_ions = int(initial_ion_proportion * len(points))
    which_are_ions = [False for i in range(len(points))]
    which_are_ions[0:num_ions] = [True for i in range(num_ions)]
    return which_are_ions


def update_ion_densities():
    sphere_to_consider = 0.2
    global points
    global which_are_ions
    global local_ion_densities
    for p_index, point in enumerate(points):
        dists_to_point = get_dists(point, points)
        # how many points are within the max sphere of this point, and are ions? 
        which_are_close = dists_to_point <= sphere_to_consider
        local_ion_densities[p_index] = np.sum(which_are_close & which_are_ions)


def get_dists(point, mat):

    def minus_point_func(vec):
        return vec - point
    mat_minus_point = np.apply_along_axis(minus_point_func, 1, mat)
    dist_to_point = LA.norm(mat_minus_point, axis=1)
    return dist_to_point


def update_points(num, line):
    global points
    global speeds
    global local_ion_densities
    c_acceleration = -0.01
    accelerations = local_ion_densities * temperature_e * c_acceleration
    accelerations[accelerations > 0] = 0
    speeds = speeds + accelerations
    speeds[speeds < 0] = 0.05
    speeds_to_use = np.transpose(np.array([speeds, speeds, speeds]))
    points = points + (np.multiply(speeds_to_use, np.apply_along_axis(lambda v: v / LA.norm(v), 1, points)))
    line.set_data(np.transpose(points[:, 0:2]))
    line.set_3d_properties(np.transpose(points[:, 2]))
    return line,


def update_fun(num, line):
    update_points(num, line)
    update_ion_densities()


v_0 = 0.1
points = create_ellipsoid_shell(0, 3)
speeds = np.ones(len(points)) * v_0
temperature_e = 25
local_ion_densities = np.zeros(len(points))
which_are_ions = initialize_which_are_ions()
runSim()
