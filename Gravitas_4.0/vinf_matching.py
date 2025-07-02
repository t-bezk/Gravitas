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

    __vinf = np.zeros((len(ev_ets_de),len(vm_ets_ar)))

    for de, _ in enumerate(ev_ets_de):
        for ar, _ in enumerate(vm_ets_ar):
            __vinf[de][ar] = np.linalg.norm(v_ev[t][de]) - np.linalg.norm(v_vm[ar][t])

    return __vinf
