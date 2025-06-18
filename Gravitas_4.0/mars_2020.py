"""""""""""""""""""""""""""""""""
----------------------------------
GRAVITAS v.4.0.1 - mars2020 demo
by Tomas Bezkorowajnyj c. June 2025
----------------------------------
"""""""""""""""""""""""""""""""""

import pathlib
import numpy as np
from matplotlib import pyplot as plt
from encounters import generate_porkchop
from spice_video import visual_animation
from dictionaries import m_2020

##  Retrieve local file directory
PROJ_DIR = pathlib.Path(__file__).parent.resolve()

## Transfer between planets as layed out in transfer definition
v0, v1, vp, va  = generate_porkchop(m_2020)

##  Define meshgrids for contour plot
c3 = np.linalg.norm(v0 - vp, axis=2)**2
vi = np.linalg.norm(v1 - va, axis=2)

##  Generate figure
fig, ax = plt.subplots(figsize=(10,12))
c3_contour = ax.contour(c3, levels=np.linspace(0,40,10), colors=[(0.0,0.0,1.0)])
vi_contour = ax.contour(vi, levels=np.linspace(0,4,10), colors=[(1.0,0.0,0.0)])
ax.clabel(c3_contour, inline=1, fontsize=10)
ax.clabel(vi_contour, inline=1, fontsize=10)
ax.set_title(f'{m_2020["out_title"]}')
ax.set_xlabel(f'Departure Window (Days after UST:{m_2020["d_time0"]})')
ax.set_ylabel(f'Arrival Window (Days after UST:{m_2020["a_time1"]})')
fig.savefig(f'{PROJ_DIR}/video_output/{m_2020["out_title"]}.png')
visual_animation(m_2020, "2020-12-01T00:00:00", "2021-12-01T00:00:00", vi)

plt.show()
plt.close()
