# This is the content for: scripts/scenes.py
from manim import *

class IntroductionScene(Scene):
    def construct(self):
        # Create a text object
        title = Text("BB84: Quantum Key Distribution")

        # Animate the text appearing on screen
        self.play(Write(title))

        # Wait for 2 seconds before the scene ends
        self.wait(2)