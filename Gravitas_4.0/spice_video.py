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
from Display.display_orbit import plot_trajectory
from time_stepped import get_min_dist, timestepped_ephemeris

## pathlib directory
PROJ_DIR = pathlib.Path(__file__).parent.resolve()

def visual_animation(dict_values, t_de, t_ar, velo):
    """generates GIF of orbital transfer given specified parameters

    Args:
        dict_values (dictionary): dictionaty
        t_de (string): departure time
        t_ar (string): arrival time
        velocity (string 3_): initial velocity of probe relative to sun on departure
    """
    ## Get seperate time and position arrays from ephemeris data
    eph_tme,eph_trj_a = en.load_ephemeris_arrays(dict_values, t_de, t_ar,'target')
    _, eph_trj_b = en.load_ephemeris_arrays(dict_values, t_de, t_ar,'origin')
    prb_eph = timestepped_ephemeris(dict_values,eph_trj_a,eph_trj_b,velo)

    print(get_min_dist(dict_values,eph_trj_a,prb_eph,velo))

    ## Create a figure and axes
    fig, _ = plt.subplots(figsize=(10, 6))

    orb_trj_a = plot_trajectory(eph_trj_a[0][3:]*1e3,eph_trj_a[0][:3]*1e3) * 1e-3
    orb_trj_b = plot_trajectory(eph_trj_b[0][3:]*1e3,eph_trj_b[0][:3]*1e3) * 1e-3
    orb_prb = plot_trajectory(prb_eph[0][3:]*1e3,prb_eph[0][:3]*1e3) * 1e-3

    ## Function to update the plot for each frame of the animation
    def animate(i):
        fig.clear()
        ax = fig.add_subplot(projection='3d')
        ax.set_xlim(-5e8, 5e8)
        ax.set_ylim(-5e8, 5e8)
        ax.set_zlim(-5e7, 5e7)
        ax.scatter(eph_trj_a[i][0], eph_trj_a[i][1], eph_trj_a[i][2])
        ax.plot(-orb_trj_a[0],-orb_trj_a[1],-orb_trj_a[2])
        ax.scatter(eph_trj_b[i][0], eph_trj_b[i][1], eph_trj_b[i][2])
        ax.plot(-orb_trj_b[0],-orb_trj_b[1],-orb_trj_b[2])
        ax.scatter(prb_eph[i][0],prb_eph[i][1],prb_eph[i][2])
        ax.plot(-orb_prb[0],-orb_prb[1],orb_prb[2])

    plt.grid(None)

    ## Creating a FuncAnimation object
    ani = atn.FuncAnimation(fig, animate, interval=1, frames=range(len(eph_tme)))

    ## Save the animation as a GIF using the PillowWriter
    ani.save(f'{PROJ_DIR}/fig/animation.gif', writer='pillow')

def visual_animation_3(dict_1, dict_2, t_de, t_ar, t_tr, velo):
    """generates GIF of orbital transfer given specified parameters

    Args:
        dict_values (dictionary): dictionaty
        t_de (string): departure time
        t_ar (string): arrival time
        velocity (string 3_): initial velocity of probe relative to sun on departure
    """
    ## Get seperate time and position arrays from ephemeris data
    eph_tme,eph_trj_a = en.load_ephemeris_arrays(dict_values, t_de, t_ar,'target')
    _, eph_trj_b = en.load_ephemeris_arrays(dict_values, t_de, t_ar,'origin')
    prb_eph = timestepped_ephemeris(dict_values,eph_trj_a,eph_trj_b,velo)

    print(get_min_dist(dict_values,eph_trj_a,prb_eph,velo))

    ## Create a figure and axes
    fig, _ = plt.subplots(figsize=(10, 6))

    orb_trj_a = plot_trajectory(eph_trj_a[0][3:]*1e3,eph_trj_a[0][:3]*1e3) * 1e-3
    orb_trj_b = plot_trajectory(eph_trj_b[0][3:]*1e3,eph_trj_b[0][:3]*1e3) * 1e-3
    orb_prb = plot_trajectory(prb_eph[0][3:]*1e3,prb_eph[0][:3]*1e3) * 1e-3

    ## Function to update the plot for each frame of the animation
    def animate(i):
        fig.clear()
        ax = fig.add_subplot(projection='3d')
        ax.set_xlim(-5e8, 5e8)
        ax.set_ylim(-5e8, 5e8)
        ax.set_zlim(-5e7, 5e7)
        ax.scatter(eph_trj_a[i][0], eph_trj_a[i][1], eph_trj_a[i][2])
        ax.plot(-orb_trj_a[0],-orb_trj_a[1],-orb_trj_a[2])
        ax.scatter(eph_trj_b[i][0], eph_trj_b[i][1], eph_trj_b[i][2])
        ax.plot(-orb_trj_b[0],-orb_trj_b[1],-orb_trj_b[2])
        ax.scatter(prb_eph[i][0],prb_eph[i][1],prb_eph[i][2])
        ax.plot(-orb_prb[0],-orb_prb[1],orb_prb[2])

    plt.grid(None)

    ## Creating a FuncAnimation object
    ani = atn.FuncAnimation(fig, animate, interval=1, frames=range(len(eph_tme)))

    ## Save the animation as a GIF using the PillowWriter
    ani.save(f'{PROJ_DIR}/fig/animation.gif', writer='pillow')
