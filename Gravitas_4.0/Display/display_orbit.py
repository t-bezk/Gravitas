"""""""""""""""""""""""""""""""""
----------------------------------
GRAVITAS v.4.0.1 - display module
by Tomas Bezkorowajnyj c. June 2025
----------------------------------
"""""""""""""""""""""""""""""""""

import numpy as np

MU = 6.67e-11*1.989e30
AU = 1.495979e11
AUDAY = AU*1.1574e-5

def display_orbit(a,e,i,omega,Omega):
    """generate a plottable trajectory path

    Args:
        a (_type_): semi major axis
        e (_type_): eccentricity
        i (_type_): inclination angle
        omega (_type_): _description_
        Omega (_type_): _description_

    Returns:
        ndarray: trajectory points
    """
    # Generate true anomaly values from 0 to 2π
    nu = np.linspace(0, 2 * np.pi, 500)

    # Calculate the radius for each true anomaly (orbit equation)
    r = (a * (1 - np.linalg.norm(e)**2)) / (1 + np.linalg.norm(e) * np.cos(nu))

    # Position in the orbital plane (x', y')
    x_prime = r * np.cos(nu)
    y_prime = r * np.sin(nu)
    z_prime = np.zeros_like(nu)

    # Rotation matrix components (to transform the orbit to 3D space)
    cos_Omega = np.cos(Omega)
    sin_Omega = np.sin(Omega)
    cos_omega = np.cos(omega)
    sin_omega = np.sin(omega)
    cos_i = np.cos(i)
    sin_i = np.sin(i)

    # Rotation matrix to convert from orbital plane to 3D space
    R11 = cos_Omega * cos_omega - sin_Omega * sin_omega * cos_i
    R12 = -cos_Omega * sin_omega - sin_Omega * cos_omega * cos_i
    R13 = sin_Omega * sin_i
    R21 = sin_Omega * cos_omega + cos_Omega * sin_omega * cos_i
    R22 = -sin_Omega * sin_omega + cos_Omega * cos_omega * cos_i
    R23 = -cos_Omega * sin_i
    R31 = sin_omega * sin_i
    R32 = cos_omega * sin_i
    R33 = cos_i

    # Apply the rotation matrix to each point in the orbital plane
    x = R11 * x_prime + R12 * y_prime + R13 * z_prime
    y = R21 * x_prime + R22 * y_prime + R23 * z_prime
    z = R31 * x_prime + R32 * y_prime + R33 * z_prime

    ## Return 3d position components
    return np.array([x,y,z])


def plot_trajectory(V,R):
    """_summary_

    Args:
        V (_type_): _description_
        R (_type_): _description_

    Returns:
        _type_: _description_
    """
    H_e = np.cross(R, V)
    R_mod = np.linalg.norm(R)
    V_mod = np.linalg.norm(V)
    E_e = V_mod**2 / 2 - MU / R_mod
    H_e_mod = np.linalg.norm(H_e)
    e_e = np.cross(V, H_e) / MU - R / R_mod
    n_e = np.cross([0,0,1], H_e)
    i_e = np.arccos(H_e[2]/H_e_mod)
    W_e = np.arccos(n_e[0]/np.linalg.norm(n_e))
    w_e = np.arccos(np.dot(n_e,e_e)/(np.linalg.norm(n_e)*np.linalg.norm(e_e)))
    a_e = -MU/(2*E_e)
    return display_orbit(a_e,e_e,i_e,w_e,W_e)
