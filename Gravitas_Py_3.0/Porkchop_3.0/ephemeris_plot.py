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
    "d_time0":      "2016-05-01T00:00:00",
    "d_time1":      "2021-11-01T00:00:00",
    "a_time0":      "2018-12-01T00:00:00",
    "a_time1":      "2027-01-01T00:00:00",

    "target":       "VENUS BARYCENTER",
    "origin":       "EARTH BARYCENTER",
    "observer":     "SOLAR SYSTEM BARYCENTER",
    "frame":        "ECLIPJ2000",
    "abcorr":       "NONE",

    "step":         3600*12*30,
    "out_title":    "Venus to Mars Transfer Window",
}

v_2020 = {
    "d_time0":      "2016-05-01T00:00:00",
    "d_time1":      "2021-11-01T00:00:00",
    "a_time0":      "2018-12-01T00:00:00",
    "a_time1":      "2027-01-01T00:00:00",

    "target":       "MARS BARYCENTER",
    "origin":       "VENUS BARYCENTER",
    "observer":     "SOLAR SYSTEM BARYCENTER",
    "frame":        "ECLIPJ2000",
    "abcorr":       "NONE",

    "step":         3600*12*30,
    "out_title":    "Mars 2020",
}


##  Retrieve local file directory
dir = pathlib.Path(__file__).parent.resolve()


##--Plot porkchops with c3 and v-infinity data--##

v_leaving_1, v_arriving_1 = P_Solve_vec(m_2020, dir)
v_leaving_2, v_arriving_2 = P_Solve_vec(v_2020, dir)

##  Define figure
fig, ax = plt.subplots(figsize=(10,12))


## Genetic Algorithms
## Knapsack problem
## FYP
## J_2(r) Perturbations (Bessel Functions) inclination?
## typetheory <-> Category theory



#CS = ax.contour(porkchop_array, levels=np.linspace(20,200,20), colors=[(1.0,0.0,0.0)])
#ax.clabel(CS, inline=1, fontsize=10)

v_inf_comparison = np.zeros((len(v_leaving_2), len(v_arriving_1)))

for i in range(len(v_leaving_2)):
    for j in range(len(v_arriving_1)):
        v_inf_comparison[i][j] = np.linalg.norm(v_leaving_2[i] - v_arriving_1[j])

CS1 = ax.contour(v_inf_comparison, levels = np.linspace(0,1e3,20))

ax.clabel(CS1, inline=1, fontsize=10)

#DS1 = ax.contour(vinfinity_array_2, levels=np.linspace(2,9,12), colors=[(1.0,0.0,0.0)])
#ax.clabel(DS1, inline=1, fontsize=10)

#CS2 = ax.contour(time_of_flight, colors=[(0.0,1.0,0.0)])
#ax.clabel(CS2, inline=1, fontsize=10)

plt.title(v_2020["out_title"])
plt.xlabel(f'Departure Window (Days after UST:{v_2020["d_time0"]})')
plt.ylabel(f'Arrival Window (Days after UST:{v_2020["a_time1"]})')

plt.savefig(f'{dir}/video_output/{v_2020["out_title"]}.png')

plt.close()


##  Offload spice kernel to prevent data leaks
spice.kclear()

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