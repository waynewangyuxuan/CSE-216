# NIRVANA sessions report (Bet 6)

Numbers come from `scripts/run_all.sh`, which replays saved labels and calls no model. Two runs give identical files.

**Every number here is AI-to-AI consistency.** Coders and adjudicators are AI models and can share a bias. No human coded anything. Nothing here validates claims about cognition. No window has an offloading or surrender label; that is Bet 5's job.

## Bottom line

- **All 347 NIRVANA windows have final v1.1 labels, so all 71 sessions are complete.** File: `results/final_labels_nirvana.csv`. 16 of 3,123 label cells are `UNSETTLED`: 11 rulings, 4 derived from them, and Bet 4's 1.
- **The coders agree well.** On the 295 adjudicated windows: `decision` κ 0.80, `verification` 0.79, `uptake` 0.85. The lowest Q3–Q5 κ on any subset is 0.48 (`verification` on C2), with a session interval of [0.17, 0.69]. The point estimate is above the 0.4 stop line, but the interval is not.
- **Full history changed 6 coded labels on 5 of the 18 recoded windows.** It confirmed both Bet 4 flags: `NIRVANA-e58-t10` `decision` went from D1 to D2, and `NIRVANA-e61-t07` `prior_own_work` went from NONE_VISIBLE to VISIBLE_PARTIAL.
- **The adjudicator sided with Coder A, its own requested model, 159 to 45.** That is a stronger lean than Bet 4's 25 to 13.
- **Blindness held for coders; adjudicators broke the order rule twice.** None of the 41 agents touched a forbidden path, and every coder labeled each window before reading the next turn. Two adjudicators each read one later part early. Both rulings were redone by fresh agents and came out the same.

## Coverage

| | Windows | Sessions | Final label from |
|---|---|---|---|
| New, coded here | 277 | 62 | Bet 6: A=B, ruling, or s7 script |
| Bet 4 windows with unseen older turns, recoded with full history | 18 | 6 | Bet 6 (rule S05) |
| Other Bet 4 windows | 52 | 20 | Bet 4, unchanged |
| **All** | **347** | **71** | `source` column; Bet 4 labels kept in `bet4_` columns for all 70 |

Every final label traces to A=B, a row in `results/adjudication_log.csv`, the s7 script rule, or Bet 4's committed `final_labels.csv`. `finalize.py` stops on any field with no source. The log's `rule` column is a short citation of at most 60 characters, such as `s5 step 2`. Free-text reasons stay in the git-excluded `blind/`. `blind/` is excluded only through the local `.git/info/exclude`, so a fresh clone would need that line.

## How coders saw a window

| | Bet 4 | Bet 6 |
|---|---|---|
| Earlier turns | Last 3, cut to 500 characters | All of them, uncut: editor, request, AI response, what happened next |
| Later turns | None | None. One part file per turn; a label is written before the next part is opened (S02) |
| Revising a label | Possible | Refused by `add_label.py` |
| Codebook | Whole v1.1 | v1.1 without s9 (the risk indicators), made by script; the frozen file is unchanged (S03) |
| Agents | 5 + 5 coders, 1 adjudicator | 16 + 16 coders, 7 adjudicators, 2 redo adjudicators |

Requested and served models matched on every agent: A and adjudicators were `claude-opus-5-5`, B was `claude-sonnet-5-5`. Batches held 13 to 31 windows and 144 to 159 KB, with sessions whole.

## Agreement, A vs B

295 adjudicated windows (277 new + 18 recoded), 62 sessions. Bootstrap, 2,000 draws, fixed seed, Bet 4's code imported.

| Field | % | κ | κ CI, sessions | Follow-up κ (n=289) [sessions] |
|---|---|---|---|---|
| `family` | 92.9 | 0.91 | [0.87, 0.95] | 0.91 [0.87, 0.95] |
| `operation` | 92.5 | 0.91 | [0.87, 0.95] | 0.91 [0.87, 0.94] |
| `process` (derived) | 95.3 | 0.93 | [0.90, 0.96] | 0.93 [0.90, 0.96] |
| `function` | 90.2 | 0.87 | [0.82, 0.92] | 0.87 [0.82, 0.92] |
| `object` | 92.5 | 0.87 | [0.81, 0.92] | 0.87 [0.82, 0.93] |
| `prior_own_work` | 86.1 | 0.76 | [0.61, 0.91] | 0.78 [0.63, 0.92] |
| `decision` (Q3) | 85.1 | 0.80 | [0.72, 0.87] | 0.80 [0.72, 0.88] |
| `verification` (Q4) | 92.5 | 0.79 | [0.66, 0.87] | 0.76 [0.63, 0.86] |
| `uptake` (Q5) | 88.1 | 0.85 | [0.79, 0.90] | 0.85 [0.79, 0.90] |

| Q3–Q5 κ by subset [session CI] | `decision` | `verification` | `uptake` |
|---|---|---|---|
| C1, n=110 | 0.73 [0.53, 0.91] | 0.96 [0.91, 1.0] | 0.75 [0.51, 0.92] |
| C2, n=179 | 0.82 [0.74, 0.88] | **0.48 [0.17, 0.69]** | 0.81 [0.73, 0.88] |

- **This is below Bet 4** (`decision` 0.94, `uptake` 0.92 on 100 windows). Full histories give coders more to weigh, and pilot-session windows are new to these rules. I can't separate the two.
- **`verification` on C2 is weak.** 18 of its 20 disagreements are V0 vs V1, and A uses V1 far more than B (25 vs 9 of 179). This is Bet 4's G02 and this bet's H04.
- **`u4_subtype` is in no agreement claim.** Per-label counts and all subsets are in `results/tables.md` and `results/agreement.json`.

## Adjudication

| | Count |
|---|---|
| Windows with any disagreement | 138 of 295 |
| Disputed fields | 215 of 2,065 coded fields |
| Ruled for A / for B | 159 / 45 (one A ruling was later changed by the s7 rule, so 158 final fields come from A rulings) |
| Third code | 0 |
| Not settled | 11 (on 8 windows) |
| Redone by a fresh agent (S08) | 7 fields on 2 windows; all 7 matched the first ruling |
| Changed by the s7 script rule (U1 vs U2) | 3, two of them A=B U2 changed to U1 |
| First-shown label won / second | 122 / 82 |

| Field | Disputed | A / B / unsettled |
|---|---|---|
| `decision` | 44 | 34 / 9 / 1 |
| `prior_own_work` | 41 | 36 / 5 / 0 |
| `uptake` | 35 | 23 / 9 / 3 |
| `function` | 29 | 23 / 5 / 1 |
| `operation` | 22 | 13 / 7 / 2 |
| `object` | 22 | 15 / 5 / 2 |
| `verification` | 22 | 15 / 5 / 2 |

- **The 159 to 45 lean toward A cannot be told apart from rule fit.** Coder identity was hidden and order was flipped by seed. The adjudicator and A are the same model. Treat contested labels as A-leaning.
- **Adjudicators read some rules differently from one another.** On U3 "added beside", one read it broadly, one narrowly, and one left it open. On praise-only verdicts, two ruled D0 and one ruled AI-origin. Each packet held whole sessions, so a session's rulings are internally consistent but may differ from another packet's (`rule_gaps_for_v2.tsv` H01, H02).
- **Unsettled fields:** `NIRVANA-e04-t16` verification, `e13-t02` operation, `e19-t01` decision and uptake, `e25-t16` verification, `e34-t01` object, `e42-t08` uptake, `e47-t01` uptake, `e68-t06` operation, function and object. Plus Bet 4's `e06-t02` verification. Bet 5 should leave these out or run both readings.

## 3-turn sensitivity

Rule S05 was fixed before any Bet 6 label existed: the 18 windows take the full-history label, whatever it is.

| Measure | Result |
|---|---|
| Coded fields changed, final Bet 4 → Bet 6 | 6 of 126, on 5 of 18 windows |
| On the 10 windows that reuse unseen AI text | 2 changed, both as Bet 4 predicted |
| The other 8 of those 10 | Every field unchanged, including their `D1` and `VISIBLE_DRAFT` labels |

| Window | Field | Bet 4 (3 turns) | Bet 6 (full) | Reuses unseen AI text |
|---|---|---|---|---|
| `NIRVANA-e58-t10` | `decision` | D1 | D2 (adj=A) | yes |
| `NIRVANA-e61-t07` | `prior_own_work` | NONE_VISIBLE | VISIBLE_PARTIAL (A=B) | yes |
| `NIRVANA-e29-t07` | `decision` | D0 | D1 (adj=A) | |
| `NIRVANA-e29-t06` | `operation`, `function` | O05, F1 | O14, F8 | |
| `NIRVANA-e61-t06` | `object` | CLAIM | PROSE (adj=B) | |

- **Different agents coded each side.** A change can come from the view or from coder noise. As a rough bar, the 52 Bet 4 windows that were not recoded for the final file had little hidden, and the same coder role matched Bet 4 on 90–96% of Q3–Q5 fields there.
- **Bet 4's flag on `NIRVANA-e58-t10` is resolved in the final file** (D2). The `NIRVANA-e61-t07` artifact is resolved too. Bet 4's own `final_labels.csv` is unchanged.

## Script audit (uptake, 204 C2 windows)

| Check | Result |
|---|---|
| Final `U1`/`U2` that the script agrees with | 74 of 74, after the s7 rule changed 3 |
| Final `U7` with no script match | 71 of 74 |
| Final labels flagged by the script | 12. Six are chat or no-trace labels where the script found a paste; coder notes say at least 4 of those pastes came from an earlier AI turn or from outside the chat (H08). Three are U7 with a run. Three are insertion labels with no run, one of them Bet 4's `NIRVANA-e56-t01` |

Details: `results/overlap_audit.json`. As in Bet 4, only U1 vs U2 is the script's to settle.

## Blindness (from transcripts)

`results/access_audit.json`, `scripts/audit_access.py`, 41 agents.

| Check | Result |
|---|---|
| Any tool call touching `inference/`, `coding/`, `codebook/` (including the frozen file with s9), `data/`, `results/`, `.wayne`, pilot, gold or Fable paths, or the other coder | 0 |
| Coder labels written before the next part of the session was read | All 347 for A, all 347 for B |
| Every line of every assigned part returned to the agent | All 41 |
| Writes to label files other than through the gate | 0 |
| Adjudicator rulings written after a later part was read | 2 windows (`e10-t01`, `e13-t01`). Both followed a failed batched call; the failed calls held the same rulings. Redone (S08) |
| Directory listings | Own folder, or the `blind/` top level. That listing shows folder names plus `batches.json` and `index.json`, which hold no labels and were not opened. The e10 redo listed `blind/adjudication/` in the same call that read its brief (file names only) |
| Other exposure | Coder B batch 7 ran `wc -c` on its part files, so it saw byte sizes of later parts but not their content. The coder codebook keeps the project title and v1.1 s1's line that Q3–Q5 are reported as risk indicators, so coders knew the framing but not the mapping |

The audit first counted a failed `add_ruling` call as written, which hid the packet 6 breach that its adjudicator had reported. I fixed it to count only calls that returned `ok`, and that also found the packet 5 case. Separation is not enforced by the file system: transcripts show what agents did. The audit needs local transcripts, so `run_all.sh` does not rerun it, and the committed JSON is the record.

## Label frequencies, final, 347 windows

| Field | Labels |
|---|---|
| `decision` | D0 50, D1 52, D2 152, D3 45, D4 47, UNSETTLED 1 |
| `verification` | V0 269, V1 51, V2 4, V3 13, VX 7, UNSETTLED 3 |
| `uptake` | U1 66, U2 17, U3 32, U4 110, U5 1, U6 5, U7 74, U8 29, UX 10, UNSETTLED 3 |
| `prior_own_work` | VISIBLE_DRAFT 174, VISIBLE_PARTIAL 113, NONE_VISIBLE 60 |

Whole sessions contain `V2` (4) and `V3` (13), which the 100-window sample did not. These are counts, not rates of checking. Bet 5 owns what they mean.

## Still weak

1. **No human reading.** All of this is consistency between AI models.
2. **`verification` on C2,** κ 0.48 [0.17, 0.69].
3. **Adjudication leans to A,** 159 to 45, and adjudicators read H01 and H02 differently across packets.
4. **`prior_own_work`** has the most disputes (41): 30 are VISIBLE_DRAFT vs VISIBLE_PARTIAL, 10 are NONE_VISIBLE vs VISIBLE_PARTIAL, and 1 is NONE_VISIBLE vs VISIBLE_DRAFT (H06).
5. **Mixed views in the final file.** 52 windows keep labels coded from 3-turn views and a codebook that included s9; 295 come from full history without s9.
6. **Within-coder drift** across 16 batches is not measured.
7. **Sensitivity changes** cannot be split into view effect and coder noise.

## Files

`results/final_labels_nirvana.csv` · `results/labels_ab.csv` · `results/adjudication_log.csv` · `results/agreement.json`, `tables.md` · `results/sensitivity.json` · `results/overlap_audit.json`, `overlap_facts.csv` · `results/access_audit.json` · `decisions.tsv` (S01–S08) · `rule_gaps_for_v2.tsv` (H01–H15) · `coder_brief.md`, `adjudicator_brief.md`, `coder_codebook_v1.1.md` · `scripts/` · `blind/` (git-excluded: part files, coder notes, rulings, adjudicator gap notes)

## Gate

**First pass: failed, on one blocking problem.** A fresh critic with no access to my reasoning ran its own scripts. It found one false sentence: `prior_own_work` disputes are not all at the DRAFT vs PARTIAL line. The other five checks passed:
- Blindness, from its own audit of all 41 transcripts, with the two adjudicator breaches stated accurately.
- Traceability of every field (0 mismatches).
- Identical hashes on rerun, and its own κ.
- No dataset text in any committed version.
- Pre-stated rules S05 and S08.

I fixed the sentence and its minor points: the listing wording, the `wc -c` exposure, the rule column, the headline and the 158 count. No label or number changed. Report: `.wayne/bets/0007-nirvana-sessions/gate/critic_report.md`.

**Recheck:** pending.
