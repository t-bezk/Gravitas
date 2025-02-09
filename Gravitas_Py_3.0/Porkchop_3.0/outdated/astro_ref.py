from astropy import units as u

import numpy as np

import spiceypy as spice

print(spice.tkvrsn('TOOLKIT'))

from poliastro.iod import izzo

from poliastro.bodies import Sun

import pathlib


dir = pathlib.Path(__file__).parent.resolve()


print(dir)

# Load SPICE kernels
spice.furnsh(f"{dir}/de421.bsp")  # Ephemeris data
spice.furnsh(f"{dir}/naif0012.tls")  # leap seconds


# Define departure times
departure_time0 = "2020-06-01T00:00:00"
departure_time1 = "2020-08-01T00:00:00"


# Define arrival times
arrival_time0 = "2021-01-01T00:00:00"
arrival_time1 = "2021-08-01T00:00:00"

# Convert to Ephemeris Time
et_de0 = spice.str2et(departure_time0)
et_de1 = spice.str2et(departure_time1)

et_ar0 = spice.str2et(arrival_time0)
et_ar1 = spice.str2et(arrival_time1)

# Time step (1 hour increments)
step = 3600  # seconds
ets_de = np.arange(et_de0, et_de1, step)
ets_ar = np.arange(et_ar0, et_ar1, step)

# Define target and observer
target = "EARTH"
observer = "SUN"
frame = "ECLIPJ2000"
abcorr = "NONE"

# Collect trajectory data
trajectory_departure = np.array([spice.spkezr(target, et, frame, abcorr, observer)[0] for et in ets_de])
trajectory_arrival = np.array([spice.spkezr(target, et, frame, abcorr, observer)[0] for et in ets_ar])



#v0, v = izzo.lambert(Sun.k)

# Unload kernels after use to prevent data leaks
spice.kclear()
