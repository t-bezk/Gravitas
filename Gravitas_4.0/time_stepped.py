"""""""""""""""""""""""""""""""""
----------------------------------
GRAVITAS v.4.0.1 - timestep module
by Tomas Bezkorowajnyj c. June 2025
----------------------------------
"""""""""""""""""""""""""""""""""

import numpy as np

def get_min(arr) -> tuple[float,float]:
    """Get indices for 2d array minimum value"""
    arr_min = np.min(arr)
    return np.concatenate(np.where(arr==arr_min))
