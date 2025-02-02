#math_func.py

mu = 6.67e-11*1.989e30

au = 1.495979e11

auday = au*1.1574e-5

dt = 100

import numpy as np

def mag(vec):
    
    a=0
    for i in vec:
        a+=i**2
    return np.sqrt(a)
    
    