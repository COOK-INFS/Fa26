from manim import *


class HowAnLLMGeneratesText(Scene):
    def token_box(self, word, color=BLUE):
        label = Text(word, font_size=28)
        box = RoundedRectangle(
            width=max(0.85, label.width + 0.35),
            height=0.65,
            corner_radius=0.12,
            color=color,
        )
        box.set_fill(color, opacity=0.2)
        return VGroup(box, label)

    def choices(self, predictions):
        rows = VGroup()

        for word, probability in predictions:
            label = Text(word, font_size=25)
            percent = Text(f"{probability:.0%}", font_size=24)
            bar = Rectangle(
                width=3.2 * probability,
                height=0.22,
                stroke_width=0,
                fill_color=YELLOW,
                fill_opacity=0.9,
            )

            row = VGroup(label, bar, percent)
            label.move_to([-2.8, 0, 0])
            bar.move_to([0.2 + bar.width / 2, 0, 0])
            percent.move_to([3.5, 0, 0])
            rows.add(row)

        rows.arrange(DOWN, buff=0.25).move_to([0, -1.9, 0])
        return rows

    def construct(self):
        title = Text("How an LLM generates text", font_size=42).to_edge(UP)
        caption = Text(
            "Simplified example; probabilities are illustrative",
            font_size=20,
            color=GRAY_B,
        ).to_edge(DOWN)

        prompt_label = Text("Text so far:", font_size=26).move_to([-4.9, 1.8, 0])
        tokens = VGroup(
            *[self.token_box(word) for word in
              ["The", "cat", "sat", "on", "the"]]
        )
        tokens.arrange(RIGHT, buff=0.12).move_to([0.5, 1.8, 0])

        model_box = RoundedRectangle(
            width=4.5, height=1.0, corner_radius=0.18, color=PURPLE
        ).set_fill(PURPLE, opacity=0.2)
        model_box.move_to([0, 0.35, 0])
        model_text = Text(
            "LLM: use the context",
            font_size=28,
        ).move_to(model_box)
        model = VGroup(model_box, model_text)

        down_arrow = Arrow(tokens.get_bottom(), model_box.get_top(), buff=0.15)
        choices_label = Text(
            "Possible next tokens",
            font_size=27,
        ).move_to([0, -0.6, 0])

        first_choices = self.choices([
            ("mat", 0.62),
            ("floor", 0.22),
            ("sofa", 0.16),
        ])

        self.play(Write(title), FadeIn(caption))
        self.play(Write(prompt_label), FadeIn(tokens, lag_ratio=0.15))
        self.play(Create(down_arrow), FadeIn(model))
        self.play(Write(choices_label), FadeIn(first_choices))
        self.wait(1)

        # For this illustration, the next token is "mat".
        selected = self.token_box("mat", GREEN)
        selected.next_to(tokens, RIGHT, buff=0.12)
        self.play(
            FadeOut(first_choices),
            FadeIn(selected),
        )
        self.wait(0.5)

        # The enlarged context produces a new set of predictions.
        second_choices = self.choices([
            (".", 0.78),
            ("!", 0.14),
            ("today", 0.08),
        ])
        self.play(FadeIn(second_choices))
        self.wait(1)

        period = self.token_box(".", GREEN)
        period.next_to(selected, RIGHT, buff=0.12)
        self.play(FadeOut(second_choices), FadeIn(period))
        self.wait(1)