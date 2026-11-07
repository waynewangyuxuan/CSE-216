# Bet 5: inference layer (codebook v1.2)

**Bottom line.** Codebook v1.2 adds §9, an ordered rule table (R00–R20, R99) from the frozen v1.1 codes to one window category with a strength. `scripts/apply_rules.py` applies it. On the 100 coded windows, **79 get a category other than `INDETERMINATE`** (NIRVANA 58/70, WildChat 21/30). Categories are literature-grounded inferences from behavior. They are not probabilities, not measures of cognition, and no human has checked them. The rules were frozen before this bet read any Bet 6–7 label: freeze 1 in 771ebf3, then freeze 2 after the gate critic's fixes, with categories on the 100 windows unchanged (`FROZEN.md`).

**Read with care.** The rules were revised on the same 100 windows they are reported on, so these coverage and distribution numbers are optimistic. The out-of-sample test is applying the frozen rules to Bets 6–7. Half of the 37 surrender-leaning windows (19) are `weak`, and all 15 in WildChat rest on request type alone (R16).

Rerun: `sh scripts/run_all.sh` (no model calls). Per-window output: `calibration/final/window_categories.csv`.

## 1. Categories and sources

| Category | Kept? | Main sources (opened) | Note |
|---|---|---|---|
| `SURRENDER_LEANING` | Kept | Shaw & Nave 2026, Table 2 p. 16, pp. 17–18; Bastani et al. pp. 14–15; Contractor & Reyes (C&R) p. 68, p. 23 | Shaw & Nave define surrender partly by absent deliberation, which logs cannot show |
| `OFFLOADING` | Kept | Risko & Gilbert 2016 ms pp. 2, 9, 14; Shaw & Nave Table 2 | Project definition: demand reduction where the writer keeps the substance |
| `AUGMENTING` | **Kept, with a caveat** | C&R pp. 22–23, 68, 77; Maier et al. pp. 2, 10; Bastani p. 15 | C&R separate it from automation by behavior and outcome. Maier would call it beneficial offloading. Both sit on RQ1's "supports" side |
| `NEUTRAL_MECHANICAL` | Kept | **No source**: a project category from v1.1 `D0` | Risko & Gilbert ms p. 14: mechanical work is not automatically low stakes |
| `INDETERMINATE` | Kept | Project category | – |
| Hybrid / "writer retains control" | Not added | Shaw & Nave recursive routes | Folded into `OFFLOADING` (R04, R08) as a **project choice**: Table 2 gives that row no locus, and it also lists post-hoc rationalization |

No proposed category was cut. Sources that use "offloading" for substitution: PAUSE (abstract only), Maier ("answer offloading"), C&R's narrative coding (p. 77). The project uses Risko & Gilbert's sense with Shaw & Nave's condition. Versions and read levels are in `sources.tsv`: Bastani is the working paper, not the PNAS version (PMC blocked by reCAPTCHA, not bypassed), and Shaw & Nave is the OSF PDF.

**Not a stop condition.** The offloading/surrender split for RQ1 holds. The disagreement over the word "offloading" was already in Bet 2's comparison, and the project's definition is stated.

## 2. Rule table (summary; full table with sources and alternatives in v1.2 §9.3)

| Rule | Pattern | Category / strength | Windows |
|---|---|---|---|
| R00 | Unrecognized code or forbidden combination | INDET | 1 |
| R01 | `D0` + `F4` | INDET | 2 |
| R02 | `D0` | NEUTRAL / moderate | 14 |
| R03 | `C0`, `UX` or `DX` | INDET | 6 |
| R04 | `V3`/`V4` | OFFLOADING / moderate | 0 |
| R05 | `U6` | INDET | 2 |
| R06 | `D3` + `U1`/`U2` + no check | SURRENDER / moderate | 2 |
| R07 | `D3`, chat only, no own work visible | SURRENDER / weak | 1 |
| R08 | `D3` or `U3` | OFFLOADING / moderate | 6 |
| R09 | `D4` + no check + `U1`/`U2` + `NONE_VISIBLE` + `C2` | SURRENDER / strong | 2 |
| R10 | `D4` + `F1`/`F6` | AUGMENTING / weak | 1 |
| R11 | `D4` + no check | SURRENDER / moderate | 5 |
| R12 | `D1` + `U7` | AUGMENTING / moderate | 1 |
| R13 | `D1` + `F5`/`F8` | OFFLOADING / moderate | 7 |
| R14 | `D1` | OFFLOADING / weak | 2 |
| R15 | `D2` + `F4` + `V1` | SURRENDER / moderate | 9 |
| R16 | `D2` + `F4` + `V0`/`V2`, chat | SURRENDER / weak | 18 |
| R17 | `D2` + `F4` + `U7` + own draft visible | AUGMENTING / weak | 3 |
| R18 | `D2` + `F1`/`F6` | AUGMENTING / moderate | 5 |
| R19 | `D2` + `F2`/`F3` + `U7` | AUGMENTING / weak | 2 |
| R20 | `D2` + `F7` + `U7` | OFFLOADING / weak | 1 |
| R99 | Anything else | INDET | 10 |

"No check" means `V0`, `V1` or `V2`. First match wins and R99 matches everything, so each window gets exactly one category. The gate critic enumerated all 98,000 code combinations: 0 errors. Combinations v1.1 forbids go to R00.

## 3. Calibration: coverage and distribution

| | n | Not indeterminate | SURRENDER s/m/w | OFFLOADING m/w | AUGMENTING m/w | NEUTRAL | INDET |
|---|---|---|---|---|---|---|---|
| NIRVANA | 70 | 58 (83%) | 2 / 16 / 4 | 9 / 3 | 6 / 6 | 12 | 12 |
| WildChat | 30 | 21 (70%) | 0 / 0 / 15 | 4 / 0 | 0 / 0 | 2 | 9 |
| **All** | 100 | **79** | 2 / 16 / 19 | 13 / 3 | 6 / 6 | 14 | 21 |

By coverage, the share not indeterminate is: C0 2/8, C1 46/57, C2 31/35. Draft 0, written from the sources before any per-window output was seen, also reached 77/100. Both versions are saved in `calibration/`.

**Session measures** (v1.2 §9.5; `calibration/final/session_measures.json`) are computed for the 37 sampled sessions, which hold 2–3 windows each and are incomplete. 20 contain a surrender-leaning window, and the mean number of switches is 0.95. The commonest transition is SURRENDER→SURRENDER (14). Complete sessions come from Bets 6–7.

## 4. Counterexamples and fixes

Two fresh agents read all 100 window views (Bet 4's coder views) against draft 0. A third agent, kept from their notes, reread the 16 windows that changed.

| Pass | OK | Wrong category | Wrong strength | Code doubt |
|---|---|---|---|---|
| Draft 0, batch A (52) | 40 | 9 | 1 | 2 |
| Draft 0, batch B (48) | 40 | 8 | 0 | 0 |
| Recheck of 16 changed windows | 12 | 3 | 0 | 1 |

| Fix | Windows it fixed | Source basis |
|---|---|---|
| R06: a partial verbatim paste with no check is surrender-leaning, not writer control | e58-t09, e61-t05 | Shaw & Nave Table 2 |
| R09 strong no longer requires `F4` | e05-t02 | Bastani p. 14; Shaw & Nave |
| R12: `D1` + `U7` is feedback use | e71-t02 | C&R p. 68 |
| R17: `F4` + `U7` with a visible own draft is AUGMENTING weak | e24-t02, e24-t03, e56-t02 | C&R p. 68 |
| R20: look-up feeding own text is OFFLOADING weak | e75-t01 | Risko & Gilbert ms p. 9 |
| `D0` + `F1` is NEUTRAL (was AUGMENTING weak) | e29-t06, e63-t01 | Project `D0` |
| R01: `D0` + `F4` is INDET | 7ce4-t01 | – |
| R07 → SURRENDER weak; R10 → AUGMENTING weak (two readers each) | e37-t02, e26-t10 | Shaw & Nave Table 2; C&R p. 68 |
| `V2` treated as no independent check | none (0 `V2` windows; untested) | v1.1 §6 |

Every change, with its evidence, is in `decisions.tsv`. Iteration stopped after the recheck, because further changes would rest on single windows.

## 5. Still weak

| Weakness | Effect |
|---|---|
| R16 rests on request type only (C&R): no adoption is seen | 18 windows, including **all 15 WildChat surrender-leaning windows**. In WildChat, "surrender-leaning" mostly means "asked the AI to write it" |
| No human has read a category; three AI readers, two of them the same model family | Agreement on categories is unmeasured |
| Calibrated on the same 100 windows that are reported | Coverage of 79% is optimistic |
| Left as known misfits: e06-t03 (critique of AI-written text read as feedback), e55-t01 (missing-input repair read as surrender), WILDCHAT-2d9a-t01 and 62387-t01 (options in chat; reviewers split), e46-t02, 56e6-t02 | Codes cannot tell these apart from neighbours |
| R16 and R17 read an `F4` request in opposite ways: R16 follows C&R (asking for text is automation), R17 overrides that on uptake when an own draft is visible; R17 is also shadowed by R15 when `V1` | 3 windows via R17 |
| Splits that turn on one code: R15 vs R16 (`V1` vs `V0`), `F2`/`F3` vs `F4` | The strength or category follows a coding boundary that Bet 4 coders may draw differently |
| Code doubts on frozen v1.1 codes: e19-t03, e51-t02, e63-t01, e37-t02 | Reported only, not recoded |
| WildChat has no editor: R06, R09, R12, R17, R19 and R20 cannot fire. This sample has no WildChat `AUGMENTING` (R10 and R18 could fire there) | Cross-dataset comparisons mix coverage with behavior |
| R04 (`V3`/`V4`) never fired: there are 0 reasoned checks in the sample | Its link to offloading is untested |
| `NEUTRAL_MECHANICAL` has no source | A project choice |
| Bastani read as the working paper; PAUSE abstract only | Page numbers may differ from the versions of record |

## 6. Gate

A fresh critic checked citations against the source texts, total coverage and priority (98,000 combinations), the freeze order in git, the rerun, and committed files for dataset text. **All five items passed.** Citations passed with fixes: one false claim (the reason for the hybrid fold), one overstated source (R17), an unclear strength scale, and 11 minor issues. All were fixed before freeze 2 (`decisions.tsv`, 04:05–04:15). A recheck of those fixes is recorded in `decisions.tsv`.
