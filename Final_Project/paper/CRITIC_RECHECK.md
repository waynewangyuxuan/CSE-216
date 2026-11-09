# Independent recheck of the paper after fixes

Reviewed `main.tex` and its companion files at commit 5356000. Line numbers below are current ones. I edited no file except this one, pushed nothing and downloaded nothing. No dataset text appears in this report.

## Overall verdict: PASS

**0 blocking problems, 14 minor problems.** Every blocking finding is either fixed or correctly deferred to Wayne. All 14 minor problems have exact fixes below. The one number to correct first is N1: the NIRVANA-only rate is 0.50, not 0.51.

| Check | Result |
|---|---|
| CRITIC.md blocking findings (20) | 18 FIXED, 2 DEFERRED, 0 NOT FIXED |
| CRITIC.md minor findings (25) | 24 FIXED, 1 DEFERRED, 0 NOT FIXED |
| PROOFREAD.md rows (25) | 23 FIXED, 1 DEFERRED, 1 NOT FIXED (row 25, recorded as N14) |
| TODO_WAYNE.md section 7 | All four choices acceptable |
| Script checks | All pass; body 18 pages, total 25 |
| TeX log files left behind | None |
| Commits since e4c6ee1 touching `Reflection/` or `report/M2_draft.md` | 0 |
| No dataset text | 0 shared 8-word runs in all 5 files |
| Barriers against Limitations | 0 shared runs of 4 or more words |

## 1. Status of each finding

### CRITIC.md blocking

| # | Status | Where and notes |
|---|---|---|
| B1 | FIXED | L32 |
| B2 | FIXED | L451, matches `lit/framework_comparison.md` bottom line |
| B3 | FIXED | L70, L416, L459. Wording issues in N7 and N8 |
| B4 | FIXED | L396, L71, L334 |
| B5 | FIXED | L409. Wording issue in N9 |
| B6 | DEFERRED | L186 TODO; TODO_WAYNE section 1 item 4. L185 adds a precedent citation from `lit/` only (N10) |
| B7 | FIXED | L404 |
| B8 | FIXED | L138 |
| B9 | FIXED | L132 |
| B10 | FIXED | L105 |
| B11 | FIXED | L314. The text was added as specified, but its 0.51 is a rounding error (N1) |
| B12 | FIXED | L103 |
| B13 | FIXED | L95, L83, L105, L400 |
| B14 | FIXED | L368, L370. The motive is removed and recorded in section 7. The new heading traces to `report/M2_draft.md` L42 and `BRIEF.md` L22, but overstates (N2) |
| B15 | FIXED | L416, L422, L434 |
| B16 | FIXED | L434, L441 |
| B17 | FIXED | L71, L445 |
| B18 | FIXED | `CITATIONS.tsv`, `refs.bib` L15, L90. `alam2026` is disclosed rather than harmonized. That is acceptable, because the literature stage and the inference stage read different amounts and the paper's use is abstract-level. Bastani note in N11 |
| B19 | FIXED | SUPPLEMENT L31 |
| B20 | DEFERRED | L25, L98, L99, L133, L186, L364, L491, L492, L495; TODO_WAYNE sections 1 and 3; SUPPLEMENT section 2. `check_todos.py` confirms 9 of 9 listed |

### CRITIC.md minor

| # | Status | Where and notes |
|---|---|---|
| m1 | FIXED | No `p = 0.0005` remains |
| m2 | FIXED | L266, L276 |
| m3 | FIXED | L65, L317 |
| m4 | FIXED | L295, L298 |
| m5 | FIXED | L451 |
| m6 | FIXED | L441 |
| m7 | FIXED | L445 |
| m8 | FIXED | L459 |
| m9 | FIXED | New L382 paragraph; L406 keeps the effect on claims; "with more time" is at section level in L384, as m9 allowed. The framework-rater sentence stays in L406, which is acceptable because it is phrased as a claim constraint. Side effect in N3 and N4 |
| m10 | FIXED | L261, matches `report/narratives.md` sections 4 and 5 |
| m11 | FIXED | L406, matches `inference/FROZEN.md` |
| m12 | FIXED | L177 |
| m13 | FIXED | No "gold" remains in `main.tex`. SUPPLEMENT L18 still says "gold-set", but m13 was scoped to the paper |
| m14 | FIXED | L81 |
| m15 | FIXED | L152, L719 |
| m16 | FIXED | L321 |
| m17 | FIXED | L334, L348, L356. One leftover in N6 |
| m18 | FIXED | L81 is now grouped by trace type |
| m19 | FIXED | L3, TODO_WAYNE section 2. Page count now stale (N12) |
| m20 | FIXED | `CITATIONS.tsv` notes; years match `lit/related_work.md` |
| m21 | FIXED | L466, L478, L483 |
| m22 | DEFERRED | TODO_WAYNE section 7 |
| m24 | FIXED | SUPPLEMENT L5, section 2 item 2. Leftover in N13 |
| m25 | FIXED | L32, L117, L314 |
| m26 | FIXED | L422 |

### PROOFREAD.md

| Row | Status | Where and notes |
|---|---|---|
| 1 | FIXED | L90 |
| 2 | FIXED | L400 |
| 3 | FIXED | L319 |
| 4 | FIXED | L321 |
| 5 | FIXED | L681 |
| 6 | FIXED | L261 |
| 7 | FIXED | L459 |
| 8 | FIXED | L389 |
| 9 | FIXED | L204 |
| 10 | FIXED | L406 |
| 11 | DEFERRED | TODO_WAYNE section 7, acceptable |
| 12 | FIXED | L290 |
| 13 | FIXED | L232 |
| 14 | FIXED | L295 |
| 15 | FIXED | L298 |
| 16 | FIXED | L314 |
| 17 | FIXED | L348, as "not proposed", per m17 |
| 18 | FIXED | L704 |
| 19 | FIXED | L708, L709, L711, L713 |
| 20 | FIXED | L717, L718 |
| 21 | FIXED | L105 |
| 22 | FIXED | L235 |
| 23 | FIXED | L376 |
| 24 | FIXED | L451 |
| 25 | **NOT FIXED** | `refs.bib` L229 still has the stray space, and it is not listed in section 7. See N14 |
| Note (Padmakumar) | DEFERRED | TODO_WAYNE section 7, acceptable |

### TODO_WAYNE.md section 7: are the choices acceptable?

| Item | Verdict |
|---|---|
| Title (m22) | Acceptable. The critic left it to Wayne, and L394 states what is not measured |
| Serial commas (row 11) | Acceptable. A consistency matter, not an error |
| Padmakumar given names | Acceptable. The registry lacks them, and inventing them would be worse |
| Barriers motive "to save two hours" | Acceptable. Removal is the safe default, and the item says how to restore it |

## 2. Numbers and sentences re-verified

| Item | Source | Result |
|---|---|---|
| Pooled next-window rates 0.21, 0.65 | `mining.md` s3; recomputed with `mine.pairs` | Correct: 19/89 = 0.2135, 101/156 = 0.6474 |
| NIRVANA-only **0.24 and 0.51** | `SKEPTIC_T.md` C11 gives 0.237, 0.505; recomputed | 0.24 correct (18/76 = 0.2368). **0.51 is wrong:** 54/107 = 0.5047, which rounds to 0.50. Double rounding through 0.505. See N1 |
| 16-session rates 0.18, 0.26 | `SKEPTIC_T.md` C11; recomputed | Correct: 9/51 = 0.1765, 7/27 = 0.2593. The 16 are 15 NIRVANA and 1 WildChat (N1) |
| Nine of 35 articles; all 3 audit rejections among them | `wildchat/REPORT.md` Sample, Precision | Correct |
| 43 labels record Claude Sonnet 5 | `wildchat/REPORT.md` Dataset, Screen labeller | Correct (43 of 4,052) |
| Barrier: WildChat coder batch, 24 windows | `wildchat/REPORT.md` Coder separation | Correct (20 one ahead, 4 two ahead). Omits that those labels were not redone (N3) |
| Barrier: two NIRVANA adjudicators, redone, same result | `sessions/REPORT.md` Bottom line, Blindness | Correct |
| Barrier: one WildChat adjudicator, partial reads, not redone | `wildchat/REPORT.md` Coder separation | Correct |
| Barrier: "Transcript audits found all of this" | `sessions/REPORT.md` Blindness | Slightly over: one breach was reported by its adjudicator and first hidden by an audit bug (N3) |
| "Not established" paragraph, L451 | `lit/framework_comparison.md` Bottom line and section 3; `report/M2_draft.md` s4 | Correct: 3 pairs (1, 2, 7); NIRVANA separates 1 and 2; pair 7 could not fail. 30 of 32 and 44 of 52 match `patterns.md` s1 |
| `CITATIONS.tsv` notes: `alam2026` | `lit/papers.csv`, `inference/sources.tsv`, framework comparison | Correct. The paper's two uses are abstract-level |
| `CITATIONS.tsv` notes: `contractor2026` | `inference/sources.tsv` | Correct |
| `CITATIONS.tsv` notes: `bastani2025` | `inference/sources.tsv`, `lit/citation_check.csv` | Page list incomplete, and "not read" conflicts with the literature-stage record (N11) |
| `CITATIONS.tsv` notes: `jelson2026chi`, `joshi2025` | `lit/related_work.md`, `refs.bib` | Correct |
| L314 transitions; 17 of 29, 2 of 21 | `mining.md` s3, s6; `SKEPTIC_T.md` C13 | Correct |
| Multi-window figures, L284, L303 | `mining.md` s10 | Correct |
| L295, L298 pooled labels; 27 of 29 exits | `mining.md` s3, s4; `SKEPTIC_T.md` C7 | Correct; the NIRVANA rows sum to 27 |
| Trigger figures, L334 and table | `mining.md` s9, s10 | Correct |
| Rewritten L81 | `lit/related_work.md`; Yang abstract in `lit/screening` | Supported at each source's read level |
| L185 "Cohen's kappa, as in prior studies" | `lit/related_work.md` L68; `lit/framework_comparison.md` L97 | Those records show kappa was reported, not that it was Cohen's (N10) |

## 3. New problems, with exact fixes

No blocking problem. All are minor.

**N1. L314: 0.51 should be 0.50, and the 16 sessions are not labeled.** Replace "and 0.24 against 0.51 in NIRVANA alone" with "and 0.24 against 0.50 in NIRVANA alone". Replace "in the 16 sessions where the draft flag varies" with "in the 16 sessions (15 in NIRVANA) where the draft flag varies".

**N2. L370: the heading and one sentence overstate.** `data/REPORT.md` records LLM-clear at 1.72% of English records and 1,704 rule-clear conversations corpus-wide, all unverified, so "WildChat held too few" is not shown at corpus level. The proposal named this as a risk, and the M2 draft gives it as the reason. Replace the heading with `\paragraph{The research-writing sample fell short and could not be reproduced.}`. Replace "WildChat held too few genuine research-writing conversations for the plan." with "Milestone 1's count was below the proposal's target of 100 and no person had verified it, and too few genuine research-writing conversations was the risk the proposal had named."

**N3. L382: who found what, and one omission.** Replace "One WildChat coder batch read ahead on 24 windows." with "One WildChat coder batch read ahead on 24 windows, and its labels were not redone." Replace "Transcript audits found all of this." with "Transcript audits and critic reads of the transcripts found these, except one NIRVANA breach, which its adjudicator reported and the first audit script missed."

**N4. L384 no longer fits the new Barrier.** That Barrier is an explicit rule that was broken, and part of it was not recovered. Replace "Every recovery above was possible" with "Most recoveries above were possible". Replace "left implicit: a target, a screen, a view, an index." with "left implicit or enforced only by instruction: a target, a screen, a view, an index, a reading order."

**N5. L334: the table does not hold four rules, and Figure 5 is never cited.** The table has three rules and their union, and `fig:triggers` has no `\ref`. Replace the first sentence of the paragraph with "Four rules were computed from the NIRVANA keystroke log alone, with no codes and no text, of which two are proposed as triggers (Table~\ref{tab:triggers}, Figure~\ref{fig:triggers})."

**N6. L400: leftover from m17.** Replace "and 4 triggers without correction" with "and 4 log-only rules without correction".

**N7. L70: "speed" conflicts with "time".** Dwell does differ across the categories, and only the copy does not. Replace "pasting and speed do not separate" with "pasting and time to first copy do not separate".

**N8. L416: "that side" collides with "support side".** Replace "so that side of the boundary follows from their definition" with "so that part of the boundary follows from their definition".

**N9. L409: "roughly halves" is loose.** It traces to `THESES.md` C9, but 0.256 is 64% of 0.401. Replace "although the own-work link roughly halves on multi-window sessions" with "although the own-work link weakens from 0.40 to 0.26 on multi-window sessions".

**N10. L185: claim slightly beyond the record.** Replace the sentence with "Agreement is Cohen's $\kappa$, with bootstrapped intervals over 2,000 draws and sessions as the resampling unit where sessions matter; prior studies that code prompts also report $\kappa$ \cite{jelson2026chi,poquet2026}."

**N11. `CITATIONS.tsv` Bastani note.** `inference/sources.tsv` lists pp. 11 and 13-15 read, and `lit/citation_check.csv` records PMC abstract and introduction read at the literature stage. In `scripts/build_refs.py` `NOTES`, set `bastani2025` to "PMC abstract and introduction read at the literature stage (lit/citation_check.csv); PMC later blocked by reCAPTCHA, so the working-paper version on a third-party host was read for the rules (abstract, pp. 11, 13-15; cited pp. 2, 14, 15, per inference/sources.tsv); PNAS version of record not read in full". Then regenerate.

**N12. TODO_WAYNE section 2: stale count.** Replace "17 body pages, 24 total" with "18 body pages, 25 total".

**N13. SUPPLEMENT section 2 item 2.** An agent-internal sentence sits in Wayne's list. Delete "The parent session pushes after verifying."

**N14. `refs.bib` L229 (PROOFREAD row 25): stray space prints in the reference list.** It comes from the registry title, so a hand edit would be overwritten. In `scripts/build_refs.py`, add `"AI -assisted": "AI-assisted"` handling after the `CLEAN` replacements, then regenerate. Check against the published title. Fix this before submission, since the rubric penalizes spelling errors.

## 4. Scripts and repository state

| Command | Result |
|---|---|
| `python3 scripts/spellcheck.py` | Pass: 1,998 distinct words, 2 allowlisted |
| `python3 scripts/check_tex.py` | Pass: about 7,523 body words, 5 figures, 9 tables |
| `python3 scripts/check_todos.py` | Pass: 9 TODOs, 9 listed |
| `python3 scripts/check_build.py` | Pass: **18 body pages**, 25 total, no overfull lines over 2.0 pt, 44 missing-field warnings (registry gaps, nothing invented) |
| `python3 Final_Project/paper/scripts/check_supplement.py` | Before this file existed: 93 paths, 81 tracked, 11 local only, and 1 missing, which was this file (exit 1). After writing it: 0 missing, exit 0, with this file local until committed. The 11 other local paths are marked local in the table |

No `.log`, `.aux`, `.blg`, `.bbl`, `.out`, `.xdv`, `.fls`, `.fdb_latexmk` or `.synctex` file exists under `Final_Project/paper` after the build check. `git log e4c6ee1..HEAD -- Reflection Final_Project/report/M2_draft.md` is empty. The working-tree changes to `Reflection/` are uncommitted and are not part of any paper commit.

## 5. No dataset text

Scratch script outside the repository, logic copied from `check_no_text.py`, counts only. `windows.jsonl` was read both raw and as parsed JSON strings, because JSON escapes can break word runs.

| File | `sessions/blind/parts` (347 files) | `wildchat/blind/views` (151 files) | `windows.jsonl` raw | `windows.jsonl` parsed |
|---|---|---|---|---|
| main.tex | 0 | 0 | 0 | 0 |
| SUPPLEMENT.md | 0 | 0 | 0 | 0 |
| TODO_WAYNE.md | 0 | 0 | 0 | 0 |
| CITATIONS.tsv | 0 | 0 | 0 | 0 |
| refs.bib | 0 | 0 | 0 | 0 |

## 6. Standing constraints

- **No human coded data:** stated at L32, L55, L389, L480 and L490, with no agreement called human.
- **Findings direct, caveats collected:** yes. I did not ask for caveats on individual sentences.
- **Citations only from `lit/`:** yes, 32 keys. B6 awaits Wayne's approval.
- **Barriers are process, Limitations are claims:** yes, with no repeated text. The new protocol Barrier gives the events, and L406 gives only the effect on claims.
- **AI Use Statement:** claims no human review. L483's "A fresh critic rechecked the edits" is true as of this report for the edits in 5356000. It would not cover later edits, such as the fixes above, unless they are rechecked too.
- **Statements about Wayne:** L488 matches `product.md` decisions 1, 4, 6, 7, 8 and 12. The "with more time" and "What I learned" sentences are agent-drafted and are covered by the section-level TODO at L364.
