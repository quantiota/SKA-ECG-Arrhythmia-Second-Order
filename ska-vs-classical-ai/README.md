# How SKA differs from a classical AI

![SKA learner versus classical learner](ska_vs_classical.png)

## Classical AI (right)

A classical AI learns from ECGs that cardiologists have already labelled: normal beat,
premature ventricular beat, atrial fibrillation, and so on.

It goes over thousands of labelled beats many times until it can repeat the labels on its own.
For a new ECG it then gives an answer, for example "this beat is a PVC".

You get the answer, but not the reason: the decision comes from millions of internal numbers
that nobody can read.

## SKA (left)

SKA receives the raw ECG, wave after wave: P, Q, R, S, T, then the next beat. It is given no
labels and no diagnosis.

It reads the recording once, in real time, and arranges what it reads into a 3D cube. The
structure of the heart appears in that cube:

- the five transitions of the beat (P→Q, Q→R, R→S, S→T, T→P) form five bands;
- a heart that repeats the same cycle stays in its bands;
- a cycle that differs leaves them.

Only then are the cardiologists' labels placed on the cube.

## Example: MIT-BIH record 119

In the cube of the time between cycles, the cycle-to-cycle intervals form three bands:

- short (about 0.5 s): from a normal beat to a premature ventricular beat (V), the coupling
  interval (145 intervals);
- middle (about 0.9 s): from a normal beat to the next normal beat, the normal rhythm (404);
- long (about 1.3 s): from the V to the next normal beat, the compensatory pause (146).

Every interval falls in its band, with no mixing. SKA was never told what a V or a compensatory
pause is. It placed them apart on its own; the labels only show what each band is.

## In one sentence

A classical AI repeats the labels it was taught. SKA shows the structure of the heart, and the
cardiologist reads that structure with their own labels.