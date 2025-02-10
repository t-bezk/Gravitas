#ephemeris_plot.py

"""""""""""""""""""""""""""""""""
----------------------------------
GRAVITAS V.3.0 - Porkchop Plotter
by Tomas Bezkorowajnyj c. February 2025
----------------------------------
"""""""""""""""""""""""""""""""""


import numpy as np

import scipy.optimize as op

from matplotlib import pyplot as plt

from video_manager import *

from Trajectory_Char import *

from Physics import *

import pathlib

import spiceypy as spice

print(spice.tkvrsn('TOOLKIT'))

from poliastro.iod import izzo

from poliastro.bodies import Sun

from poliastro.bodies import Earth

from astropy import units as u

import lambert_tools as lt

##  Retrieve local file directory
dir = pathlib.Path(__file__).parent.resolve()

##  Print local file directory (Debug)
print(dir)






##  Set the path to the image folder
image_folder = f"{dir}/fig/"




##  Set the desired output video file name
output_video_file = f"{dir}/video_output/output_video.mp4"




## Load JED object planetary data and extract position and velocity data from files
space_objects = np.loadtxt(f"{dir}/space_objects.csv", delimiter=',',skiprows=1,usecols=np.arange(1,7)).T


angle_res = 20


##  Define departure and arrival parameters from spice kernels

# Load SPICE kernels
spice.furnsh(f"{dir}/de421.bsp")  # Ephemeris data
spice.furnsh(f"{dir}/naif0012.tls")  # leap seconds


# Define departure times
departure_time0 = "2020-05-01T00:00:00"
departure_time1 = "2020-11-01T00:00:00"


# Define arrival times
arrival_time0 = "2020-12-01T00:00:00"
arrival_time1 = "2022-01-01T00:00:00"

# Convert to Ephemeris Time
et_de0 = spice.str2et(departure_time0)
et_de1 = spice.str2et(departure_time1)

et_ar0 = spice.str2et(arrival_time0)
et_ar1 = spice.str2et(arrival_time1)

# Time step (1 hour increments)
step = 3600*12*4  # seconds
ets_de = np.arange(et_de0, et_de1, step)
ets_ar = np.arange(et_ar0, et_ar1, step)

# Define target and observer
target = "MARS BARYCENTER"
origin = "EARTH BARYCENTER"
observer = "SOLAR SYSTEM BARYCENTER"
frame = "ECLIPJ2000"
abcorr = "NONE"

# Collect trajectory data
trajectory_departure = np.array([spice.spkezr(origin, et, frame, abcorr, observer)[0] for et in ets_de])
trajectory_arrival = np.array([spice.spkezr(target, et, frame, abcorr, observer)[0] for et in ets_ar])



porkchop_array = np.zeros((len(trajectory_arrival),len(trajectory_departure)))
vinfinity_array = np.zeros((len(trajectory_arrival),len(trajectory_departure)))
v_array = np.zeros((len(trajectory_arrival),len(trajectory_departure)))


for i in range(len(trajectory_arrival)):

    print(f'{i} of {len(trajectory_arrival)}')

    for j in range(len(trajectory_departure)):
        
        v0 = 0
        v = 0
        #lambert = lt.lamberts_universal_variables(1e-3*trajectory_departure[j][:3],1e-3*trajectory_arrival[i][:3],(ets_ar[i]*u.s - ets_de[j]*u.s), tm=1, mu = Sun.k.value)
        lambert = izzo.lambert(Sun.k, trajectory_departure[j][:3]*u.km, trajectory_arrival[i][:3]*u.km, (ets_ar[i]*u.s - ets_de[j]*u.s),M=0)   # :3

        v0, v = next(lambert)

        vp = trajectory_departure[j][3:]

        va = trajectory_arrival[i][3:]
        
        c3 = np.linalg.norm(v0.value - vp)**2

        v_inf_ar = np.linalg.norm(v.value - va)

        porkchop_array[i][j] = c3
        vinfinity_array[i][j] = v_inf_ar
        v_array[i][j] = np.linalg.norm(v0.value - vp)


fig, ax = plt.subplots(figsize=(12,8))

CS = ax.contour(porkchop_array, np.arange(20,200,20), label='c3')
ax.clabel(CS, inline=1, fontsize=10)

#CS1 = ax.contour(np.arange(len(trajectory_departure)),np.arange(len(trajectory_arrival)), vinfinity_array, label='v-inf')
#ax.clabel(CS1, inline=1, fontsize=10)

ax.set_title('Mars 2020 Transfer')
ax.set_xlabel('Departure Window (Days after UST:2020-12-01T00:00:00)')
ax.set_ylabel('Arrival Window (Days after UST:2022-01-01T00:00:00)')

#ax.set_facecolor((0.0,0.0,0.0))

fig.savefig(f'{dir}/video_output/pork_out.png')

plt.close()

#fig.show()

plt.imshow(v_array)
plt.colorbar()
plt.savefig(f'{dir}/video_output/v_out.png')

plt.close()

##  Delete buffer file contents
delete_contents(image_folder)

spice.kclear()

print('c3 min: ', np.min(porkchop_array))
print('v-inf min: ', np.min(vinfinity_array))

"""
for i in range(300):

    plt.title(f'i = {i}')
    ax.scatter(trajectory_departure[i][0],trajectory_departure[i][1],trajectory_departure[i][2])


     ## Save Image to buffer file
    #plt.savefig(f'{dir}/fig/im{i}.png',dpi=300)

    print(f'{i} out of {len(trajectory_departure)}')


    #plt.close()
plt.savefig(f'{dir}/fig/im.png',dpi=300)
## Output video simulation
#video_manager(image_folder, output_video_file, 60)
plt.show()
# Unload kernels after use to prevent data leaks

"""

"""


# Define vessel
k_v_vel = np.array([0.000,0.003,0.003])




#Define the vessel position and velocity parameters
v_pos = np.array([space_objects[0][2],space_objects[1][2],space_objects[2][2]])
v_vel = np.array([space_objects[3][2]+k_v_vel[0],space_objects[4][2]+k_v_vel[1],space_objects[5][2]+k_v_vel[2]])




## Extract initial position and velocity data
R = au*np.array([space_objects[0][2],space_objects[1][2],space_objects[2][2]])
V = auday*np.array([space_objects[3][2],space_objects[4][2],space_objects[5][2]])



## Correctional Matrix filps the orbit projection if facing the wrong way round
cm = [ 1,1,-1,-1 ]




##  Delete buffer file contents
delete_contents(image_folder)



##  Planetary indices of those to be visible
N = [ 0, 1, 2, 3 ]


DX = []
DV = []


loop_l = 300000     ## Keep log value less than 5 to prevent video manager from producing flickering footage

frame_capture = 1000


## Time Loop
for q in range(loop_l,2*loop_l):


    ## Time step orbits of planets by dt
    for p in N:
        updatePlanetaryPhysics(p, space_objects)

    
    ## Time step vessel trajectory by dt and then store velocity and position vectors in global variable
    vecs = updateVesselPhysics(v_pos,v_vel)

    v_pos = vecs[0]
    v_vel = vecs[1]


    ## Frame Capture for every other frame
    if q % frame_capture == 0:
        
        #print(v_pos)

        ## Setup Graph
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')


       ## Plot positions of all N planets
        for p in N:
            aw = plotOrbs(p, space_objects)
            ax.plot(aw[0],-aw[1],-aw[2],label="orbit")
            ax.scatter(au*space_objects[0][p],au*space_objects[1][p],au*space_objects[2][p])


        ## Update orbits based on updated orbital parameters
        qq = plotTraj(auday*v_vel,au*v_pos)
        ax.plot(qq[0],-qq[1],-qq[2],label="orbit")
        ax.scatter(au*v_pos[0],au*v_pos[1],au*v_pos[2])



        ## Save Image to buffer file
        plt.savefig(f'{dir}/fig/im{int(q/1000)}.png',dpi=300)

        #plt.show()

        plt.close()


        ## Record displacement data
        mars_pos = np.sqrt(space_objects[0][3]**2+space_objects[1][3]**2+space_objects[2][3]**2)
        mars_vel = np.sqrt(space_objects[3][3]**2+space_objects[4][3]**2+space_objects[5][3]**2)
        DX.append(mag(v_pos) - mars_pos)
        DV.append(mag(v_vel) - mars_vel)

        
## Output video simulation
video_manager(image_folder, output_video_file, 60)


## Show displacement data
#DX = np.array(DX)
#plt.plot(DX)
#plt.show()

#DV = np.array(DV)
#plt.plot(DV)
#plt.show()

"""