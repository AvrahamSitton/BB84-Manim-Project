# In scripts/scenes.py
from manim import *

class RealIntroduction(Scene):
    def construct(self):
        # 1. Create the title and subtitle
        main_title = Text("BB84")
        subtitle = Text("Quantum Key Distribution", font_size=36)
        
        # Position them
        main_title.to_edge(UP)
        subtitle.next_to(main_title, DOWN, buff=0.2)

        # 2. Create points for Alice and Bob
        alice_dot = Dot(point=LEFT * 5, color=BLUE)
        alice_label = Text("Alice", font_size=24).next_to(alice_dot, DOWN)
        
        bob_dot = Dot(point=RIGHT * 5, color=YELLOW)
        bob_label = Text("Bob", font_size=24).next_to(bob_dot, DOWN)

        # 3. Create the connecting line
        connecting_line = Line(alice_dot.get_center(), bob_dot.get_center(), stroke_width=2)

        # 4. Animate the scene
        self.play(Write(main_title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1)

        # Animate Alice and Bob appearing
        self.play(FadeIn(alice_dot), FadeIn(alice_label))
        self.play(FadeIn(bob_dot), FadeIn(bob_label))

        # Draw the line between them
        self.play(Create(connecting_line))
        self.wait(2)

        # A final fade out to prepare for the next scene
        self.play(
            FadeOut(main_title),
            FadeOut(subtitle),
            FadeOut(alice_dot),
            FadeOut(alice_label),
            FadeOut(bob_dot),
            FadeOut(bob_label),
            FadeOut(connecting_line)
        )
        self.wait(1)