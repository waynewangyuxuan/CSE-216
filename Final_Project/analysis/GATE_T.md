# Gate check of M2_draft.md (Bet 9, theses rebuild)

**Overall verdict: FAIL** on check 1 only: four numbers or labels don't match their sources, plus small overreaches. Checks 2–4 and the honesty statements PASS. Every fix is a wording or citation change.

## 1. Claim tracing: FAIL

Almost every number in §1, §4, §7, §8, §9 and §10 matches mining.md, out_of_sample.md, patterns.md, sensitivity.md or lit/framework_comparison.md exactly or after rounding. That covers the archetype table, the paste-by-decision table, the outcome ρ values, stage shares, the lagged model, the triggers, the R99 gaps, the 16/20 UNSETTLED windows, the 48/96 R16-U8 windows and the e41 narrative figures. These do not:

- **§7.3 "Switching": the "In NIRVANA" label is wrong.** mining §3 pools both datasets. I recomputed with `mine.load()` (scratch code, nothing written). WildChat windows add 1 switch and 8 stays to the "leave" cells and 14 pairs to the "enter, draft/notes" cells. NIRVANA alone gives: leave 9/17 with a draft, 14/34 with notes, 4/21 with nothing visible; enter 16/41 with notes, 10/59 with a draft. THESES C12 has the same error. SKEPTIC_T C12 asked for "Say NIRVANA" and did not check the pooling.
- **§7.4 "The copy is not faster": p 0.62 belongs to a different contrast.** In mining §7, p 0.6157 is SLb vs **support** (support median 10.35 s). The draft pairs it with offloading (10.3 s), and no SLb-vs-OFF test exists. THESES C17 has the same error.
- **§7.4 "Dwell": "The gap appears in every position bin"** is in no results file (not mining §7 or §10). It comes only from SKEPTIC_T C15's scratch recompute.
- **"no V4" / "0 `V4`"** (§7.0, §10) cannot be traced to a results file. patterns.md §1 reports V3 and V4 together (13). V4 = 0 appears only in SKEPTIC_T.

Overreach, or wording that says more than the number:

- **§8 RQ3, last paragraph:** "WildChat sessions in them rarely come back (2 of 21)". The 2 of 21 counts every WildChat session that turns surrender-leaning (mining §6), not the sessions that contain runs of generation follow-ups.
- **§1 T2:** "Sessions that start from it stay on the support side". 7 of the 18 NIRVANA sessions that open on a draft have a surrender-leaning window; the number shows a mean support share of 0.77 vs 0.50.
- **§1 T2:** "In WildChat, where no editor exists, 2 of 21…" credits the editor for the low return rate. SKEPTIC_T C13 dropped that credit because the datasets differ in many ways.
- **§1 T1:** the paste shares (66%/64%), the 6 chars / 71 s and 305 / 288 s medians, and the ρ values are NIRVANA-only, but §1 frames them as covering 106 sessions. §10 says so; §1 does not.

Consistency: the draft follows THESES.md T1–T4 and takes in the skeptic's rewordings (C3 "only weakly", C5 definitional caveat, C7 "most commonly", T2 "strongest predictor" dropped, T3 restated around typing, T4 cut to two log events, C23 not used as a trigger). Between-session caveats are in §10. Apart from the C12/C13 points above, nothing contradicts SKEPTIC_T.

Minor, not required: the §7.1 table shows "–" for Unresolved median GPT Final %, but mining §8 has 0.0 (n = 6).

## 2. Byte-identical reruns: PASS

`run_all.sh` exited 0. The 57 files under results/, figures/ and derived/ hash identically before and after (diff empty). The log shows: frozen ok (both hashes), check_outputs ok (19 result files, 25 figures), check_no_text ok, run_all: ok. `git status --short Final_Project` showed nothing after the run.

## 3. Frozen v1.2 unchanged: PASS

- `apply_rules.py` sha256 95ca3316…46ac1 and `CSE216_Writing_Codebook_v1.2.md` sha256 de6663da…6b5f both match FROZEN.md (freeze 2).
- `git log 0d1b3d3..HEAD -- Final_Project/inference` is empty.

## 4. No dataset text: PASS

- check_no_text: 53 files checked against 499 source files, no shared 8-word run.
- narratives.md §4 (e41) and §5 (e24) paraphrase what happened. Nothing in quotation marks is dataset content.
- The draft quotes only the proposal ("I remain the primary coder"), literature phrases (cognitive surrender, LLM fallacy, Maier's support levels), code names and its own label "asked the AI to write it".
- derived/*.csv: outcome_nirvana (71 rows), timing_nirvana (347) and timing_wildchat (151) hold only ids (window_id, session_id) and numeric columns. Every non-id value parses as a number. There are no demographic columns: outcome holds essay %, word counts, time, ownership and self-efficacy.

## Honesty statements: PASS

All present:

- No human coded anything (§1, §10).
- All agreement is AI-to-AI, including the Fable gold set (§2, §6, §10).
- The reversal of "I remain the primary coder" (§2, §10).
- Scope adapted to formal long-form writing (§2, §10).
- Categories are not calibrated probabilities (§1, §2, §10).
- `NEUTRAL_MECHANICAL` has no source (§5.3, §10).
- V2–V4 essentially absent (§10).
- Adjudicator lean 25:13, 159:45, 54:17 (§6, §10).
- WildChat surrender-leaning is mostly "asked the AI to write it", 67/69 (§7.0, §10).
- Related schemes credited (§3).

## Required fixes

1. **§7.3, "Switching" bullet:** replace "In NIRVANA" with "Across both datasets" and keep the counts. Alternatively, keep "In NIRVANA" with the NIRVANA-only counts (9/17, 14/34, 4/21; 16/41, 10/59), but only after `mine.py` prints them. Fix THESES C12 to match.
2. **§7.4, "The copy is not faster":** write "15.5 s for behavior-based surrender and 10.35 s for support windows (p 0.62)", or keep offloading 10.3 s and drop the p-value. Fix THESES C17 to match.
3. **§7.4, "Dwell":** delete "The gap appears in every position bin", or add a dwell-by-position-bin table to `mine.py` §10 and cite it.
4. **§7.0 "(`V3`, no `V4`)" and §10 "0 `V4`":** have `patterns.py` report V3 and V4 separately, or cite SKEPTIC_T.md C17 for V4 = 0.
5. **§8 RQ3, last sentence:** change "WildChat sessions in them rarely come back (2 of 21)" to "WildChat sessions that turn surrender-leaning rarely come back (2 of 21)".
6. **§1 T2, first sentence:** change "stay on the support side" to "lean to the support side (mean support share 0.77 with a draft vs 0.50 with nothing visible)".
7. **§1 T2, last sentence:** change "In WildChat, where no editor exists," to "In WildChat (chat only),".
8. **§1 T1, third sentence:** start it with "In NIRVANA, writers paste…".
