from manim import *

import numpy as np

class RotatedHyperbolicMotion(Scene):
    def construct(self):
        # Define the axes (unchanged)
        axes = Axes(
            x_range=[-5, 5, 1],  
            y_range=[-2, 6, 1],  
            axis_config={"color": WHITE}
        )

        # Define the hyperbolic function: y = sqrt(x^2 + 1)
        def hyperbolic_func(x):
            return np.sqrt(x**2 + 1) - 1

        # Generate the curve BEFORE rotating it
        original_curve = axes.plot(hyperbolic_func, x_range=[-3, 3], color=BLUE)

        # Rotate the curve by 45 degrees
        rotated_curve = original_curve.copy().rotate(0 * DEGREES, about_point=axes.c2p(0, 0))

        # Create the ball at the starting position (leftmost point)
        ball = Dot(color=RED).move_to(rotated_curve.get_start())

        planet = Circle(radius=0.2, color=RED)

        # Create a "revealing" curve
        revealed_curve = VMobject(color=BLUE)
        revealed_curve.set_stroke(width=4)
        revealed_curve.set_points_as_corners([ball.get_center()])  # Start with one point

        # Function to update the revealed curve
        def update_curve(curve):
            new_point = ball.get_center()
            if len(curve.get_points()) == 0 or np.linalg.norm(curve.get_points()[-1] - new_point) > 0.05:
                curve.add_points_as_corners([new_point])

        revealed_curve.add_updater(update_curve)

        # Ball movement animation along the rotated curve
        ball_movement = MoveAlongPath(ball, rotated_curve, run_time=5, rate_func=smooth)

        # Animate
        self.play(Create(axes))
        self.play(Create(planet))
        self.play(Create(ball))
        self.add(revealed_curve)  # Add the revealing curve before animation
        self.play(ball_movement)
        self.wait(2)

        # Remove updaters to keep final state
        revealed_curve.clear_updaters()


class AcceleratingBalls(Scene):
    def construct(self):

        # Create a time tracker to control velocity functions
        time_tracker = ValueTracker(0)
        t_max = 3  # Time duration for acceleration

        # Velocity functions (change these to modify motion)
        def big_velocity_func(t):
            if t < t_max:
                return 0.5 * t**2  # Quadratic acceleration
            else:
                return 0.5 * t_max**2  # Maintain final velocity after t_max

        def small_velocity_func(t):
            if t < t_max:
                return 0.3 * t  # Linear acceleration
            else:
                return 0.3 * t_max  # Maintain final velocity after t_max

        # Ball properties
        big_ball = Circle(radius=0.6, color=LIGHT_GRAY, fill_opacity=1).move_to(LEFT * 4)
        big_ball.set_stroke(BLUE, width=4)

        small_ball = Circle(radius=0.2, color=PINK, fill_opacity=1).move_to(LEFT * 4 + DOWN * 2)
        small_ball.set_stroke(BLUE, width=4)

        # Initial arrows (zero velocity at start)
        big_arrow = always_redraw(lambda: Arrow(
            start=big_ball.get_center(), 
            end=big_ball.get_center() + RIGHT * big_velocity_func(time_tracker.get_value()), 
            buff=0, color=WHITE
        ))
        small_arrow = always_redraw(lambda: Arrow(
            start=small_ball.get_center(), 
            end=small_ball.get_center() + RIGHT * small_velocity_func(time_tracker.get_value()), 
            buff=0, color=WHITE
        ))

        # Define update functions
        def update_big_ball(mob, dt):
            time_tracker.increment_value(dt)  # Keep track of time
            velocity = big_velocity_func(time_tracker.get_value())  
            mob.shift(RIGHT * velocity * dt)  

        def update_small_ball(mob, dt):
            velocity = small_velocity_func(time_tracker.get_value())  
            mob.shift(RIGHT * velocity * dt)

        # Create animation
        self.play(Create(big_ball), Create(small_ball))
        self.wait(1)

        # Add updaters
        big_ball.add_updater(update_big_ball)
        small_ball.add_updater(update_small_ball)
        self.add(big_arrow, small_arrow)  # Keep arrows dynamically updating

        self.wait(1)  # Run animation long enough to see acceleration + constant motion

        # Stop updates and hold final position
        big_ball.clear_updaters()
        small_ball.clear_updaters()
        self.wait(2)
