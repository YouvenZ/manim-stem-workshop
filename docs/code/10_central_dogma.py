"""
10 · Bioinformatics — The central dogma: DNA -> mRNA -> protein
Transcription copies the template strand into mRNA (T becomes U);
the ribosome then reads the mRNA three letters at a time, adding one
amino acid per codon until it meets a stop codon.

Manim ideas: reusable "tile" mobjects, coordinated LaggedStart +
moving machinery, Brace for codons, building a chain step by step.

Render:
    manim -pqm scenes/10_central_dogma.py CentralDogma
"""
from manim import *

COLORS = {"A": "#FF5C8A", "T": "#FFD166", "U": "#FF8A3D", "G": "#3DDC97", "C": "#4F9DFF"}
DNA_PAIR = {"A": "T", "T": "A", "G": "C", "C": "G"}
RNA_FROM_TEMPLATE = {"A": "U", "T": "A", "G": "C", "C": "G"}
CODON_TABLE = {"AUG": "Met", "GCU": "Ala", "UUC": "Phe", "GGA": "Gly", "UAA": "Stop"}
AA_COLORS = ["#B57BFF", "#4F9DFF", "#3DDC97", "#FFD166"]
BG = "#0B0F19"

CODING = "ATGGCTTTCGGATAA"
STEP = 0.58


def tile(base):
    box = RoundedRectangle(width=0.5, height=0.6, corner_radius=0.08, stroke_width=0,
                           fill_color=COLORS[base], fill_opacity=0.9)
    letter = Text(base, font="Monospace", font_size=26, color=BG, weight=BOLD).move_to(box)
    return VGroup(box, letter)


def strand(seq, y):
    row = VGroup(*[tile(b) for b in seq])
    for k, t in enumerate(row):
        t.move_to(np.array([(k - (len(seq) - 1) / 2) * STEP, y, 0]))
    return row


class CentralDogma(Scene):
    def construct(self):
        title = Text("The central dogma", font_size=40).to_edge(UP, buff=0.25)
        self.play(Write(title))

        template_seq = "".join(DNA_PAIR[b] for b in CODING)
        coding = strand(CODING, 2.0)
        template = strand(template_seq, 1.2)
        bonds = VGroup(*[Line(c.get_bottom(), t.get_top(), color=GREY_B, stroke_width=2)
                         for c, t in zip(coding, template)])
        lab_c = Text("coding 5'→3'", font_size=20, color=GREY_B).next_to(coding, LEFT, buff=0.25)
        lab_t = Text("template 3'→5'", font_size=20, color=GREY_B).next_to(template, LEFT, buff=0.25)

        self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.2) for t in coding], lag_ratio=0.04),
                  LaggedStart(*[FadeIn(t, shift=UP * 0.2) for t in template], lag_ratio=0.04),
                  FadeIn(lab_c), FadeIn(lab_t))
        self.play(Create(bonds))

        # 1. Transcription
        step1 = Text("1 · Transcription", font_size=30, color=COLORS["U"]).next_to(title, DOWN, buff=0.15)
        self.play(FadeIn(step1), FadeOut(bonds),
                  VGroup(coding, lab_c).animate.shift(UP * 0.35).set_opacity(0.45))

        mrna_seq = "".join(RNA_FROM_TEMPLATE[b] for b in template_seq)
        mrna = strand(mrna_seq, 0.3)
        polymerase = Ellipse(width=1.3, height=1.9, color=WHITE, fill_color=WHITE, fill_opacity=0.12)
        polymerase.move_to(np.array([mrna[0].get_x(), 0.75, 0]))
        pol_label = Text("RNA pol", font_size=18).next_to(polymerase, DOWN, buff=0.1)
        self.play(FadeIn(polymerase), FadeIn(pol_label))
        self.play(
            VGroup(polymerase, pol_label).animate.shift(RIGHT * STEP * (len(mrna) - 1)),
            LaggedStart(*[TransformFromCopy(t, m) for t, m in zip(template, mrna)], lag_ratio=0.25),
            run_time=5, rate_func=linear,
        )
        note = Text("T → U  in RNA", font_size=24, color=COLORS["U"]).next_to(mrna, DOWN, buff=0.3)
        self.play(FadeIn(note))
        self.wait(0.5)

        # 2. Translation
        self.play(FadeOut(VGroup(coding, template, lab_c, lab_t, polymerase, pol_label, note)),
                  mrna.animate.move_to(np.array([0, -2.0, 0])))
        step2 = Text("2 · Translation", font_size=30, color="#B57BFF").move_to(step1)
        lab_m = Text("mRNA 5'→3'", font_size=20, color=GREY_B).next_to(mrna, LEFT, buff=0.25)
        self.play(ReplacementTransform(step1, step2), FadeIn(lab_m))

        codons = [VGroup(*mrna[3 * k:3 * k + 3]) for k in range(len(mrna) // 3)]
        braces = VGroup(*[Brace(c, DOWN, buff=0.08, color=GREY_B) for c in codons])
        self.play(LaggedStart(*[GrowFromCenter(b) for b in braces], lag_ratio=0.15))

        ribosome = VGroup(
            RoundedRectangle(width=2.0, height=0.9, corner_radius=0.35, fill_color="#B57BFF", fill_opacity=0.25,
                             stroke_color="#B57BFF"),
            RoundedRectangle(width=1.6, height=1.0, corner_radius=0.4, fill_color="#B57BFF", fill_opacity=0.18,
                             stroke_color="#B57BFF"),
        )
        ribosome[1].next_to(ribosome[0], UP, buff=-0.15)
        ribosome.move_to(codons[0].get_center() + UP * 0.35)
        self.play(FadeIn(ribosome, scale=0.8))

        chain, links = VGroup(), VGroup()
        for k, codon in enumerate(codons):
            word = "".join(mrna_seq[3 * k:3 * k + 3])
            aa = CODON_TABLE[word]
            if k > 0:
                self.play(ribosome.animate.move_to(codon.get_center() + UP * 0.35), run_time=0.7)
            lookup = Text(f"codon {word} → {aa}", font_size=28).next_to(step2, DOWN, buff=0.35)
            if aa == "Stop":
                stop = Text("STOP", font_size=30, color=COLORS["A"], weight=BOLD).next_to(ribosome, UP, buff=0.15)
                self.play(FadeIn(lookup), FadeIn(stop, scale=1.4))
                self.play(FadeOut(lookup))
                break
            bead = VGroup(Circle(radius=0.38, fill_color=AA_COLORS[k], fill_opacity=0.9, stroke_color=WHITE,
                                 stroke_width=2),
                          Text(aa, font_size=20, color=BG, weight=BOLD))
            bead.move_to(codon.get_center() + UP * 1.75)
            anims = [FadeIn(lookup), GrowFromPoint(bead, codon.get_center())]
            if chain:
                link = Line(chain[-1].get_right(), bead.get_left(), color=WHITE, stroke_width=4)
                links.add(link)
                anims.append(Create(link))
            self.play(*anims, run_time=0.8)
            self.play(FadeOut(lookup), run_time=0.3)
            chain.add(bead)

        # Release the peptide.
        peptide = VGroup(links, chain)
        self.play(peptide.animate.shift(UP * 1.3), FadeOut(ribosome), FadeOut(stop))
        protein = Text("protein: Met–Ala–Phe–Gly …", font_size=28).next_to(peptide, UP, buff=0.35)
        summary = VGroup(
            Text("DNA", font_size=34, color=COLORS["G"]), Arrow(LEFT, RIGHT, buff=0),
            Text("RNA", font_size=34, color=COLORS["U"]), Arrow(LEFT, RIGHT, buff=0),
            Text("Protein", font_size=34, color="#B57BFF"),
        ).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.25)
        self.play(Write(protein))
        self.play(FadeIn(summary, shift=UP * 0.3))
        self.wait(2)
