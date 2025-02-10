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
    "a_time1":       "2022-01-01T00:00:00",

    "target":       "MARS BARYCENTER",
    "origin":       "EARTH BARYCENTER",
    "observer":     "SOLAR SYSTEM BARYCENTER",
    "frame":        "ECLIPJ2000",
    "abcorr":       "NONE",

    "step":         3600*12*5,
    "out_title":    "Mars 2020 Transfer Window",
}


##  Retrieve local file directory
dir = pathlib.Path(__file__).parent.resolve()


##--Plot porkchops with c3 and v-infinity data--##

porkchop_array, vinfinity_array, time_of_flight = P_Solve(m_2020, dir)


##  Define figure
fig, ax = plt.subplots(figsize=(10,12))

CS = ax.contour(porkchop_array, levels=np.linspace(20,200,20), colors=[(1.0,0.0,0.0)])
ax.clabel(CS, inline=1, fontsize=10)

CS1 = ax.contour(vinfinity_array, levels=np.linspace(2,9,12), colors=[(0.0,0.0,1.0)])
ax.clabel(CS1, inline=1, fontsize=10)

CS2 = ax.contour(time_of_flight, colors=[(0.0,1.0,0.0)])
ax.clabel(CS2, inline=1, fontsize=10)

plt.title(m_2020["out_title"])
plt.xlabel(f'Departure Window (Days after UST:{m_2020["d_time0"]})')
plt.ylabel(f'Arrival Window (Days after UST:{m_2020["a_time1"]})')

plt.savefig(f'{dir}/video_output/{m_2020["out_title"]}.png')

plt.close()


##  Offload spice kernel to prevent data leaks
spice.kclear()


##  Store Minimum Values
c3_min = np.min(porkchop_array)
v_inf_min = np.min(vinfinity_array)

print('c3 min: ', c3_min)
print('v-inf min: ', v_inf_min)

min_i = 0
min_j = 0
"""
for i in range(len(trajectory_arrival)):
    for j in range(len(trajectory_departure)):
        if porkchop_array[i][j] == c3_min:
            min_i = i
            min_j = j
            break

##  Plot trajectory
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#ax.set_facecolor((0.0,0.0,0.0))
#ax.grid(False)


aw = plotTraj(1e3*trajectory_departure[min_j][3:], 1e3*trajectory_departure[min_j][:3])
ax.plot(aw[0],-aw[1],-aw[2],label="orbit")
ax.scatter(1e3*trajectory_departure[min_j][0],1e3*trajectory_departure[min_j][1],1e3*trajectory_departure[min_j][2])

aw1 = plotTraj(1e3*trajectory_arrival[min_i][3:], 1e3*trajectory_arrival[min_i][:3])
ax.plot(aw1[0],-aw1[1],-aw1[2],label="orbit")
ax.scatter(1e3*trajectory_arrival[min_i][0],1e3*trajectory_arrival[min_i][1],1e3*trajectory_arrival[min_i][2])

aw2 = plotTraj(1e3*vel_vec[min_i][min_j], 1e3*trajectory_departure[min_j][:3])
ax.plot(aw2[0],-aw2[1],-aw2[2],label="orbit")

plt.savefig(f'{dir}/video_output/min_traj.png',dpi=300)
plt.show()
"""