# Codebook pilot report (Bet 3, for checkpoint C2)

**Reading time: 15 minutes.** Numbers come from `scripts/run_all.sh`, which replays saved coder labels and calls no model. **All agreement here is between two AI coders. It is a consistency check, not validation.** No human has used v1.1 yet.

## Bottom line

- **v1.1 is frozen.** Two AI coders can apply its final text. On round 4 (22 windows), `decision` κ is 0.78, `verification` 1.0, `uptake` 0.94.
- **Don't trust those numbers too far.** Round 4 is small with wide intervals, and I wrote the rules after reading these coders' disagreements.
- **The stop signal was not hit.** `decision` and `verification` were 0.38 on follow-up windows under v1.0, and rose after rule changes.
- **C3 will take about 90 minutes to 2 hours, not 1.** The gold windows hold about 13,700 words on the page.
- **One finding is held back until C3 is saved.** `REPORT_AFTER_C3.md` covers how often each check code appeared. **Read it after C3.** It could prime your `V` codes, and it affects the proposal's success criterion.

## Label changes, v1.0 → v1.1

Full list with evidence: `decisions.tsv` (read it after C3; it has label counts). Some rows are wording cuts with no pilot evidence behind them, and the log says so.

| Change | v1.0 | v1.1 | Evidence |
|---|---|---|---|
| **Cut** | `D5` | Into `D3` | R1: 3 labels, none agreed. R2 with a strict rule: 0 of 80. Lit: no source |
| **Cut** | `V5` | Into `V4` | No use in R1–R2. Lit: no source |
| **Cut** | `process` coded | Script derives it | Equals the map 160 of 160 |
| **New** | none | `U8_MOVED_ON` | R1 `U4` vs `UX` (2 disagreements), and 16 uptake flags of all kinds. Mysore Table 4 separates new requests from follow-ups. Used 47 of 184 labels in R2–R4, 17 on enriched windows |
| **New** | none | `prior_own_work` | Lit rec 1 (4 sources). κ 0.72, 0.80, 0.86, 0.79 |
| **Rule** | `D0` includes polish, as read | Polish is `D1` | R1: 7 of 19 decision disagreements |
| **Rule** | `D4` "traceable" | Stated yes or a verbatim run; typed echo is `D2` | R1: named in both coders' final messages |
| **Rule** | `DX` | Missing input is `D2` | R2 flags from both. R3: `DX` 0 of 60 |
| **Rule** | `D0` plain explanation | A summary or analysis of supplied material is AI-origin | R3 flags from both. R5: both coders `D2` on 2 real summary windows |
| **Rule** | `D3` and `D4` on part of a response | Under half pasted is `D3`; half or more verbatim is `D4` | Critic found a conflict. R4: 1 such window |
| **Rule** | `V3` any challenge | Words only, weak evidence | R1 `V0` vs `V3`; Tao 2026 |
| **Rule** | `V` any trace | Next action only | R1 flag on a request-side challenge |
| **Rule** | `U6` | Saying no beats `U4` | R2: 2 disagreements. R3: 0 |
| **Note** | `U4` | Subtypes stay secondary | Mysore Table 4. κ 0.48, 0.43, 1.0, 0.71, on 5 to 15 windows each |
| **Script** | `U1`/`U2` by reading | Script audits, settles `U1` vs `U2` | See below |
| **Report** | 16 operations | 7 families | Chen 2026 informed this; the grouping is mine |
| **Fix** | Harvard Writing Center | Writing Program | Opened the page: "A Publication of the Harvard College Writing Program" |

**Kept though rare:** several labels. Reasons are in `decisions.tsv` K03–K04 and `REPORT_AFTER_C3.md`, both for after C3. Families protect reporting from empty operations.

## Recommendations from the lit review

| # | Recommendation | Decision |
|---|---|---|
| 1 | `prior_own_work` | Added |
| 2 | Q3–Q5 as risk indicators, no per-window verdict | Done (s1, s9), following C1 default (c) as relayed by the parent session. **It is in no file, so please confirm it** |
| 3 | `U4` subtypes as notes | Done, not promoted, not in C3 |
| 4 | `V3` weak; test `V5` | `V3` marked weak; `V5` cut |
| 5 | Text overlap by script | Done (`scripts/overlap.py`) |
| 6 | Report operation families | Done |
| 7 | Test `D5` strictly | Tested, cut |
| 8 | Do not code AI correctness | Not coded; limit stated |
| 9 | Credit related schemes | Done (header, s9) |
| Open | Poquet's active or passive axis | **Not tested** as a field |

## Agreement per question

| Field | R1 v1.0, n=40: % / κ | R2, n=40: % / κ [95% CI] | R3, n=30: % / κ [95% CI] | **R4 final text, n=22: % / κ [95% CI]** |
|---|---|---|---|---|
| `family` (Q1) | 97.5 / 0.97 | 90.0 / 0.86 [0.72, 0.97] | 93.3 / 0.92 [0.79, 1.0] | 86.4 / 0.82 [0.62, 1.0] |
| `operation` (Q1) | 97.5 / 0.97 | 90.0 / 0.87 [0.74, 0.97] | 93.3 / 0.92 [0.80, 1.0] | 81.8 / 0.77 [0.57, 0.94] |
| `function` (Q2) | 95.0 / 0.93 | 82.5 / 0.75 [0.58, 0.89] | 93.3 / 0.92 [0.77, 1.0] | 81.8 / 0.75 [0.54, 0.94] |
| `object` (Q2) | 90.0 / 0.81 | 92.5 / 0.84 [0.63, 1.0] | 86.7 / 0.81 [0.62, 0.95] | 90.9 / 0.86 [0.63, 1.0] |
| `prior_own_work` | 82.5 / 0.72 | 87.5 / 0.80 [0.64, 0.96] | 90.0 / 0.86 [0.68, 1.0] | 86.4 / 0.79 [0.52, 1.0] |
| `decision` (Q3) | 52.5 / 0.42 | 82.5 / 0.75 [0.57, 0.90] | 90.0 / 0.87 [0.73, 1.0] | 86.4 / 0.78 [0.51, 1.0] |
| `verification` (Q4) | 82.5 / 0.62 | 95.0 / 0.84 [0.54, 1.0] | 93.3 / 0.84 [0.59, 1.0] | 100 / 1.0 [1.0, 1.0] |
| `uptake` (Q5) | 92.5 / 0.90 | 85.0 / 0.81 [0.65, 0.93] | 100 / 1.0 [1.0, 1.0] | 95.5 / 0.94 [0.77, 1.0] |

**Follow-up windows only (C1 and C2),** because `C0` forces `V` and `U`:

| κ | R1 | R2 | R3 | R4 |
|---|---|---|---|---|
| `decision` | 0.38 | 0.73 | 0.87 | 0.84 |
| `verification` | 0.38 | 0.72 | 0.82 | 1.0 |
| `uptake` | 0.88 | 0.78 | 1.0 | 0.94 |

**Random windows only,** leaving out the keyword-chosen or script-chosen ones:

| κ | R1 n=40 | R2 n=30 | R3 n=16 | R4 n=19 |
|---|---|---|---|---|
| `decision` | 0.42 | 0.81 | 1.0 | 0.72 |
| `verification` | 0.62 | 0.83 | 0.73 | 1.0 |
| `uptake` | 0.90 | 0.80 | 1.0 | 0.93 |

**Windows where both coders chose a label, out of windows where either did, all rounds:**

| Field | Counts |
|---|---|
| `decision` | `D0` 12/27, `D1` 26/38, `D2` 43/58, `D3` 7/16, `D4` 12/14, `DX` 0/8 |
| `uptake` | `U1` 17/19, `U2` 3/6, `U3` 7/8, `U4` 40/47, `U6` 4/6, `U7` 17/17, `U8` 22/25, `UX` 12/14 |

How to read these:

- R1 was v1.0 plus two trial fields. R2 and R3 used drafts, not archived. R4 used the frozen text. So `R4` is the number for v1.1.
- Windows are new each round, but not always new sessions: 7 of 30, 5 of 16 and 11 of 19 random windows in R2, R3 and R4 come from sessions coded earlier.
- Intervals treat windows as independent, so they ignore session clusters.
- Field κ can sit high when one label dominates.
- `domain` on WildChat only: κ 1.0, 0.65, 1.0, 0.78, on 8 to 21 windows.
- Coders were requested as `opus` (A) and `sonnet` (B). The served model was not recorded, and temperature cannot be set. Briefs are in `coder_briefs/`, with each coder's hardest rules in `coder_final_messages.md`.

**Round 5 (10 windows, one rule).** R4 had no summary request, so R5 drew windows whose request mentions summarizing or explaining. The keyword mostly caught polish templates: only 2 of 10 were real summaries. Both coders chose `D2` on those 2, and agreed on `decision` and `uptake` on all 10. κ on so few windows means little, so R5 is not in the tables above.

**Constructed cases (12, not data, so that every label gets a test).** Both coders matched my key on 11 of 12 for each of `V`, `U` and `D`. On the two misses shared by both, I now think my key was weak or wrong (`VIG-10`, `VIG-12`). I wrote these cases, so they test only whether the rules can be told apart.

**Script audit.** 32 of 34 `U7` labels had no text match. Both exceptions are on the only retyped-run window, where both coders said `U7` and the script found a verbatim run. The script agrees with 39 of 45 `U1` and `U2` labels. On one window both coders gave `U4` although the script found a paste matching this response. Its match or no-match split equals Bet 1's linkage on 201 of 204 C2 windows. The other 3 are short pastes under 30 characters, which Bet 1 calls no match and this script counts as a match (`overlap.py --all`).

## How the pilot was blinded

| Check | Result |
|---|---|
| Windows, sessions, participants shared with sample or gold | 0, 0, 0 (`scripts/check_blinding.py`) |
| Why whole sessions were blocked | A neighbouring window carries the next request, so it would leak test text |
| LLM labels or linkage in coder views | None (whitelist in `scripts/views.py`) |
| Gold or sample text I read | None; scripts printed counts only |
| Human labels protected | `make_c3.py` will not overwrite a filled sheet |
| v1.1 and this report | No 40-character run from any window |
| AI labels in the C3 packet | None (`check_c3.py --blank`) |

Limit: the leak test counts rare 40-character runs shared with one held-out window, and fails at 60. I set that threshold after seeing data. The worst view has 41 (about 80 characters). A critic's wider test agrees. Coder separation was by instruction and parallel runs, not enforced by the file system.

## Still weak

1. **AI-only agreement.** C3 is the first human test. Gold has 20 windows and may show lower numbers.
2. **Rules tuned on these coders.** Fresh windows reduce this but don't remove it.
3. **`D3` is the weak decision label:** 7 of 16. Round 4's coders also split on a response that evaluates supplied material (`D0`, `D1` or `D2`), and on bare requests.
   - **The summary rule is barely tested.** It moves summaries away from `D0`, the code most `F1` windows got before it. Only 2 real summary windows met it, neither a request only to understand, and one coder's flags name `D1` as the close alternative on both. If C3 shows trouble here, this is the first place to look.
   - **Open seams, left for v2.0:** a summary of the writer's own text can read as `D1` or `D2`; an assignment prompt's summary can read as `D0` or AI-origin; a retyped run under half has no `D` rule; a chat turn that resubmits blended text fits `U4` loosely.
4. **The retyped-run rule is barely tested.** One window met it, and both coders missed the run. Bet 4 should use the script audit to catch this.
5. **`U2` vs `U3`** stays a judgment. `U2` is 3 of 6.
6. **Thin objections.** `V1` vs `V3` on a brief complaint stays arguable.
7. **Essay-heavy pool.** `O07` and `O16` were never used. The claim family has 11 labels of 264.
8. **WildChat windows rest on unverified LLM screening.** C3's yes or no column is the first human check.
9. **Drafts between rounds were not archived.** `decisions.tsv` is the record of what changed when.
10. **Mysore:** I read Table 4 and the section explaining it, not the whole paper. **Harvard:** I opened the page in a browser, and the critic's own fetch got HTTP 403, so it relied on `lit/citation_check.csv`.

## For Bet 4

Use `scripts/views.py` for coder views. `sample.csv` lacks the editor state that `prior_own_work` needs. Compute `process`, families and the overlap audit by script. Report session clustering. Bet 4 should also leave `u4_subtype` out of agreement claims.

## What to check at C2

1. Are you fine with `D5` and `V5` gone, and with `U8` added?
2. Is the `D1` rule right: polishing the writer's claims counts as `D1`, not `D0`?
3. Are you fine that `process` is derived, not coded?
4. Is C1 default (c) right as written in v1.1 section 9?
5. Is about 2 hours for C3 acceptable? `PACING.md` still says 1.

## Files

`CSE216_Research_Writing_Codebook_v1.1.md` · `decisions.tsv` (after C3) · `C3_INSTRUCTIONS.md` · `REPORT_AFTER_C3.md` (after C3) · `c3_gold_sheet.csv` and `c3_gold_windows.html` (git-excluded) · `pilot_results/` labels and statistics, no text · `pilot/` views and coder files (git-excluded) · `coder_briefs/` · `scripts/`

## Gate

**Passed on the third critic pass.** Critics were fresh agents with no access to my reasoning. Reports are in `.wayne/bets/0004-codebook-pilot-freeze/gate/`; read them after C3.

| Pass | Result | What it caught |
|---|---|---|
| 1 | Fail, 6 blocking | Unlogged changes, a script that could wipe your labels, wrong reading list, wrong time claim, checker rejecting Excel saves, 2 rule conflicts. The final text had also been piloted on no window, so I added R4 |
| 2 | Fail, 3 blocking | More unlogged changes, wording that could prime you before C3, a rule logged as tested when it was not, so I added R5 |
| 3 | **Pass**, 0 blocking | 9 minor groups |

**One limit.** After pass 3 I fixed most of those minors: log rows, wording, ban list, checker edges. No critic rechecked these fixes. I reran `run_all.sh` and the checker tests myself. v1.1 did not change (sha1 `0b5e1ac`). Critics recomputed every κ and % independently.
