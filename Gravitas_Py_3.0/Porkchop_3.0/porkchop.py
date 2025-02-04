#main.py

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

## Define plotting parameters
E = np.linspace(0.001,0.01,40)     ##Define as a velocity for now
phi = np.linspace(0,2*np.pi,angle_res)
theta = np.linspace(0,np.pi,angle_res)

min_E = np.zeros(len(E))

for E_i in range(len(E)):

    DX=np.zeros((angle_res,angle_res))

    for q1 in range(len(phi)):
        for q2 in range(len(theta)):

            
            #   Define vessel
            k_v_vel = np.array([E[E_i]*np.cos(phi[q1])*np.sin(theta[q2]), E[E_i]*np.sin(phi[q1])*np.sin(theta[q2]), E[E_i]*np.cos(theta[q2])])




            #   Define the vessel position and velocity parameters
            v_pos = np.array([space_objects[0][2],space_objects[1][2],space_objects[2][2]])
            v_vel = np.array([space_objects[3][2]+k_v_vel[0],space_objects[4][2]+k_v_vel[1],space_objects[5][2]+k_v_vel[2]])
            

            
            
            ##  Extract initial position and velocity data
            R = au*np.array([space_objects[0][2],space_objects[1][2],space_objects[2][2]])
            V = auday*np.array([space_objects[3][2],space_objects[4][2],space_objects[5][2]])




            ##  Get parameters for planets
            M_par = plotOrbs(3, space_objects)




            ##  Get parameters of spacecraft
            qq = plotTraj(auday*v_vel,au*v_pos)




            ##  Store min displacement angle for given parameters
            m_mod_val = np.sqrt(M_par[0]**2 + M_par[1]**2 + M_par[2]**2)
            s_mod_val = np.sqrt(qq[0]**2 + qq[1]**2 + qq[2]**2)
            
            dx_vec = np.abs(m_mod_val - s_mod_val)

            DX[q1][q2] = np.min(dx_vec)

            #print(mod_val)
            #print("-----")
    
    min_E[E_i] = np.min(DX)

    #plt.imshow(DX)
    #plt.colorbar()

    #plt.show()

dEmin_dE = (min_E[1:]-min_E[:-1]) / (E[1:]-E[:-1])

d2Emin_dE2 = (dEmin_dE[1:]-dEmin_dE[:-1]) / (E[2:]-E[:-2])

dEmin = np.max(d2Emin_dE2)

Emax = 0

for i in range(len(d2Emin_dE2)):
    if d2Emin_dE2[i] == dEmin:
        Emax = E[i]
        break

plt.plot(E,min_E)

print(Emax)

plt.show()


g=input()







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