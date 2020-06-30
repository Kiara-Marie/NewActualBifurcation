import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
from particleManager import ParticleManager


def runSim():
    small_border = -10
    big_border = 10

    fig = plt.figure()
    ax = p3.Axes3D(fig)

    p_mngr = ParticleManager()
    line, = ax.plot(xs=p_mngr.points[:, 0], ys=p_mngr.points[:, 1],
                    zs=p_mngr.points[:, 2], ls='', marker='.')
    # Creating the Animation object
    line_anim = animation.FuncAnimation(fig, p_mngr.update_fun, frames=20,
                                        fargs=(line,), repeat=False,
                                        interval=100, blit=False)
    ax.set_xlim3d([small_border, big_border])
    ax.set_ylim3d([small_border, big_border])
    ax.set_zlim3d([small_border, big_border])

    # Set up formatting for the movie files
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=15, metadata=dict(artist='Kiara'), bitrate=1800)

    line_anim.save('drifting_lobes.mp4', writer=writer)
    #  plt.show()
    return


runSim()
