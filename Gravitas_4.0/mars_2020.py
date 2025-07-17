"""""""""""""""""""""""""""""""""
----------------------------------
GRAVITAS v.4.0.1 - mars2020 demo
by Tomas Bezkorowajnyj c. June 2025
----------------------------------
"""""""""""""""""""""""""""""""""

import pathlib
from datetime import datetime, timedelta
import numpy as np
from matplotlib import pyplot as plt
from encounters import generate_porkchop
from kernel_handling import setup_kernel, destroy_kernel
from spice_video import visual_animation
from Display.figures import gen_porkchop_plot
from time_stepped import get_min
from dictionaries import M_2020

##  Retrieve local file directory
PROJ_DIR = pathlib.Path(__file__).parent.resolve()

def mars_2020():
    """Generate porkchop plot and transfer profile for most optimum Mars-2020 trajectory"""

    v0, v1, vp, va  = generate_porkchop(M_2020)

    ##  Define meshgrids for contour plot
    c3 = np.linalg.norm(v0 - vp, axis=2)**2
    vi = np.linalg.norm(v1 - va, axis=2)

    ##  Generate figure
    gen_porkchop_plot(M_2020, c3, vi)

    iy, ix = get_min(vi)
    vel_min = v0[iy][ix]

    print(np.min(vi))
    print(ix,iy)

    t_delta_x = timedelta(seconds=float(ix)*M_2020['step'])
    t_delta_y = timedelta(seconds=float(iy)*M_2020['step'])
    departure_time = datetime.strptime(M_2020['d_time0'], "%Y-%m-%dT%H:%M:%S") + t_delta_x
    arrival_time = datetime.strptime(M_2020['a_time0'], "%Y-%m-%dT%H:%M:%S") + t_delta_y

    visual_animation(M_2020, departure_time, arrival_time, vel_min)

    plt.show()
    plt.close()

    plt.show()


if __name__ == "__main__":

    setup_kernel()

    try:
        mars_2020()
    except IndexError as e:
        print(f'error: \n{e}')
    finally:
        destroy_kernel()
