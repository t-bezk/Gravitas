"""""""""""""""""""""""""""""""""
----------------------------------
GRAVITAS v.4.0.1 - figure module
by Tomas Bezkorowajnyj c. July 2025
----------------------------------
"""""""""""""""""""""""""""""""""

import pathlib
import numpy as np
import matplotlib.pyplot as plt

PROJ_DIR = pathlib.Path(__file__).parent.parent.resolve()

def gen_porkchop_plot(d_vals, c3, vi):
    """Graph a porkchop plot from data

    Args:
        d_vals (_type_): _description_
        c3 (_type_): _description_
        vi (_type_): _description_
    """
    fig1, ax1 = plt.subplots(figsize=(10,12))
    ev_c3_contour = ax1.contour(c3, levels=np.linspace(0,40,10), colors=[(0.0,0.0,1.0)])
    ev_vi_contour = ax1.contour(vi, levels=np.linspace(0,40,10), colors=[(1.0,0.0,0.0)])
    ax1.clabel(ev_c3_contour, inline=1, fontsize=10)
    ax1.clabel(ev_vi_contour, inline=1, fontsize=10)
    ax1.set_title(f'{d_vals["out_title"]}')
    ax1.set_xlabel(f'Departure Window (Days after UST:{d_vals["d_time0"]})')
    ax1.set_ylabel(f'Arrival Window (Days after UST:{d_vals["a_time1"]})')
    fig1.savefig(f'{PROJ_DIR}/video_output/{d_vals["out_title"]}.png')
