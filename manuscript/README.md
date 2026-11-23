# Residual order four in GP(7,2): an alternative proof for Hausmann's Question 5.4

Posing locator: arXiv:2611.05178v1, Section 5, Question 5.4. After AFTD (2026).

Haobo Ma — ChronoAI Pte Ltd, Singapore.  
Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore.

## Result

The generalized Petersen graph GP(7,2) is connected and cubic, has odd girth
five, and has minimum largest complementary component order four over all
independent sets. It answers Question 5.4 of Will Hausmann, *Weighted Max Cut
in Subcubic Graphs*, arXiv:2611.05178v1, negatively.

This is an alternative to the earlier Wagner-graph answer, dated November 5,
2026, by AFTD:
<https://rainwangphy.github.io/aftd-platform/blog/2026-11-05-op-1087/>.

The complete written proof in `note.tex` classifies maximal independent sets
into five simultaneous rotation/reflection classes and gives a partition
attaining complementary component orders 4, 3, and 2. Its three corollaries
give the universal interval 4 <= K_5 <= 6 (using the prior order-six bound),
induced-subgraph and disjoint-union consequences, and the component-union
obstruction for every nonempty independent side in GP(7,2).

For Question 5.3, the printed universal condition over vertices of L is
vacuous for L empty, with empty parts allowed. The nonempty version and
the version separately requiring a bipartite complement are not asserted
in the printed question; the note proves their obstruction on GP(7,2).

## Files and reproduction

- `note.tex`: self-contained LaTeX source and bibliography.
- `metadata.json`: title, creators, license, problem identifier, and evidence link.
- `verify.py`: finite graph checks, using only the Python 3 standard library.
- `verification.json`: expected exact output of the finite checks.
- `LICENSE.txt`: CC BY 4.0 attribution and license link.

Build with Tectonic 0.17.0:

```sh
tectonic note.tex
```

Alternatively run `pdflatex note.tex` twice; the bibliography is embedded
in the LaTeX source and requires no separate BibTeX database.

Reproduce and compare the finite checks:

```sh
python3 verify.py > verification.actual.json
python3 -c 'import json; assert json.load(open("verification.actual.json")) == json.load(open("verification.json"))'
```

The program examines all 16,384 vertex subsets, finds 435 independent sets
and 49 maximal independent sets, checks all five symmetry classes, compares
graph traversal with union-find on every independent complement, and finds
zero partitions with residual order at most three. The exact optimum is four.
It also checks all five odd-cycle certificates and finds that the empty
independent set is the only solution to the printed component-union
bipartiteness condition on this graph. A separate 256-subset enumeration
reproduces the earlier Wagner-graph obstruction.

## Mathematical sources and scope

The posing source is <https://arxiv.org/html/2611.05178v1#S5.Thmtheorem4>.
The comparison with a maximum-average-degree sufficient condition uses
Cranston and Yancey, *Vertex Partitions into an Independent Set and a Forest
with Each Component Small*, arXiv:2006.11445v2, Theorem 1, at
<https://arxiv.org/html/2006.11445v2>.

The formal declaration is `result : ¬ claim` in namespace
`D5.S3.Combinatorics.Graph.ComponentPacking.HausmannQuestion54Refutation`, at
<https://github.com/the-omega-institute/trureturing/blob/6974dba01daa1a25cc74b87a86c191e95fe2c681/D5/S3/Combinatorics/Graph/ComponentPacking/HausmannQuestion54Refutation.lean>.
It proves the negation of the universal component-order-three assertion
using the same labelled graph. Its helpers establish the graph hypotheses
and four connected residual vertices for every independent set. The
five-class classification and the exact optimum four have complete written
proofs in the note and finite checks in the accompanying program.

The earlier Wagner-graph formal source is
<https://github.com/rainwangphy/aftd-platform/blob/433d28c73eba86e5864ff92226afde4bb1c6e270/lean/AFTD/Kb/Tcs/SubcubicOddGirthFivePartitionComponentLeThreeNegation.lean>.
Its main negation declaration excludes a universal partition statement
for triangle-free nonbipartite subcubic graphs, and its `_wg_key`
declaration supplies the four-vertex residual obstruction on the Wagner
graph. Its other helpers establish degree, triangle exclusion and
nonbipartiteness; the explicit five-cycle supplies exact odd girth five.
These declarations do not concern the GP(7,2) classification or corollaries.

The note's coverage table distinguishes Question 5.4 and the literal
Question 5.3 from Questions 5.1, 5.2, 5.5 and the weighted maximum-cut
conjecture, which are not covered. No minimality or priority claim is made.

## License

Copyright 2026 Haobo Ma and Wenlin Zhang. Licensed under Creative Commons
Attribution 4.0 International, CC BY 4.0 (identifier `cc-by-4.0`).
