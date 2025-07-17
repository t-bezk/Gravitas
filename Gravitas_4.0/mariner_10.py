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
from encounters import generate_porkchop
from kernel_handling import setup_kernel, destroy_kernel
from vinf_matching import vinfinity_match_3
from dictionaries import MARINER_10_EV, MARINER_10_VM
from spice_video import visual_animation_3

##  Retrieve local file directory
PROJ_DIR = pathlib.Path(__file__).parent.resolve()
MU = 6.67e-20*1.989e30  ## in km
EPS = 0.01
CLOSEST_APPROACH = 1.182e4

T_INDEX = 60

## Transfer between planets as layed out in transfer definition

def mariner_10():
    """Locates transfer window that matches Mariner 10 mission trajectory"""

    ev_v0, ev_v1, ev_vp, ev_va  = generate_porkchop(MARINER_10_EV)
    vm_v0, vm_v1, vm_vp, vm_va  = generate_porkchop(MARINER_10_VM)
    ev_c3 = np.linalg.norm(ev_v0 - ev_vp, axis=2)**2
    ev_vi = np.linalg.norm(ev_v1 - ev_va, axis=2)
    vm_c3 = np.linalg.norm(vm_v0 - vm_vp, axis=2)**2
    vm_vi = np.linalg.norm(vm_v1 - vm_va, axis=2)
    v_inf_in = ev_v1-ev_va
    v_inf_ou = vm_v0-vm_vp

    vinf = []

    i_gh = v_inf_in.shape[1]
    j_gh = v_inf_ou.shape[0]
    t_gh = v_inf_ou.shape[1]

    for _t in range(t_gh):
        vinf.append(vinfinity_match_3(MARINER_10_EV, MARINER_10_VM, ev_v1-ev_va, vm_v0-vm_vp, _t))
    vinf = np.array(vinf)

    v_match = []

    print(vinf.shape)

    for _t in range(t_gh):
        for i in range(i_gh):
            for j in range(j_gh):
                ab_dot = np.dot(v_inf_in[_t][i],v_inf_ou[j][_t])
                ab_prod = np.linalg.norm(v_inf_in[_t][i]) * np.linalg.norm(v_inf_ou[j][_t])
                theta = 0.5 * np.arccos( ab_dot / ab_prod )
                r_pfb = (MU / np.linalg.norm(v_inf_ou[j][_t])**2) * (-1 + 1 / np.sin(theta)) * 2E-6
                vi = np.sqrt(ev_c3[_t][j])

                if np.abs(vinf[_t][i][j]) < EPS and 6052. < r_pfb < 50000.:
                    v_match.append([j, i, _t, r_pfb, vi])

    v_match = np.array(v_match)

    v_inf_match = []

    for r in v_match:
        e_imp = datetime.strptime(MARINER_10_EV['d_time0'], "%Y-%m-%dT%H:%M:%S") + timedelta(seconds=float(r[1])*MARINER_10_EV['step'])
        v_imp = datetime.strptime(MARINER_10_EV['a_time0'], "%Y-%m-%dT%H:%M:%S") + timedelta(seconds=float(r[2])*MARINER_10_EV['step'])
        m_imp = datetime.strptime(MARINER_10_VM['a_time0'], "%Y-%m-%dT%H:%M:%S") + timedelta(seconds=float(r[0])*MARINER_10_EV['step'])
        v_inf_match.append([str(e_imp), str(v_imp), str(m_imp), int(r[3]), float(r[4])])

    for r in v_inf_match:
        print(r)
    print(len(v_inf_match))

if __name__ == "__main__":

    setup_kernel()
    try:
        mariner_10()
    except Exception as e:
        print(f'error: \n{e}')
    finally:
        destroy_kernel()
