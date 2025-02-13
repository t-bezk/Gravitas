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
    "d_time0":      "2020-12-01T00:00:00",
    "d_time1":      "2022-02-01T00:00:00",
    "a_time0":      "2021-04-01T00:00:00",
    "a_time1":      "2022-12-01T00:00:00",

    "target":       "VENUS BARYCENTER",
    "origin":       "EARTH BARYCENTER",
    "observer":     "SOLAR SYSTEM BARYCENTER",
    "frame":        "ECLIPJ2000",
    "abcorr":       "NONE",

    "step":         3600*12*5,
    "out_title":    "Earth-Venus-Mars Transfer qq",
}

v_2020 = {
    "d_time0":      "2021-04-01T00:00:00",
    "d_time1":      "2022-12-01T00:00:00",
    "a_time0":      "2021-01-01T00:00:00",
    "a_time1":      "2023-01-01T00:00:00",

    "target":       "MARS BARYCENTER",
    "origin":       "VENUS BARYCENTER",
    "observer":     "SOLAR SYSTEM BARYCENTER",
    "frame":        "ECLIPJ2000",
    "abcorr":       "NONE",

    "step":         3600*12*5,
    "out_title":    "Mars 2020",
}

e_2020 = {
    "d_time0":      "2021-01-01T00:00:00",
    "d_time1":      "2023-01-01T00:00:00",
    "a_time0":      "2021-06-01T00:00:00",
    "a_time1":      "2023-12-01T00:00:00",

    "target":       "EARTH BARYCENTER",
    "origin":       "MARS BARYCENTER",
    "observer":     "SOLAR SYSTEM BARYCENTER",
    "frame":        "ECLIPJ2000",
    "abcorr":       "NONE",

    "step":         3600*12*5,
    "out_title":    "Mars 2020",
}

def add_2d_arrays(*arrays):
    # Find the max size in each dimension
    max_rows = max(arr.shape[0] for arr in arrays)
    max_cols = max(arr.shape[1] for arr in arrays)

    # Create a result array filled with zeros
    result = np.zeros((max_rows, max_cols))

    for arr in arrays:
        # Get the shape of the current array
        rows, cols = arr.shape
        
        # Add the valid portion of arr to result (avoiding out-of-bounds errors)
        result[:rows, :cols] += arr

    return result

##  Retrieve local file directory
dir = pathlib.Path(__file__).parent.resolve()


##--Plot porkchops with c3 and v-infinity data--##

v0,v1,vp,va  = P_Solve(m_2020, dir)
v0s,v1s,vps,vas  = P_Solve(v_2020, dir)
#v0e,v1e,vpe,vae  = P_Solve(e_2020, dir)

##  Define meshgrids for contour plot
c3 = np.linalg.norm(v0 - vp, axis=2)**2
vi = np.linalg.norm(v1 - va, axis=2)

c3s = np.linalg.norm(v0s - vps, axis=2)**2
vis = np.linalg.norm(v0s - vps, axis=2)

#c3e = np.linalg.norm(v0e - vpe, axis=2)**2
#vie = np.linalg.norm(v0e - vpe, axis=2)

##  Define figure
fig, ax = plt.subplots(figsize=(10,12))

v_infinity_ev = add_2d_arrays(vi, -vis.T)

CS = ax.contour(v_infinity_ev, levels=np.linspace(-25,25,5), colors=[(0.0,0.0,1.0)])
ax.clabel(CS, inline=1, fontsize=10)

#CS1 = ax.contour(vi, levels=np.linspace(0,20,20), colors=[(0.0,0.0,1.0)])
#ax.clabel(CS1, inline=1, fontsize=10)


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
