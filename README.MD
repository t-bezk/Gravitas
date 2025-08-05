# Gravitas v.4.0.1 - Gravity Assist Simulator

*Made by: Tomas Bezkorowajnyj 2025*

*Github: @Attempt4*

*Version: 4.0.1*

*Last updated: 16-06-2025*


===================

Gravitas is a python-based simulator which can predict chains of slingshot trajectories between planets in the solar system using a Lambert's solver and v-infinity matching.

This is a developing passion project of mine which will be worked on alone and aims to be completed by the end of summer 2025. The main goal for the program is to have it able to continously run and look for trajectories without intervention.

===================

*To-do list:*

~Clean and optimize porkchop code. Look into parallels~

- Develop N-body simulator and suitable regression system: So that you can take results from a Lambert's solver and use it in a real N-body simulation

~V-infinity matching for simple encounters i.e., Mariner 10 mission Earth->Venus->Mercury~

- Test N-body solver for simple slingshot encounter missions

- Dismantle Izzo's algorithm and understand it from first principles, load spice kernel data into C and then implement Izzo into C. Utilise Ctypes and JIT compilers to reduce computation times.

### Updates since v.3.0

Clutter files from previous installments have been removed.

v-infinity matching implemented on meshgrid data without regression. This will need to be improved later on.

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
>     "step":         86400,                           ## Time step in seconds
>     "out_title":    "Mars 2020 transfer window",     ## File name (for data or plots only)
> }
> ```
These indices define the initial conditions and timeframes in which trajectories are to be simulated. Definitions for planet names can be found in the spiceypy documentation.

Now call the function `generate_porkchop()` to generate an array of values for velocity. Note that the size of the arrays generated depend on the window size and the timestep. Smaller increments will take longer to generate, so a recommended step of 86400 seconds (one day) is default. To then display the associated porkshop plot graphically, use the display function `gen_porkshop_plot()` along with matplotlib. The code below is from the file `mars_2020.py` and generates a contour plot of the c3 and v_departure magnitudes from different transfers.

With a correctly defined dictionary, generate velocity arrays and then calculate arrival velocity and c3 meshgrids for each configuration like so.

> ```py
> import matplotlib.pyplot as plt
> from dictionaries import M_2020
> from encounters import generate_porkchop
> from Display.figures import gen_porkchop_plot
>
> def mars_2020():
>   
>   ## Solve for velocities using packaged Lambert's solver
>   v0, v1, vp, va  = generate_porkchop(M_2020)
>   
>   ##  Define meshgrids for contour plot
>   c3 = np.linalg.norm(v0 - vp, axis=2)**2
>   v2 = np.linalg.norm(v1 - va, axis=2)
>   
>   ##  Generate figure
>   gen_porkchop_plot(M_2020, c3, v2)
> ```

Finally, to run the code, a spice kernel has to be loaded in order to get the ephemeris data. The following code allows for safe data handling in case of an error in the function.

> ```py
> from kernel_handling import setup_kernel, destroy_kernel
>
> if __name__ == "__main__":
> 
>     setup_kernel()    ## Load kernel
> 
>     try:  ## mission code
>         mars_2020()
>     except Exception as e:
>         print(f'error: \n{e}')
>     finally:  ## Destroy kernel after use prevents data leaks
>         destroy_kernel()
> ```
>

*v-infinity matching*

For a transfer between three or more bodies,