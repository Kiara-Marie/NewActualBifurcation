import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import matplotlib
# this line should be uncommented when running on ComputeCanada.
#matplotlib.use('Agg')
from particleManager import ParticleManager
import argparse
import config

def runSim():
    small_border = -10
    big_border = 10

    fig = plt.figure()
    ax = p3.Axes3D(fig)

    result = get_settings()
    target_shells = vars(result)['shells']
    num_points = vars(result)['points']
    check_time = vars(result)['time']
    filename = vars(result)['name']
    num_frames = vars(result)['frames']
    fps = vars(result)['fps']
    c_acceleration = vars(result)['a']
    max_dist = vars(result)['dist']
    frame_length = 1000 / fps
    config.SAVE = vars(result)['save']
    config.SHOW = vars(result)['show']
    config.CAREFUL = vars(result)['c']

    p_mngr = ParticleManager(target_shells, num_points, check_time, c_acceleration, max_dist)
    line, = ax.plot(xs=p_mngr.points[:, 0], ys=p_mngr.points[:, 1],
                    zs=p_mngr.points[:, 2], ls='', marker='.')
    # Creating the Animation object
    line_anim = animation.FuncAnimation(fig, p_mngr.update_fun, frames=num_frames,
                                        fargs=(line,), repeat=False,
                                        interval=frame_length, blit=False)
    ax.set_xlim3d([small_border, big_border])
    ax.set_ylim3d([small_border, big_border])
    ax.set_zlim3d([small_border, big_border])

    # Set up formatting for the movie files
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=fps, metadata=dict(artist='Kiara'), bitrate=1800)

    if (config.SAVE):
        line_anim.save(filename, writer=writer)
    if (config.SHOW):
        plt.show()
    return


def get_settings():

    parser = argparse.ArgumentParser(description='Run the bifurcation model')

    parser.add_argument('--shells', type=int, nargs='?',
                        help='Target number of shells', action='store', default=5)
    parser.add_argument('--points', type=int, nargs='?',
                        help='Target number of particles', action='store', default=1000)
    parser.add_argument('--c', '--careful', type=bool, nargs='?',
                        help='Whether to run extra (time consuming) checks to verify code is working properly',
                        action='store', default=True)
    parser.add_argument('--show', type=bool, nargs='?',
                        help='Whether to show the animation',
                        action='store', default=False)
    parser.add_argument('--save', type=bool, nargs='?',
                        help='Whether to save results to file',
                        action='store', default=True)
    parser.add_argument('--time', type=int, nargs='?',
                        help='Time (in ns) to consider densities from RESMO', 
                        action='store', default=20)
    parser.add_argument('--name', type=str, nargs='?',
                        help='Filename for file to save', 
                        action='store', default="animation.mp4")
    parser.add_argument('--frames', type=int, nargs='?',
                        help='Number of frames for the animation',
                        action='store', default='100')
    parser.add_argument('--fps', type=int, nargs='?',
                        help='Framerate for the animation',
                        action='store', default='60')
    parser.add_argument('--a', type=float, nargs='?',
                        help='Acceleration coefficient; should be negative',
                        action='store', default='-0.01')
    parser.add_argument('--dist', type=float, nargs='?',
                        help='Maximum distance for an ion to be considered near',
                        action='store', default='0.2')
    result = parser.parse_args()
    return result


runSim()
