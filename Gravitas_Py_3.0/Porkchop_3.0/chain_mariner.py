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
    "d_time0":      "1973-07-01T00:00:00",
    "d_time1":      "1974-02-01T00:00:00",
    "a_time0":      "1974-01-04T00:00:00",
    "a_time1":      "1974-04-06T00:00:00",

    "target":       "VENUS BARYCENTER",
    "origin":       "EARTH BARYCENTER",
    "observer":     "SOLAR SYSTEM BARYCENTER",
    "frame":        "ECLIPJ2000",
    "abcorr":       "NONE",

    "step":         3600*24,
    "out_title":    "Mariner 10 Venus Arrival v-inf",
}

m_2020_2 = {
    "d_time0":      "1974-01-04T00:00:00",
    "d_time1":      "1974-04-06T00:00:00",
    "a_time0":      "1974-02-01T00:00:00",
    "a_time1":      "1974-05-01T00:00:00",

    "target":       "MERCURY BARYCENTER",
    "origin":       "VENUS BARYCENTER",
    "observer":     "SOLAR SYSTEM BARYCENTER",
    "frame":        "ECLIPJ2000",
    "abcorr":       "NONE",

    "step":         3600*24,
    "out_title":    "Mariner 10 Venus Departure v-inf",
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

print((v1 - va)[65][120])
#print((v02 - vp2)[65][130])



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

CS = ax.contour(c3, levels=np.linspace(0,150,15), colors=[(0.0,0.0,1.0)])
ax.clabel(CS, inline=1, fontsize=10)

CS1 = ax.contour(c32.T, levels=np.linspace(0,150,15), colors=[(1.0,0.0,0.0)])
ax.clabel(CS1, inline=1, fontsize=10)

plt.title(m_2020_1["out_title"])
plt.xlabel(f'Departure Window (Days after UST:{m_2020_1["d_time0"]})')
plt.ylabel(f'Arrival Window (Days after UST:{m_2020_1["a_time0"]})')

plt.savefig(f'{dir}/video_output/Mariner_a_trans_together.png')
plt.close()

fig, ax = plt.subplots(figsize=(10,12))

CS1 = ax.contour(c32.T, levels=np.linspace(0,150,15), colors=[(0.0,0.0,1.0)])
ax.clabel(CS1, inline=1, fontsize=10)

plt.title(m_2020_2["out_title"])
plt.xlabel(f'Departure Window (Days after UST:{m_2020_2["d_time0"]})')
plt.ylabel(f'Arrival Window (Days after UST:{m_2020_2["a_time0"]})')

plt.savefig(f'{dir}/video_output/mariner_b_trans.png')
plt.close()

pp1_dep = len(c3[0])
pp1_arr = len(c3)

pp2_dep = len(c32[0])
pp2_arr = len(c32)

# 1. Trim arrays to the smaller shape

c32t = c32.T

dvinf = c3[:,:len(c32t[0])] - c32t

fig, ax = plt.subplots(figsize=(10,12))

CS2 = ax.contour(dvinf, levels=np.linspace(-100,100,15), colors=[(0.0,0.0,1.0)])
ax.clabel(CS2, inline=1, fontsize=10)


plt.title('Mariner 10 Venusian Transfer dv_inf')
plt.xlabel(f'Departure Window (Days after UST:{m_2020_2["d_time0"]})')
plt.ylabel(f'Arrival Window (Days after UST:{m_2020_2["a_time0"]})')

plt.savefig(f'{dir}/video_output/mariner_10_dv.png')
plt.close()

# 2. Compute V-Infinity mismatch
delta_v_inf = np.linalg.norm(v0_23_trimmed - v_12_trimmed, axis=2)  # Shape: (N, M)

# 3. Find best match (minimum ΔV∞)
best_match_index = np.unravel_index(np.argmin(delta_v_inf), delta_v_inf.shape)

# Print results
print(f"Best match index: {best_match_index}")
print(f"Minimum ΔV∞: {delta_v_inf[best_match_index]:.3f} km/s")

for i in range(pp1_arr):

    dv_inf_meshgrid = np.zeros((pp1_arr, pp2_dep))

    for j in range(pp1_dep):

        c3_1_2 = c3[i][j]
        c3_2_3 = c32[i]

        dV = c3_2_3 - c3_1_2

        #plt.plot(dV)
        #plt.show()

        dv_inf_meshgrid[i] = dV

    fig, ax = plt.subplots(figsize=(10,12))

    print(dv_inf_meshgrid)

    CS1 = ax.contour(dv_inf_meshgrid, levels=np.linspace(-1.5,1.5,15), colors=[(0.0,0.0,1.0)])
    ax.clabel(CS1, inline=1, fontsize=10)
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
