"""""""""""""""""""""""""""""""""
----------------------------------
GRAVITAS v.4.0.1 - Mariner 10 demo
by Tomas Bezkorowajnyj c. July 2025
----------------------------------
"""""""""""""""""""""""""""""""""

import pathlib
import numpy as np
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
from encounters import generate_porkchop, setup_kernel, destroy_kernel
from vinf_matching import vinfinity_match_3
from dictionaries import MARINER_10_EV, MARINER_10_VM
from spice_video import visual_animation_3

##  Retrieve local file directory
PROJ_DIR = pathlib.Path(__file__).parent.resolve()
MU = 6.67e-20*1.989e30  ## in km
EPS = 0.01

## Transfer between planets as layed out in transfer definition
setup_kernel()

ev_v0, ev_v1, ev_vp, ev_va  = generate_porkchop(MARINER_10_EV)
vm_v0, vm_v1, vm_vp, vm_va  = generate_porkchop(MARINER_10_VM)
ev_c3 = np.linalg.norm(ev_v0 - ev_vp, axis=2)**2
ev_vi = np.linalg.norm(ev_v1 - ev_va, axis=2)
vm_c3 = np.linalg.norm(vm_v0 - vm_vp, axis=2)**2
vm_vi = np.linalg.norm(vm_v1 - vm_va, axis=2)

vinf = []
for _t in range(45):
    vinf.append(vinfinity_match_3(MARINER_10_EV, MARINER_10_VM, ev_v1-ev_va, vm_v0-vm_vp, _t))
vinf = np.array(vinf)
v_inf_in = ev_v1-ev_va
v_inf_ou = vm_v0-vm_vp  #).transpose(1,0,2)

i_gh = np.min([len(v_inf_in), len(v_inf_ou)])
j_gh = np.min([len(v_inf_in[0]), len(v_inf_ou[0])])

print(v_inf_in.shape)
print(v_inf_ou.shape)
print(i_gh)
print(j_gh)

v_x_t = []
v_y_t = []

v_match = []

for _t in range(45):
    v_x = []
    v_y = []

    for i in range(i_gh):
        for j in range(j_gh):
            ab_dot = np.dot(v_inf_in[_t][j],v_inf_ou[i][_t])
            ab_prod = np.linalg.norm(v_inf_in[_t][j]) * np.linalg.norm(v_inf_ou[i][_t])
            theta = 0.5 * np.arccos( ab_dot / ab_prod )
            r_pfb = (MU / np.linalg.norm(v_inf_ou[i][_t])**2) * (-1 + 1 / np.sin(theta)) * 2E-6
            vi = np.sqrt(ev_c3[_t][j])
            
            if np.abs(vinf[_t][j][i]) < EPS and 2500. < r_pfb < 20000. and vi < 4.5:
                v_match.append([j, i, _t, r_pfb, vi])

v_match = np.array(v_match).T

print(v_match)

departure_time = datetime.strptime(MARINER_10_EV['d_time0'], "%Y-%m-%dT%H:%M:%S") + timedelta(seconds=float(35)*MARINER_10_EV['step'])
arrival_time = datetime.strptime(MARINER_10_EV['a_time0'], "%Y-%m-%dT%H:%M:%S") + timedelta(seconds=float(35)*MARINER_10_EV['step'])


#visual_animation_3(MARINER_10_EV,MARINER_10_VM, departure_time, arrival_time, ev_v0[35][33], 35)



plt.show()

destroy_kernel()
