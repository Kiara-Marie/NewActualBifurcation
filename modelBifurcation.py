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
    line_anim = animation.FuncAnimation(fig, update_points, frames=180,
                                       fargs=(line,), repeat=False,
                                       interval=10, blit=False)
    ax.set_xlim3d([small_border, big_border])
    ax.set_ylim3d([small_border, big_border])
    ax.set_zlim3d([small_border, big_border])

    # # Set up formatting for the movie files
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=15, metadata=dict(artist='Kiara'), bitrate=1800)

    line_anim.save('drifting_lobes.mp4', writer=writer)
    plt.show()


def createEllipsoid(num_points=1000, r=3):
    A = np.array([-1, 0, 0])
    B = np.array([1, 0, 0])
    rng = default_rng()
    unfiltered_points = (rng.random(size=(int(num_points*10), 3)) * r) - (r/2)
    dists_to_A = getDists(A, unfiltered_points)
    dists_to_B = getDists(B, unfiltered_points)
    total_dists = dists_to_A + dists_to_B
    filtered_points = unfiltered_points[(total_dists <= r), :]
    return filtered_points

def getDists(point, mat):
    def minus_point_func(vec):
        return vec - point

    mat_minus_point = np.apply_along_axis(minus_point_func, 1, mat)
    dist_to_point = LA.norm(mat_minus_point, axis=1)
    return dist_to_point


def update_points(num, line):
    max = 30
    if (num == max):
        return None
    global points
    global speeds
    def acceleration_fun(vec):
        x_factor = -0.05
        y_factor = 0.05
        return np.abs(vec[0])**(1/2) * x_factor + np.abs(vec[1])**(1/2) * y_factor
    accelerations = np.apply_along_axis(acceleration_fun, 1, points)
    accelerations[accelerations > 0] = 0
    speeds = speeds + accelerations
    speeds[speeds < 0] = 0.05
    speeds_to_use = np.transpose(np.array([speeds, speeds, speeds]))
    points = points + (np.multiply(speeds_to_use, np.apply_along_axis(lambda v: v / LA.norm(v), 1, points)))
    line.set_data(np.transpose(points[:, 0:2]))
    line.set_3d_properties(np.transpose(points[:, 2]))
    return line,

v_0 = 0.1
points = createEllipsoid()
speeds = np.ones(len(points)) * v_0
runSim()
