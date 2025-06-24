"""""""""""""""""""""""""""""""""
----------------------------------
GRAVITAS v.4.0.1 - video module
by Tomas Bezkorowajnyj c. June 2025
----------------------------------
"""""""""""""""""""""""""""""""""

import pathlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as atn
import encounters as en
from Physics.Physics import updateVesselPhysics
from Display.display_orbit import plot_trajectory



PROJ_DIR = pathlib.Path(__file__).parent.resolve()

def visual_animation(dict_values, departure_time, arrival_time, velo):
    """_summary_

    Args:
        dict_values (_type_): _description_
        departure_time (_type_): _description_
        arrival_time (_type_): _description_
        velocity (_type_): _description_
    """
    en.setup_kernel()
    eph_tme = en.get_ephemeris_time(str(departure_time), str(arrival_time), dict_values['step'])
    __frame = dict_values['frame']
    __abcorr = dict_values['abcorr']
    __observer = dict_values['observer']
    eph_trj_a = en.get_trajectory_data(dict_values['target'],eph_tme,__frame,__abcorr,__observer)
    eph_trj_b = en.get_trajectory_data(dict_values['origin'],eph_tme,__frame,__abcorr,__observer)

    ## generate transfer positions
    prb_eph = np.zeros(shape=(len(eph_trj_a),6))
    prb_eph[0] = np.concatenate([eph_trj_b[0][:3], velo])
    for q, _ in enumerate(prb_eph):
        if q == 0:
            continue
        prb_eph[q] = updateVesselPhysics(prb_eph[q-1][:3],prb_eph[q-1][3:], dict_values['step'])

    ## Create a figure and axes
    fig, _ = plt.subplots(figsize=(10, 6))
    
    
    orb_trj_a = plot_trajectory(eph_trj_a[0][:3],eph_trj_a[0][3:])
    orb_trj_b = plot_trajectory(eph_trj_b[0][:3],eph_trj_b[0][3:])
    orb_prb = plot_trajectory(prb_eph[0][:3],prb_eph[0][3:])
    

    ## Function to update the plot for each frame of the animation
    def animate(i):
        fig.clear()
        ax = fig.add_subplot(projection='3d')
        ax.set_xlim(-5e8, 5e8)
        ax.set_ylim(-5e8, 5e8)
        ax.set_zlim(-5e7, 5e7)
        
        ax.scatter(eph_trj_a[i][0], eph_trj_a[i][1], eph_trj_a[i][2])
        #ax.plot(orb_trj_a[0],orb_trj_a[1],orb_trj_a[2])
        
        ax.scatter(eph_trj_b[i][0], eph_trj_b[i][1], eph_trj_b[i][2])
        #ax.plot(orb_trj_b[0],orb_trj_b[1],orb_trj_b[2])
        
        ax.scatter(prb_eph[i][0],   prb_eph[i][1],   prb_eph[i][2]  )
        #ax.plot(orb_prb[0],orb_prb[1],orb_prb[2])
        
    plt.grid(None)

    ## Creating a FuncAnimation object
    ani = atn.FuncAnimation(fig, animate, interval=1, frames=range(len(eph_tme)))

    ## Save the animation as a GIF using the PillowWriter
    ani.save(f'{PROJ_DIR}/fig/animation.gif', writer='pillow')
