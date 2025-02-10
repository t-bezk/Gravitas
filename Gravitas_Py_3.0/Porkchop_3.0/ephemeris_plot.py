#ephemeris_plot.py

"""""""""""""""""""""""""""""""""
----------------------------------
GRAVITAS V.3.0 - Porkchop Plotter
by Tomas Bezkorowajnyj c. February 2025
----------------------------------
"""""""""""""""""""""""""""""""""


import numpy as np

from matplotlib import pyplot as plt

from video_manager import *

from N_Body_Physics.Trajectory_Char import *

from N_Body_Physics.Physics import *

import pathlib

import spiceypy as spice

from poliastro.iod import izzo

from poliastro.bodies import Sun, Earth

from astropy import units as u



##  Retrieve local file directory
dir = pathlib.Path(__file__).parent.resolve()

##  Set the path to the image folder
image_folder = f"{dir}/fig/"

##  Set the desired output video file name
output_video_file = f"{dir}/video_output/output_video.mp4"

##  Output file name
output_plot_title = "Mars 2020 Transfer Window"


##  Debug Package Loading
print(dir)
print(spice.tkvrsn('TOOLKIT'))



##--Define departure and arrival parameters from spice kernels--##

#   Load SPICE kernels
spice.furnsh(f"{dir}/Spice_Kernels/de421.bsp")  # Ephemeris data
spice.furnsh(f"{dir}/Spice_Kernels/naif0012.tls")  # leap seconds


#   Time step
step = 3600*12*5  # seconds


#   Define departure times
departure_time0 = "2020-05-01T00:00:00"
departure_time1 = "2020-11-01T00:00:00"

#   Define arrival times
arrival_time0 = "2020-12-01T00:00:00"
arrival_time1 = "2022-01-01T00:00:00"


#   Convert to Ephemeris Time
et_de0 = spice.str2et(departure_time0)
et_de1 = spice.str2et(departure_time1)

et_ar0 = spice.str2et(arrival_time0)
et_ar1 = spice.str2et(arrival_time1)


##  Ephemeris time arrays
ets_de = np.arange(et_de0, et_de1, step)
ets_ar = np.arange(et_ar0, et_ar1, step)


#   Define origin, target, and observer
target = "MARS BARYCENTER"
origin = "EARTH BARYCENTER"
observer = "SOLAR SYSTEM BARYCENTER"
frame = "ECLIPJ2000"
abcorr = "NONE"


#   Collect trajectory data
trajectory_departure = np.array([spice.spkezr(origin, et, frame, abcorr, observer)[0] for et in ets_de])
trajectory_arrival = np.array([spice.spkezr(target, et, frame, abcorr, observer)[0] for et in ets_ar])


##  Define array packets
porkchop_array = np.zeros((len(trajectory_arrival),len(trajectory_departure)))
vinfinity_array = np.zeros((len(trajectory_arrival),len(trajectory_departure)))
time_of_flight = np.zeros((len(trajectory_arrival),len(trajectory_departure)))



##--Programming Loop--##

for i in range(len(trajectory_arrival)):


    print(f'{i} of {len(trajectory_arrival)}')

    for j in range(len(trajectory_departure)):
        
        ##  Define velocity vectors
        v0 = 0
        v = 0
        vp = trajectory_departure[j][3:]
        va = trajectory_arrival[i][3:]


        ##  Izzo Lambert Solver
        lambert = izzo.lambert(Sun.k, trajectory_departure[j][:3]*u.km, trajectory_arrival[i][:3]*u.km, (ets_ar[i]*u.s - ets_de[j]*u.s),M=0)   # :3


        ##  Unpack initial and final velocity
        v0, v = next(lambert)


        ##  Solve characteristic velocity and v-infinity
        c3 = np.linalg.norm(v0.value - vp)**2
        v_inf_ar = np.linalg.norm(v.value - va)


        ##  Store values in array packets
        porkchop_array[i][j] = c3
        vinfinity_array[i][j] = v_inf_ar
        time_of_flight[i][j] = (ets_ar[i] - ets_de[j])/(3600*24)


##--Plot porkchops with c3 and v-infinity data--##

##  Define figure
fig, ax = plt.subplots(figsize=(10,12))

CS = ax.contour(porkchop_array, levels=np.linspace(20,200,20), colors=[(1.0,0.0,0.0)])
ax.clabel(CS, inline=1, fontsize=10)

CS1 = ax.contour(vinfinity_array, levels=np.linspace(2,9,12), colors=[(0.0,0.0,1.0)])
ax.clabel(CS1, inline=1, fontsize=10)

CS2 = ax.contour(time_of_flight, colors=[(0.0,1.0,0.0)])
ax.clabel(CS2, inline=1, fontsize=10)

plt.title(output_plot_title)
plt.xlabel(f'Departure Window (Days after UST:{departure_time0})')
plt.ylabel(f'Arrival Window (Days after UST:{arrival_time0})')

plt.savefig(f'{dir}/video_output/{output_plot_title}.png')

plt.close()


##  Offload spice kernel to prevent data leaks
spice.kclear()


##  Store Minimum Values
c3_min = np.min(porkchop_array)
v_inf_min = np.min(vinfinity_array)

print('c3 min: ', c3_min)
print('v-inf min: ', v_inf_min)
