#display_manager.py


import numpy as np
    
from math_func import mag

def displayOrbit(a,e,i,omega,Omega):
    
    # Generate true anomaly values from 0 to 2π
    nu = np.linspace(0, 2 * np.pi, 500)

    # Calculate the radius for each true anomaly (orbit equation)
    r = (a * (1 - mag(e)**2)) / (1 + mag(e) * np.cos(nu))

    # Position in the orbital plane (x', y')
    x_prime = r * np.cos(nu)
    y_prime = r * np.sin(nu)
    z_prime = np.zeros_like(nu)  # z' is zero in the orbital plane

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

    
    return np.array([x,y,z])


if __name__ == "__main__":
    
    print("display_manager.py successfully loaded")