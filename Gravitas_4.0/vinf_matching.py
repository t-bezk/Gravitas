"""""""""""""""""""""""""""""""""
----------------------------------
GRAVITAS v.4.0.1 - v-infinity module
by Tomas Bezkorowajnyj c. July 2025
----------------------------------
"""""""""""""""""""""""""""""""""

import numpy as np
from encounters import load_ephemeris_arrays

def vinfinity_match_3(dic_1, dic_2, v_ev, v_vm, t):
    """Matches v-infinities for different configurations

    Args:
        dic_1 (_type_): _description_
        dic_2 (_type_): _description_
        v_ev (_type_): _description_
        v_vm (_type_): _description_
        t (_type_): _description_

    Returns:
        _type_: _description_
    """
    ev_ets_de, _ = load_ephemeris_arrays(dic_1,dic_1['d_time0'],dic_1['d_time1'],'origin')
    vm_ets_ar, _ = load_ephemeris_arrays(dic_2,dic_2['a_time0'],dic_2['a_time1'],'target')

    ev_vecs = v_ev[t][:len(ev_ets_de)]
    vm_vecs = np.array([v_vm[ar][t] for ar in range(len(vm_ets_ar))])

    norms_ev = np.linalg.norm(ev_vecs, axis=1)[:, None]
    norms_vm = np.linalg.norm(vm_vecs, axis=1)[None, :]

    return norms_ev - norms_vm
