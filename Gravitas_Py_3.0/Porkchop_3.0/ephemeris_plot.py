#ephemeris_plot.py

"""""""""""""""""""""""""""""""""
----------------------------------
GRAVITAS V.3.0 - Porkchop Plotter
by Tomas Bezkorowajnyj c. February 2025
----------------------------------
"""""""""""""""""""""""""""""""""

from matplotlib import pyplot as plt

from encounter import *


# Instantiating with a dictionary-like structure
m_2020 = {
    "d_time0":      "2020-05-01T00:00:00",
    "d_time1":      "2020-11-01T00:00:00",
    "a_time0":      "2020-12-01T00:00:00",
    "a_time1":      "2021-11-01T00:00:00",

    "target":       "MARS BARYCENTER",
    "origin":       "EARTH BARYCENTER",
    "observer":     "SOLAR SYSTEM BARYCENTER",
    "frame":        "ECLIPJ2000",
    "abcorr":       "NONE",

    "step":         3600*12*10,
    "out_title":    "Mars Transfer Window",
}

v_2020 = {
    "d_time0":      "2020-12-01T00:00:00",
    "d_time1":      "2022-01-01T00:00:00",
    "a_time0":      "2021-03-01T00:00:00",
    "a_time1":      "2022-11-01T00:00:00",

    "target":       "MARS BARYCENTER",
    "origin":       "VENUS BARYCENTER",
    "observer":     "SOLAR SYSTEM BARYCENTER",
    "frame":        "ECLIPJ2000",
    "abcorr":       "NONE",

    "step":         3600*12,
    "out_title":    "Mars 2020",
}


##  Retrieve local file directory
dir = pathlib.Path(__file__).parent.resolve()


##--Plot porkchops with c3 and v-infinity data--##

v0,v1,vp,va  = P_Solve(m_2020, dir)

##  Define meshgrids for contour plot
c3 = np.linalg.norm(v0 - vp, axis=2)**2
vi = np.linalg.norm(v1 - va, axis=2)

##  Define figure
fig, ax = plt.subplots(figsize=(10,12))



CS = ax.contour(c3, levels=np.linspace(0,25,20), colors=[(1.0,0.0,0.0)])
ax.clabel(CS, inline=1, fontsize=10)

CS1 = ax.contour(vi, levels=np.linspace(0,20,20), colors=[(0.0,0.0,1.0)])
ax.clabel(CS1, inline=1, fontsize=10)


plt.title(m_2020["out_title"])
plt.xlabel(f'Departure Window (Days after UST:{m_2020["d_time0"]})')
plt.ylabel(f'Arrival Window (Days after UST:{m_2020["a_time1"]})')

plt.savefig(f'{dir}/video_output/{m_2020["out_title"]}.png')

plt.close()


##  Offload spice kernel to prevent data leaks
spice.kclear()

min_i = 0
min_j = 0



## Genetic Algorithms
## Knapsack problem
## FYP
## J_2(r) Perturbations (Bessel Functions) inclination?
## typetheory <-> Category theory
