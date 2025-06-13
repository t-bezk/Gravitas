#Trajectory_Char.py

from display_manager import *

from math_func import *

import numpy as np

def plotOrbs(i, sp_obj):
    
    R_e = au*np.array([sp_obj[0][i],sp_obj[1][i],sp_obj[2][i]])
    V_e = auday*np.array([sp_obj[3][i],sp_obj[4][i],sp_obj[5][i]])

    H_e = np.cross(R_e, V_e)
    R_e_mod = np.linalg.norm(R_e)
    V_e_mod = np.linalg.norm(V_e)
    E_e = V_e_mod**2 / 2 - mu / R_e_mod
    H_e_mod = np.linalg.norm(H_e)
    e_e = np.cross(V_e, H_e) / mu - R_e / R_e_mod
    n_e = np.cross([0,0,1], H_e)
    i_e = np.arccos(H_e[2]/H_e_mod)
    W_e = np.arccos(n_e[0]/np.linalg.norm(n_e))
    w_e = np.arccos(np.dot(n_e,e_e)/(np.linalg.norm(n_e)*np.linalg.norm(e_e)))
    a_e = -mu/(2*E_e)

    return displayOrbit(a_e,e_e,i_e,w_e,W_e)

def getPlanetOrbit(i, sp_obj):
    
    R_e = au*np.array([sp_obj[0][i],sp_obj[1][i],sp_obj[2][i]])
    V_e = auday*np.array([sp_obj[3][i],sp_obj[4][i],sp_obj[5][i]])

    H_e = np.cross(R_e, V_e)
    R_e_mod = np.linalg.norm(R_e)
    V_e_mod = np.linalg.norm(V_e)
    E_e = V_e_mod**2 / 2 - mu / R_e_mod
    H_e_mod = np.linalg.norm(H_e)
    e_e = np.cross(V_e, H_e) / mu - R_e / R_e_mod
    n_e = np.cross([0,0,1], H_e)
    i_e = np.arccos(H_e[2]/H_e_mod)
    W_e = np.arccos(n_e[0]/np.linalg.norm(n_e))
    w_e = np.arccos(np.dot(n_e,e_e)/(np.linalg.norm(n_e)*np.nlinalg.normorm(e_e)))
    a_e = -mu/(2*E_e)

    return np.array([a_e,e_e,i_e,w_e,W_e])




def plotTraj(V,R):

    H_e = np.cross(R, V)
    R_mod = np.linalg.norm(R)
    V_mod = np.linalg.norm(V)
    E_e = V_mod**2 / 2 - mu / R_mod
    H_e_mod = np.linalg.norm(H_e)
    e_e = np.cross(V, H_e) / mu - R / R_mod
    n_e = np.cross([0,0,1], H_e)
    i_e = np.arccos(H_e[2]/H_e_mod)
    W_e = np.arccos(n_e[0]/np.linalg.norm(n_e))
    w_e = np.arccos(np.dot(n_e,e_e)/(np.linalg.norm(n_e)*np.linalg.norm(e_e)))
    a_e = -mu/(2*E_e)

    return displayOrbit(a_e,e_e,i_e,w_e,W_e)



def getSpacecraftOrbit(V,R):

    H_e = np.cross(R, V)
    R_mod = np.norm(R)
    V_mod = np.norm(V)
    E_e = V_mod**2 / 2 - mu / R_mod
    H_e_mod = np.norm(H_e)
    e_e = np.cross(V, H_e) / mu - R / R_mod
    n_e = np.cross([0,0,1], H_e)
    i_e = np.arccos(H_e[2]/H_e_mod)
    W_e = np.arccos(n_e[0]/np.norm(n_e))
    w_e = np.arccos(np.dot(n_e,e_e)/(np.norm(n_e)*np.norm(e_e)))
    a_e = -mu/(2*E_e)

    return ([a_e,e_e,i_e,w_e,W_e])

