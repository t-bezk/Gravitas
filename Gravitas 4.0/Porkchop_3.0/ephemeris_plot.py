#ephemeris_plot.py

"""
----------------------------------
GRAVITAS V.3.0 - Porkchop Plotter
by Tomas Bezkorowajnyj c. February 2025
----------------------------------
"""

from matplotlib import pyplot as plt

from encounter import *


# Instantiating with a dictionary-like structure
m_2020 = {
    "d_time0":      "2020-05-01T00:00:00",
    "d_time1":      "2020-09-01T00:00:00",
    "a_time0":      "2020-12-01T00:00:00",
    "a_time1":      "2021-04-01T00:00:00",

    "target":       "MARS BARYCENTER",
    "origin":       "EARTH BARYCENTER",
    "observer":     "SOLAR SYSTEM BARYCENTER",
    "frame":        "ECLIPJ2000",
    "abcorr":       "NONE",

    "step":         3600*24,
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

##  Retrieve local file directory
dir = pathlib.Path(__file__).parent.resolve()

"""--Plot porkchops with c3 and v-infinity data--"""

## Transfer between planets as layed out in transfer definition
v0,v1,vp,va  = porkchop_solve(m_2020)

##  Define meshgrids for contour plot
c3 = np.linalg.norm(v0 - vp, axis=2)**2
vi = np.linalg.norm(v1 - va, axis=2)

##  Define figure
fig, ax = plt.subplots(figsize=(10,12))

contour_plot = ax.contour(vi, levels=np.linspace(0,4,10), colors=[(0.0,0.0,1.0)])
ax.clabel(contour_plot, inline=1, fontsize=10)


plt.title(m_2020["out_title"])
plt.xlabel(f'Departure Window (Days after UST:{m_2020["d_time0"]})')
plt.ylabel(f'Arrival Window (Days after UST:{m_2020["a_time1"]})')

plt.savefig(f'{dir}/video_output/{m_2020["out_title"]}.png')
plt.show()
plt.close()
