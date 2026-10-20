# SKA-ECG Arrhythmia Second Order

 [![arXiv](https://img.shields.io/badge/arXiv-2503.13942-b31b1b)](https://arxiv.org/abs/2503.13942)   [![arXiv](https://img.shields.io/badge/arXiv-2504.03214-b31b1b)](https://arxiv.org/abs/2504.03214)   [![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-SKA-orange)](https://huggingface.co/quant-iota) [![Sponsor](https://img.shields.io/badge/Sponsor-quantiota-ea4aaa?logo=github-sponsors)](https://github.com/sponsors/quantiota)

**Second-order SKA learning of arrhythmic hearts: the learner reads its own first-order result, one
step per cycle.**

The method is the one of
[SKA-ECG-Second-Order](https://github.com/quantiota/SKA-ECG-Second-Order), applied to the first-order
results of [SKA-ECG-Arrhythmia](https://github.com/quantiota/SKA-ECG-Arrhythmia).

## From the first order to the second

The first-order SKA learner turns the ECG into five bands, one per transition of the cardiac cycle
(P→Q, Q→R, R→S, S→T, T→P), each at its own height P = exp(−|ΔH/H|).

1. **Cycle vector** — each cycle k gives v_k = (P of P→Q, Q→R, R→S, S→T, T→P).
2. **Path** — the rank of the five heights in v_k: the order in which the cycle goes up and down
   through the bands.
3. **Scalar product** — c_k = cos(v_k, v_k+1), two successive cycles compared.
4. **Return** — (c_k − c_k−1) / c_k−1, the simple return (no log), what the second-order learner reads, one step per cycle.

A heart that repeats the same cycle gives one band. A cycle that differs from the one before
leaves it.

## The second-order axes

| | first order: one step per transition | second order: one step per cycle |
|---|---|---|
| knowledge | z = ‖Z‖, learned from the 5 transitions | z₂ = ‖Z₂‖, learned from the returns of c_k |
| time step | Δt = time between two waves | Δt₂ = time between two cycles |
| rate | ż = dz/dt | ż₂ = dz₂/dt₂ |
| probability | P = exp(−\|ΔH/H\|) | P₂ = exp(−\|ΔH₂/H₂\|) |

## Data

[`mitdb/`](mitdb/) — the 46 records of the PhysioNet MIT-BIH Arrhythmia Database with a lead MLII,
360 Hz, first order at scale 25 from [SKA-ECG-Arrhythmia](https://github.com/quantiota/SKA-ECG-Arrhythmia)
(700 cycles per record). It holds `data/`, `figures/` and `vr/` (four cubes per record, links in
[`mitdb/vr/README.md`](mitdb/vr/README.md)).

## Labels

Every cycle of MIT-BIH was annotated by cardiologists. Each cycle of the learner gets the label of
the annotation nearest its R peak (within 150 ms). A second-order step is the interval from one cycle
to the next, so it carries two labels: N→V is a normal cycle followed by a premature ventricular
contraction. The labels of a record are in the title of its label cubes: the counts of the cycles and
of the intervals. Clicking a point shows its interval, the cycle number, Δt₂ and the return; clicking
an interval in the legend highlights it.

| label | meaning |
|---|---|
| N | normal |
| L | left bundle branch block |
| R | right bundle branch block |
| A | atrial premature |
| a | aberrated atrial premature |
| J | nodal (junctional) premature |
| S | supraventricular premature |
| V | premature ventricular contraction |
| F | fusion of ventricular and normal |
| ! | ventricular flutter wave |
| e | atrial escape |
| j | nodal (junctional) escape |
| n | supraventricular escape |
| E | ventricular escape |
| / | paced |
| f | fusion of paced and normal |
| Q | unclassifiable |
| ? | no annotation within 150 ms |

N means a normal cycle, not a healthy heart: every MIT-BIH record is from a patient.

## Bands in Δt₂

In some records the Δt₂ cube shows two or three bands, and they follow the MIT-BIH labels:

| record | short band | long band |
|---|---|---|
| mitdb119 | three bands: N→V coupling interval (~0.5 s), N→N normal rhythm (~0.9 s), V→N compensatory pause (~1.3 s) | |
| mitdb231 | R cycles (bundle branch block) | N cycles in 2:1 AV block: one P out of two is not conducted |
| mitdb232 | A and R cycles | the long pauses after the atrial premature cycles |
| mitdb221 | atrial fibrillation: irregular cycles, the two bands are less clean | |

## Cubes

PhysioNet MIT-BIH Arrhythmia Database, lead MLII, 360 Hz. Four cubes per record: second-order learning (scale 25) of its first-order run at scale 25. Axes z₂, ż₂ and P₂ or Δt₂ (time between two cycles); colour = the sign of the return. The two label cubes are the same with the MIT-BIH labels: the counts in the title, the interval of each point (e.g. N→V) on click.

| record | sex, age | labels (cycles) | P₂ cube | Δt₂ cube | P₂ labels | Δt₂ labels |
|---|---|---|---|---|---|---|
| mitdb100 | M, 69 | 694 N, 6 A | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb100_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb100_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb100_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb100_scale25_scale25_dt_label_vr.html) |
| mitdb101 | F, 75 | 695 N, 2 ?, 2 A, 1 Q | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb101_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb101_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb101_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb101_scale25_scale25_dt_label_vr.html) |
| mitdb103 | M, ? | 700 N | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb103_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb103_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb103_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb103_scale25_scale25_dt_label_vr.html) |
| mitdb105 | F, 73 | 680 N, 20 V | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb105_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb105_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb105_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb105_scale25_scale25_dt_label_vr.html) |
| mitdb106 | F, 24 | 663 N, 37 V | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb106_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb106_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb106_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb106_scale25_scale25_dt_label_vr.html) |
| mitdb107 | M, 63 | 696 /, 4 V | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb107_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb107_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb107_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb107_scale25_scale25_dt_label_vr.html) |
| mitdb108 | F, 87 | 690 N, 8 V, 1 F, 1 A | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb108_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb108_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb108_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb108_scale25_scale25_dt_label_vr.html) |
| mitdb109 | M, 64 | 691 L, 7 V, 2 F | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb109_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb109_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb109_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb109_scale25_scale25_dt_label_vr.html) |
| mitdb111 | F, 47 | 699 L, 1 V | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb111_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb111_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb111_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb111_scale25_scale25_dt_label_vr.html) |
| mitdb112 | M, 54 | 700 N | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb112_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb112_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb112_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb112_scale25_scale25_dt_label_vr.html) |
| mitdb113 | F, 24 | 696 N, 4 a | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb113_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb113_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb113_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb113_scale25_scale25_dt_label_vr.html) |
| mitdb114 | F, 72 | 653 N, 36 V, 5 A, 4 F, 2 J | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb114_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb114_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb114_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb114_scale25_scale25_dt_label_vr.html) |
| mitdb115 | F, 39 | 700 N | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb115_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb115_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb115_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb115_scale25_scale25_dt_label_vr.html) |
| mitdb116 | M, 68 | 671 N, 29 V | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb116_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb116_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb116_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb116_scale25_scale25_dt_label_vr.html) |
| mitdb117 | M, 69 | 699 N, 1 A | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb117_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb117_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb117_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb117_scale25_scale25_dt_label_vr.html) |
| mitdb118 | M, 69 | 668 R, 26 A, 6 V | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb118_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb118_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb118_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb118_scale25_scale25_dt_label_vr.html) |
| mitdb119 | F, 51 | 553 N, 147 V | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb119_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb119_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb119_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb119_scale25_scale25_dt_label_vr.html) |
| mitdb121 | F, 83 | 700 N | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb121_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb121_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb121_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb121_scale25_scale25_dt_label_vr.html) |
| mitdb122 | M, 51 | 700 N | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb122_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb122_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb122_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb122_scale25_scale25_dt_label_vr.html) |
| mitdb123 | F, 63 | 700 N | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb123_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb123_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb123_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb123_scale25_scale25_dt_label_vr.html) |
| mitdb124 | M, 77 | 646 R, 29 J, 19 V, 3 F, 2 j, 1 A | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb124_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb124_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb124_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb124_scale25_scale25_dt_label_vr.html) |
| mitdb200 | M, 64 | 493 N, 204 V, 3 A | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb200_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb200_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb200_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb200_scale25_scale25_dt_label_vr.html) |
| mitdb201 | M, 68 | 684 N, 6 j, 5 V, 2 a, 2 A, 1 J | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb201_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb201_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb201_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb201_scale25_scale25_dt_label_vr.html) |
| mitdb202 | M, 68 | 692 N, 8 A | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb202_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb202_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb202_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb202_scale25_scale25_dt_label_vr.html) |
| mitdb203 | M, 43 | 594 N, 101 V, 2 a, 2 ?, 1 Q | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb203_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb203_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb203_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb203_scale25_scale25_dt_label_vr.html) |
| mitdb205 | M, 59 | 683 N, 16 V, 1 A | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb205_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb205_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb205_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb205_scale25_scale25_dt_label_vr.html) |
| mitdb207 | F, 89 | 548 L, 81 R, 41 !, 26 V, 4 ? | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb207_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb207_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb207_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb207_scale25_scale25_dt_label_vr.html) |
| mitdb208 | F, 23 | 521 N, 148 F, 31 V | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb208_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb208_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb208_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb208_scale25_scale25_dt_label_vr.html) |
| mitdb209 | M, 62 | 672 N, 28 A | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb209_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb209_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb209_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb209_scale25_scale25_dt_label_vr.html) |
| mitdb210 | M, 89 | 692 N, 8 V | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb210_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb210_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb210_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb210_scale25_scale25_dt_label_vr.html) |
| mitdb212 | F, 32 | 509 R, 191 N | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb212_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb212_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb212_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb212_scale25_scale25_dt_label_vr.html) |
| mitdb213 | M, 61 | 565 N, 94 F, 35 V, 6 A | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb213_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb213_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb213_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb213_scale25_scale25_dt_label_vr.html) |
| mitdb214 | M, 53 | 617 L, 82 V, 1 Q | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb214_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb214_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb214_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb214_scale25_scale25_dt_label_vr.html) |
| mitdb215 | M, 81 | 659 N, 39 V, 2 A | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb215_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb215_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb215_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb215_scale25_scale25_dt_label_vr.html) |
| mitdb217 | M, 65 | 569 /, 60 f, 50 V, 21 N | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb217_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb217_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb217_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb217_scale25_scale25_dt_label_vr.html) |
| mitdb219 | M, ? | 693 N, 4 A, 2 V, 1 F | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb219_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb219_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb219_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb219_scale25_scale25_dt_label_vr.html) |
| mitdb220 | F, 87 | 676 N, 24 A | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb220_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb220_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb220_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb220_scale25_scale25_dt_label_vr.html) |
| mitdb221 | M, 83 | 688 N, 12 V | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb221_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb221_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb221_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb221_scale25_scale25_dt_label_vr.html) |
| mitdb222 | F, 84 | 668 N, 17 A, 15 j | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb222_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb222_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb222_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb222_scale25_scale25_dt_label_vr.html) |
| mitdb223 | M, 73 | 656 N, 21 A, 13 V, 6 F, 4 e | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb223_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb223_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb223_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb223_scale25_scale25_dt_label_vr.html) |
| mitdb228 | F, 80 | 491 N, 208 V, 1 ? | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb228_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb228_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb228_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb228_scale25_scale25_dt_label_vr.html) |
| mitdb230 | M, 32 | 700 N | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb230_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb230_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb230_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb230_scale25_scale25_dt_label_vr.html) |
| mitdb231 | F, 72 | 577 R, 120 N, 2 V, 1 A | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb231_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb231_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb231_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb231_scale25_scale25_dt_label_vr.html) |
| mitdb232 | F, 76 | 534 A, 166 R | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb232_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb232_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb232_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb232_scale25_scale25_dt_label_vr.html) |
| mitdb233 | M, 57 | 506 N, 186 V, 5 F, 3 A | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb233_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb233_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb233_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb233_scale25_scale25_dt_label_vr.html) |
| mitdb234 | F, 56 | 700 N | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb234_scale25_scale25_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb234_scale25_scale25_dt_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb234_scale25_scale25_label_vr.html) | [open](https://quantiota.github.io/SKA-ECG-Arrhythmia-Second-Order/mitdb/vr/ska2_ecg_mitdb234_scale25_scale25_dt_label_vr.html) |

## Run

```bash
cd scripts
python cycle_vectors.py mitdb mitdb100 25            # cycle vectors, path, c_k, return
python learn_second_order.py mitdb mitdb100 25 25    # second-order learning (second-order scale 25)
python plot_second_order.py mitdb mitdb100 25 25     # figure
python build_cube2.py mitdb mitdb100 25 25           # P₂ cube
python build_cube2.py mitdb mitdb100 25 25 dt        # Δt₂ cube
python build_cube2.py mitdb mitdb100 25 25 label     # P₂ cube with the MIT-BIH labels
python build_cube2.py mitdb mitdb100 25 25 dt label  # Δt₂ cube with the MIT-BIH labels
```

The first-order results are read from `../SKA-ECG-Arrhythmia/ska-ecg-engine/results/` and the labels from
`../SKA-ECG-Arrhythmia/ecg-data-validation/data/<record>.atr` (clone it next to this repository). The SKA learner itself is not included in this repository.

## License

Scripts: MIT. ECG data: PhysioNet, under the license of the MIT-BIH Arrhythmia Database; cite the
database when you use it.
