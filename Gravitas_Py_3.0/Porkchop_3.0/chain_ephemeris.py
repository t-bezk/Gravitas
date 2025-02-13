#chain_ephemeris.py

"""""""""""""""""""""""""""""""""
----------------------------------
GRAVITAS V.3.0 - V-infinity Matching
by Tomas Bezkorowajnyj c. February 2025
----------------------------------
"""""""""""""""""""""""""""""""""

from matplotlib import pyplot as plt

from encounter import *


# Instantiating with a dictionary-like structure
m_2020_1 = {
    "d_time0":      "2020-01-01T00:00:00",
    "d_time1":      "2022-11-01T00:00:00",
    "a_time0":      "2020-07-01T00:00:00",
    "a_time1":      "2024-11-01T00:00:00",

    "target":       "MARS BARYCENTER",
    "origin":       "EARTH BARYCENTER",
    "observer":     "SOLAR SYSTEM BARYCENTER",
    "frame":        "ECLIPJ2000",
    "abcorr":       "NONE",

    "step":         3600*24*5,
    "out_title":    "Mars Transfer Window",
}

m_2020_2 = {
    "d_time0":      "2020-01-01T00:00:00",
    "d_time1":      "2022-11-01T00:00:00",
    "a_time0":      "2020-07-01T00:00:00",
    "a_time1":      "2024-11-01T00:00:00",

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

vinf = v1 - va

for trial_index in range(vinf.shape[1]):

    tof_pm, dv_pm  = P_Match(m_2020_2, dir, trial_index, vinf[:,trial_index,:])

    if any(y < 0 for y in dv_pm):
        plt.plot(tof_pm, dv_pm)

        plt.show()

##  Define meshgrids for contour plot
#c3 = np.linalg.norm(v0 - vp, axis=2)**2
#vi = np.linalg.norm(v1 - va, axis=2)


## Genetic Algorithms
## Knapsack problem
## FYP
## J_2(r) Perturbations (Bessel Functions) inclination?
## typetheory <-> Category theory
