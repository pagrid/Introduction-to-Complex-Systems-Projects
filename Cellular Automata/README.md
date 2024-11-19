# Cellular Automata Simulations

This project investigates the behavior of diploid cellular automata and asynchronous cellular automata. It explores how different rules and parameters affect the dynamics and equilibrium states of 1D cellular automata.

## Contents

The simulations focus on:

* Diploid Cellular Automata: Combining two rules f_1 and f_2 probabilistically based on a parameter λ.
* Asynchronous Cellular Automata: Alternating between a local rule f_1 and an identity rule f_2 using a probability parameter α.

## Features

* Diploid Cellular Automata
Simulation of cellular automata with two rules applied probabilistically:

𝜙 = (1−𝜆) 𝑓_1 + 𝜆 𝑓_2

Includes:

 1> Rule Encoding: Efficient representation of f_1 and f_2.
 2> Density Analysis: Final density as a function of 𝜆
 3> Phase Transitions: Identify critical 𝜆 values for abrupt density changes.

* Asynchronous Cellular Automata
Simulates asynchronous dynamics where:
𝜙 = 𝛼 f_1 + (1-a) f_2.


Investigates rules 𝑓_1 ∈ [6,50,178] with 𝑓_2 = 204.

Analyzes:

  1. Space-Time Diagrams: Visualize automaton evolution for varying α.
  2. Equilibrium Density Curves: Investigate critical points as a function of 𝛼.
  3. Critical α: Analyze qualitative changes in behavior.

## Acknowledgements
This project was initialy developed as part of the Introduction to Complex Systems course at Utrecht University.
