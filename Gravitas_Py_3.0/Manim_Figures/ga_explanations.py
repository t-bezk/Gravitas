from manim import *

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
