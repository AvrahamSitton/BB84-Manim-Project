#
# MANIM SCRIPT: BB84_Protocol_As_Card_Game.py
# DESCRIPTION: A visual demonstration of the BB84 protocol using a card game analogy.
#              This script outlines the animations and logic for an educational video.
#

from manim import *

# --- Helper Class Definitions (Assumed for context) ---
# class Character(VGroup):
#     def __init__(self, name, position): ...
#     def emote(self, emotion): ... # e.g., 'confused', 'happy'
#
# class Card(VGroup):
#     def __init__(self, value, basis, is_face_up=False): ...
#     def flip(self): ... # Animation to turn the card over
#     def flip_with_randomization(self): ... # Animation that flashes 0/1 before settling
#     def alter_basis(self, new_basis): ... # Animation that repaints the card's back
#
# class Messenger(VMobject):
#     def travel(self, path): ... # Animation to move along a path
# ---

class IntroductionScene(Scene):
    def construct(self):
        # 1. Setup Title and Characters
        title = Text("BB84: The Protocol as a Card Game", font_size=48)
        self.play(FadeIn(title))
        self.wait(1)
        self.play(FadeOut(title))

        alice = Character(name="Alice", position=LEFT * 5)
        bob = Character(name="Bob", position=RIGHT * 5)
        self.play(FadeIn(alice), FadeIn(bob))

        # 2. Narrate the Premise
        narrator_text = Text(
            "A game whose rules are a direct analogy for the laws of quantum mechanics.",
            font_size=32
        ).to_edge(UP)
        self.play(Write(narrator_text))

        # 3. Introduce the Cards
        deck = VGroup(*[Card(value=None, basis=None) for _ in range(8)]).arrange(RIGHT, buff=0.1)
        deck.move_to(ORIGIN)
        self.play(FadeIn(deck))
        self.wait(2)
        self.play(FadeOut(VGroup(narrator_text, deck, alice, bob)))

class TheSetupScene(Scene):
    def construct(self):
        # 1. Establish Players
        alice = Character(name="Alice", position=LEFT * 5)
        bob = Character(name="Bob", position=RIGHT * 5)
        moshe = Character(name="Moshe", position=DOWN * 2)
        self.add(alice, bob, moshe)

        # 2. Public Channel
        public_channel = DashedLine(alice.get_right(), bob.get_left(), color=GREY)
        public_label = Text("Public Channel", font_size=24).next_to(public_channel, UP)
        self.play(Create(public_channel), Write(public_label))

        open_message = VGroup(Rectangle(width=1, height=0.5), Text("Hi Bob!", font_size=18)).move_to(alice.get_right())
        moshe_reads_line = Line(moshe.get_top(), public_channel.get_center(), color=YELLOW)
        self.play(open_message.animate.move_to(bob.get_left()))
        self.play(Create(moshe_reads_line), run_time=0.5)
        self.play(FadeOut(moshe_reads_line), run_time=0.5)
        self.play(FadeOut(open_message))

        # 3. Quantum Channel
        quantum_channel = Line(alice.get_right(), bob.get_left(), color=BLUE_C, stroke_width=6)
        quantum_label = Text("Quantum Channel", font_size=24).next_to(quantum_channel, DOWN)
        self.play(ReplacementTransform(public_channel, quantum_channel), ReplacementTransform(public_label, quantum_label))
        
        sealed_package = VGroup(Rectangle(width=1.2, height=0.7, fill_opacity=1, color=DARK_GREY)).move_to(alice.get_right())
        messenger = Messenger().move_to(alice.get_right())
        self.play(FadeIn(sealed_package), FadeIn(messenger))
        self.play(messenger.travel(quantum_channel))
        self.wait(2)

class AlicePreparesAndEncodesScene(Scene):
    def construct(self):
        # 1. Alice's Workspace
        alice = Character(name="Alice", position=LEFT * 5)
        self.add(alice)
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.set(width=8).move_to(alice.get_center() + RIGHT*2))

        # 2. Generate Random Sequences
        bit_values = [0, 1, 1, 0, 1, 0, 0, 1]
        basis_choices = ['Z', 'X', 'Z', 'X', 'X', 'Z', 'Z', 'X']

        bit_labels = VGroup(*[Integer(b) for b in bit_values]).arrange(RIGHT, buff=0.5).next_to(alice, RIGHT)
        basis_labels = VGroup(*[
            Rectangle(width=0.5, height=0.8, color=(BLUE if b == 'Z' else RED)).add(Text(b))
            for b in basis_choices
        ]).arrange(RIGHT, buff=0.4).next_to(bit_labels, DOWN, buff=0.5)

        self.play(Write(Text("Alice's Bits:").next_to(bit_labels, LEFT)))
        self.play(AnimationGroup(*[FadeIn(b, shift=UP) for b in bit_labels], lag_ratio=0.1))
        self.play(Write(Text("Alice's Bases:").next_to(basis_labels, LEFT)))
        self.play(AnimationGroup(*[FadeIn(b, shift=UP) for b in basis_labels], lag_ratio=0.1))
        self.wait(1)

        # 3. Encode Cards
        encoded_cards = VGroup()
        for i in range(len(bit_values)):
            card = Card(value=bit_values[i], basis=basis_choices[i])
            self.add(card.move_to(bit_labels[i].get_center() + DOWN * 3))
            self.play(card.flip(), run_time=0.5) # Flip it to be face down
            self.play(card.animate.move_to(ORIGIN + DOWN*2 + RIGHT*(i - 3.5)*0.8), run_time=0.5)
            encoded_cards.add(card)

        # 4. Package and Send
        package = Rectangle(width=encoded_cards.width + 0.5, height=encoded_cards.height + 0.5, color=DARK_GREY)
        self.play(Create(package))
        self.play(FadeOut(encoded_cards), FadeOut(package)) # Visual shorthand for packaging
        self.play(Restore(self.camera.frame))
        self.wait(1)

class MosheInterceptsScene(Scene):
    def construct(self):
        # 1. Interception
        moshe = Character(name="Moshe", position=DOWN * 2)
        self.add(moshe)
        card_to_intercept = Card(value=0, basis='Z', is_face_up=False) # Example: Alice sent |0>
        self.play(card_to_intercept.animate.move_to(moshe.get_center() + UP*1.5))

        # 2. Scenario: Mismatched Basis Guess
        guess_text = Text("Moshe's Guess: Basis 'X' (Incorrect)", font_size=28).to_edge(UP)
        self.play(Write(guess_text))
        
        red_measurement_mat = Rectangle(width=1.5, height=2, color=RED, fill_opacity=0.3).next_to(moshe, UP)
        self.play(FadeIn(red_measurement_mat))
        self.play(card_to_intercept.animate.move_to(red_measurement_mat.get_center()))
        
        # This is the key visual: the flip randomizes the state and alters the card
        self.play(card_to_intercept.flip_with_randomization()) # Outcome is now random, e.g., 1
        self.wait(0.5)
        self.play(card_to_intercept.alter_basis('X')) # The card's back is now repainted red
        self.wait(0.5)
        self.play(card_to_intercept.flip()) # Flip it back face down
        
        result_text = Text("Result: Card is now |1> encoded in 'X' basis. An error is introduced.", font_size=24)
        result_text.next_to(guess_text, DOWN)
        self.play(Write(result_text))
        self.wait(2)
        
        # 3. Moshe returns the altered card
        self.play(FadeOut(card_to_intercept, guess_text, result_text, red_measurement_mat))

class BobMeasuresScene(Scene):
    def construct(self):
        # 1. Setup Bob's workspace
        bob = Character(name="Bob", position=RIGHT * 5)
        self.add(bob)
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.set(width=8).move_to(bob.get_center() + LEFT*2))

        # 2. Bob receives cards and chooses bases
        # Simplified for clarity: we show one card measurement
        received_card = Card(value=1, basis='X', is_face_up=False) # This is the card Moshe altered
        bobs_basis_choice = 'Z' # Bob guesses wrong as well
        
        self.play(received_card.animate.move_to(bob.get_center() + LEFT * 2))
        
        bobs_basis_text = Text(f"Bob's Basis Choice: '{bobs_basis_choice}'", font_size=28).to_edge(UP)
        self.play(Write(bobs_basis_text))

        blue_measurement_mat = Rectangle(width=1.5, height=2, color=BLUE, fill_opacity=0.3).next_to(bob, LEFT)
        self.play(FadeIn(blue_measurement_mat))
        self.play(received_card.animate.move_to(blue_measurement_mat.get_center()))

        # 3. Bob measures
        # Because bases (card's 'X' vs Bob's 'Z') are mismatched, the result is random
        self.play(received_card.flip_with_randomization())
        # Let's say the random result is 0
        bobs_result = Text("Bob's Result: 0", font_size=28).next_to(bobs_basis_text, DOWN)
        self.play(Write(bobs_result))
        self.wait(2)
        self.play(Restore(self.camera.frame))

class TheSiftScene(Scene):
    def construct(self):
        # 1. Display Basis sequences
        alice_bases = ['Z', 'X', 'Z', 'X', 'X', 'Z', 'Z', 'X']
        bob_bases =   ['Z', 'Z', 'Z', 'X', 'Z', 'Z', 'X', 'X']

        alice_row = VGroup(*[
            Rectangle(width=0.5, height=0.8, color=(BLUE if b == 'Z' else RED)).add(Text(b))
            for b in alice_bases
        ]).arrange(RIGHT, buff=0.4).shift(UP * 2)
        
        bob_row = VGroup(*[
            Rectangle(width=0.5, height=0.8, color=(BLUE if b == 'Z' else RED)).add(Text(b))
            for b in bob_bases
        ]).arrange(RIGHT, buff=0.4)
        
        self.play(Write(Text("Alice's Bases:").next_to(alice_row, LEFT)), FadeIn(alice_row))
        self.play(Write(Text("Bob's Bases:").next_to(bob_row, LEFT)), FadeIn(bob_row))
        self.wait(1)

        # 2. Compare each basis
        comparison_results = VGroup()
        for i in range(len(alice_bases)):
            highlighter = SurroundingRectangle(VGroup(alice_row[i], bob_row[i]), buff=0.2)
            self.play(Create(highlighter))
            
            if alice_bases[i] == bob_bases[i]:
                result = VGroup(Checkmark(color=GREEN), Text("KEEP")).arrange(DOWN)
            else:
                result = VGroup(Cross(color=RED), Text("DISCARD")).arrange(DOWN)
            
            result.next_to(highlighter, DOWN)
            self.play(FadeIn(result))
            self.play(FadeOut(highlighter))
            comparison_results.add(result)
        self.wait(2)

class ErrorCheckingScene(Scene):
    def construct(self):
        # 1. Define Sifted Keys (Alice's original vs Bob's measured)
        # Bases matched at indices 0, 2, 3, 5, 7
        alice_sifted_key = [0, 1, 0, 0, 1] # Original values
        bob_sifted_key =   [0, 1, 1, 0, 1] # Bob's values. Note the error at index 2 from Moshe's interception.

        alice_display = VGroup(*[Integer(b) for b in alice_sifted_key]).arrange(RIGHT).shift(UP*2)
        bob_display = VGroup(*[Integer(b) for b in bob_sifted_key]).arrange(RIGHT)

        self.play(Write(Text("Alice's Sifted Key:").next_to(alice_display, LEFT)), FadeIn(alice_display))
        self.play(Write(Text("Bob's Sifted Key:").next_to(bob_display, LEFT)), FadeIn(bob_display))
        self.wait(1)

        # 2. Select Test Bits
        test_indices = [1, 2, 4] # They agree to compare these
        test_label = Text("Publicly Comparing Test Bits", font_size=32).to_edge(UP)
        self.play(Write(test_label))
        
        highlights = VGroup()
        for i in test_indices:
            highlights.add(SurroundingRectangle(alice_display[i], color=YELLOW))
            highlights.add(SurroundingRectangle(bob_display[i], color=YELLOW))
        self.play(Create(highlights))
        self.wait(1)

        # 3. Reveal Error
        error_index = 2
        error_highlight = SurroundingRectangle(VGroup(alice_display[error_index], bob_display[error_index]), color=RED, stroke_width=8)
        error_text = Text("ERROR DETECTED!", color=RED).next_to(error_highlight, DOWN)
        self.play(Create(error_highlight))
        self.play(Write(error_text))

        # 4. Abort Protocol
        abort_text = Text("Key is Compromised! ABORT.", font_size=40, color=RED)
        self.wait(1)
        self.play(
            FadeOut(VGroup(alice_display, bob_display, highlights, error_highlight, error_text, test_label)),
            FadeIn(abort_text)
        )
        self.wait(2)

class ConclusionScene(Scene):
    def construct(self):
        # NOTE: This scene shows the successful case for a good conclusion.
        # In a full video, this would follow a successful ErrorCheckScene.
        
        # 1. Show the final, secure key
        final_key = VGroup(*[Integer(d) for d in [0, 0]]).arrange(RIGHT, buff=0.5) # The non-test bits
        final_key_label = Text("Final Shared Secret Key", font_size=40, color=GREEN)
        VGroup(final_key_label, final_key).arrange(DOWN, buff=0.5)
        self.play(Write(final_key_label), FadeIn(final_key))
        self.wait(1)

        # 2. Concluding Text
        conclusion_text = Text(
            "Security is guaranteed by the principle of observation.",
            font_size=32
        ).to_edge(DOWN)
        self.play(Write(conclusion_text))
        self.wait(2)
        
        # 3. Transition back to the article
        transition_text = Text("Now, let's connect these rules to the principles of quantum mechanics.", font_size=32)
        self.play(FadeOut(VGroup(final_key_label, final_key, conclusion_text)), FadeIn(transition_text))
        self.wait(3)