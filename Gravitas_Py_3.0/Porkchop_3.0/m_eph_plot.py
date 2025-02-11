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
    "d_time0":      "2018-05-01T00:00:00",
    "d_time1":      "2020-11-01T00:00:00",
    "a_time0":      "2019-12-01T00:00:00",
    "a_time1":      "2024-05-01T00:00:00",

    "target":       "MARS BARYCENTER",
    "origin":       "VENUS BARYCENTER",
    "observer":     "SOLAR SYSTEM BARYCENTER",
    "frame":        "ECLIPJ2000",
    "abcorr":       "NONE",

    "step":         3600*12*10,
    "out_title":    "Venus to Mars Transfer Window",
}

v_2020 = {
    "d_time0":      "2020-04-01T00:00:00",
    "d_time1":      "2020-12-01T00:00:00",
    "a_time0":      "2020-11-01T00:00:00",
    "a_time1":      "2022-10-01T00:00:00",

    "target":       "MARS BARYCENTER",
    "origin":       "EARTH BARYCENTER",
    "observer":     "SOLAR SYSTEM BARYCENTER",
    "frame":        "ECLIPJ2000",
    "abcorr":       "NONE",

    "step":         3600*12*10,
    "out_title":    "Mars 2020",
}


##  Retrieve local file directory
dir = pathlib.Path(__file__).parent.resolve()


##--Plot porkchops with c3 and v-infinity data--##

porkchop_array, vinfinity_array, time_of_flight = P_Solve(v_2020, dir)


from manim import *
import numpy as np
import matplotlib.pyplot as plt

class ContourAndEllipses(ThreeDScene):
    def construct(self):
        # --- Left Side: Contour Plot ---
        # Example 2D NumPy array (replace with actual porkchop array)
        my_array = np.random.uniform(2, 40, (20, 20))  
        num_levels = 10
        rows, cols = my_array.shape

        contour_axes = Axes(
            x_range=[0, cols - 1, 1], 
            y_range=[0, rows - 1, 1], 
            x_length=5, y_length=5,
            axis_config={"color": WHITE},
            x_axis_config={"include_ticks": False, "font_size": 24},  
            y_axis_config={"include_ticks": False, "font_size": 24}
        ).to_edge(LEFT, buff=1)

        x_label = contour_axes.get_x_axis_label("Departure Window", direction=DOWN, buff=0.5)
        y_label = contour_axes.get_y_axis_label("Arrival Window", direction=UP, buff=0.5)

        levels = np.linspace(2, 40, num_levels)
        X, Y = np.meshgrid(np.arange(cols), np.arange(rows))
        fig, ax = plt.subplots()
        contour = ax.contour(X, Y, my_array, levels, colors=['blue', 'red', 'green'])

        contour_lines = VGroup()
        for i, collection in enumerate(contour.collections):
            color = ['blue', 'red', 'green'][i % 3]  
            for path in collection.get_paths():
                verts = path.vertices
                split_indices = np.where(np.linalg.norm(np.diff(verts, axis=0), axis=1) > 2)[0]
                sub_paths = np.split(verts, split_indices + 1)  

                for sub_path in sub_paths:
                    points = [contour_axes.c2p(x, y) for x, y in sub_path]
                    if len(points) > 1:
                        contour_line = VMobject().set_points_as_corners(points).set_stroke(color, 2)
                        contour_lines.add(contour_line)

        # --- Right Side: Rotating Ellipses ---
        ellipses_axes = ThreeDAxes(x_length=5, y_length=5, z_length=5).to_edge(RIGHT, buff=1)

        ellipse1 = ParametricFunction(
            lambda t: np.array([2 * np.cos(t), np.sin(t), 0]),
            t_range=[0, TAU], color=YELLOW
        )
        ellipse2 = ParametricFunction(
            lambda t: np.array([np.cos(t), 2 * np.sin(t), 0]),
            t_range=[0, TAU], color=RED
        )

        ellipses_group = VGroup(ellipse1, ellipse2)
        ellipses_group.rotate(PI / 4, axis=UP)

        # --- Camera Settings ---
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        # --- Animations ---
        self.play(Create(contour_axes))
        self.play(Write(x_label), Write(y_label))
        self.wait(1)
        self.play(LaggedStart(*[Create(line) for line in contour_lines], lag_ratio=0.1))
        self.wait(1)

        self.add(ellipses_axes, ellipses_group)
        self.play(Rotate(ellipses_group, angle=TAU, axis=OUT, run_time=5, rate_func=linear))
        self.wait(2)

