"""""""""""""""""""""""""""""""""
----------------------------------
GRAVITAS v.4.0.1 - encounter module
by Tomas Bezkorowajnyj c. June 2025
----------------------------------
"""""""""""""""""""""""""""""""""

import numpy as np
from kernel_handling import load_ephemeris_arrays
from poliastro.iod import izzo
from poliastro.bodies import Sun
from astropy.units import si as u

CURSOR_UP = "\033[1A"
CLR = "\x1b[2K"
MU = 6.67e-20*1.989e30  ## in km

def lambert_solve(trajectory_departure, trajectory_arrival, ets_de, ets_ar, no_rotations=0):
    """
        Inputs a departure and arrival window and its corresponding time arrays
        and outputs four vector arrays encoding the initial and final velocities determined
        from the use of a Lambert's solver and the origin and target planet velocities.
    """
    for i, _ in enumerate(trajectory_arrival):
        debug_message = f'Generating Layers: {100 * i / len(trajectory_arrival)}% complete'
        print(debug_message)
        for j, _ in enumerate(trajectory_departure):
            v0 = 1e20 * u.km / u.s
            v = 1e20 * u.km / u.s
            if ets_ar[i] - ets_de[j] < 0:
                continue    ## Ignore negative time

            ## Izzo Lambert Solver
            try:
                lambert = izzo.lambert(
                    Sun.k, trajectory_departure[j][:3] * u.km,
                    trajectory_arrival[i][:3] * u.km,
                    ets_ar[i] * u.s - ets_de[j] * u.s, M = no_rotations) # :3
                v0, v = next(lambert)
            except ImportError:
                v0, v = None, None
            yield v0, v, trajectory_departure[j][3:], trajectory_arrival[i][3:]
        print(CURSOR_UP + CLR, end="")

def generate_porkchop(di,no_rotations=0):
    """
        vo, v1, vd, va = generate_porkchop(dictionary)
        
        Solve for velocity values in 2d meshgrid format and return
        them as an array of four vectors.


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

def get_periapsis(v_inf_in, v_inf_ou):
    """Returns closest approach distance based on relative approach and departure velocities"""
    ab_dot = np.dot(v_inf_in,v_inf_ou)
    ab_prod = np.linalg.norm(v_inf_in) * np.linalg.norm(v_inf_ou)
    theta = 0.5 * np.arccos( ab_dot / ab_prod )
    return (MU / np.linalg.norm(v_inf_ou)**2) * (-1 + 1 / np.sin(theta)) * 2E-6

def get_orbital_period(r):
    """Returns orbital period from radial distance"""
    return ( 4 * np.pi**2 / MU * np.linalg.norm(r)**3 ) ** 0.5
