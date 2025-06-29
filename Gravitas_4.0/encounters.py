"""""""""""""""""""""""""""""""""
----------------------------------
GRAVITAS v.4.0.1 - encounter module
by Tomas Bezkorowajnyj c. June 2025
----------------------------------
"""""""""""""""""""""""""""""""""

import pathlib
import numpy as np
import spiceypy as spice
from poliastro.iod import izzo
from poliastro.bodies import Sun
from astropy import units as u

## project constants
PROJ_DIR = pathlib.Path(__file__).parent.resolve()
SP_DIR = 'Spice_Kernels'    ## Kernel dir
CURSOR_UP = "\033[1A"
CLR = "\x1b[2K"


def setup_kernel():
    """Locate spice kernel data"""
    try:
        print(spice.tkvrsn('TOOLKIT'))
    except NotImplementedError as e:
        raise ValueError(f'Toolkit not found: {e}') from e

    ## Load SPICE kernels from file
    spice.furnsh(f"{PROJ_DIR}/{SP_DIR}/de421.bsp")
    spice.furnsh(f"{PROJ_DIR}/{SP_DIR}/naif0012.tls")


def get_ephemeris_time(lower_bond, upper_bound, time_step):
    """Convert to ephemeris time and return ordered array"""
    eph0, eph1 = spice.str2et(lower_bond), spice.str2et(upper_bound)
    return np.arange(eph0, eph1, time_step)


def get_trajectory_data(origin, ets, frame, abcorr, observer):
    """Get position data array from time array"""
    return [spice.spkezr(origin, et, frame, abcorr, observer)[0] for et in ets]


def lambert_solve(trajectory_departure, trajectory_arrival, ets_de, ets_ar, no_rotations=0):
    """_summary_

    Args:
        trajectory_departure (_type_): _description_
        trajectory_arrival (_type_): _description_
        ets_de (_type_): _description_
        ets_ar (_type_): _description_
        no_rotations (int, optional): _description_. Defaults to 0.

    Yields:
        _type_: _description_
    """
    for i, _ in enumerate(trajectory_arrival):
        debug_message = f'Generating Layers: {100 * i / len(trajectory_arrival)}% complete'
        print(debug_message)
        for j, _ in enumerate(trajectory_departure):
            ##  Define velocity vectors
            v0 = 1e20*u.km/u.s
            v = 1e20*u.km/u.s
            if ets_ar[i] - ets_de[j] < 0:
                continue    ## Ignore negative time

            ##  Izzo Lambert Solver
            try:
                lambert = izzo.lambert(
                    Sun.k, trajectory_departure[j][:3]*u.km,
                    trajectory_arrival[i][:3]*u.km,
                    ets_ar[i]*u.s - ets_de[j]*u.s,M=no_rotations) # :3
                v0, v = next(lambert)
            except ImportError:
                v0, v = None, None

            yield v0, v, trajectory_departure[j][3:], trajectory_arrival[i][3:]

        print(CURSOR_UP + CLR, end="")

    ## Offload spice kernel to prevent data leaks
    spice.kclear()


def generate_porkchop(dict_values,no_rotations=0):
    """Solve for velocity values in 2d meshgrid format

    Args:
        dict_values (_type_): _description_
        no_rotations (int, optional): _description_. Defaults to 0.

    Returns:
        _type_: _description_
    """
    setup_kernel()

    ## Load ephemeris data
    __frame = dict_values["frame"]
    __abcorr = dict_values["abcorr"]
    __observer = dict_values["observer"]
    ets_de = get_ephemeris_time(dict_values['d_time0'],dict_values['d_time1'],dict_values['step'])
    ets_ar = get_ephemeris_time(dict_values['a_time0'],dict_values['a_time1'],dict_values['step'])
    trj_de = get_trajectory_data(dict_values["origin"], ets_de, __frame, __abcorr, __observer)
    trj_ar = get_trajectory_data(dict_values["target"], ets_ar, __frame, __abcorr, __observer)

    ## Generate solution grid and reshape to appropriate format
    gen_arrays  = list(lambert_solve(trj_de, trj_ar, ets_de, ets_ar, no_rotations))
    v0_m, v1_m, vp_m, va_m = tuple(np.array([r[i] for r in gen_arrays]) for i in range(4))
    v0_m = v0_m.reshape(len(trj_ar), len(trj_de), 3)
    v1_m = v1_m.reshape(len(trj_ar), len(trj_de), 3)
    vp_m = vp_m.reshape(len(trj_ar), len(trj_de), 3)
    va_m = va_m.reshape(len(trj_ar), len(trj_de), 3)

    return v0_m, v1_m, vp_m, va_m
