# Figure critic report

Independent review of the 11 figures in `main.tex` / `main.pdf` at commit 8c492e9 (working tree clean for `Final_Project/paper`). I edited nothing except this file. No dataset text is quoted here.

**Verdict: FAIL.** 9 blocking problems, 16 minor problems.

Blocking means the figure or caption says or implies something false, misleads about a claim, drops something the claim needs, or fails a stated requirement. Minor means incomplete or unpolished.

## 1. Mechanical checks

| Check | Result |
|---|---|
| `python3 scripts/check_build.py` | PASS. 19 body pages (limit 20), 27 total, no overfull line over 2 pt |
| `python3 scripts/spellcheck.py` | PASS. 2,048 distinct words. The script reads `figures/figure_text.txt`, so figure text is included |
| `python3 scripts/check_tex.py` | PASS. 11 figures, 3 floating tables |
| `python3 scripts/check_palette.py` | Runs, with no pass or fail logic. Worst pair: normal 14.7 (SLr, IND), protan 11.4 (SLb, NEU), deutan 13.4 (SLr, IND), tritan 12.8 (OFF, NEU). Smallest greyscale L* gap is 7.8 (SLb 54.2 and NEU 46.4; also SLr 77.7 and AUG 69.8). See B8 |
| 8-word overlap with dataset text (scratch script, logic from `analysis/scripts/check_no_text.py`; 499 source files, 1,202,598 source runs) | PASS. `main.tex` 0 of 13,761 runs; `main.tex` with LaTeX removed 0 of 12,153; `figure_text.txt` 0 of 1,091; `figure_text.txt` joined across lines 0 |
| Figures reproduce | PASS. `make_figures.py` rerun into a scratch folder gave byte-identical copies of all 11 PDFs and `figure_text.txt` |
| Every thesis has a visual | PASS. T1 Figs 7 and 8, T2 Fig 9, T3 Fig 10, T4 Fig 11 |
| Text and captions no longer refer to removed tables | PASS. Only `tab:agreement`, `tab:rq2` and `tab:aiuse` are referenced, and all three exist |
| Country is USA; matching TODO updated | PASS. `main.tex` line 28; `TODO_WAYNE.md` section 1 item 1 says the country is set to USA |
| AI Use Statement still true | FAIL, see B9 |

## 2. Figure by figure

Rendered pages were read in color and greyscale (pages 5 to 14). The text block is about 6.0 in wide, so figures print at about 100%. The smallest type is 6.8 to 6.9 pt, which is legible. Figure numbers below follow the PDF.

| Fig | Name | 1 Readable, placement | 2 Correct | 3 Colors, greyscale | 4 Earns its space | 5 Caption, ref, Description | 6 No dataset text |
|---|---|---|---|---|---|---|---|
| 1 | flow | PASS | **FAIL** (B3) | PASS (M12) | PASS (M2) | **FAIL** (B3, B4) | PASS |
| 2 | anatomy | PASS | PASS (M11) | PASS | PASS | PASS | PASS |
| 3 | worked | PASS | **FAIL** (B5) | PASS | PASS | PASS | PASS |
| 4 | concept_map | PASS (M5) | **FAIL** (B6, B7, M3) | PASS (M5) | PASS (M4) | **FAIL** (B6, B7) | PASS |
| 5 | categories | PASS (M6) | PASS | **FAIL** (B8) | PASS | PASS | PASS |
| 6 | archetypes | PASS (M14) | PASS | **FAIL** (B8) | PASS | PASS | PASS |
| 7 | after_response | PASS | PASS (M7) | PASS | PASS | PASS (M7) | PASS |
| 8 | outcome | PASS (M8) | PASS | PASS | PASS | PASS | PASS |
| 9 | own_work | PASS | PASS | PASS (M12) | PASS | **FAIL** (M1) | PASS |
| 10 | dwell | PASS (M15) | PASS | PASS | PASS | PASS (M9) | PASS |
| 11 | signals | PASS (M10) | **FAIL** (B1) | PASS (M12) | **FAIL** (B2) | **FAIL** (B1, B2) | PASS |

### Numbers traced

- **Fig 1.** `data/REPORT.md` Coverage (C0 7, C1 136, C2 204; 71 students). `wildchat/REPORT.md` Funnel and Sample (837,989; 139,736; 1,200; 114; 35 conversations; 151 windows). 347 + 151 + 30 = 528, and 498 windows in 106 sessions. All match.
- **Fig 3.** `analysis/results/inputs/labels_final.csv`, `v12_final/window_categories.csv`, `report/narratives.md` s4 and s5, `derived/timing_nirvana.csv` and the rule table in `inference/CSE216_Writing_Codebook_v1.2.md`. NIRVANA-e41-t06: F8, D4, V0, U1, NONE_VISIBLE, C2, R09, strong; 6.5 s, 4,681 pasted. NIRVANA-e24-t01: F4, D3, V0, U3, NONE_VISIBLE, C2, R08, moderate; 1,271 typed, 334 pasted, 576.7 s. Codes, rules and numbers match. The wording of the observation does not (B5).
- **Fig 4.** `patterns.md` s1, recomputed from labels: D1 F5 68 and 46 OFF; D2 U7 52 and 37 AUG; V3 13 OFF; D3 46 and 37 OFF; D2 V1 U4 30 and 21 SLb; D4 V0 U1 32 and 30 SLb; D2 F4 U4/U5 72 and 69 surrender-leaning. Counts match. Positions are labeled schematic in the caption.
- **Fig 5.** `mining.md` s5 and `out_of_sample.md` s3 and s7c. All match.
- **Fig 6.** `mining.md` s1 and s8 and `mining/archetypes.csv`. All means, shares, dataset counts and medians match. The session e70 sequence matches `report/narratives.md` s1.
- **Fig 7.** `mining.md` s5 and s7. All dwell, typed and count values match. Recomputed medians match.
- **Fig 8.** `mining/outcome_sessions.csv` (71 rows) and `mining.json`. Recomputed rho 0.603, 0.191, -0.546.
- **Fig 9.** `mining.md` s5 and `mining.json`. Bars match. Recomputed scatter is 65 points, rho 0.401.
- **Fig 10.** `mining.md` s7 and s10 and `derived/timing_nirvana.csv`. Medians recomputed: 44.0, 65.4, 173.8, 126.35 and 26.4, 15.5, 10.3, 22.7. Right panel matches.
- **Fig 11.** `mining.md` s9 and s10. Fired counts, percentages and rho values match. The definition of precision does not (B1). The top panel is labeled schematic on the axis and in the caption.

### Claims and numbers lost when tables were removed (`git show 07e948d:Final_Project/paper/main.tex`)

| Removed table | Lost | Needed? |
|---|---|---|
| `tab:triggers` | The caption's statement that precision and recall use windows with a surrender or support category | **Yes. The new caption states the opposite (B1)** |
| `tab:triggers` | "Fires when" for Quick return (60 s, under 50 typed). Paste, then straight back is new and has never had a definition in the paper | **Yes (B2)** |
| `tab:triggers` | Third-decimal precision and recall (for example 0.327, 0.587) | No. Rounded values remain, and the paper's headline values are in the prose |
| `tab:data` | WildChat coverage C0 32, C1 119; earlier sample's 11 conversations; "Turns 1 to 10" | Not for a claim, but the figure prints coverage for NIRVANA only (M2) |
| `tab:framework` | Rule to category to grounding at a glance, including the indeterminate row | No claim is lost, because the appendix rule table and Section 3.5 keep it. Section 4.3's pointer is now overstated (M4) |
| `tab:categories` | Support totals 150 and 25, neutral or indeterminate totals 99 and 57 | No. They are sums of what Fig 5 shows, apart from M6 |
| `tab:archetypes` | "1.7 switches" for long working sessions | No |
| `tab:paste` | "about half or more" in the D4 label | No. Defined in the appendix |

No other number was lost. A script compared every number in the old body against the new body plus figure text.

## 3. Blocking problems

**B1. Fig 11 defines precision wrongly, and the base rate has no stated denominator.** The caption says precision is "the share of fired windows that are surrender-leaning". `mine.py` (`log_triggers`, column `SL_among_fired_determinate`) divides by fired windows with a surrender or support category only. By the caption's definition the values would be 58.2% (32 of 55), 43.6% (44 of 101) and 44.3% (62 of 140), not 64, 59 and 56. The base rate has the same hidden denominator: 39.5% is 98 of 248, while 98 of 347 is 28.2%. The removed table stated this correctly.
Fix: replace that caption sentence with "Precision is the share of fired windows with a surrender or support category that are surrender-leaning, against a base rate of 39.5\% on the same windows (98 of 248); recall is the share of all surrender-leaning windows caught, both by the AI-coded labels." In Section 4.7 change "with precision 55.9\%" to "with precision 55.9\% among fired windows that have a surrender or support category". Add the same phrase in Section 7.3 after "Precision of 56\%".

**B2. Fig 11 shows two rules the paper no longer defines.** Quick return and Paste, then straight back have bars, and the prose relies on them ("Speed alone does not qualify"), but no thresholds appear anywhere in the body.
Fix: add to the Fig 11 caption "Quick return: next request within 60 s of the response, with under 50 characters typed. Paste, then straight back: 200 or more characters pasted and the next request within 90 s." (`mining.md` s9).

**B3. Fig 1 attributes AI and script output to the dataset authors.** The figure's stated purpose is "who or what did each step", and the caption and legend say plain boxes are the dataset authors' work. "528 request windows" and "Final codes" are plain boxes. The authors made neither, and "Final codes" is AI adjudicator output, in a paper whose central disclosure is that no human coded.
Fix in `make_figures.py`: line 100 use `fc=SCRIPT_FILL`; line 111 use `box(ax, 2.4, y, 1.2, 0.28, "Final codes", fc="white", ls="--")`.

**B4. Fig 1 caption reads as if the capped conversations were excluded.** "Three WildChat conversations are capped at ten turns, and the 30 earlier windows are incomplete, so they stay out of every session measure." The 3 capped conversations are in the 106 sessions (`truncated_session` is set on 3 of them; the abstract also counts them).
Fix: "Three WildChat conversations are capped at ten turns and remain in the session measures; the 30 earlier windows are incomplete and stay out of every session measure."

**B5. Fig 3 places "A short note is in the editor" beside the code "none visible".** The appendix defines notes and fragments as `VISIBLE PARTIAL`, so the example appears to show a coding error in the figure meant to teach coding. The narrative explains it: the note became the request, and the codes are right. That explanation was dropped.
Fix, line 179 text: `"The only text in the editor becomes the\nrequest. The writer copies one AI sentence,\nchanges its ending and types a paragraph:\n1,271 characters typed, 334 pasted, 577 s."`

**B6. Fig 4 hatching misstates the largest box, and two boxes count the same windows.** The caption says hatching marks request-only, and the hatched box reads "69 surrender-leaning". Only 48 of those are request-only (R16); 21 are R15, behavior-based. Those same 21 windows are also the 21 in the adjacent "Surface-only iteration" box (22 windows are in both signatures). A reader adding boxes double counts.
Fix: line 218 label `"Draft requested, kept in chat\n(D2 F4 U4/U5) 72 windows:\n48 request-only, 21 behavior"`. Add to the caption "A window can match more than one signature: 22 windows are in both surface-only iteration and draft requested." Update `\Description` to match.

**B7. Fig 4 draws neutral-mechanical inside the Support side.** The box says "outside both axes" and the `\Description` says it "sits apart", but it sits on the blue support shading. Neutral-mechanical is excluded from support everywhere else in the paper.
Fix: delete line 202 (the lower-left blue rectangle) so that corner is unshaded. Move "Writer's text reworded" to y = 2.02 in line 212 so it sits wholly in the blue area. Change the `\Description` to "Upper areas are the support side..." and "Neutral-mechanical sits in an unshaded corner, outside both axes."

**B8. Figs 5 and 6 do not separate behavior-based surrender from neutral-mechanical in greyscale.** The L* gap is 7.8. On the greyscale pages the legend swatches and tiles look the same: Fig 6's One-shot paste panel reads as seven identical tiles, although 2 are neutral and 5 are surrender-leaning, and Fig 5's 69 and 48 segments match. This is the paper's key category against a non-finding.
Fix: `HATCH = {"SLr": "////", "NEU": "xxxx"}` at line 27. All tile, bar and legend code already reads `HATCH`, and the white edge color makes the hatch visible. Check the text box on the Fig 5 "48" and "5" labels after rebuilding.

**B9. The AI Use Statement is stale, and it says it is meant to be complete.** The section is unchanged from before commit 8c492e9. That commit replaced six tables and added diagrams (197 changed lines in `main.tex`). The Editing row ends with the critic's minor corrections "applied afterward and not rechecked", which implies those were the last edits. The Analysis row credits figures to "Byte-identical reruns and skeptic agents", but no skeptic reviewed the new figures.
Fix: add a row: `Figures & Redrew the figures in one palette, replaced six tables with figures and added explanatory diagrams, using Opus 5.5 & Scripted rerun, palette and text-overlap checks, and a fresh figure critic; corrections made after that critic were not rechecked \\`. Adjust the last clause if a recheck is run. In the Analysis row, change "made the figures" to "made the first versions of the figures".

## 4. Minor problems

**M1. Fig 9 caption does not stand alone.** It does not define support share, "unseen", or which sessions are shown. The bars show 65 of 71 NIRVANA and 31 of 35 WildChat sessions. Support share here is over surrender and support windows only, unlike `support_share` in `outcome_sessions.csv`.
Fix: add "Support share is offloading and augmenting windows as a share of a session's windows with a surrender or support category; sessions with none, and one WildChat session whose first-window field is unsettled, are not shown. Unseen means a chat-only first window with no writer text."

**M2. Fig 1 prints coverage only for NIRVANA.**
Fix: change the WildChat box to "35 whole conversations, 151 windows (C0 32, C1 119),\nplus 30 windows from an earlier sample".

**M3. Fig 4 neutral box says "(D0) ... 53 windows".** There are 57 D0 windows, of which 53 are neutral-mechanical.
Fix: "No substantive decision\n(D0), 57 windows, 53 neutral-\nmechanical, outside both axes".

**M4. Indeterminate is missing from Fig 4, and Section 4.3 overstates the figure.** The caption says "Concept map of the categories", but 103 whole-session windows are indeterminate, and Section 4.3 says categories are "defined in Section 3.5 and Figure 4".
Fix: Section 4.3 "defined in Section 3.5 and Appendix A and placed in Figure 4". Add to the caption "Indeterminate windows have no position on these axes."

**M5. Fig 4 vertical axis has no pole labels, and the side boundary almost disappears in greyscale.**
Fix: add "yes" and "no" at the ends of the axis, and draw a dashed `INK2` outline around the surrender-leaning rectangle.

**M6. Fig 5 x-label says "with counts", but WildChat's 2 and 3 are unlabeled.**
Fix: add to the caption "Unlabeled WildChat segments are behavior-based, 2, and augmenting, 3."

**M7. Fig 7 window counts are not the counts behind the medians.** Dwell exists for 21 of 42, 23 of 32 and 20 of 29 windows. First-copy ticks use a different population from the bars. The same-population medians are 17.15, 17.85 and 8.8 s.
Fix: add to the caption "Dwell uses the 21, 23 and 20 windows that have a next request." Preferably draw first-copy ticks from the paste windows, and add those medians to `mining.md`.

**M8. Fig 8 hides points.** 21 of 71 sessions sit at exactly (0, 0) in the left panel, and 58 of 71 sessions have request-only share 0 in the middle panel, so the 0.19 rests on 13 non-zero x values.
Fix: size markers by count at each location, and add the 13 to the caption.

**M9. Section 4.6 cites Fig 10 after claims it does not show (every fifth of a session, 13 of 17 sessions).**
Fix: move the reference to the sentence "The gap is typing time."

**M10. Fig 11, a T4 result, floats into the middle of the Section 5 Barriers text on page 14.**
Fix: move its source before the T4 heading, or add `\usepackage{placeins}` and `\FloatBarrier` before Section 5, then recheck pages.

**M11. Fig 2 caption says "a chat-only log (C1)".** NIRVANA's 136 C1 windows come from a logged editor, with no editor action in that window.
Fix: "a chat-only window (C1)".

**M12. Category colors are reused for non-categories.** Fig 1's "Category, strength" box uses IND grey, Fig 11's signal markers and boxes use SLb orange although signals are not a category, and `#444444` in Figs 9 and 11 is close to NEU.
Fix: use `SCRIPT_FILL` in Fig 1, `INK` for the Fig 11 signals, and `#222222` for the dark bars.

**M13. `check_palette.py` always exits 0.**
Fix: exit 1 when the smallest unhatched L* gap is under 15, or when any CVD delta is under 10.

**M14. Fig 6 panels use different x ranges (4 to about 27), so tile width varies roughly tenfold, and One-shot paste is mostly empty.**
Fix: add "Panels use different horizontal scales." to the caption.

**M15. Fig 10's median labels 174 and 44 sit over dots.**
Fix: draw the labels to the right of the strip, at `i + 0.42` with `ha="left"`.

**M16. Many figure numbers are typed into `make_figures.py`, not read from results** (`ARCH_DESC`, `fig_concept`, `fig_after`, the right panel of `fig_dwell`, `fig_signals`, and the `else 65` fallback). All match today, but Section 3.7 says each stage's numbers rerun from saved labels.
Fix: read them from `mining.json` and `patterns.md`, or add to Section 3.7 "Numbers in the schematic figures and some labels are typed from the results files."

## 5. What passes

All figure references resolve and appear in numeric order of first mention, and every figure has a `\Description`. Apart from B6 and B7 the descriptions are accurate. The schematic parts of Figs 4 and 11 are labeled. Figures replace tables without losing a number that a claim needs, apart from B1 and B2. Thesis-to-visual coverage is complete.
