# WildChat formal writing (Bet 7)

Numbers come from `scripts/run_all.sh`, which replays cached labels and calls no model. Rerunning it gives byte-identical results files (checked, see Gate).

**Every judgment here is an AI's.** The screen, the audit, both coders and the adjudicator are Claude models. Precision is one model's agreement with another, and coder agreement is AI-to-AI consistency. No human read any conversation or checked any label. No window has an offloading or surrender label; that is Bet 5's job.

## Bottom line

- **The screen is precise but finds only a small share.** The auditor agrees on 118 of 120 random accepted conversations (98.3%, CI 94–99.5%). Formal long-form writing is about 10% of eligible conversations, so roughly 14,000 exist, and the accepted pool of 2,236 holds roughly 12–16% of them.
- **The coded sample is new, random and whole.** 35 conversations and 151 windows, drawn only from the random seed, so keyword and embedding ranking cannot bias it. The auditor rejects 3 of the 35 (9 windows); their labels stay.
- **The coders agree closely.** On Q3–Q5, κ is 0.92 for `decision`, 0.94 for `verification` and 0.92 for `uptake`. On follow-up windows it is 0.83 to 0.94, and no Q3–Q5 session interval drops below 0.61. `prior_own_work` (0.75) and `object` (0.76) are the weakest.
- **19 fields are `UNSETTLED`**, 11 of them `prior_own_work`, from gaps in v1.1 (`rule_gaps_v1_1.tsv`).
- **No stop condition was hit.**

## Definition

`DEFINITION.md`, committed in `c00b797` before any record was labelled. Its hash is logged as `decisions.tsv` W01.

| Part | Rule |
|---|---|
| Include | The user produces or revises an extended formal text: essay, research paper or a section of one, report, thesis, literature review, proposal or business plan, article for publication, or formal statement. Asking the AI to write all of it counts |
| Exclude | Fiction and poetry, emails and letters, CVs, marketing and SEO copy, speeches and slides, short answers, code, translation only, reading summaries, chat with no target text |
| Boundary calls | Expository blog articles count; promotional ones don't. One paragraph of a longer document counts. "Answer in N words" counts only at several paragraphs. A mixed conversation counts if any part qualifies |
| Mechanical | WildChat-1M non-toxic release, English, at least 2 non-blank user turns, a user turn after the first writing turn (W02), not used in Bet 4 or the codebook pilot, deduplicated |

## Funnel

| Step | Records | Note |
|---|---|---|
| WildChat-1M | 837,989 | Pinned revision. `toxic` is false on every record |
| Not English | −359,491 | |
| Under 2 non-blank user turns | −321,381 | |
| Duplicate hash or first turn | −17,381 | |
| **Eligible** | **139,736** | 72 already used in Bet 4 or the pilot are kept out of selection. 4,014 contact patterns are masked |
| Random seed, LLM-labelled | 1,200 | INCLUDE 120 (10.0%, CI 8.4–11.8%), UNSURE 16. 114 pass the follow-up rule |
| Enrichment, LLM-labelled | 600 | From the top 6,000 of a first ranking. INCLUDE 384. Used for training only |
| Ranked by embeddings + keywords | 139,664 | Logistic regression trained on 1,204 labels |
| Top 2,500, LLM-confirmed | 2,500 | INCLUDE 2,039, and 1,975 pass the follow-up rule. Per 500-rank band, 462 falling to 365 |
| **Accepted pool (unused)** | **2,236** | 114 from the seed, 367 from enrichment, 1,755 from confirmation |
| Coded sample | 35 conversations, 151 windows | From the seed's 114 only |

- **Screen labeller.** Requested `claude-sonnet-5-5` through `claude -p` (CLI 2.1.318), tools off. 43 of 4,052 labels (23 in the seed) record `claude-sonnet-5` alongside it as served (cause not known); the label model is not separable per row. It reads the whole conversation, with user turns cut to 1,500 characters and AI turns to 500 (W05). Prompt: `scripts/screen_prompt.txt`.
- **Embeddings.** `BAAI/bge-small-en-v1.5`, revision `5c38ec7c`, sentence-transformers 3.3.1 on MPS. Input is masked user text, first 2,000 characters (W07, `results/embed_meta.json`).
- **Bet 1's 2,399 cached labels** aren't reused as labels (W04): they used a research-only definition on the first 3 user turns. The 281 eligible records of Bet 1's random draw are in the seed. On them, old `CLEAR_RESEARCH_WRITING` maps to INCLUDE 6 of 8, while 15 of 113 old `OTHER_WRITING` or `ACADEMIC_NOT_RESEARCH` records are now INCLUDE.
- **Model cost** was $33.70 in all (`results/llm_cost_log.tsv`). Coder and adjudicator runs are not in it.

## Precision and recall

The auditor is `claude-opus-5-5` with its own prompt (`scripts/audit_prompt.txt`), run as fresh processes. It saw all 415 audited records in one seeded shuffled order, sent in 21 batches of about 20, never saw screen labels, and was not told which set a record came from.

| Audit set | n | Auditor INCLUDE | Share [95% CI] | Reads as |
|---|---|---|---|---|
| Random accepted | 120 | 118 | 98.3% [94.1, 99.5] | **Precision of the pool** |
| Coded sample | 35 | 32 | 91.4% [77.6, 97.0] | Precision of the coded set |
| Random confirm rejects | 100 | 29 | 29.0% [21.0, 38.5] | The screen is cautious near the cut |
| Random never-labelled | 150 | 17 | 11.3% [7.2, 17.4] | Matches the seed's 10% |

- **Screen vs auditor** on the 265 records both labelled: 88.7% agree, κ 0.74. Disagreements go mostly one way: the screen said EXCLUDE and the auditor INCLUDE on 20, against 5 the other way.
- **Recall is rough, about 12%.** Estimated true positives found: 2,198. Estimated misses: 523 among labelled rejects and about 15,300 among never-labelled records. As a second check, 10 of the 56 held-out seed positives rank in the top 2,500 (18%). The confirm pass stops at 2,500, and its INCLUDE rate is still 71% at ranks 2,000–2,500 (counting only records first labelled there), so a deeper cut would find more. "2,500 confirmed" includes 259 records already labelled in the seed or enrichment, with the same prompt.
- **The 3 coded conversations the auditor rejects** are all ones the screen called `article`. They are `d429342fd747`, `8af2896cda07` and `e6acb3ce8d84`: the auditor read them as other, fiction and marketing, together 9 windows. The article boundary is the screen's soft spot.

## Sample

| Item | Value |
|---|---|
| Conversations | 35, one per IP cluster, from the seed's 114 accepted (W10) |
| Windows coded | 151: 119 `C1`, 32 `C0`, 0 `CX` |
| Cap | Turns 1 to 10 only (W11). 3 conversations were capped, leaving 20 later turns uncoded |
| User turns per conversation | median 4, range 2 to 17 |
| Screen genre | article 9, essay 8, research paper 8, report 3, proposal 3, literature review 2, thesis 1, other 1 |
| Not reused | No conversation from Bet 4 or the codebook pilot |

## Coding

| Role | Requested | Served (transcripts) | Runs |
|---|---|---|---|
| Coder A | `opus` | `claude-opus-5-5` | 4 fresh agents, one per batch |
| Coder B | `sonnet` | `claude-sonnet-5-5` | 4 fresh agents, one per batch |
| Adjudicator | `opus` | `claude-opus-5-5` | 1 fresh agent |

Views are one part file per window: request, response and next user turn, uncut, with contacts masked (W12). Coders read parts in order, so parts 1 to N give the full history up to window N. Batches are whole conversations, about 145 KB each. The coder brief and adjudicator brief adapt Bet 4's to part files. v1.1 is unchanged.

## Agreement, A vs B

2,000-draw bootstrap with a fixed seed. Session = conversation. The full tables are in `results/agreement_tables_wildchat.md`.

| Field | n | % | κ | κ CI, windows | κ CI, conversations | Follow-up `C1` κ (n=119) [conv CI] |
|---|---|---|---|---|---|---|
| `domain` | 151 | 90.7 | 0.86 | [0.79, 0.92] | [0.69, 0.97] | 0.87 [0.71, 0.97] |
| `family` (Q1) | 151 | 90.7 | 0.85 | [0.78, 0.92] | [0.69, 0.96] | 0.82 [0.64, 0.95] |
| `operation` (Q1) | 151 | 90.1 | 0.85 | [0.78, 0.92] | [0.69, 0.95] | 0.83 [0.67, 0.95] |
| `process` (derived) | 151 | 92.7 | 0.88 | [0.80, 0.94] | [0.70, 0.99] | 0.85 [0.66, 0.99] |
| `function` (Q2) | 151 | 95.4 | 0.92 | [0.85, 0.97] | [0.82, 0.99] | 0.90 [0.79, 1.0] |
| `object` (Q2) | 151 | 90.1 | 0.76 | [0.64, 0.86] | [0.51, 0.94] | 0.74 [0.49, 0.93] |
| `prior_own_work` | 151 | 85.4 | 0.75 | [0.66, 0.84] | [0.60, 0.89] | 0.75 [0.57, 0.91] |
| `decision` (Q3) | 151 | 96.7 | 0.92 | [0.85, 0.98] | [0.83, 0.99] | 0.94 [0.84, 1.0] |
| `verification` (Q4) | 151 | 97.4 | 0.94 | [0.88, 0.99] | [0.88, 0.99] | 0.83 [0.61, 0.96] |
| `uptake` (Q5) | 151 | 94.7 | 0.92 | [0.86, 0.97] | [0.86, 0.97] | 0.86 [0.77, 0.95] |

- **`C0` forces `VX` and `UX`**, which lifts all-window κ on Q4 and Q5. Read the follow-up column.
- **`verification` rests on `V0` and `V1`.** Final labels: V0 107, V1 11, V2 1, VX 32, and no V3 or V4. A 0.83 does not test grading the grounds of a check.
- **Main confusions:** `prior_own_work` UNOBSERVABLE vs PARTIAL 11 and DRAFT vs PARTIAL 11; `uptake` U4 vs U8 7; `domain` ACADEMIC_STATED vs OTHER_WRITING 7.
- **High agreement between models is not evidence that labels are right.** Same-family models, and rules tightened in earlier rounds, could both push it up.

**Final labels** (`results/final_labels_wildchat.csv`): `decision` D0 7, D1 35, D2 108, D3 1. `uptake` U4 43, U6 1, U8 73, UX 32, UNSETTLED 2. `domain` OTHER_WRITING 66, RESEARCH_EXPLICIT 47, DOMAIN_UNKNOWN 18, ACADEMIC_STATED 15, UNSETTLED 5. `prior_own_work` UNOBSERVABLE 79, VISIBLE_DRAFT 38, VISIBLE_PARTIAL 23, UNSETTLED 11. This sample is not an estimate of all WildChat writing windows: long conversations are capped and IP clusters limited.

## Adjudication

| | Count |
|---|---|
| Windows with any disagreement | 64 of 151 |
| Disputed fields | 90 of 1,208 |
| Ruled for A / for B | 54 / 17 |
| Third code | 0 |
| `UNSETTLED` | 19: `prior_own_work` 11, `domain` 5, `uptake` 2, `object` 1 |

- **54 to 17 favours A, the adjudicator's own requested model.** Coders were shown as first and second with a seeded flip, and identity was never shown. A same-model preference still can't be ruled out. It is stronger than Bet 4's 25 to 13.
- **Every final label traces** to A=B or a row of `results/adjudication_log_wildchat.csv` (checked by `12_finalize.py`, 0 problems). Free-text reasons stay in git-excluded `blind/`.
- **Rule gaps** go to `rule_gaps_v1_1.tsv` (G1–G7) for a later codebook. v1.1 did not change.

## Coder separation

From transcripts, by `scripts/audit_access.py` → `results/access_audit.json`.

| Check | Result |
|---|---|
| Paths outside each agent's allowed set (other coder, results, screen labels, `inference/`, `data/`, `coding/`) | 0 of 9 agents |
| Served model matches requested | 9 of 9 |
| Label written before the next part was read | 7 of 8 coders on every window. Coder B batch 3 read one part ahead on 20 windows and two ahead on 4, and wrote 3 windows of `953148aa3d57` in one loop with identical codes |
| A and B ran in parallel, in separate folders | Yes |

One part ahead shows the next AI response and the user turn after it, so B batch 3 saw later turns on 24 windows. It broke the read-in-order rule, and its labels were not redone. The adjudicator read parts up to each conversation's highest disputed turn, so for lower windows it may have seen later turns. It also often read long parts only partly, through `head` or `grep` extracts (for example about 198 of 483 lines on one conversation), against its brief. Its rulings rest on partial reads in those cases; they were not redone. Separation is by instruction, not by file permissions.

## Bet 4's 30 windows, re-judged

Bet 4's 30 WildChat windows come from 11 conversations. Both the screen labeller and the auditor judged these conversations against the new definition. **No Bet 4 label was changed.**

| | INCLUDE | EXCLUDE |
|---|---|---|
| Screen (`sonnet`) | 10 | 1 |
| Auditor (`opus`) | 11 | 0 |

- `2d9abc984de9` is the split case: the screen says short answer, the auditor says report. Fable rejected the same conversation's window as research writing in Bet 4. It is a boundary case under either definition.
- Under the wider definition, all of Bet 4's conversations count as writing for at least one judge. Fable's 2-of-6 doubt was about *research* writing, which this definition no longer asks for.

## Still weak

1. **No human has checked anything.** Precision, recall and agreement are all Claude models judging Claude models.
2. **The screen and auditor are one model family.** Different sizes and prompts reduce shared bias, but they don't remove it.
3. **Recall is about 12%, and rough.** The accepted pool of 2,236 is not "all formal writing in WildChat"; it leans to high-ranked, keyword-like conversations. The coded sample avoids this by drawing from the random seed.
4. **The article boundary is soft.** All 3 audit rejections in the coded sample are screen "articles".
5. **`prior_own_work` and `domain` are weak.** Their κ is 0.75 and 0.86, they hold 16 of the 19 `UNSETTLED`, and `domain` is no longer a reporting split (Nov 7 direction).
6. **The adjudicator favoured its own model 54 to 17.** This can't be told apart from rule fit.
7. **Coder B batch 3 read ahead** on 24 windows, and the adjudicator read some parts only partly.
8. **Within-coder drift** across batches is not measured.
9. **Checks are almost absent.** 1 `V2`, and no V3 or V4.

## For Bet 5 and Bet 8

- Use `results/final_labels_wildchat.csv`. Keep the 19 `UNSETTLED` fields out, or run both readings.
- Report sessions as clusters (35 conversations). The 9 windows of `d429342fd747`, `8af2896cda07` and `e6acb3ce8d84` may be out of scope; run with and without them.
- Window ids follow Bet 4's form (`WILDCHAT-<12 hex>-tNN`). None overlap Bet 4's.

## Files

`DEFINITION.md` · `decisions.tsv` · `rule_gaps_v1_1.tsv` · `coder_brief.md`, `adjudicator_brief.md` · `results/` holds ids, hashes, labels and counts only: `funnel.json`, `funnel_eligible.json`, `screen_labels.jsonl`, `audit_labels.jsonl`, `audit_sets.tsv`, `seed_ids.tsv`, `rank_*.tsv`, `selected_conversations.tsv`, `windows_wildchat.csv`, `labels_ab_wildchat.csv`, `final_labels_wildchat.csv`, `adjudication_log_wildchat.csv`, `agreement_wildchat.json`, `agreement_tables_wildchat.md`, `access_audit.json`, `agents.tsv`, `embed_meta.json`, `llm_cost_log.tsv` · `scripts/` (`run_all.sh`, `check_staged.py`, `commit_paths.sh`) · `blind/` (git-excluded: text, embeddings, views, coder notes, rulings).

## Gate

**Passed**, by a fresh critic agent with no access to my reasoning (`.wayne/bets/0008-wildchat-writing/gate/critic_report.md`). It found:

- The definition was committed before any screen label and has not changed since.
- `run_all.sh` gives 16 of 16 results hashes identical to HEAD, and its own script reproduced every checked number.
- The audit used a separate model and prompt and was drawn by seeded script.
- No coder touched another coder's files, results, `inference/`, `data/`, `coding/` or `sessions/`, from reading all 9 transcripts.
- All 1,208 final fields trace.
- 0 of 40 random snippets from the selected conversations are in git history.

No blocking problems. These corrections came from it and are made above: B batch 3 read ahead on 24 windows, not 22; reading ahead also shows the next user turn; the adjudicator read some parts partly; 43 labels record a second served model; the 71% band; batched audit input; and the 0.61 floor holds for Q3–Q5 only.

`check_staged.py` then flagged 3 false positives: the definition's own list of paper section names also occurs in two users' text. The check now leaves out runs found in `DEFINITION.md` as committed before any conversation was read, and `--all-tracked` gives 0 problems. `audit_access.py` now parses loop-written window ids. No critic rechecked these fixes.
