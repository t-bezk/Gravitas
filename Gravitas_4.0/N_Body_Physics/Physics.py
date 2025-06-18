"""""""""""""""""""""""""""""""""
----------------------------------
GRAVITAS v.4.0.1 - timestep physics module
by Tomas Bezkorowajnyj c. February 2025
----------------------------------
"""""""""""""""""""""""""""""""""


mu = 6.67e-11*1.989e30

au = 1.495979e11

auday = au*1.1574e-5

dt = 100

import numpy as np

def updatePlanetaryPhysics(i, sp_obj):

    pos_0 = au*np.array([sp_obj[0][i],sp_obj[1][i],sp_obj[2][i]])
    vel_0 = auday*np.array([sp_obj[3][i],sp_obj[4][i],sp_obj[5][i]])
    
    acc = -mu * np.power(np.linalg.norm(pos_0),-2) * (pos_0 / np.linalg.norm(pos_0))
    
    sp_obj[3][i] += acc[0] * dt / auday
    sp_obj[4][i] += acc[1] * dt / auday
    sp_obj[5][i] += acc[2] * dt / auday
    
    sp_obj[0][i] += vel_0[0] * dt / au
    sp_obj[1][i] += vel_0[1] * dt / au
    sp_obj[2][i] += vel_0[2] * dt / au

def updateVesselPhysics(x_vec, v_vec):

    pos_0 = au*x_vec
    vel_0 = auday*v_vec
    
    acc = -mu * np.power(np.linalg.norm(pos_0),-2) * (pos_0 / np.linalg.norm(pos_0))

    vel_0[0] += acc[0] * dt
    vel_0[1] += acc[1] * dt
    vel_0[2] += acc[2] * dt
    
    pos_0[0] += vel_0[0] * dt
    pos_0[1] += vel_0[1] * dt
    pos_0[2] += vel_0[2] * dt

    vel_0[0] /= auday
    vel_0[1] /= auday
    vel_0[2] /= auday

    pos_0[0] /= au
    pos_0[1] /= au
    pos_0[2] /= au

    return [pos_0, vel_0]


if __name__ == "__main__":
    
    print("Physics.py successfully loaded")