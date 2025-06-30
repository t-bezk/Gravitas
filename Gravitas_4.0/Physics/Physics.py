"""""""""""""""""""""""""""""""""
----------------------------------
GRAVITAS v.4.0.1 - timestep physics module
by Tomas Bezkorowajnyj c. February 2025
----------------------------------
"""""""""""""""""""""""""""""""""

import numpy as np


MU = 6.67e-11*1.989e30
AU = 1.495979e11
AUDAY = AU*1.1574e-5


def update_vessel_physics(x_vec, v_vec, deltatime=3600):
    """timestep probe position about parent object

    Args:
        x_vec (tuple): position vector
        v_vec (tuple): velocity vector
        deltatime (int): time step amount. Defaults to 3600.
    """
    pos_0 = x_vec
    vel_0 = v_vec
    acc = - MU * np.power(np.linalg.norm(pos_0),-2) * (pos_0 / np.linalg.norm(pos_0)) * 1e-9

    ## step velocity
    vel_0[0] += acc[0] * deltatime
    vel_0[1] += acc[1] * deltatime
    vel_0[2] += acc[2] * deltatime

    ## step position
    pos_0[0] += vel_0[0] * deltatime
    pos_0[1] += vel_0[1] * deltatime
    pos_0[2] += vel_0[2] * deltatime

    return np.concatenate([pos_0, vel_0])


def update_planetary_physics(i, sp_obj,deltatime=3600):
    """timestep planetary position based on poliastro object profile

    Args:
        i (int): object index
        sp_obj (_type_): ephemeris data array [ pos, vel ]
    """
    pos_0 = AU * np.array([sp_obj[0][i],sp_obj[1][i],sp_obj[2][i]])
    vel_0 = AUDAY * np.array([sp_obj[3][i],sp_obj[4][i],sp_obj[5][i]])
    acc = - MU * np.power(np.linalg.norm(pos_0),-2) * (pos_0 / np.linalg.norm(pos_0))

    ## step velocity
    sp_obj[3][i] += acc[0] * deltatime / AUDAY
    sp_obj[4][i] += acc[1] * deltatime / AUDAY
    sp_obj[5][i] += acc[2] * deltatime / AUDAY

    ## step position
    sp_obj[0][i] += vel_0[0] * deltatime / AU
    sp_obj[1][i] += vel_0[1] * deltatime / AU
    sp_obj[2][i] += vel_0[2] * deltatime / AU


if __name__ == "__main__":
    print("Physics.py successfully loaded")
