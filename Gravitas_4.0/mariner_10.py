"""""""""""""""""""""""""""""""""
----------------------------------
GRAVITAS v.4.0.1 - Mariner 10 demo
by Tomas Bezkorowajnyj c. June 2025
----------------------------------
"""""""""""""""""""""""""""""""""

import pathlib
from datetime import datetime, timedelta
import numpy as np
from matplotlib import pyplot as plt
from encounters import generate_porkchop, setup_kernel, destroy_kernel
from spice_video import visual_animation
from time_stepped import get_min, perturbate_step
from Display.figures import gen_porkchop_plot
from dictionaries import MARINER_10_EV, MARINER_10_VM

##  Retrieve local file directory
PROJ_DIR = pathlib.Path(__file__).parent.resolve()

## Transfer between planets as layed out in transfer definition
setup_kernel()

ev_v0, ev_v1, ev_vp, ev_va  = generate_porkchop(MARINER_10_EV)
ev_c3 = np.linalg.norm(ev_v0 - ev_vp, axis=2)**2
ev_vi = np.linalg.norm(ev_v1 - ev_va, axis=2)

vm_v0, vm_v1, vm_vp, vm_va  = generate_porkchop(MARINER_10_VM)
vm_c3 = np.linalg.norm(vm_v0 - vm_vp, axis=2)**2
vm_vi = np.linalg.norm(vm_v1 - vm_va, axis=2)

##  Generate figures
gen_porkchop_plot(MARINER_10_EV, ev_c3, ev_vi)
gen_porkchop_plot(MARINER_10_VM, vm_c3, vm_vi)

plt.show()
plt.close()

plt.show()

destroy_kernel()
