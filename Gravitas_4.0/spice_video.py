"""""""""""""""""""""""""""""""""
----------------------------------
GRAVITAS v.4.0.1 - video module
by Tomas Bezkorowajnyj c. June 2025
----------------------------------
"""""""""""""""""""""""""""""""""

import pathlib
import matplotlib.pyplot as plt
import matplotlib.animation as atn
import encounters as en
import numpy as np


PROJ_DIR = pathlib.Path(__file__).parent.resolve()

def visual_animation(dict_values, departure_time, arrival_time, velocity):
    """_summary_

    Args:
        dict_values (_type_): _description_
        departure_time (_type_): _description_
        arrival_time (_type_): _description_
        velocity (_type_): _description_
    """
    en.setup_kernel()
    eph_tme = en.get_ephemeris_time(departure_time, arrival_time, dict_values['step'])
    __frame = dict_values['frame']
    __abcorr = dict_values['abcorr']
    __observer = dict_values['observer']
    eph_trj_a = en.get_trajectory_data(dict_values['target'], eph_tme, __frame, __abcorr, __observer)
    eph_trj_b = en.get_trajectory_data(dict_values['origin'], eph_tme, __frame, __abcorr, __observer)
    
    # Create a figure and axes
    fig, _ = plt.subplots(figsize=(10, 6))

    # Function to update the plot for each frame of the animation
    def animate(i):
        fig.clear()
        ax = fig.add_subplot(projection='3d')
        ax.set_xlim(-5e8, 5e8)
        ax.set_ylim(-5e8, 5e8)
        ax.set_zlim(-5e7, 5e7)
        ax.scatter(eph_trj_a[i][0], eph_trj_a[i][1], eph_trj_a[i][2])
        ax.scatter(eph_trj_b[i][0], eph_trj_b[i][1], eph_trj_b[i][2])

    plt.grid(None)

    # Creating a FuncAnimation object
    ani = atn.FuncAnimation(fig, animate, interval=10, frames=range(len(eph_tme)))

    # Save the animation as a GIF using the PillowWriter
    ani.save(f'{PROJ_DIR}/fig/animation.gif', writer='pillow')
