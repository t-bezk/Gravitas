"""""""""""""""""""""""""""""""""
----------------------------------
GRAVITAS v.4.0.1 - timestep module
by Tomas Bezkorowajnyj c. June 2025
----------------------------------
"""""""""""""""""""""""""""""""""

import numpy as np
from Physics.Physics import update_vessel_physics
from encounters import load_ephemeris_arrays

def get_min(arr) -> tuple[float,float]:
    """Get indices for 2d array minimum value"""
    arr_min = np.min(arr)
    return np.concatenate(np.where(arr==arr_min))

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

def perturbate_step(dict_values,t_de,t_ar,vel,v_arange):
    """_summary_

    Args:
        dict_values (_type_): _description_
        trj_a (_type_): _description_
        trj_b (_type_): _description_
        velo (_type_): _description_
        v_arange (_type_): _description_
    """
    eph_tme,eph_trj_a = load_ephemeris_arrays(dict_values, t_de, t_ar,'target')
    _, eph_trj_b = load_ephemeris_arrays(dict_values, t_de, t_ar,'origin')
    prb_eph = timestepped_ephemeris(dict_values,eph_trj_a,eph_trj_b,vel)


    __st_pos = np.zeros((len(v_arange),len(v_arange),3))
    for i,vi in enumerate(v_arange):
        for j,vj in enumerate(v_arange):
            _tr_vel = np.array([ vel[0] + vi, vel[1], vel[2] + vj ])
            __st_pos[i][j] = get_min_dist(dict_values,eph_trj_a,prb_eph,_tr_vel)[:3]
        print(i)
    return __st_pos
