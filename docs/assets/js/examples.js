// Single source of truth for the gallery (website) and the slide deck.
// Edit REPO_URL after you fork / rename the repository.
window.REPO_URL = "https://github.com/YouvenZ/manim-stem-workshop";

window.DISCIPLINES = {
  math:    { label: "Mathematics",    color: "#4F9DFF", icon: "∑" },
  physics: { label: "Physics",        color: "#FF8A3D", icon: "⚛" },
  biology: { label: "Biology",        color: "#3DDC97", icon: "🧬" },
  code:    { label: "Code",           color: "#B57BFF", icon: "{ }" },
  bioinfo: { label: "Bioinformatics", color: "#FF5C8A", icon: "⌬" },
};

window.EXAMPLES = [
  {
    slug: "01_pythagoras", cls: "Pythagoras", discipline: "math", level: "Beginner",
    title: "Pythagoras without words",
    summary: "Four triangles, two arrangements of the same square: the leftover area is c² and then a² + b².",
    concepts: ["Polygon", ".animate.shift", "MathTex colours", "TransformFromCopy"],
    classroom: "Pause before the rearrangement and ask students to predict what the empty area will become.",
  },
  {
    slug: "02_fourier_series", cls: "FourierSquareWave", discipline: "math", level: "Intermediate",
    title: "Fourier series of a square wave",
    summary: "Odd harmonics are added one by one until the sum hugs the square wave — and the Gibbs overshoot refuses to disappear.",
    concepts: ["Axes.plot", "Transform between graphs", "Integer counter"],
    classroom: "Ask: will the overshoot shrink if we add more terms? Then show N = 81.",
  },
  {
    slug: "03_pendulum_phase_space", cls: "PendulumPhaseSpace", discipline: "physics", level: "Intermediate",
    title: "Damped pendulum & phase space",
    summary: "A pendulum and its (θ, θ̇) state move in lock-step; damping turns the orbit into an inward spiral.",
    concepts: ["NumPy RK4", "ValueTracker clock", "always_redraw", "TracedPath"],
    classroom: "Link energy loss to the shrinking loops; try γ = 0 to get closed orbits.",
  },
  {
    slug: "04_standing_waves", cls: "StandingWaves", discipline: "physics", level: "Beginner",
    title: "Standing waves from superposition",
    summary: "Two waves travelling in opposite directions add up to a wave that oscillates in place, with fixed nodes.",
    concepts: ["Stacked Axes", "ValueTracker time", "always_redraw plots"],
    classroom: "Connect to guitar strings: where are the nodes for the 2nd harmonic?",
  },
  {
    slug: "05_dna_double_helix", cls: "DNAHelix", discipline: "biology", level: "Intermediate",
    title: "DNA double helix & base pairing",
    summary: "A rotating “fake 3D” helix with depth cueing, then the complementary strand is read off A–T, G–C.",
    concepts: ["Procedural frames", "Depth by opacity", "LaggedStart"],
    classroom: "Students write the complementary strand on paper before the reveal.",
  },
  {
    slug: "06_predator_prey", cls: "PredatorPrey", discipline: "biology", level: "Advanced",
    title: "Predator–prey (Lotka–Volterra)",
    summary: "Prey and predator populations over time, and the same story as a closed orbit in the phase plane.",
    concepts: ["scipy.solve_ivp", "Linked axes", "pointwise_become_partial"],
    classroom: "Why do predator peaks lag behind prey peaks? Read it from both plots.",
  },
  {
    slug: "07_bubble_sort", cls: "BubbleSort", discipline: "code", level: "Beginner",
    title: "Bubble sort with live code",
    summary: "Bars are compared and swapped while the matching line of Python is highlighted.",
    concepts: ["Monospace Text", "Highlight cursor", "path_arc swaps", "Counters"],
    classroom: "Count comparisons by hand, then derive n(n−1)/2.",
  },
  {
    slug: "08_gradient_descent", cls: "GradientDescent", discipline: "code", level: "Intermediate",
    title: "Gradient descent & learning rate",
    summary: "The same bowl, two step sizes: smooth convergence versus zig-zagging across the valley.",
    concepts: ["Contours as Ellipses", "Arrow steps", "Loss curve"],
    classroom: "Ask students to guess the largest learning rate that still converges (η < 0.25).",
  },
  {
    slug: "09_needleman_wunsch", cls: "NeedlemanWunsch", discipline: "bioinfo", level: "Advanced",
    title: "Global alignment (Needleman–Wunsch)",
    summary: "The DP matrix fills cell by cell, then the traceback path spells out the optimal alignment.",
    concepts: ["Grids from NumPy", "Colour scales", "Traceback path"],
    classroom: "Hand out a blank matrix; students fill the second row before the animation does.",
  },
  {
    slug: "10_central_dogma", cls: "CentralDogma", discipline: "bioinfo", level: "Intermediate",
    title: "Central dogma: DNA → RNA → protein",
    summary: "Transcription builds the mRNA (T→U); the ribosome reads codons and grows the peptide until STOP.",
    concepts: ["Reusable tiles", "Brace", "Moving machinery"],
    classroom: "Give a new DNA sequence and let students predict the peptide.",
  },
];
