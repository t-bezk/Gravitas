"""""""""""""""""""""""""""""""""
----------------------------------
GRAVITAS v.4.0.1 - Mariner 10 demo
by Tomas Bezkorowajnyj c. July 2025
----------------------------------
"""""""""""""""""""""""""""""""""

import pathlib
import numpy as np
from matplotlib import pyplot as plt
from encounters import generate_porkchop, setup_kernel, destroy_kernel
from vinf_matching import vinfinity_match_3
from dictionaries import MARINER_10_EV, MARINER_10_VM

##  Retrieve local file directory
PROJ_DIR = pathlib.Path(__file__).parent.resolve()
MU = 6.67e-20*1.989e30

## Transfer between planets as layed out in transfer definition
setup_kernel()

ev_v0, ev_v1, ev_vp, ev_va  = generate_porkchop(MARINER_10_EV)
vm_v0, vm_v1, vm_vp, vm_va  = generate_porkchop(MARINER_10_VM)
ev_c3 = np.linalg.norm(ev_v0 - ev_vp, axis=2)**2
ev_vi = np.linalg.norm(ev_v1 - ev_va, axis=2)
vm_c3 = np.linalg.norm(vm_v0 - vm_vp, axis=2)**2
vm_vi = np.linalg.norm(vm_v1 - vm_va, axis=2)

vinf = vinfinity_match_3(MARINER_10_EV, MARINER_10_VM, ev_v1-ev_va, vm_v0-vm_vp, 35)

v_inf_in = ev_v1-ev_va
v_inf_ou = vm_v0-vm_vp
theta = 0.5 * np.arccos( np.dot(v_inf_in[35][33],v_inf_ou[29][35]) / ( np.linalg.norm(v_inf_in[35][33]) * np.linalg.norm(v_inf_ou[30][35]) ) )
r_pfb = (MU / np.linalg.norm(v_inf_ou[29][35])**2) * (-1 + 1 / np.sin(theta)) * 2E-6

print(r_pfb)

cont = plt.contour(vinf,levels=np.linspace(0,5,10))
plt.clabel(cont, inline=1, fontsize=10)

plt.show()
plt.close()
plt.show()

destroy_kernel()
