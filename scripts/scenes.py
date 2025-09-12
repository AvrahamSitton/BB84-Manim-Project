# Save this code as scenes.py
# In your Google Colab notebook, after cloning your repo, run:
# !manim -pql scenes.py BB84ProtocolScene

from manim import *
import random

# --- Configuration and Styling ---
# Consistent colors to match the script
Z_BASIS_COLOR = BLUE
X_BASIS_COLOR = RED
EVE_COLOR = PURPLE
BACKGROUND_COLOR = "#0E161F"  # A dark, 3b1b-style background

# Card dimensions
CARD_HEIGHT = 1.2
CARD_WIDTH = 0.8

class QubitCard(VGroup):
    """A custom Mobject to represent a qubit as a card."""
    def __init__(self, bit_value, basis, is_face_down=True):
        super().__init__()
        self.bit_value = bit_value  # 0 or 1
        self.basis = basis          # 'Z' or 'X'
        self.is_face_down = is_face_down
        self.corrupted = False      # Flag for Eve's interference

        # Visual components
        self.back = RoundedRectangle(
            width=CARD_WIDTH,
            height=CARD_HEIGHT,
            corner_radius=0.1,
            stroke_width=2,
            stroke_color=WHITE
        )
        self.face = self.back.copy()
        self.face_value_text = Text(str(self.bit_value), font_size=48).move_to(self.face.get_center())
        
        self.basis_symbol = Text(self.basis, font_size=24).move_to(
            self.back.get_center() + DOWN * 0.35 + RIGHT * 0.25
        )

        # Set colors based on basis
        basis_color = Z_BASIS_COLOR if self.basis == 'Z' else X_BASIS_COLOR
        self.back.set_fill(basis_color, opacity=1.0)
        self.face.set_fill(DARK_GRAY, opacity=1.0)

        # Assemble the card
        self.add(self.back, self.basis_symbol)
        if not self.is_face_down:
            self.remove(self.back, self.basis_symbol)
            self.add(self.face, self.face_value_text)

    def flip_card(self, scene):
        """Animates the flipping of the card."""
        target = self.copy()
        if self.is_face_down:
            # Flip to show face
            target.remove(target.back, target.basis_symbol)
            target.add(target.face, target.face_value_text)
        else:
            # Flip to show back
            target.remove(target.face, target.face_value_text)
            target.add(target.back, target.basis_symbol)
        
        self.is_face_down = not self.is_face_down
        scene.play(Transform(self, target, run_time=0.7))


class BB84ProtocolScene(MovingCameraScene):
    """
    A single, continuous scene that visualizes the entire BB84 protocol.
    This approach allows for smooth camera movements and transitions between phases.
    """
    def construct(self):
        # Set background color
        self.camera.background_color = BACKGROUND_COLOR

        # --- 1. Introduction and Setup ---
        self.setup_characters_and_channels()
        
        # --- 2. Alice Generates and Sends ---
        alice_bits, alice_bases, qubit_cards = self.alice_prepares_qubits()
        self.alice_sends_package(qubit_cards)

        # --- 3. Eve Intercepts ---
        eve_bases, eve_results = self.eve_eavesdrops(qubit_cards)

        # --- 4. Bob Receives and Measures ---
        self.messenger_continues_to_bob(qubit_cards)
        bob_bases, bob_results = self.bob_measures_qubits(qubit_cards)

        # --- 5. Basis Comparison ---
        sifted_key_indices = self.basis_comparison(alice_bases, bob_bases)

        # --- 6. Verification and Conclusion ---
        self.verify_key(sifted_key_indices, alice_bits, bob_results, eve_results)


    def setup_characters_and_channels(self):
        # Narrator: "Meet Alice and Bob, who wish to share a secret key..."
        alice = Text("Alice").to_corner(UL, buff=1)
        bob = Text("Bob").to_corner(UR, buff=1)
        eve = Text("Eve (Moshe)", color=EVE_COLOR).to_edge(DOWN, buff=0.5)

        self.add(alice, bob, eve)
        self.alice_pos, self.bob_pos, self.eve_pos = alice.get_center(), bob.get_center(), eve.get_center()

        # Narrator: "Between them are two communication channels."
        classical_channel = DashedLine(
            alice.get_bottom() + DOWN*0.2,
            bob.get_bottom() + DOWN*0.2,
            color=GRAY
        )
        classical_label = Text("Classical Channel", font_size=24).next_to(classical_channel, DOWN)
        
        quantum_channel = Line(
            alice.get_right() + RIGHT*0.5,
            bob.get_left() + LEFT*0.5,
            color=BLUE,
            stroke_width=6
        ).shift(UP*1.5)
        quantum_label = Text("Quantum Channel", font_size=24).next_to(quantum_channel, UP)

        self.play(
            Write(alice),
            Write(bob),
            Write(eve),
            Create(classical_channel),
            Write(classical_label),
            Create(quantum_channel),
            Write(quantum_label),
        )
        self.wait(2)
        
        self.classical_channel = classical_channel
        self.quantum_channel = quantum_channel


    def alice_prepares_qubits(self):
        # Narrator: "Alice begins by generating two random sequences..."
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.set(width=8).move_to(self.alice_pos + RIGHT*2 + DOWN))

        # Generate Alice's random bits and bases
        num_qubits = 8
        alice_bits = [random.randint(0, 1) for _ in range(num_qubits)]
        alice_bases = [random.choice(['Z', 'X']) for _ in range(num_qubits)]

        bits_text = Text("Bits (aᵢ): ", font_size=32).to_edge(UP, buff=1)
        bases_text = Text("Bases (bᵢ):", font_size=32).next_to(bits_text, DOWN, aligned_edge=LEFT)
        self.play(Write(bits_text), Write(bases_text))
        self.wait()

        bit_mobs = VGroup(*[Text(str(b)) for b in alice_bits]).arrange(RIGHT).next_to(bits_text, RIGHT)
        base_mobs = VGroup(*[
            Text(b, color=Z_BASIS_COLOR if b == 'Z' else X_BASIS_COLOR) for b in alice_bases
        ]).arrange(RIGHT).next_to(bases_text, RIGHT)

        self.play(LaggedStart(*[Write(mob) for mob in bit_mobs], lag_ratio=0.2))
        self.play(LaggedStart(*[Write(mob) for mob in base_mobs], lag_ratio=0.2))
        self.wait(2)

        # Narrator: "For each bit, Alice prepares a qubit – a single card."
        qubit_cards = VGroup(*[
            QubitCard(bit_value=alice_bits[i], basis=alice_bases[i]) for i in range(num_qubits)
        ]).arrange(RIGHT, buff=0.2).next_to(base_mobs, DOWN, buff=1)
        
        self.play(LaggedStart(*[FadeIn(card, shift=UP) for card in qubit_cards], lag_ratio=0.2))
        self.wait(2)
        
        self.play(FadeOut(bits_text, bases_text, bit_mobs, base_mobs))
        return alice_bits, alice_bases, qubit_cards


    def alice_sends_package(self, qubit_cards):
        # Narrator: "She then flips the cards face down and places them into a package."
        package = SurroundingRectangle(qubit_cards, buff=0.2, color=YELLOW)
        package_label = Text("Quantum Package", font_size=24).next_to(package, UP)
        
        self.play(Create(package), Write(package_label))
        self.wait()
        
        self.messenger = VGroup(package, package_label, qubit_cards)
        self.play(self.messenger.animate.move_to(self.quantum_channel.get_start()))
        self.play(Restore(self.camera.frame))
        self.wait()

    def eve_eavesdrops(self, qubit_cards):
        # Narrator: "Eve, a malicious third party, attempts to learn the key."
        self.play(self.messenger.animate.move_to(self.quantum_channel.point_from_proportion(0.5)))
        self.play(self.camera.frame.animate.set(width=10).move_to(self.eve_pos + UP*2))
        
        eve_bases = [random.choice(['Z', 'X']) for _ in range(len(qubit_cards))]
        eve_results = [None] * len(qubit_cards)

        eve_bases_text = Text("Eve's Bases:", font_size=28, color=EVE_COLOR).next_to(self.eve_pos, UP, buff=1.5, aligned_edge=LEFT)
        self.play(Write(eve_bases_text))

        for i, card in enumerate(qubit_cards):
            original_basis = card.basis
            eve_basis = eve_bases[i]
            
            # Eve chooses a basis to measure
            eve_basis_mob = Text(eve_basis, color=Z_BASIS_COLOR if eve_basis == 'Z' else X_BASIS_COLOR)
            eve_basis_mob.next_to(eve_bases_text, RIGHT, buff=i+1)
            self.play(Write(eve_basis_mob))
            
            # Eve measures the card
            card.save_state()
            self.play(card.animate.scale(1.2).next_to(eve_basis_mob, DOWN, buff=0.5))
            
            # Flip card to "measure"
            card.flip_card(self)

            if original_basis == eve_basis:
                # Narrator: "If Eve guesses the correct basis, she discovers the original bit..."
                eve_results[i] = card.bit_value
                self.play(Indicate(card.face_value_text))
            else:
                # Narrator: "But if Eve guesses the wrong basis... the very act of 'looking' changes the card."
                # TODO: Implement flashing number animation
                new_bit = random.randint(0, 1)
                new_face_text = Text(str(new_bit)).move_to(card.face_value_text.get_center())
                self.play(Transform(card.face_value_text, new_face_text))
                
                # The card is now corrupted
                card.bit_value = new_bit
                card.basis = eve_basis # The basis collapses to what it was measured in
                card.corrupted = True
                eve_results[i] = new_bit

            self.wait(0.5)
            card.flip_card(self) # Flip back face down
            self.play(Restore(card))
            self.wait(0.5)

        self.play(FadeOut(eve_bases_text, VGroup(*self.mobjects[-len(qubit_cards):]))) # Fade out basis texts
        return eve_bases, eve_results

    def messenger_continues_to_bob(self, qubit_cards):
        # Narrator: "Bob confirms to Alice that the cards have arrived."
        self.play(Restore(self.camera.frame))
        self.play(self.messenger.animate.move_to(self.quantum_channel.get_end()))
        self.wait(1)

    def bob_measures_qubits(self, qubit_cards):
        # Narrator: "Bob also randomly chooses his own sequence of measurement bases."
        self.play(self.camera.frame.animate.set(width=8).move_to(self.bob_pos + LEFT*2 + DOWN))

        bob_bases = [random.choice(['Z', 'X']) for _ in range(len(qubit_cards))]
        bob_results = [None] * len(qubit_cards)

        bob_bases_text = Text("Bob's Bases (b'ᵢ):", font_size=32).to_edge(UP, buff=1)
        bob_results_text = Text("Bob's Results (a'ᵢ):", font_size=32).next_to(bob_bases_text, DOWN, aligned_edge=LEFT)
        self.play(Write(bob_bases_text), Write(bob_results_text))

        base_mobs = VGroup(*[
            Text(b, color=Z_BASIS_COLOR if b == 'Z' else X_BASIS_COLOR) for b in bob_bases
        ]).arrange(RIGHT).next_to(bob_bases_text, RIGHT)
        self.play(Write(base_mobs))
        self.wait()

        self.play(qubit_cards.animate.arrange(RIGHT, buff=0.2).next_to(bob_results_text, DOWN, buff=1))

        result_mobs = VGroup()
        for i, card in enumerate(qubit_cards):
            card.flip_card(self)
            
            if card.basis != bob_bases[i] and not card.corrupted:
                 # TODO: Implement flashing number animation for collapse
                card.bit_value = random.randint(0, 1)
                new_face_text = Text(str(card.bit_value)).move_to(card.face_value_text.get_center())
                self.play(ReplacementTransform(card.face_value_text, new_face_text))
            
            bob_results[i] = card.bit_value
            result_mob = Text(str(bob_results[i])).move_to(card.get_center())
            result_mobs.add(result_mob)

        self.play(Transform(qubit_cards, result_mobs))
        self.wait(2)
        self.play(FadeOut(bob_bases_text, bob_results_text, base_mobs, qubit_cards))
        return bob_bases, bob_results


    def basis_comparison(self, alice_bases, bob_bases):
        # Narrator: "Now, Alice and Bob communicate again over the classical channel..."
        self.play(Restore(self.camera.frame))
        
        comparison_title = Text("Phase 5: Basis Comparison").to_edge(UP)
        self.play(Write(comparison_title))

        alice_text = Text("Alice's Bases:", font_size=36).shift(UP*2 + LEFT*4)
        bob_text = Text("Bob's Bases:", font_size=36).shift(UP*1 + LEFT*4)
        
        alice_base_mobs = VGroup(*[
            Text(b, color=Z_BASIS_COLOR if b == 'Z' else X_BASIS_COLOR) for b in alice_bases
        ]).arrange(RIGHT).next_to(alice_text, RIGHT)
        bob_base_mobs = VGroup(*[
            Text(b, color=Z_BASIS_COLOR if b == 'Z' else X_BASIS_COLOR) for b in bob_bases
        ]).arrange(RIGHT).next_to(bob_text, RIGHT)
        
        self.play(Write(alice_text), Write(bob_text), Write(alice_base_mobs), Write(bob_base_mobs))
        self.wait(2)

        sifted_key_indices = []
        discard_pile = VGroup().to_corner(DR)
        
        for i in range(len(alice_bases)):
            a_base = alice_base_mobs[i]
            b_base = bob_base_mobs[i]
            
            match_box = SurroundingRectangle(VGroup(a_base, b_base))
            self.play(Create(match_box))

            if alice_bases[i] == bob_bases[i]:
                # Narrator: "Only in positions where their bases match..."
                sifted_key_indices.append(i)
                self.play(match_box.animate.set_color(GREEN))
                self.wait(0.2)
            else:
                # Narrator: "All other bits are discarded."
                self.play(match_box.animate.set_color(RED))
                self.play(
                    FadeOut(match_box),
                    a_base.animate.move_to(discard_pile),
                    b_base.animate.move_to(discard_pile)
                )

        self.wait(2)
        sifted_key_text = Text("Sifted Key Indices: " + ", ".join(map(str, sifted_key_indices))).next_to(comparison_title, DOWN, buff=2)
        self.play(Write(sifted_key_text))
        self.wait(2)
        
        # Cleanup
        self.play(FadeOut(comparison_title, alice_text, bob_text, alice_base_mobs, bob_base_mobs, sifted_key_text, VGroup(*[m for m in self.mobjects if isinstance(m, SurroundingRectangle)])))
        return sifted_key_indices


    def verify_key(self, sifted_indices, alice_bits, bob_results, eve_results):
        # Narrator: "To ensure no one interfered, they randomly select a small number of bits..."
        verification_title = Text("Phase 6: Sampling and Verification").to_edge(UP)
        self.play(Write(verification_title))

        # Reconstruct the sifted keys
        alice_sifted = [alice_bits[i] for i in sifted_indices]
        bob_sifted = [bob_results[i] for i in sifted_indices]
        
        alice_sifted_text = Text("Alice's Sifted Key:", font_size=36).shift(UP*2 + LEFT*4)
        bob_sifted_text = Text("Bob's Sifted Key:", font_size=36).shift(UP*1 + LEFT*4)
        
        alice_mobs = VGroup(*[Text(str(b)) for b in alice_sifted]).arrange(RIGHT).next_to(alice_sifted_text, RIGHT)
        bob_mobs = VGroup(*[Text(str(b)) for b in bob_sifted]).arrange(RIGHT).next_to(bob_sifted_text, RIGHT)
        
        self.play(Write(alice_sifted_text), Write(bob_sifted_text), Write(alice_mobs), Write(bob_mobs))
        self.wait(2)
        
        # Choose a random test bit
        test_index = random.randint(0, len(alice_sifted)-1)
        
        test_bit_indicator = Arrow(
            start=UP, end=DOWN
        ).next_to(alice_mobs[test_index], UP)
        self.play(Create(test_bit_indicator))
        
        # Compare test bits
        alice_test_bit = alice_sifted[test_index]
        bob_test_bit = bob_sifted[test_index]
        
        if alice_test_bit == bob_test_bit:
            # Narrator: "If all test bits match, they assume the channel was clean!"
            result_text = Text("Test Bits Match!", color=GREEN, font_size=48).shift(DOWN*2)
            self.play(Write(result_text))
            
            final_key = alice_sifted
            final_key.pop(test_index)
            key_text = Text(f"Shared Secret Key: {''.join(map(str, final_key))}", font_size=48).move_to(result_text).shift(DOWN)
            self.play(Write(key_text))
        else:
            # Narrator: "But if even one bit doesn't match – it's a definite indication that Eve was listening!"
            result_text = Text("Eavesdropping Detected!", color=RED, font_size=48).shift(DOWN*2)
            self.play(Write(result_text))
            
            compromised_text = Text("Key Discarded. Restart Protocol.", font_size=48).move_to(result_text).shift(DOWN)
            self.play(Write(compromised_text))
            
        self.wait(5)