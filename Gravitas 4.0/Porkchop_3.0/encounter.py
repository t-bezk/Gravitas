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

from datetime import datetime, timedelta

##  Retrieve local file directory
sp_path = pathlib.Path(__file__).parent.resolve()

def add_time_to_datetime(time_str, delt):   ##  Add time in seconds

    # Convert to datetime object
    time_obj = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S")

    # Add 60 days
    new_time_obj = time_obj + timedelta(seconds = delt)

    # Convert back to string in the same format
    new_time_str = new_time_obj.strftime("%Y-%m-%dT%H:%M:%S")

    return new_time_str


class P_CONFIG:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)  # Assign all key-value pairs as attributes


def porkchop_solve(dict_values):
    """
    Parameters:
    ---------------
    dict_values {

        d_time0 - departure window lower bound
        d_time1 - departure window upper bound
        a_time0 - arrival window lower bound
        a_time1 - arrival window upper bound

        target - 
        origin - 
        observer - 
        frame - 
        abcorr - 

        step - time step (recommended 1 day)
        out_title - 
    
    }

    Returns:
    ---------------

    """

    ##  Debug Package Loading
    print(spice.tkvrsn('TOOLKIT'))

    # Load SPICE kernels
    spice.furnsh(f"{sp_path}/Spice_Kernels/de421.bsp")
    spice.furnsh(f"{sp_path}/Spice_Kernels/naif0012.tls")

    # Convert to Ephemeris Time
    et_de0 = spice.str2et(dict_values["d_time0"])
    et_de1 = spice.str2et(dict_values["d_time1"])
    et_ar0 = spice.str2et(dict_values["a_time0"])
    et_ar1 = spice.str2et(dict_values["a_time1"])

    ##  Ephemeris time arrays
    ets_de = np.arange(et_de0, et_de1, dict_values["step"])
    ets_ar = np.arange(et_ar0, et_ar1, dict_values["step"])

    #   Collect trajectory data
    trajectory_departure = np.array([spice.spkezr(dict_values["origin"], et, dict_values["frame"], dict_values["abcorr"], dict_values["observer"])[0] for et in ets_de])
    trajectory_arrival = np.array([spice.spkezr(dict_values["target"], et, dict_values["frame"], dict_values["abcorr"], dict_values["observer"])[0] for et in ets_ar])

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

    for i, _ in enumerate(trajectory_arrival):

        debug_message = f'Generating Layers {i} of {len(trajectory_arrival)}'
        print(debug_message)

        for j, _ in enumerate(trajectory_departure):
            
            ##  Define velocity vectors
            v0 = 1e20*u.km/u.s
            v = 1e20*u.km/u.s
            vp = trajectory_departure[j][3:]
            va = trajectory_arrival[i][3:]


            if ets_ar[i] - ets_de[j] < 0:
                tf_m[i][j] = 1e20
                v0_m[i][j] = 1e20
                v1_m[i][j] = 1e20
                vp_m[i][j] = vp
                va_m[i][j] = va
                continue

            ##  Izzo Lambert Solver
            try:
                lambert = izzo.lambert(Sun.k, trajectory_departure[j][:3]*u.km, trajectory_arrival[i][:3]*u.km, (ets_ar[i]*u.s - ets_de[j]*u.s),M=0)   # :3
                v0, v = next(lambert)

                tf_m[i][j] = (ets_ar[i] - ets_de[j])/(3600*24)
            except:
                print("Lambert solver failed")

            v0_m[i][j] = v0
            v1_m[i][j] = v
            vp_m[i][j] = vp
            va_m[i][j] = va

        print(CURSOR_UP + CLEAR, end="")

    ## Offload spice kernel to prevent data leaks
    spice.kclear()
    
    return np.array([v0_m, v1_m, vp_m, va_m])


def P_Match(pd, sp_path, v_infinity, time_of_flight):

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

    second_time = add_time_to_datetime(config.d_time0, time_of_flight)

    et_de1 = spice.str2et(config.d_time1)

    et_ar0 = spice.str2et(config.a_time0)
    et_ar1 = spice.str2et(second_time)

    ets_ar = np.arange(et_ar0, et_ar1, config.step)

    dv_mag_2d = np.zeros((100, len(ets_ar)))

    for dt in range(100):
        #   Convert to Ephemeris Time
        et_de0 = spice.str2et(add_time_to_datetime(config.d_time0, 3600*24*dt))

        #   Collect trajectory data
        trajectory_departure = spice.spkezr(config.origin, et_de0, config.frame, config.abcorr, config.observer)[0]

        trajectory_arrival = np.array([spice.spkezr(config.target, et, config.frame, config.abcorr, config.observer)[0] for et in ets_ar])

        tf_m = np.zeros((len(trajectory_arrival)))
        dv_inf = np.zeros((len(trajectory_arrival), 3))


        ##--Programming Loop--##

        print('Getting Matching array...')

        for i in range(len(ets_ar)):

            ##  Define velocity vectors
            v0 = 0*u.km/u.s
            v = 0*u.km/u.s
            vp = trajectory_departure[3:]
            va = trajectory_arrival[i][3:]


            ##  Izzo Lambert Solver
            try:
                lambert = izzo.lambert(Sun.k, trajectory_departure[:3]*u.km, trajectory_arrival[i][:3]*u.km, ets_ar[i]*u.s,M=0)   # :3
                v0, v = next(lambert)

                tf_m[i] = ets_ar[i]/(3600*24)
            except:
                v0, v = 1e10*u.km/u.s, 1e10*u.km/u.s


            dv_inf[i,:] = (v0.value - vp)

        dv_i = np.linalg.norm(v_infinity - dv_inf, axis=1)

        #plt.plot(ets_ar, dv_i)
        dv_mag_2d[dt] = dv_i
        #plt.show()

    return dv_mag_2d

















def getPlanetaryEphemeris(pd, sp_path):

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

    return trajectory_departure, trajectory_arrival
