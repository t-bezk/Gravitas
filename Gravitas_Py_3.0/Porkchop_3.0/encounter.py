#ephemeris_plot.py

"""""""""""""""""""""""""""""""""
----------------------------------
GRAVITAS V.3.0 - Porkchop Plotter
by Tomas Bezkorowajnyj c. February 2025
----------------------------------
"""""""""""""""""""""""""""""""""


import numpy as np

from video_manager import *

from N_Body_Physics.Trajectory_Char import *

from N_Body_Physics.Physics import *

from display_manager import *

import pathlib

import spiceypy as spice

from poliastro.iod import izzo

from poliastro.bodies import Sun, Earth

from astropy import units as u


class P_CONFIG:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)  # Assign all key-value pairs as attributes

def P_Match(pd, sp_path):

    config = P_CONFIG(**pd)

    ##  Set the path to the image folder
    image_folder = f"{sp_path}/fig/"

    ##  Set the desired output video file name
    output_video_file = f"{sp_path}/video_output/output_video.mp4"

    ##  Output file name
    output_plot_title = config.out_title


    ##  Debug Package Loading
    print(spice.tkvrsn('TOOLKIT'))



    ##--Define departure and arrival parameters from spice kernels--##

    #   Load SPICE kernels
    spice.furnsh(f"{sp_path}/Spice_Kernels/de421.bsp")  # Ephemeris data
    spice.furnsh(f"{sp_path}/Spice_Kernels/naif0012.tls")  # leap seconds


    #   Convert to Ephemeris Time
    et_de0 = spice.str2et(config.d_time0)
    et_de1 = spice.str2et(config.d_time1)

    et_ar0 = spice.str2et(config.a_time0)
    et_ar1 = spice.str2et(config.a_time1)


    ##  Ephemeris time arrays
    ets_de = np.arange(et_de0, et_de1, config.step)
    ets_ar = np.arange(et_ar0, et_ar1, config.step)


def P_Solve(pd, sp_path):

    config = P_CONFIG(**pd)

    ##  Set the path to the image folder
    image_folder = f"{sp_path}/fig/"

    ##  Set the desired output video file name
    output_video_file = f"{sp_path}/video_output/output_video.mp4"

    ##  Output file name
    output_plot_title = config.out_title


    ##  Debug Package Loading
    print(spice.tkvrsn('TOOLKIT'))



    ##--Define departure and arrival parameters from spice kernels--##

    #   Load SPICE kernels
    spice.furnsh(f"{sp_path}/Spice_Kernels/de421.bsp")  # Ephemeris data
    spice.furnsh(f"{sp_path}/Spice_Kernels/naif0012.tls")  # leap seconds


    #   Convert to Ephemeris Time
    et_de0 = spice.str2et(config.d_time0)
    et_de1 = spice.str2et(config.d_time1)

    et_ar0 = spice.str2et(config.a_time0)
    et_ar1 = spice.str2et(config.a_time1)


    ##  Ephemeris time arrays
    ets_de = np.arange(et_de0, et_de1, config.step)
    ets_ar = np.arange(et_ar0, et_ar1, config.step)


    #   Collect trajectory data
    trajectory_departure = np.array([spice.spkezr(config.origin, et, config.frame, config.abcorr, config.observer)[0] for et in ets_de])
    trajectory_arrival = np.array([spice.spkezr(config.target, et, config.frame, config.abcorr, config.observer)[0] for et in ets_ar])

    v0_m = np.zeros((len(trajectory_arrival),len(trajectory_departure), 3))
    v1_m = np.zeros((len(trajectory_arrival),len(trajectory_departure), 3))
    vp_m = np.zeros((len(trajectory_arrival),len(trajectory_departure), 3))
    va_m = np.zeros((len(trajectory_arrival),len(trajectory_departure), 3))
    tf_m = np.zeros((len(trajectory_arrival),len(trajectory_departure)))

    ##--Programming Loop--##

    debug_message = ''

    CURSOR_UP = "\033[1A"
    CLEAR = "\x1b[2K"

    print('Getting c3 array...')

    for i in range(len(trajectory_arrival)):

        debug_message = f'Generating Layers {i} of {len(trajectory_arrival)}'
        print(debug_message)

        for j in range(len(trajectory_departure)):
            
            if ets_ar[i] - ets_de[j] < 0:
                tf_m[i][j] = 1e20
                continue


            ##  Define velocity vectors
            v0 = 0*u.km/u.s
            v = 0*u.km/u.s
            vp = trajectory_departure[j][3:]
            va = trajectory_arrival[i][3:]


            ##  Izzo Lambert Solver
            try:
                lambert = izzo.lambert(Sun.k, trajectory_departure[j][:3]*u.km, trajectory_arrival[i][:3]*u.km, (ets_ar[i]*u.s - ets_de[j]*u.s),M=0)   # :3
                v0, v = next(lambert)

                tf_m[i][j] = (ets_ar[i] - ets_de[j])/(3600*24)
            except:
                pass

            v0_m[i][j] = v0
            v1_m[i][j] = v
            vp_m[i][j] = vp
            va_m[i][j] = va

        print(CURSOR_UP + CLEAR, end="")

    
    return np.array([v0_m, v1_m, vp_m, va_m])