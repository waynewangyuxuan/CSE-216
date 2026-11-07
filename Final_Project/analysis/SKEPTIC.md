# Skeptic review of Bet 8 findings

I tried to refute each of F1–F13 in `FINDINGS.md`, using only codes, ids and numbers: committed results, the scripts, and my own recomputations. My scripts are in `analysis/blind/skeptic/` (git-excluded) and run with `analysis/.venv/bin/python`:

- `recompute.py`: shares by dataset, R09 positions, session types, escalation shuffle, coder A/B disagreements, out-of-sample coverage, IND-removed shuffle
- `ind_placement.py`: where `INDETERMINATE` windows sit, and the shuffle test with them removed
- `position_bins.py`: position shares with centred bins and without R16
- `drift.py`: mean relative position of SL and support windows against a within-session shuffle

Every number in the findings table that I recomputed matches the scripts' output. The problems are in interpretation, not arithmetic. A caveat that applies to all 13 findings: every code, category and check here comes from AI readers. "Robust" below means robust across AI coders and rule variants, never validated by a person.

**Tally: 0 SURVIVES, 10 SURVIVES WITH COUNTERPOINT, 3 REFUTED as written (F5, F6, F8).**

---

## F1. Out-of-sample coverage 78.5%
**Verdict: SURVIVES WITH COUNTERPOINT**

- **Strongest refutation tried:** coverage depends on a single rule and says nothing about validity.
- **Evidence:**
  - Recomputed 336/428. 
  - With R16 treated as indeterminate, whole-session coverage falls from 79.3% to 60.0% (`results/sensitivity.md`). R16 is request type alone.
  - WildChat out of sample is 65.6%, below its in-sample 70.0% (21/30). Of its 52 IND windows, 25 are R03 (no next action seen, mostly the last turn of a chat).
  - The C0 13.6% and C2 93.6% figures are over all 528 windows, not the 428 new ones. Out of sample alone they are C0 4/36 (11.1%) and C2 159/169 (94.1%) (`recompute.py`).
- **Counterpoint to state:** "Coverage counts any non-indeterminate label, not a correct one; no human checked any category. Without R16 (request type only), coverage is 60%. WildChat coverage fell out of sample (70% to 66%). The C0/C2 shares are over all 528 windows."

## F2. A third surrender-leaning, a third support
**Verdict: SURVIVES WITH COUNTERPOINT**

- **Strongest refutation tried:** the pooled shares are a blend of two very different datasets.
- **Evidence (`recompute.py`):**
  - NIRVANA: SL 98/347 (28.2%), support 150/347 (43.2%).
  - WildChat: SL 69/151 (45.7%), support 25/151 (16.6%).
  - "A third / a third" holds in neither dataset.
  - Weighting each session equally instead of each window: SL 31.3%, support 36.4%.
  - The weak share mixes denominators: 112/182 is over all 528 windows. Over whole sessions it is 97/167 (58%).
  - Half of the whole-session R16 windows (48/96) are `U8`: the writer asked for text and then ignored it. Those count as surrender-leaning.
- **Counterpoint to state:** "The pooled one-third/one-third split is a dataset mix: NIRVANA 28% SL / 43% support, WildChat 46% / 17%. Whole-session weak SL is 97 of 167. Half of R16's surrender-leaning windows are ones where the writer moved on without using the output."

## F3. Strong surrender-leaning is rare: 15 windows, all NIRVANA
**Verdict: SURVIVES WITH COUNTERPOINT**

- **Strongest refutation tried:** "rare" and "all NIRVANA" follow from how the rule is built, not from behavior.
- **Evidence:**
  - R09 needs C2 (editor visible), so it cannot fire in WildChat by construction.
  - R09 also needs `NONE_VISIBLE`. The same behavior (`D4`, no check, `U1`/`U2`) appears in 45 whole-session windows. 30 of them have visible own work (19 partial, 11 draft) and become R11 moderate (`recompute.py`).
  - 7 of the 15 R09 windows are window 1 of their session, and 4 are single-window sessions.
  - 2 of the 15 (e05-t01, e05-t02) carry Bet 4 labels coded from 3-turn views.
  - Coder B alone gives 14 strong windows, coder A 15.
- **Counterpoint to state:** "'All NIRVANA' holds by construction: R09 needs the editor. Wholesale unchecked pasting of AI text is 45 windows. Only the 15 with no own work visible are rated strong, and these sit mostly at session start."

## F4. Session types 34 / 23 / 40 / 9
**Verdict: SURVIVES WITH COUNTERPOINT**

- **Strongest refutation tried:** the types track session length and a single rule.
- **Evidence (`recompute.py`):**
  - Mixed sessions average 9.3 windows. SL-only sessions average 4.0, support-only 3.3, and none-type 1.7.
  - 11 single-window sessions cannot be mixed.
  - With R16 treated as indeterminate, SL-only falls from 34 to 17 and "none" rises from 9 to 26.
  - WildChat supplies 19 of the 34 SL-only sessions.
  - Under coder A alone the counts are 37/22/40/7, and under coder B alone 34/27/40/5. This part is stable.
- **Counterpoint to state:** "Session type largely reflects session length (mixed sessions average 9.3 windows, single-type ones 3–4) and R16. Without R16, SL-only halves to 17. Types are a description of make-up, not kinds of writer."

## F5. SL→SL persistence: pooled p 0.045, WildChat p 0.001
**Verdict: REFUTED as written (the pooled and WildChat order claims)**

- **Strongest refutation tried:** the shuffle null moves `INDETERMINATE` windows, which mostly sit at session ends.
- **Evidence:**
  - In WildChat, 30 of 52 IND windows are the last window of their session; 25 of those are R03 (no next action) (`ind_placement.py`). Shuffling moves these into the middle of SL runs, which deflates the shuffled count.
  - With IND removed before shuffling (already computed in `results/sessions.json` under `perm_test_excl_ind` but not reported), persistence disappears everywhere:
    - Pooled SL→SL: 88 vs 89.2, p 0.73.
    - NIRVANA: 43 vs 43.6, p 0.68.
    - WildChat: 45 vs 45.5, p 0.84.
  - WildChat OFF→OFF (p 0.037 in `fig05`) becomes 8 vs 7.9, p 0.73.
  - The pooled p 0.045 is one of 21 uncorrected tests (7 pairs × 3 sets). It already rises above 0.05 under the UNSETTLED, truncation and auditor variants (`results/sensitivity.md`).
- **What the report may say instead:** "SL→SL is the commonest transition because SL-heavy sessions have many SL windows. Once indeterminate windows (often the closing turn) are set aside, no dataset shows more persistence than a within-session shuffle (pooled 88 vs 89.2)." Drop the p 0.045 and p 0.001 claims.

## F6. Symmetric switching, 29 each way; no drift toward surrender
**Verdict: REFUTED as written (the "no drift" clause and the reading of symmetry as evidence)**

- **Strongest refutations tried:** the symmetry is arithmetic, and a direct drift test.
- **Evidence (`recompute.py`, `drift.py`):**
  - **The symmetry is close to arithmetic.** After IND and NEU windows are dropped, each session's SL→support count minus its support→SL count is +1, −1 or 0, set only by its first and last state. 29 = 29 is the same fact as "6 mixed sessions run SL…support and 6 run support…SL".
  - **"In 23 sessions" is tautological.** It equals the number of sessions with both SL and support.
  - **One session carries a large share.** One session contributes 10 of the 58 switches.
  - **The direct drift test finds drift.** NIRVANA SL windows not from R16 sit later in the session than a within-session shuffle predicts: mean relative position 0.577, p 0.013, n 64.
  - **Pooled SL looks "earlier" only because of WildChat.** WildChat's R16 windows open sessions and its IND windows close them.
  - **Possible artifact in the drift itself.** R11 (paste with visible own work) can only fire once own work exists, so part of the late shift may come from the rules. Still, the report cannot say no drift is visible.
- **What the report may say instead:** "Equal switch counts follow from 6 mixed sessions starting SL and ending support, and 6 the reverse. Behavior-based surrender-leaning (not R16) occurs later in NIRVANA sessions than chance (p 0.013, uncorrected), possibly partly because R11 needs visible own work."

## F7. 19/50 SL sessions later reach support (NIRVANA 17/29, WildChat 2/21)
**Verdict: SURVIVES WITH COUNTERPOINT**

- **Strongest refutation tried:** coverage and rule structure explain the dataset gap, and the pooled figure mixes the two.
- **Evidence:**
  - WildChat can produce support: it has 25 support windows, via R13 18, R14 4 and R18 3 (`recompute.py`).
  - So the gap is not only missing U3/U7. In WildChat the first SL is always R16 at the opening request (17/17). Follow-up chat iteration on that AI draft is coded `D2 F4 U4` and returns to R16 again.
  - Of 86 windows after the first SL in WildChat, 48 are SL and 28 are IND.
  - Variant range: 15/43 with Bet 4 labels dropped; 17/52 under coder A, 21/52 under coder B.
- **Counterpoint to state:** "Don't headline the pooled 38%: it averages 59% and 10%. The WildChat figure is low partly because the rules read every chat follow-up on an AI draft as R16 surrender, and partly because the editor is missing, not only because writers stay. WildChat can produce support (25 windows via R13/R14/R18)."

## F8. SL starts at window 1; its share falls across the session
**Verdict: REFUTED as written (the "share falls" sentence); the first-window count survives with a counterpoint**

- **Strongest refutations tried:** single-rule and dataset-mix artifacts, plus a binning bug.
- **Evidence (`position_bins.py`, `drift.py`, `recompute.py`):**
  - **The decline is R16 in WildChat.** Without R16, pooled SL share rises across the five bins: 11, 12, 16, 17, 19%.
  - **NIRVANA is flat.** Its SL share by bin is 29, 30, 31, 28, 28%.
  - **WildChat's fall is two artifacts.** It runs from 63% to 33%: R16 opening requests at the start, and R03 IND closing turns at the end (30 of 35 sessions end on IND).
  - **The binning is biased.** `sessions.py` uses `int(5*i/n)`, so the last window of a 3- or 4-window session never lands in the last fifth (bin sizes 103/88/82/88/58). With centred bins, NIRVANA SL is 31, 26, 28, 28, 33%, higher at the end.
  - **The first-window count holds, but it is R16.** 33/52 is correct. All 17 WildChat cases are R16, and 7 of 16 NIRVANA cases are R16.
  - **NIRVANA window 1 is structurally different.** 33/71 NIRVANA first windows have `NONE_VISIBLE`, against 27/276 later windows, and R09 needs `NONE_VISIBLE`.
- **What the report may say instead:** "When present, SL often appears at window 1, almost always because the opening request asks the AI to write (R16). There is no decline across NIRVANA sessions. The pooled decline in `fig06` comes from WildChat R16 openings and indeterminate closing turns."

## F9. D1→D4 "escalation" in 6 NIRVANA sessions; WildChat has no D4
**Verdict: SURVIVES WITH COUNTERPOINT (the counts are right; "escalation" overclaims)**

- **Strongest refutation tried:** check whether D1-then-D4 ordering beats chance.
- **Evidence (`recompute.py`):**
  - Shuffling each session's D codes 2,000 times gives a mean of 6.93 sessions with D1-then-D4, p(≥6) = 0.87. The reverse order (D4, later D1) occurs in 7 sessions.
  - 10 sessions contain both D1 and D4.
  - Coder B alone gives 5 escalation sessions.
  - WildChat's zero D4 (also 0 under coder A and under coder B) is mostly coverage. One of D4's two routes is verbatim reuse in the editor (D4 definition, `inference/CSE216_Writing_Codebook_v1.2.md` decision table), which WildChat cannot show.
- **Counterpoint to state:** "Six sessions have a D1 window later followed by D4. This is no more than a within-session shuffle gives (6.9), and the reverse order occurs in 7 sessions, so it is not evidence of escalation. WildChat's lack of D4 reflects the missing editor."

## F10. Signatures map to categories consistently, except U8
**Verdict: SURVIVES WITH COUNTERPOINT**

- **Strongest refutation tried:** the mapping is definitional.
- **Evidence:**
  - Signatures are code combinations, and the rules are code combinations (`apply_rules.py`).
  - "Draft kept in chat" (`D2 F4 U4/U5`) is R15 or R16 by definition whenever V is V0, V1 or V2. Its 3 exceptions are R00 and R04.
  - "Whole paste" is R09 or R11 by definition; its 2 AUG windows are R10.
  - The table checks the rule table against itself, not behavior.
- **Counterpoint to state:** "This consistency is a property of the frozen rule table, not an empirical regularity. The only informative row is U8, where the rules label 'asked for text, then ignored it' as surrender-leaning (R16)."

## F11. Reasoned checks rare: 13 windows, 6 sessions, all NIRVANA
**Verdict: SURVIVES WITH COUNTERPOINT**

- **Strongest refutation tried:** coder dependence, clustering and truncation.
- **Evidence (`recompute.py`):**
  - V3/V4: coder A 13, coder B 16. V2: A 8, B 4, final 5. "Rare" holds.
  - The 13 windows are concentrated in 6 sessions.
  - WildChat is chat-only and capped at 10 turns, and source comparison is easier to see with an editor.
  - In sample, R04 never fired (`inference/REPORT.md` §5).
- **Counterpoint to state:** "Thirteen windows from 6 sessions: a handful of writers, not a rate. 'All NIRVANA' may partly reflect WildChat's chat-only, 10-turn view."

## F12. Categories do not hinge on the adjudicator
**Verdict: SURVIVES WITH COUNTERPOINT**

- **Strongest refutation tried:** look only at the windows where the coders disagree.
- **Evidence (`recompute.py`):**
  - A and B categories differ on 57 windows. On those, the final category matches A in 44, B in 12, and neither in 1.
  - That 44:12 is the same lean seen in Bets 4, 6 and 7.
  - On 13 further windows A and B agree, but final differs from both.
  - Whole-session SL count: A 177, B 167, final 167. The SL total is stable within about 10 windows.
  - κ 0.86 is agreement between two AI models (one the adjudicator's own model), not validity. WildChat's 96.7% agreement is high partly because both coders apply R16 to the request type.
- **Counterpoint to state:** "Aggregate counts are stable across coders (SL 177 A / 167 B / 167 final, whole sessions). Where the coders' categories differ, the final follows A, the adjudicator's own model, 44 to 12. Agreement is between AI coders and is not validation."

## F13. 20 UNSETTLED windows; 6 could be SL
**Verdict: SURVIVES WITH COUNTERPOINT**

- **Strongest refutation tried:** "could be" understates the case.
- **Evidence (`results/out_of_sample.md` §5):**
  - 4 windows are SL under every value of the unsettled field (WILDCHAT-14140e33cb98-t01, e6acb3ce8d84-t01, f6837354bd04-t03, f6837354bd04-t04). Their unsettled field is `prior_own_work`, which R16 does not read.
  - 5 more are OFF under every value, and 2 are NEU under every value.
  - So R00 discards 11 windows whose category does not depend on the unsettled field.
  - Adding the 6 possible SL windows moves whole-session SL from 167 to at most 173 (34.7%). The "under 2 points" claim holds.
- **Counterpoint to state:** "4 of the 6 are SL under every reading, and 11 of the 20 get the same category whatever the unsettled value. R00 is stricter than needed, which lowers coverage, but the shares move by under 2 points."

---

## Other problems found

1. **`fig05` and the `sessions.md` shuffle table report only the IND-kept test.** The IND-removed test, already computed in `sessions.json` as `perm_test_excl_ind`, shows no persistence anywhere. The figure's title ("Is surrender sticky beyond session make-up?") and its p 0.001 and p 0.037 WildChat dots mislead. The figure should show the IND-removed test, or both.
2. **`sessions.py` position bins are biased.** `int(5*i/n)` never puts the last window of a 3- or 4-window session in the last fifth, which leaves the last bin smaller (58 against 82–103). Use `min(4, int(5*(i+0.5)/n))`.
3. **`fig06` is misleading in two ways.** It pools the two datasets, so its visible SL decline is WildChat's R16 openings and R03 closing turns. Its stacked segments are also each drawn 0.3 points short (`v - 0.3`), so the bars do not reach 100%. Show it per dataset.
4. **Per-dataset contrasts are made without correction.** p-values for 21 shuffle tests are printed without correction. No test accounts for clustering beyond the within-session shuffle. Pooled percentages in F2, F7 and F8 are each dominated by one dataset; report them per dataset.
5. **Denominators are mixed.** F1 (C0/C2 over all 528) and F2 (weak 112/182 over all 528) mix the 528-window set with the 428 out-of-sample or 498 whole-session sets.
6. **Two rules raise face-validity questions the report should state.**
   - R16 labels `U8` (asked, then ignored the output) as surrender-leaning. That is 48 of the 96 whole-session R16 windows.
   - R00 sends windows to IND even when the unsettled field cannot change the rule that fires (the 11 windows in F13).

---

*Correction added by the main session after the gate review:* in F3, the 30 unchecked pastes with visible own work are R11 28 and R10 2 (`results/out_of_sample.md` §7d), not all R11; the 2 R10 windows are augmenting. The report states the corrected split.
