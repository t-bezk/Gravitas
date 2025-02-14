#chain_ephemeris.py

"""""""""""""""""""""""""""""""""
----------------------------------
GRAVITAS V.3.0 - V-infinity Matching
by Tomas Bezkorowajnyj c. February 2025
----------------------------------
"""""""""""""""""""""""""""""""""

from matplotlib import pyplot as plt

from encounter import *

import scipy.interpolate as sc

from datetime import datetime, timedelta


# Instantiating with a dictionary-like structure
m_2020_1 = {
    "d_time0":      "2020-12-01T00:00:00",
    "d_time1":      "2022-02-01T00:00:00",
    "a_time0":      "2021-04-01T00:00:00",
    "a_time1":      "2024-07-01T00:00:00",

    "target":       "VENUS BARYCENTER",
    "origin":       "EARTH BARYCENTER",
    "observer":     "SOLAR SYSTEM BARYCENTER",
    "frame":        "ECLIPJ2000",
    "abcorr":       "NONE",

    "step":         3600*24*5,
    "out_title":    "Earth-Venus-Mars Transfer qq",
}

m_2020_2 = {
    "d_time0":      "2021-04-01T00:00:00",
    "d_time1":      "2023-07-01T00:00:00",
    "a_time0":      "2021-01-01T00:00:00",
    "a_time1":      "2024-01-01T00:00:00",

    "target":       "MARS BARYCENTER",
    "origin":       "VENUS BARYCENTER",
    "observer":     "SOLAR SYSTEM BARYCENTER",
    "frame":        "ECLIPJ2000",
    "abcorr":       "NONE",

    "step":         3600*24*5,
    "out_title":    "Mars 2020",
}

match_vm = {
    "d_time0":      "2021-04-01T00:00:00",
    "d_time1":      "2022-12-01T00:00:00",
    "a_time0":      "2021-01-01T00:00:00",
    "a_time1":      "2023-01-01T00:00:00",

    "target":       "MARS BARYCENTER",
    "origin":       "VENUS BARYCENTER",
    "observer":     "SOLAR SYSTEM BARYCENTER",
    "frame":        "ECLIPJ2000",
    "abcorr":       "NONE",

    "step":         3600*24*5,
    "out_title":    "Mars 2020",
}



##  Retrieve local file directory
dir = pathlib.Path(__file__).parent.resolve()


##--Plot porkchops with c3 and v-infinity data--##

v0,v1,vp,va  = P_Solve(m_2020_1, dir)
v02,v12,vp2,va2  = P_Solve(m_2020_2, dir)

c3 = np.linalg.norm(v1 - va, axis=2)**2
c32 = np.linalg.norm(v02 - vp2, axis=2)**2

vi = np.linalg.norm(v1 - va, axis=2)
vi2 = np.linalg.norm(v02 - vp2, axis=2)


c3_min = np.min(c3)
vi_min = np.min(vi)


min_ind_c = np.unravel_index(np.argmin(c3), c3.shape)
min_ind_v = np.unravel_index(np.argmin(vi), vi.shape)

v0_vec = v0 - vp
vi_vec = v1 - va

c3_min_v = v0_vec[min_ind_c]
vp_min_v = vp[min_ind_c]
vi_min_c = vi_vec[min_ind_v]
va_min_v = va[min_ind_v]

fig, ax = plt.subplots(figsize=(10,12))

CS = ax.contour(c3, levels=np.linspace(0,150,10), colors=[(0.0,0.0,1.0)])
ax.clabel(CS, inline=1, fontsize=10)

plt.savefig(f'{dir}/video_output/EVMEa.png')
plt.close()

fig, ax = plt.subplots(figsize=(10,12))

CS1 = ax.contour(c32, levels=np.linspace(0,150,10), colors=[(0.0,0.0,1.0)])
ax.clabel(CS1, inline=1, fontsize=10)

plt.savefig(f'{dir}/video_output/EVMEb.png')
plt.close()

pp1_dep = len(c3[0])
pp1_arr = len(c3)

pp2_dep = len(c32[0])
pp2_arr = len(c32)

for i in range(pp1_arr):

    dv_inf_meshgrid = np.zeros((pp1_arr, pp2_dep))

    for j in range(pp1_dep):

        c3_1_2 = c3[i][j]
        c3_2_3 = c32[i]

        dV = c3_2_3 - c3_1_2

        #plt.plot(dV)
        #plt.show()

        dv_inf_meshgrid[i] = dV
    
    plt.imshow(dv_inf_meshgrid)
    plt.colorbar()
    plt.savefig(f"{dir}/fig/output{i}-{j}.png")
    plt.close()




#tppp, vppp = P_Match(match_vm, dir, vi_min_c, 3600*24*200)


#CS = ax.contour(meshgrid_matrix, levels=np.linspace(0,0.1,1), colors=[(0.0,0.0,1.0)])
#ax.clabel(CS, inline=1, fontsize=10)

#plt.show()


## Genetic Algorithms
## Knapsack problem
## FYP
## J_2(r) Perturbations (Bessel Functions) inclination?
## typetheory <-> Category theory
