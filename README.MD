# Gravitas v.4.0.1 - Gravity Assist Simulator

*Made by: Tomas Bezkorowajnyj 2025*

*Github: @Attempt4*

*Version: 4.0.1*

*Last updated: 16-06-2025*


===================

Gravitas is a python-based simulator which can predict dynamic paths between planets. It utilises spice kernel data to locate gravitational slingshot trajectories between planets within the solar system using a Lambert's solver and v-infinity matching.

This is a developing passion project of mine which will be worked on alone and aims to be completed by the end of the summer.

===================

*To-do list:*

~Clean and optimize porkchop code. Look into parallels~

- Develop N-body simulator and suitable regression system: So that you can take results from a Lambert's solver and use it in a real N-body simulation

- V-infinity matching for simple encounters i.e., Mariner 10 mission Earth->Venus->Mercury

- Test N-body solver for simple slingshot encounter missions

- Dismantle Izzo's algorithm and understand it from first principles, load spice kernel data into C and then implement Izzo into C. Potential future in compiled language for faster speed


### Updates since v.3.0

Clutter files from previous installments have been removed.

### Boilerplates

*Code for generating porkchop plots*

In a new file, create a dictionary variable with the following indices.

> ```py
> transfer_dictionary = {
>     "d_time0":      "2020-05-01T00:00:00",           ## Departure window lower bound Y:M:D:H:M:S
>     "d_time1":      "2020-09-01T00:00:00",           ## Departure window upper bound Y:M:D:H:M:S
>     "a_time0":      "2020-12-01T00:00:00",           ## Arrival window lower bound Y:M:D:H:M:S
>     "a_time1":      "2021-04-01T00:00:00",           ## Arrival window upper bound Y:M:D:H:M:S
> 
>     "target":       "MARS BARYCENTER",               ## Target body (defined in astropy lib.)
>     "origin":       "EARTH BARYCENTER",              ## Origin body
>     "observer":     "SOLAR SYSTEM BARYCENTER",       ## Parental body (i.e., the sun)
>     "frame":        "ECLIPJ2000",
>     "abcorr":       "NONE",
>  
>     "step":         3600*24,                         ## Time step in seconds
>     "out_title":    "Earth-Venus-Mars Transfer qq",  ## File name (for data or plots only)
> }
> ```
These indices define the initial conditions and windows within which trajectories can be simulated. Difinitions for planet names can be found in the spiceypy documentation.

Now call the function `generate_porkchop()` to generate an array of values for velocity. Note that the size of the arrays generated depend on the window size and the timestep. Smaller increments will take longer to generate, so a recommended step of 86400 seconds (one day) is default. The code below is from the file `mars_2020.py` and generates a contour plot of the c3 and v_departure magnitudes from different transfers.

> ```py
> import pathlib
> import numpy as np
> from matplotlib import pyplot as plt
> from encounter import generate_porkchop
> from dictionaries import m_2020
> 
> ##  Retrieve local file directory
> PROJ_DIR = pathlib.Path(__file__).parent.resolve()
> 
> ## Transfer between planets as layed out in transfer definition
> v0, v1, vp, va  = generate_porkchop(m_2020)
> 
> ##  Define meshgrids for contour plot
> c3 = np.linalg.norm(v0 - vp, axis=2)**2
> vi = np.linalg.norm(v1 - va, axis=2)
> 
> ##  Generate figure
> fig, ax = plt.subplots(figsize=(10,12))
> c3_contour = ax.contour(c3, levels=np.linspace(0,40,10), colors=[(0.0,0.0,1.0)])
> vi_contour = ax.contour(vi, levels=np.linspace(0,4,10), colors=[(1.0,0.0,0.0)])
> ax.clabel(c3_contour, inline=1, fontsize=10)
> ax.clabel(vi_contour, inline=1, fontsize=10)
> ax.set_title(f'{m_2020["out_title"]}')
> ax.set_xlabel(f'Departure Window (Days after UST:{m_2020["d_time0"]})')
> ax.set_ylabel(f'Arrival Window (Days after UST:{m_2020["a_time1"]})')
> 
> fig.savefig(f'{PROJ_DIR}/video_output/{m_2020["out_title"]}.png')
> 
> plt.show()
> 
> ```


