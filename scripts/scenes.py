from manim import *

class IntroductionScene(Scene):
    def construct(self):
        # Establish the title and core problem.
        title = Text("BB84: The Protocol as a Card Game", font_size=48)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # Introduce the characters.
        alice = Character(name="Alice").to_edge(LEFT, buff=1.5)
        bob = Character(name="Bob").to_edge(RIGHT, buff=1.5)
        self.play(FadeIn(alice, shift=LEFT), FadeIn(bob, shift=RIGHT))
        self.wait(1)

        # Frame the problem as a game with specific rules.
        premise_text = Text(
            "A game whose rules are a direct analogy for quantum mechanics.",
            font_size=32
        ).to_edge(UP)
        self.play(Write(premise_text))
        
        # Introduce the main object of the game.
        deck = VGroup(*[
            Card(is_face_up=False) for _ in range(8)
        ]).arrange(RIGHT, buff=0.1).move_to(ORIGIN)
        self.play(AnimationGroup(*[FadeIn(card, shift=DOWN) for card in deck], lag_ratio=0.1))
        self.wait(2)

        # Clear the scene for the next part.
        self.play(FadeOut(VGroup(alice, bob, premise_text, deck)))


class TheSetupScene(Scene):
    def construct(self):
        # Establish the players in their positions.
        alice = Character(name="Alice").to_edge(LEFT, buff=1.5)
        bob = Character(name="Bob").to_edge(RIGHT, buff=1.5)
        moshe = Character(name="Moshe").to_edge(DOWN, buff=1)
        self.add(alice, bob, moshe)

        # Visualize the Public Channel.
        public_channel = DashedLine(alice.get_top(), bob.get_top(), color=GREY_A).shift(UP*2)
        public_label = Text("Public Channel", font_size=24).next_to(public_channel, UP, buff=0.2)
        self.play(Create(public_channel), Write(public_label))
        
        # Demonstrate that the Public Channel is readable by Moshe.
        open_message = Text("MSG: Hello Bob!", font_size=20).move_to(alice.get_center())
        moshe_reads_line = DashedLine(moshe.get_top(), public_channel.get_center(), color=YELLOW)
        self.play(open_message.animate.move_to(public_channel.get_center()))
        self.play(ShowCreation(moshe_reads_line), run_time=0.5)
        self.play(FadeOut(moshe_reads_line), run_time=0.5)
        self.play(open_message.animate.move_to(bob.get_center()), FadeOut(open_message, shift=RIGHT))
        self.wait(1)

        # Visualize the Quantum Channel.
        quantum_channel = Line(alice.get_center(), bob.get_center(), color=BLUE_C, stroke_width=6)
        quantum_label = Text("Quantum Channel", font_size=24).next_to(quantum_channel, UP, buff=0.2)
        self.play(
            ReplacementTransform(public_channel, quantum_channel),
            ReplacementTransform(public_label, quantum_label)
        )

        # Show that Moshe can only observe, not read without consequence.
        sealed_package = Rectangle(width=1, height=0.6, color=DARK_GREY, fill_opacity=1)
        messenger = Messenger(item=sealed_package).move_to(alice.get_center())
        self.play(FadeIn(messenger))
        self.play(messenger.travel(quantum_channel))
        self.wait(2)


class AlicePreparesAndEncodesScene(Scene):
    def construct(self):
        # Focus on Alice's workspace.
        alice = Character(name="Alice").to_edge(LEFT, buff=1.5)
        self.add(alice)
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.set(width=9).move_to(alice.get_center() + RIGHT*2.5))

        # Define Alice's random bit and basis sequences.
        bit_values = [0, 1, 1, 0, 1, 0, 0, 1]
        basis_choices = ['Z', 'X', 'Z', 'X', 'X', 'Z', 'Z', 'X']

        # Display the sequences visually.
        bits_header = Text("Alice's Bits:").to_corner(UL).shift(RIGHT)
        bit_mobjects = VGroup(*[Integer(b) for b in bit_values]).arrange(RIGHT, buff=0.7).next_to(bits_header, DOWN)
        
        bases_header = Text("Alice's Bases:").next_to(bit_mobjects, DOWN, buff=0.8, aligned_edge=LEFT)
        basis_mobjects = VGroup(*[
            Rectangle(width=0.6, height=0.9, color=(BLUE if b == 'Z' else RED)).add(Text(b))
            for b in basis_choices
        ]).arrange(RIGHT, buff=0.5).next_to(bases_header, DOWN)

        self.play(Write(bits_header))
        self.play(AnimationGroup(*[FadeIn(b) for b in bit_mobjects], lag_ratio=0.1))
        self.wait(0.5)
        self.play(Write(bases_header))
        self.play(AnimationGroup(*[FadeIn(b) for b in basis_mobjects], lag_ratio=0.1))
        self.wait(1)

        # Visually encode each bit into a card.
        encoded_cards = VGroup()
        for i in range(len(bit_values)):
            # Create a card with the correct value and basis (back color).
            card = Card(value=bit_values[i], basis=basis_choices[i], is_face_up=True)
            card.move_to(bit_mobjects[i].get_center() + DOWN * 4)
            self.add(card)
            # Flip it face-down to hide the number.
            self.play(card.flip(), run_time=0.5)
            encoded_cards.add(card)

        # Group the prepared cards and send them.
        self.play(encoded_cards.animate.arrange(RIGHT, buff=0.1).move_to(ORIGIN + DOWN*2))
        package = SurroundingRectangle(encoded_cards, buff=0.2, color=DARK_GREY, fill_opacity=0.8)
        self.play(Create(package))
        self.play(FadeOut(VGroup(encoded_cards, package), shift=RIGHT))
        
        # Reset camera view.
        self.play(Restore(self.camera.frame))
        self.wait(1)


class MosheInterceptsScene(Scene):
    def construct(self):
        # Moshe intercepts one card from the transmission.
        moshe = Character(name="Moshe").to_edge(DOWN, buff=1)
        self.add(moshe)
        # Example card: Alice prepared a '0' in the 'Z' (blue) basis.
        intercepted_card = Card(value=0, basis='Z', is_face_up=False).move_to(moshe.get_top() + UP)
        self.play(FadeIn(intercepted_card))
        self.wait(0.5)

        # Demonstrate the rule of mismatched basis measurement.
        guess_text = Text("Moshe's Guess: Basis 'X' (Incorrect)", font_size=28).to_edge(UP)
        self.play(Write(guess_text))
        
        # The red mat represents his choice of measurement basis.
        red_measurement_mat = Rectangle(width=1.5, height=2.0, color=RED, fill_opacity=0.3).next_to(moshe, UP)
        self.play(FadeIn(red_measurement_mat))
        self.play(intercepted_card.animate.move_to(red_measurement_mat.get_center()))
        
        # The key animation: flipping reveals a now-randomized value.
        self.play(intercepted_card.flip_with_randomization()) # The card face flashes 0/1, settles on '1'.
        self.wait(0.5)
        
        # Second consequence: the card's basis (back) is altered to match the measurement.
        self.play(intercepted_card.alter_basis('X')) # The blue back is repainted to red.
        self.wait(0.5)
        
        # Moshe places the now-corrupted card back.
        self.play(intercepted_card.flip()) # Flip it back face-down.
        
        result_text = Text("Consequence: Card state is now corrupted. Error introduced.", font_size=24)
        result_text.next_to(guess_text, DOWN)
        self.play(Write(result_text))
        self.wait(2)
        
        self.play(FadeOut(VGroup(intercepted_card, guess_text, result_text, red_measurement_mat)))


class BobMeasuresAndSiftsScene(Scene):
    def construct(self):
        # For brevity, this scene combines Bob's measurement and the public sifting.
        
        # 1. Bob's Measurement (Conceptual Representation)
        # Full animation similar to Moshe's would be here, showing Bob measuring all 8 cards.
        # We will skip to the result for this script: Bob's measured values and his bases.
        
        # 2. The Sift - Public Basis Comparison
        alice_bases = ['Z', 'X', 'Z', 'X', 'X', 'Z', 'Z', 'X']
        bob_bases =   ['Z', 'Z', 'Z', 'X', 'Z', 'Z', 'X', 'X'] # Bob's random choices

        alice_row_header = Text("Alice's Public Bases:").to_edge(UP, buff=1.5)
        alice_row = VGroup(*[
            Rectangle(width=0.6, height=0.9, color=(BLUE if b == 'Z' else RED)).add(Text(b))
            for b in alice_bases
        ]).arrange(RIGHT, buff=0.4).next_to(alice_row_header, DOWN)

        bob_row_header = Text("Bob's Public Bases:").next_to(alice_row, DOWN, buff=1.0)
        bob_row = VGroup(*[
            Rectangle(width=0.6, height=0.9, color=(BLUE if b == 'Z' else RED)).add(Text(b))
            for b in bob_bases
        ]).arrange(RIGHT, buff=0.4).next_to(bob_row_header, DOWN)
        
        self.play(Write(alice_row_header), FadeIn(alice_row, shift=UP))
        self.play(Write(bob_row_header), FadeIn(bob_row, shift=UP))
        self.wait(1)

        # Iterate through and compare each basis pair.
        for i in range(len(alice_bases)):
            highlighter = SurroundingRectangle(VGroup(alice_row[i], bob_row[i]), buff=0.1)
            self.play(Create(highlighter))
            
            if alice_bases[i] == bob_bases[i]:
                result = Text("KEEP", color=GREEN)
                VGroup(alice_row[i], bob_row[i]).set_opacity(1.0)
            else:
                result = Text("DISCARD", color=GREY)
                self.play(VGroup(alice_row[i], bob_row[i]).animate.set_opacity(0.3))

            result.next_to(highlighter, DOWN)
            self.play(Write(result))
            self.play(FadeOut(highlighter))
        self.wait(2)


class ErrorCheckingScene(Scene):
    def construct(self):
        # Display the final sifted keys for Alice and Bob.
        # Bases matched at indices: 0, 2, 3, 5, 7
        alice_sifted_bits = [0, 1, 0, 0, 1]  # Alice's original values at those indices.
        # Bob's measured value at index 2 was corrupted by Moshe's incorrect 'X' measurement,
        # followed by Bob's incorrect 'Z' measurement, resulting in a random value (e.g., 1).
        bob_sifted_bits =   [0, 1, 1, 0, 1]

        alice_header = Text("Alice's Sifted Key:").to_edge(UP, buff=1.5)
        alice_display = VGroup(*[Integer(b) for b in alice_sifted_bits]).arrange(RIGHT).next_to(alice_header, DOWN)
        bob_header = Text("Bob's Sifted Key:").next_to(alice_display, DOWN, buff=1.0)
        bob_display = VGroup(*[Integer(b) for b in bob_sifted_bits]).arrange(RIGHT).next_to(bob_header, DOWN)

        self.play(Write(alice_header), FadeIn(alice_display))
        self.play(Write(bob_header), FadeIn(bob_display))
        self.wait(1)

        # They publicly compare a random subset of these bits.
        test_indices = [1, 2, 4] # e.g., they agree to reveal the 2nd, 3rd, and 5th bits.
        test_label = Text("Publicly Comparing Test Bits...", font_size=32).to_edge(UP)
        self.play(FadeIn(test_label), FadeOut(alice_header), FadeOut(bob_header))
        
        highlights = VGroup()
        for i in test_indices:
            highlights.add(SurroundingRectangle(alice_display[i], color=YELLOW))
            highlights.add(SurroundingRectangle(bob_display[i], color=YELLOW))
        self.play(Create(highlights))
        self.wait(1)

        # The error at index 2 is revealed.
        error_index = 2
        error_highlight = SurroundingRectangle(VGroup(alice_display[error_index], bob_display[error_index]), color=RED, stroke_width=8)
        error_text = Text("ERROR DETECTED!", color=RED).next_to(error_highlight, DOWN)
        self.play(ShowCreation(error_highlight))
        self.play(Write(error_text))
        self.wait(1)

        # Because an error was found, they abort the entire protocol.
        abort_text = Text("Key Compromised! Protocol ABORTED.", font_size=48, color=RED)
        self.play(
            FadeOut(VGroup(alice_display, bob_display, highlights, error_highlight, error_text, test_label)),
            Write(abort_text)
        )
        self.wait(2)


class ConclusionScene(Scene):
    def construct(self):
        # This scene shows the successful case for a strong conclusion.
        
        # The remaining, non-disclosed bits form the key.
        final_key_bits = [0, 0] # From the previous example, bits at index 0 and 5.
        final_key_display = VGroup(*[Integer(b) for b in final_key_bits]).arrange(RIGHT, buff=0.5).scale(1.5)
        final_key_label = Text("Final Shared Secret Key", font_size=40, color=GREEN)
        final_group = VGroup(final_key_label, final_key_display).arrange(DOWN, buff=0.5)
        self.play(Write(final_group))
        self.wait(2)

        # Explain the core principle.
        principle_text = Text(
            "Security is guaranteed because observation creates detectable errors.",
            font_size=32
        ).to_edge(DOWN)
        self.play(Write(principle_text))
        self.wait(2)
        
        # Transition back to the main article.
        transition_text = Text("Now, let's connect these rules to the principles of quantum mechanics.", font_size=32)
        self.play(FadeOut(VGroup(final_group, principle_text)), FadeIn(transition_text))
        self.wait(3)