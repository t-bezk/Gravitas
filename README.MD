# Gravitas - Python Based Gravity Assist Simulator

*Made by: Tomas Bezkorowajnyj 2025*
*Github: @Attempt4*
*Version: 4.0.1*
*Last updated: 16-06-2025*

===================

Gravitas is a python-based simulator which can predict dynamic paths between planets. It can locate gravitational slingshot trajectories between planets within the solar system using a Lambert's solver and v-infinity matching. This is a developing passion project of which will be worked on solo and aims to be completed by the end of the summer. 

===================

*To-do list:*

- Clean and optimize porkchop code. Look into parallels

- Develop N-body simulator and suitable regression system: So that you can take results from a Lambert's solver and use it in a real N-body simulation

- V-infinity matching for simple encounters i.e., Mariner 10 mission Earth->Venus->Mercury

- Test N-body solver for simple slingshot encounter missions

- Dismantle Izzo's algorithm and understand it from first principles, load spice kernel data into C and then implement Izzo into C. Potential future in compiled language for faster speed


### Updates since v.3.0

Clutter files from previous installments have been removed. Porkchop plot generator and dict definitions for encounter can be located in `ephemeris_plot.py`.

### Boilerplates

*Code for generating porkchop plots*

In a new file, create a dictionary variable with the following indices.

>
> `transfer_dictionary = {`
> `    "d_time0":      "2020-05-01T00:00:00",           ## Departure window lower bound Y:M:D:H:M:S`
> `    "d_time1":      "2020-09-01T00:00:00",           ## Departure window upper bound Y:M:D:H:M:S`
> `    "a_time0":      "2020-12-01T00:00:00",           ## Arrival window lower bound Y:M:D:H:M:S`
> `    "a_time1":      "2021-04-01T00:00:00",           ## Arrival window upper bound Y:M:D:H:M:S`
> ``
> `    "target":       "MARS BARYCENTER",               ## Target body (defined in astropy lib.)`
> `    "origin":       "EARTH BARYCENTER",              ## Origin body`
> `    "observer":     "SOLAR SYSTEM BARYCENTER",       ## Parental body (i.e., the sun)`
> `    "frame":        "ECLIPJ2000",`
> `    "abcorr":       "NONE",`
> ` `
> `    "step":         3600*24,                         ## Time step in seconds`
> `    "out_title":    "Earth-Venus-Mars Transfer qq",  ## File name (for data or plots only)`
> `}`

These indices define the initial conditions and windows within which trajectories can be simulated. 

Now call the function `porkchop_solve()` to generate an array of values for velocity. Note that the size of the arrays generated depend on the window size and the timestep. Smaller increments will take longer to generate, so a recommended step of 86400 seconds (one day) is default.

> `import numpy as np`
> `import matplotlib.pyplot as plt`
>
> `## Transfer between planets as layed out in transfer definition`
> `v0,v1,vp,va  = porkchop_solve(m_2020)`
> ` `
> `##  Define meshgrids for contour plot`
> `c3 = np.linalg.norm(v0 - vp, axis=2)**2  ## relative arrival velocity`
> `vi = np.linalg.norm(v1 - va, axis=2)     ## relative departure velocity`
> ` `
> `##  Define figure`
> `fig, ax = plt.subplots(figsize=(10,12))`
> ` `
> `## Generate axis contours`
> `c3_contours = ax.contour(vi, levels=np.linspace(0,4,10), colors=[(0.0,0.0,1.0)])`
> `vi_contours = ax.contour(vi, levels=np.linspace(0,4,10), colors=[(0.0,0.0,1.0)])`
> `ax.clabel(contour_plot, inline=1, fontsize=10)`
> `plt.xlabel(f'Departure Window (Days after UST:{m_2020["d_time0"]})')`
> `plt.ylabel(f'Arrival Window (Days after UST:{m_2020["a_time1"]})')`
> `plt.title(m_2020["out_title"])`
> ` `
> `save figure and cleanup`
> `plt.savefig(f'{dir}/video_output/{m_2020["out_title"]}.png')`
> `plt.show()`
> `plt.close()`

### Documentation











---


