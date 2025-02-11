from manim import *
import numpy as np

class ContourPlot(Scene):
    def construct(self):
        # Define axes
        axes = Axes(
            x_range=[-3, 3, 1], 
            y_range=[-3, 3, 1], 
            axis_config={"color": WHITE}
        )

        # Function for Z = X^2 + Y^2
        def func(x, y):
            return x**2 + y**2

        # Generate contour lines with color gradient
        contour_lines = VGroup()
        levels = np.linspace(0, 9, 10)  # Contour levels
        colors = [WHITE, PINK, RED]  # Gradient from white to pink to red

        for i, level in enumerate(levels):
            points = []
            for theta in np.linspace(0, 2 * np.pi, 100):
                r = np.sqrt(level)
                x, y = r * np.cos(theta), r * np.sin(theta)
                points.append(axes.c2p(x, y))
            
            # Interpolate color between white, pink, and red
            color = interpolate_color(colors[0], colors[1], i / len(levels))
            if i > len(levels) // 2:
                color = interpolate_color(colors[1], colors[2], (i - len(levels) // 2) / (len(levels) // 2))

            contour_lines.add(
                VMobject().set_points_as_corners(points + [points[0]]).set_stroke(color, 3)
            )

        # Add elements to the scene
        self.play(Create(axes))
        self.wait(1)
        self.play(LaggedStart(*[Create(line) for line in contour_lines], lag_ratio=0.2))
        self.wait(2)