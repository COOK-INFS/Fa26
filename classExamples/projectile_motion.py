from manim import *


class ProjectileMotion(Scene):
    def construct(self):
        # Initial velocities are in m/s; gravity is in m/s².
        vx = 5.0
        vy = 9.8
        g = 9.8
        flight_time = 2 * vy / g  # 2 seconds

        title = Text("Projectile motion", font_size=42).to_edge(UP)
        equations = Text(
            "x = 5t       y = 9.8t - 4.9t²",
            font_size=27,
        ).next_to(title, DOWN, buff=0.25)

        axes = Axes(
            x_range=[0, 11, 1],
            y_range=[0, 6, 1],
            x_length=9,
            y_length=4,
            tips=False,
        ).shift(DOWN * 0.5)

        x_label = Text("horizontal distance (m)", font_size=22)
        x_label.next_to(axes.x_axis, DOWN, buff=0.3)

        def position(t):
            x = vx * t
            y = vy * t - 0.5 * g * t**2
            return axes.c2p(x, y)

        time = ValueTracker(0)
        ball = Dot(position(0), radius=0.12, color=YELLOW)
        ball.add_updater(lambda dot: dot.move_to(position(time.get_value())))

        path = TracedPath(
            ball.get_center,
            stroke_color=YELLOW,
            stroke_width=5,
        )

        horizontal = Arrow(
            axes.c2p(0, 0), axes.c2p(2, 0),
            buff=0, color=BLUE,
        )
        vertical = Arrow(
            axes.c2p(2, 0), axes.c2p(2, 2),
            buff=0, color=GREEN,
        )
        horizontal_label = Text("horizontal velocity", font_size=22, color=BLUE)
        horizontal_label.next_to(horizontal, DOWN, buff=0.15)
        vertical_label = Text("upward velocity", font_size=22, color=GREEN)
        vertical_label.next_to(vertical, RIGHT, buff=0.15)

        gravity = Arrow(
            axes.c2p(7, 5), axes.c2p(7, 4),
            buff=0, color=RED,
        )
        gravity_label = Text("gravity", font_size=24, color=RED)
        gravity_label.next_to(gravity, RIGHT, buff=0.15)

        self.play(Write(title), Write(equations))
        self.play(Create(axes), FadeIn(x_label))
        self.play(FadeIn(ball))
        self.play(
            GrowArrow(horizontal),
            GrowArrow(vertical),
            FadeIn(horizontal_label),
            FadeIn(vertical_label),
        )
        self.wait(1)

        self.play(
            FadeOut(horizontal),
            FadeOut(vertical),
            FadeOut(horizontal_label),
            FadeOut(vertical_label),
            GrowArrow(gravity),
            FadeIn(gravity_label),
        )

        self.add(path)
        self.play(
            time.animate.set_value(flight_time),
            run_time=5,
            rate_func=linear,
        )
        ball.clear_updaters()

        peak = Dot(axes.c2p(5, 4.9), radius=0.07, color=GREEN)
        peak_label = Text("peak: 4.9 m", font_size=25, color=GREEN)
        peak_label.next_to(peak, UP, buff=0.2)

        landing_label = Text("range: 10 m", font_size=25, color=YELLOW)
        landing_label.next_to(ball, UP, buff=0.2)

        self.play(FadeIn(peak), Write(peak_label), Write(landing_label))
        self.wait(2)