# Coding run report (Bet 4)

Numbers come from `scripts/run_all.sh`, which replays saved labels and calls no model.

**Every number here is AI-to-AI consistency.** Two or three models can share a bias. No human coded anything. The Fable comparison is a third AI check. It is not human, expert or gold-standard validation. Nothing here validates claims about cognition. No window has an offloading or surrender label.

## Bottom line

- **All 100 windows are coded** by Coders A and B, with final labels. 99 windows have a final code in every field. 1 field stays `UNSETTLED`.
- **The coders agree closely.** `decision` κ 0.94, `verification` 0.82, `uptake` 0.92.
- **No stop condition was hit.** The lowest Q3–Q5 κ between coders is 0.66 (`verification` on C1). Against Fable on all 20 windows, the lowest is 0.81 for final labels (0.78 on follow-ups) and 0.75 for a single coder (B on `uptake`), or 0.71 on follow-up windows.
- **Coders saw only the last 3 earlier turns.** 18 windows have older turns nobody read, and 10 of those reuse text from an unseen AI response. Fable shared this limit, so all three can miss the same thing. One ruling is affected (`NIRVANA-e58-t10`).
- **Truncation mattered on one gold window.** The standard page hid a paste on `NIRVANA-e27-t02`. Fable coded it `U7`, and both coders, with full text, coded `U3`.
- **Checks are nearly absent.** Final labels hold 0 `V2`, 0 `V3`, 0 `V4`. So κ on `verification` says nothing about grading the grounds of a check.
- **WildChat's research-writing screen is in doubt.** Fable said no on 2 of 6 gold windows. A, B and final labels called all 6 `RESEARCH_EXPLICIT`.

## Who coded

| Role | Requested | Served (from transcripts) | Runs |
|---|---|---|---|
| Coder A | `opus` | `claude-opus-5-5` | 5 fresh agents, one per batch |
| Coder B | `sonnet` | `claude-sonnet-5-5` | 5 fresh agents, one per batch |
| Adjudicator | `opus` | `claude-opus-5-5` | 1 fresh agent |

Batches hold 16 to 23 windows and 145 to 148 KB, the size of a Bet 3 round. Sessions stay whole. Temperature cannot be set, so labels are saved, not regenerated.

## Truncation

Settled before coding (`decisions.tsv` T01–T04).

| Block | Blocks cut at the standard cap, sample | Characters cut | On the gold page |
|---|---|---|---|
| Next actions | 8 | 77,613 (largest 36,785) | 1 (14,701) |
| Response | 1 | 1 | 0 |
| Request, editor | 0 | 0 | 0 |
| Earlier turns (500-character cap) | 139 of 274 | 202,670 | 30 |

The 31 cut blocks on the gold page are the 1 next-action block plus 30 earlier-turn blocks.

**Choice.** Coders saw every request, response, editor and next-action block uncut. Earlier turns stayed cut, except an earlier AI response whose cut part this request or editor reuses. That shows 19 windows at least one earlier response whole. Coders never saw overlap numbers, as v1.1 s7 requires. Main blocks were all readable, so the script did not need to stand in for reading them. `results/access_audit.json` confirms each view's every line was returned to its coder.

**What stayed unseen: turns older than the last 3.** Views show 3 earlier exchanges, so a coder can't tell if text in the request or editor came from an older AI response. v1.1 s2 and s5 need this: pasted AI text is not own work, and content from an earlier AI turn is AI-origin. `scripts/older_turns.py` measures it. All of this also applies to the Fable page, so it doesn't show up as disagreement. No window was recoded.

| Measure | Windows |
|---|---|
| Have older turns nobody saw | 18 of 100 (3 gold) |
| Request or editor reuses a 30+ character run from an unseen AI response | 10 |

| Window | Share of request / editor from unseen AI text | `decision`, `prior_own_work` (final) |
|---|---|---|
| `NIRVANA-e58-t10` | 0.52 / 0.53 | D1 (adjudicated for B), VISIBLE_DRAFT |
| `NIRVANA-e70-t07` (gold) | 0.45 / 0.45 | D4, VISIBLE_DRAFT |
| `NIRVANA-e70-t06` | 0.00 / 0.61 | D4, VISIBLE_DRAFT |
| `NIRVANA-e70-t05` | 0.00 / 0.28 | D1, VISIBLE_DRAFT |
| `NIRVANA-e61-t07` | 0.00 / 0.28 | D2, NONE_VISIBLE |
| `NIRVANA-e26-t11` (gold) | 0.00 / 0.22 | D0, VISIBLE_DRAFT |
| `NIRVANA-e26-t09` | 0.00 / 0.15 | D2, VISIBLE_DRAFT |
| `NIRVANA-e26-t10` | 0.00 / 0.15 | D4, VISIBLE_DRAFT |
| `NIRVANA-e58-t09` | 0.07 / 0.07 | D3, VISIBLE_DRAFT |
| `NIRVANA-e58-t08` | 0.00 / 0.06 | D0, VISIBLE_DRAFT |

- **`NIRVANA-e58-t10` `decision` is undercut.** The adjudicator ruled D1 because the view did not show most of the essay coming from the AI, and because the writer did not ask for a rework. The script finds over half of it in unseen turns alone, and the first critic's own whole-session test, which has no script in this folder, found 98% of the request and all of the editor in earlier AI turns. The label stays D1, since coders and adjudicator ruled on what they could see. Bet 5 should exclude it or run both readings.
- **`NIRVANA-e61-t07` `prior_own_work` looks like an artifact.** It is NONE_VISIBLE, while `-t05` and `-t06` were ruled VISIBLE_PARTIAL on a stance in a turn that has dropped out of view.
- **`VISIBLE_DRAFT` may overcount own work, on these windows and beyond.** On `NIRVANA-e58-t09` most reuse sat in turns the coders were shown. So the list of 10 may not catch every such window.

**Effect of the 8,000-character cap on main blocks.** 7 windows could hide uptake evidence under it. Coders agreed on all 8 cut next-action windows.

| Window | Cut, of total | Matching text in the capped view, of full | `uptake` A, B, final |
|---|---|---|---|
| `NIRVANA-e27-t02` (gold) | 14,701 of 22,701 | 1,123 of 9,431 | U3, U3, U3 |
| `NIRVANA-e63-t01` | 7,182 of 15,182 | 919 of 1,229 | U3, U3, U3 |
| `NIRVANA-e19-t04` | 827 of 8,827 | 3,118 of 3,460 | U1, U1, U1 |
| `NIRVANA-e70-t06` | 555 of 8,555 | 3,181 of 3,337 | U1, U1, U1 |
| `NIRVANA-e24-t03` | 1,104 of 9,104 | 0 of 0 | U7, U7, U7 |
| `NIRVANA-e54-t02` | 9,962 of 17,962 | 0 of 0 | U7, U7, U7 |
| `NIRVANA-e71-t01` | 36,785 of 44,785 | 0 of 0 | U7, U7, U7 |

`NIRVANA-e56-t02` is also cut, with no paste or matching run in the cut part. I did not code a capped version, so the effect on these coders is not measured. The Fable page gives the only direct case (below).

## Agreement, A vs B

Two intervals: resampling windows, and resampling the 37 sessions. Bootstrap, 2,000 draws, fixed seed.

| Field | n | % | κ | κ CI, windows | κ CI, sessions |
|---|---|---|---|---|---|
| `family` (Q1) | 100 | 96.0 | 0.95 | [0.89, 0.99] | [0.88, 1.0] |
| `operation` (Q1) | 100 | 96.0 | 0.95 | [0.90, 0.99] | [0.88, 1.0] |
| `process` (derived) | 100 | 98.0 | 0.97 | [0.93, 1.0] | [0.93, 1.0] |
| `function` (Q2) | 100 | 94.0 | 0.91 | [0.84, 0.97] | [0.82, 0.97] |
| `object` (Q2) | 100 | 95.0 | 0.91 | [0.83, 0.98] | [0.80, 0.98] |
| `prior_own_work` | 100 | 92.0 | 0.89 | [0.81, 0.94] | [0.78, 0.97] |
| `decision` (Q3) | 100 | 96.0 | 0.94 | [0.87, 0.98] | [0.88, 0.99] |
| `verification` (Q4) | 100 | 94.0 | 0.82 | [0.67, 0.94] | [0.63, 0.97] |
| `uptake` (Q5) | 100 | 94.0 | 0.92 | [0.86, 0.98] | [0.86, 0.98] |
| `domain` (WildChat only) | 30 | 100 | 1.0 | [1.0, 1.0] | [1.0, 1.0] |

κ on subsets:

| Field | NIRVANA n=70 | WildChat n=30 | Follow-up C1+C2 n=92 | C2 n=35 | C1 n=57 |
|---|---|---|---|---|---|
| `family` | 0.95 | 0.95 | 0.94 | 0.92 | 0.95 |
| `function` | 0.90 | 0.93 | 0.91 | 0.80 | 0.97 |
| `object` | 0.95 | 0.77 | 0.92 | 0.90 | 0.93 |
| `prior_own_work` | 0.88 | 0.82 | 0.88 | 0.76 | 0.93 |
| `decision` | 0.96 | 0.85 | 0.95 | 1.0 | 0.89 |
| `verification` | 0.76 | 1.0 | 0.72 | 0.84 | 0.66 |
| `uptake` | 0.95 | 0.83 | 0.92 | 0.92 | 0.87 |

All intervals and percentages by subset are in `results/agreement_tables.md`. `u4_subtype` is kept out of every agreement claim.

**How to read these.**

- **Session clustering widens intervals, slightly.** Summed over the nine coded and derived fields of the first table, session intervals are about 20% wider than window intervals. The largest change is `verification`, 0.27 to 0.34 wide. Use the session intervals.
- **Small subsets are weak.** `verification` on C2 has a session interval of [0.0, 1.0], and on C1 [0.28, 1.0]. Follow-up `verification` is 0.72 [0.42, 0.95]. These reach or near the 0.4 line, though no point estimate does.
- **`verification` κ on WildChat follow-ups is undefined.** Both coders gave `V0` on all 25, so the 1.0 above rests on the 5 `C0` windows.
- **`verification` κ rests on `V0`, `V1`, `VX`.** Both coders chose `V1` on 9 of the 13 windows where either did. `V2` is 0 of 1, `V3` is 0 of 1, `V4` never appears.
- **`C0` forces `VX` and `UX`,** so follow-up numbers are the fairer read.
- **This is above the pilot** (R4 `decision` 0.78 [0.51, 1.0], n=22). I can't say why. Same-family models, rules written after these coders' disagreements, and fuller views are all possible. High agreement between models is not evidence that the labels are right.

## Label frequencies, final labels (windows)

| Field | Labels |
|---|---|
| `decision` | D0 16, D1 16, D2 53, D3 7, D4 8 |
| `verification` | V0 78, V1 13, VX 8, UNSETTLED 1 |
| `uptake` | U1 9, U2 3, U3 7, U4 31, U5 1, U6 2, U7 13, U8 26, UX 8 |
| `family` | PROSE_CITATION 40, SURFACE 22, CLAIM_ARGUMENT 11, SOURCE_WORK 10, FRAME_IDEA_PLAN 7, REVIEW_SUBSTANCE 6, OX 4 |
| `prior_own_work` | VISIBLE_DRAFT 44, NONE_VISIBLE 21, VISIBLE_PARTIAL 18, UNOBSERVABLE 17 |
| `domain`, WildChat | RESEARCH_EXPLICIT 29, OTHER_WRITING 1 |

A, B and per-dataset counts are in `results/agreement_tables.md`. The sample is not an estimate of all windows (`data/REPORT.md`). `process` and `family` come from `operation` by script. Bet 5 owns what these mean.

## Adjudication

| | Count |
|---|---|
| Windows with any disagreement | 31 of 100 |
| Disputed fields | 39 of 800 coded fields |
| Ruled for A | 25 |
| Ruled for B | 13 |
| Third code | 0 |
| Not settled | 1 |
| Changed by the script rule (s7) | 0 |

| Field | Disputed | Biggest confusion |
|---|---|---|
| `prior_own_work` | 8 | NONE_VISIBLE vs PARTIAL 4, UNOBSERVABLE vs PARTIAL 3 |
| `verification` | 6 | V0 vs V1 4 |
| `uptake` | 6 | U4 vs U8 5 |
| `function` | 6 | F2 vs F4 2 |
| `object` | 5 | ARGUMENT vs IDEA 2 |
| `operation` | 4 | O02 vs O09 2 |
| `decision` | 4 | one each: D0/D1, D0/D2, D1/D2, D2/D3 |

- **`NIRVANA-e06-t02` `verification` is `UNSETTLED`** (A `V2`, B `V0`). v1.1 doesn't say if handing a criterion to the AI, with no failing stated, is `V2` or `V3`. Bet 5 should leave it out or run both readings.
- **25 to 13 favours A, the adjudicator's own requested model.** Labels were shown as first and second with a seeded flip, and identity was never shown. That doesn't rule out a same-model preference. By field the split is uneven: `prior_own_work` 7 to 1, `object` 1 to 4.
- **Position may have mattered too.** The second-shown label won 24 times, the first 14. With 38 rulings this can't be told from chance or from rule fit.
- **`NIRVANA-e06-t02` was not settled, though priority settled similar calls.** The adjudicator used s6 priority on `NIRVANA-e41-t02` to `t04`, and left this one open because the rule gap is on whether `V3` applies at all. So "0 `V2`, 0 `V3`" in final labels leaves this one window out; its two coders gave `V2` and `V0`. The adjudicator ruled `V0` out and left `V2` vs `V3` open.
- **`NIRVANA-e56-t01` was ruled, although `rule_gaps_for_v2.tsv` G03 says no rule covers a short paste.** Read that ruling as a call, not as an application of a settled rule.
- **Every final label traces** to A=B or a row in `results/adjudication_log.csv`. Free-text reasons stay in the git-excluded `blind/`.
- **v1.1 did not change.** Gaps are in `rule_gaps_for_v2.tsv`.

## Script audit

From `codebook/scripts/overlap.py`, on the 35 C2 windows. Results in `results/overlap_audit.json` and `results/overlap_facts.csv`.

| Check | Result |
|---|---|
| `U1`/`U2` labels the script agrees with | A 11 of 11, B 11 of 11, final 11 of 11 |
| `U7` labels with no script match | A 13 of 13, B 14 of 14, final 13 of 13 |
| The one retyped run (`NIRVANA-e61-t05`) | Script: typed match. A, B and final: `U1`. Bet 3's coders had missed this kind of case |
| Conflict in final labels | 1: `NIRVANA-e56-t01`, `U3` with no 30-character run |

`NIRVANA-e56-t01` is the weakest final label. B, Fable and the script all lean `U7`. The adjudicator ruled `U3` for A. Only a short phrase was pasted, and no rule says whether that counts as an insertion (`rule_gaps_for_v2.tsv` G03). It keeps `U3`, since v1.1 gives the script authority over `U1` vs `U2` only.

## Fable comparison (third AI check)

Opened only after final labels were committed (`c0d8944`, then the comparison in `10ed13d`). 20 windows. `results/fable_comparison.md`.

| Field | Fable vs A % / κ | Fable vs B % / κ | Fable vs final % / κ [CI] | Vs final, follow-up κ (n=18) | Vs final, without 4 marked windows % / κ (n=16) | A vs B on these 20 % / κ |
|---|---|---|---|---|---|---|
| `family` | 85.0 / 0.79 | 90.0 / 0.86 | 90.0 / 0.86 [0.67, 1.0] | 0.84 | 87.5 / 0.83 | 95.0 / 0.93 |
| `operation` | 85.0 / 0.80 | 90.0 / 0.86 | 90.0 / 0.86 [0.67, 1.0] | 0.85 | 87.5 / 0.83 | 95.0 / 0.93 |
| `process` | 95.0 / 0.93 | 95.0 / 0.93 | 95.0 / 0.93 [0.74, 1.0] | 0.91 | 93.8 / 0.90 | 100 / 1.0 |
| `function` | 90.0 / 0.83 | 95.0 / 0.91 | 95.0 / 0.91 [0.70, 1.0] | 0.89 | 93.8 / 0.88 | 95.0 / 0.91 |
| `object` | 85.0 / 0.71 | 90.0 / 0.81 | 90.0 / 0.81 [0.50, 1.0] | 0.77 | 87.5 / 0.76 | 95.0 / 0.91 |
| `prior_own_work` | 95.0 / 0.91 | 95.0 / 0.91 | 95.0 / 0.91 [0.71, 1.0] | 1.0 | 93.8 / 0.90 | 100 / 1.0 |
| `decision` | 90.0 / 0.84 | 90.0 / 0.84 | 90.0 / 0.84 [0.60, 1.0] | 0.82 | 93.8 / 0.88 | 100 / 1.0 |
| `verification` | 100 / 1.0 | 100 / 1.0 | 100 / 1.0 [1.0, 1.0] | 1.0 | 100 / 1.0 | 100 / 1.0 |
| `uptake` | 85.0 / 0.81 | 80.0 / 0.75 | 85.0 / 0.81 [0.63, 1.0] | 0.78 | 87.5 / 0.84 | 85.0 / 0.81 |
| `domain` (n=6) | 83.3 / 0.0 | 83.3 / 0.0 | 83.3 / 0.0 | 0.0 | 80.0 / 0.0 | 100 / undefined |

With one window per participant, gold has no session clusters. `domain` κ of 0 reflects one label on nearly all windows, so read the percentage.

**Q3–Q5 disagreements with final labels: 5 fields on 3 windows.**

| Window | Fable | A | B | Final | Why, as far as can be seen |
|---|---|---|---|---|---|
| `NIRVANA-e27-t02` (marked) | D2, U7 | D3, U3 | D3, U3 | D3, U3 | The cut hid the paste. Fable's own note says so |
| `NIRVANA-e56-t01` | D2, U7 | D3, U3 | D3, U7 | D3, U3 | Short paste, gap G03 |
| `NIRVANA-e01-t04` | U1 | U3 | U3 | U3 | Text pasted and kept, then new typing after it, gap G04 |

**Marked windows** (set before opening, `decisions.tsv` T04). `NIRVANA-e27-t02` had a main block cut on the Fable page. `NIRVANA-e26-t11`, `NIRVANA-e70-t07` and `WILDCHAT-0685972d7031-t03` had reused earlier AI text cut there, and Fable matched final on Q3–Q5 on all three. Nothing was rerun.

Fable, A and B all used `V0`, `V1` or `VX` on these 20, so `verification` at 100% tests only that split.

### WildChat `is_research_writing`, reported apart

Fable only, on 6 windows. A and B did not code this field.

| Result | n |
|---|---|
| Yes | 4 |
| No | 2 |
| Yes share, exact 95% CI | 0.22 to 0.96 |

- 6 windows can't estimate a rate. It does show the LLM screen is not settled. All 6 were LLM "clear", and all are `RESEARCH_EXPLICIT` in final labels.
- `WILDCHAT-30f7e79715c8-t01`: Fable `ACADEMIC_STATED`, no. Final `RESEARCH_EXPLICIT`.
- **`WILDCHAT-2d9abc984de9-t01` is inconsistent in Fable's labels:** `RESEARCH_EXPLICIT` with `is_research_writing` no. Fable's note says the task concerns a paper's methods, but the writer isn't producing a paper. Reported and not corrected.
- A and B may share a pull toward `RESEARCH_EXPLICIT`, since 29 of 30 WildChat windows came out that way. Nothing here tests it.

## Coder separation

From transcripts, by path (`results/access_audit.json`, `scripts/audit_access.py`). The audit's own first regex gave false hits on `coder_brief.md` and `tool-results`; I fixed it and reran.

| Check | Result |
|---|---|
| Any coder's tool call touching the other coder, Fable, pilot, data or results paths | 0 of 10 agents |
| Adjudicator's tool calls touching those or coder files | 0 |
| Every line of every view returned to its coder | All 10 agents, 100% |
| A and B ran in parallel | Yes |

Coder A batch 4 listed `blind/` once, which shows folder names only. It made scratch copies of its own views, then deleted them. The adjudicator's folder listing showed `flips.json`, which it did not open. Coder B wrote label-building scripts in the session scratchpad, which A could have reached. The transcripts show A did not open them. B finished first, so this exposure was real but unused. Separation is not enforced by the file system. Transcripts show what agents did. The audit needs local transcripts, so `run_all.sh` does not rerun it and the committed JSON is the record.

## Still unverified

1. **Any human reading.** No person coded any window. All three parties are AI models and may share a bias.
2. **Whether high agreement means right labels.** It doesn't show that.
3. **Grading the grounds of a check.** 0 final `V2`, `V3`, `V4` here, and the same near-absence in the pilot. The claim the lit review singled out has no data in this sample. Checks elsewhere are unseen, so this doesn't show writers don't check.
4. **What the cut cost A and B.** Only Fable's page had main blocks capped. Its one direct case is `NIRVANA-e27-t02`. Older turns were unseen by all three parties, so agreement can't reveal what that cost.
5. **Within-coder drift across batches.** Not measured.
6. **Same-model effect in adjudication.** 25 to 13, not separable from true rule fit.
7. **WildChat's domain.** The third check disagrees on 2 of 6, and the screen is unverified.
8. **AI correctness.** Not coded, by design.

## For Bet 5

- Use `results/final_labels.csv`. Exclude or double-run `NIRVANA-e06-t02` `verification`.
- Exclude or double-run `NIRVANA-e58-t10` `decision` as well. Treat `NIRVANA-e61-t07` `prior_own_work` as a likely artifact.
- Check `D1` and `VISIBLE_DRAFT` on the 10 windows in `results/older_turns.json` before relying on them. The "no visible own work" and "writer-supplied content" indicators of section 9 are exposed to this.
- Treat `NIRVANA-e56-t01` as weak, and mark `NIRVANA-e01-t04` as a rule-gap case.
- Keep NIRVANA and WildChat apart, and report sessions as clusters.
- `V2`–`V4` are absent, so section 9's "AI checks itself" indicator will be empty on final labels.

## Files

`results/final_labels.csv` · `results/labels_ab.csv` · `results/adjudication_log.csv` · `results/agreement.json`, `agreement_tables.md` · `results/fable_comparison.json`, `.md` · `results/overlap_audit.json`, `overlap_facts.csv` · `results/truncation.json`, `truncation_effect.json`, `views_expanded_prior.json`, `older_turns.json` · `results/access_audit.json` · `decisions.tsv` · `rule_gaps_for_v2.tsv` · `coder_brief.md`, `adjudicator_brief.md` · `scripts/` · `blind/` (git-excluded: views, coder and adjudicator notes)

## Gate

**First pass: failed, on one blocking problem.** A fresh critic with no access to my reasoning found that the report left out the 3-turn limit, and said nothing was left unread. Items 1 to 5 passed: separation (its own transcript read), completeness, rerun with identical hashes and its own κ, traceability on 800 fields, and no dataset text in commits. Report: `.wayne/bets/0005-coding-run/gate/critic_report.md`. The fixes are above, with no label changed.

**Recheck: passed, with 0 blocking problems.** A second fresh critic reproduced the 18 and 10 window sets with its own script, confirmed the new claims and numbers, got identical hashes on rerun, and confirmed that `final_labels.csv` and `labels_ab.csv` did not change since `c0d8944`. Report: `.wayne/bets/0005-coding-run/gate/critic_recheck.md`.

**One limit.** After the recheck I made small wording fixes from its minor list, in this report and two log files. No critic rechecked those. No label or number changed.
