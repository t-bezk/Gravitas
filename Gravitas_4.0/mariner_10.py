"""""""""""""""""""""""""""""""""
----------------------------------
GRAVITAS v.4.0.1 - Mariner 10 demo
by Tomas Bezkorowajnyj c. July 2025
----------------------------------
"""""""""""""""""""""""""""""""""

import pathlib
from datetime import datetime, timedelta
import numpy as np
from matplotlib import pyplot as plt
from encounters import generate_porkchop, setup_kernel, destroy_kernel, load_ephemeris_arrays
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
#gen_porkchop_plot(MARINER_10_EV, ev_c3, ev_vi)
#gen_porkchop_plot(MARINER_10_VM, vm_c3, vm_vi)

ev_ets_de, ev_trj_de = load_ephemeris_arrays(MARINER_10_EV,MARINER_10_EV['d_time0'],MARINER_10_EV['d_time1'],'origin')
ev_ets_ar, ev_trj_ar = load_ephemeris_arrays(MARINER_10_EV,MARINER_10_EV['a_time0'],MARINER_10_EV['a_time1'],'target')

vm_ets_de, vm_trj_de = load_ephemeris_arrays(MARINER_10_VM,MARINER_10_VM['d_time0'],MARINER_10_VM['d_time1'],'origin')
vm_ets_ar, vm_trj_ar = load_ephemeris_arrays(MARINER_10_VM,MARINER_10_VM['a_time0'],MARINER_10_VM['a_time1'],'target')


vinf = np.zeros((len(ev_ets_de),len(vm_ets_ar)))

t_in = 35

for de, d_ets in enumerate(ev_ets_de):
    for ar, a_ets in enumerate(vm_ets_ar):
        vinf[de][ar] = np.linalg.norm(ev_v1[t_in][de] - ev_va[t_in][de]) - np.linalg.norm(vm_v0[ar][t_in] - vm_vp[ar][t_in])

cont = plt.contour(vinf,levels=np.linspace(0,5,10))
plt.clabel(cont, inline=1, fontsize=10)


plt.show()
plt.close()

plt.show()

destroy_kernel()
