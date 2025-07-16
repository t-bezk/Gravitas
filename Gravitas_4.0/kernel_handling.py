"""""""""""""""""""""""""""""""""
----------------------------------
GRAVITAS v.4.0.1 - kernel handling module
by Tomas Bezkorowajnyj c. June 2025
----------------------------------
"""""""""""""""""""""""""""""""""

import pathlib
import numpy as np
import spiceypy as spice

PROJ_DIR = pathlib.Path(__file__).parent.resolve()
SP_DIR = 'Spice_Kernels'    ## Kernel dir

def setup_kernel():
    """Locate spice kernel data in SP_DIR"""
    try:
        print(spice.tkvrsn('TOOLKIT'))
    except NotImplementedError as e:
        raise ValueError(f'Toolkit not found: {e}') from e
    ## Load SPICE kernels from file
    spice.furnsh(f"{PROJ_DIR}/{SP_DIR}/de421.bsp")
    spice.furnsh(f"{PROJ_DIR}/{SP_DIR}/naif0012.tls")

def destroy_kernel():
    """Clear kernel data after use"""
    spice.kclear()

def get_ephemeris_time(lower_bond, upper_bound, time_step):
    """Convert to ephemeris time and return ordered array"""
    eph0, eph1 = spice.str2et(lower_bond), spice.str2et(upper_bound)
    return np.arange(eph0, eph1, time_step)

def get_trajectory_data(origin, ets, frame, abcorr, observer):
    """Get position data array from time array"""
    return [spice.spkezr(origin, et, frame, abcorr, observer)[0] for et in ets]

def load_ephemeris_arrays(dict_values,d_t0,a_t0,bdy_tag):
    """Returns position and velocity arrays for both departure and arrival windows"""
    __frame = dict_values["frame"]
    __abcorr = dict_values["abcorr"]
    __observer = dict_values["observer"]
    ets = get_ephemeris_time(str(d_t0), str(a_t0), dict_values['step'])
    trj = get_trajectory_data(dict_values[bdy_tag], ets, __frame, __abcorr, __observer)
    return ets, trj
