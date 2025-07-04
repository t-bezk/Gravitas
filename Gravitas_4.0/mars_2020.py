"""""""""""""""""""""""""""""""""
----------------------------------
GRAVITAS v.4.0.1 - mars2020 demo
by Tomas Bezkorowajnyj c. June 2025
----------------------------------
"""""""""""""""""""""""""""""""""

import pathlib
from datetime import datetime, timedelta
import numpy as np
from matplotlib import pyplot as plt
from encounters import generate_porkchop, setup_kernel, destroy_kernel
from spice_video import visual_animation
from Display.figures import gen_porkchop_plot
from time_stepped import get_min
from dictionaries import m_2020

##  Retrieve local file directory
PROJ_DIR = pathlib.Path(__file__).parent.resolve()

## Transfer between planets as layed out in transfer definition
setup_kernel()

v0, v1, vp, va  = generate_porkchop(m_2020)

##  Define meshgrids for contour plot
c3 = np.linalg.norm(v0 - vp, axis=2)**2
vi = np.linalg.norm(v1 - va, axis=2)

##  Generate figure
#gen_porkchop_plot(m_2020, c3, vi)
IND_DEP = 80
IND_ARR = 60

ix, iy = 15, 5
viq = v0[iy][ix]

#print(np.min(vi))
print(ix,iy)

departure_time = datetime.strptime(m_2020['d_time0'], "%Y-%m-%dT%H:%M:%S") + timedelta(seconds=float(ix)*m_2020['step'])
arrival_time = datetime.strptime(m_2020['a_time0'], "%Y-%m-%dT%H:%M:%S") + timedelta(seconds=float(iy)*m_2020['step'])


visual_animation(m_2020, departure_time, arrival_time, viq)

plt.show()
plt.close()

plt.show()

destroy_kernel()
