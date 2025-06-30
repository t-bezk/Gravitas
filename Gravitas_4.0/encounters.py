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
from Physics.physics import update_vessel_physics

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

def destroy_kernel():
    """Clear kernel"""
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

            ## Izzo Lambert Solver
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



def generate_porkchop(di,no_rotations=0):
    """Solve for velocity values in 2d meshgrid format

    Args:
        di (_type_): dictionary values
        no_rotations (int, optional): _description_. Defaults to 0.

    Returns:
        ndarray(4,N,3): velocity characteristics of simulation
    """
    try:
        ets_de, trj_de = load_ephemeris_arrays(di,di['d_time0'],di['d_time1'],'origin')
        ets_ar, trj_ar = load_ephemeris_arrays(di,di['a_time0'],di['a_time1'],'target')
    except NotImplementedError as e:
        print(f'Kernal not setup: {e}')

    ## Generate solution grid and reshape to appropriate format
    gen_arrays  = list(lambert_solve(trj_de, trj_ar, ets_de, ets_ar, no_rotations))
    v0_m, v1_m, vp_m, va_m = tuple(np.array([r[i] for r in gen_arrays]) for i in range(4))
    v0_m = v0_m.reshape(len(trj_ar), len(trj_de), 3)
    v1_m = v1_m.reshape(len(trj_ar), len(trj_de), 3)
    vp_m = vp_m.reshape(len(trj_ar), len(trj_de), 3)
    va_m = va_m.reshape(len(trj_ar), len(trj_de), 3)

    return v0_m, v1_m, vp_m, va_m

def timestepped_ephemeris(dict_values,eph_trj_a,eph_trj_b,velo):
    """_summary_

    Args:
        dict_values (_type_): _description_
        t_de (_type_): _description_
        t_ar (_type_): _description_
        velo (_type_): _description_
    """
    ## generate transfer positions
    prb_eph = np.zeros(shape=(len(eph_trj_a),6))
    prb_eph[0] = np.concatenate([eph_trj_b[0][:3], velo])   ## :3
    for q, _ in enumerate(prb_eph):
        if q == 0:
            continue
        prb_eph[q] = update_vessel_physics(prb_eph[q-1][:3],prb_eph[q-1][3:], dict_values['step'])

    return prb_eph

def get_min_dist(dict_values,trj_a,trj_b,velo):
    """_summary_

    Args:
        dict_values (_type_): _description_
        trj_a (_type_): _description_
        trj_b (_type_): _description_
        velo (_type_): _description_
    """
    pos_vec = np.abs(timestepped_ephemeris(dict_values,trj_a,trj_b,velo)[:][:3] - trj_b[:][:3])
    pos_mod = np.linalg.norm(pos_vec,axis=1)
    min_ind = np.concatenate(np.where(pos_mod == np.min(pos_mod)))
    return pos_vec[int(min_ind)]
