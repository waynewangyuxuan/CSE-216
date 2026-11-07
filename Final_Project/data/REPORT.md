# Data usability report (Bet 1, for checkpoint C1)

Counts come from `counts.json`, rebuilt by `scripts/run_all.sh`. The rebuild replays cached LLM labels and does not reproduce them. Nothing here has been coded, and no human has checked any screening result.

## Bottom line

- **Enough data to proceed.** All 347 NIRVANA windows pass the mechanical check (a non-blank request and response); codebook eligibility is left to coding, so "Hi" and "ok" still count. WildChat adds 1,460 windows from screened candidates, unverified by a human. The sample of 100 and gold set of 20 are ready.
- **347 holds, "from 77 students" does not.** The windows come from **71** students. M1 reported 77, so M2 needs a correction.
- **WildChat can support the project, but only on unverified LLM screening.** The draw's clear count sits near the report (41 vs 42), but possible does not (69 vs 40), and 21 of the 41 are not in English. Treat the match as unconfirmed.
- **ScholaWrite works as a vocabulary check.** 15 labels and its fields are confirmed from data. It has no AI interaction.

## Decisions needed from you

1. **Correct "77 students" to 71 in M2.** This contradicts something already submitted, which is a stop condition. Nothing submitted was changed here. Also, "347 distinct" holds by request event; by text within a student it is 343.
2. **Sample split of 70 NIRVANA + 30 WildChat.** This was a judgment call (D15), and it is yours to change.
3. **Before any commit, exclude the text outputs.** `windows.jsonl`, `sample.csv` and `gold.csv` hold dataset text outside the git-excluded `raw/` folder, and the repo is treated as public. The NIRVANA OSF node showed no license through its API. Keep `wildchat_llm_screen.jsonl` somewhere durable, since rebuilds need it. It holds hashes and labels only, no conversation text. I did not change `.git/info/exclude`, since it is outside this bet's folders. Nothing was committed.

## Reported vs rebuilt

| Item | Reported in M1 | Rebuilt | Note |
|---|---|---|---|
| NIRVANA windows | 347 | **347** (0% off) | Log has 348 request rows; essay 69 logs one block twice |
| NIRVANA students | 77 | **71** with windows | The other 6 (essays 2, 8, 21, 23, 45, 52) never asked ChatGPT |
| WildChat screened | 2,000 | Rules: all 837,989 records. LLM: 2,399 of them | Original draw method lost, so this is not a replication |
| WildChat clear + possible | 42 + 40 | LLM on draw: **41 + 69**. Rules on draw: **3 + 15** | See below |
| ScholaWrite labels | 15 | **15**, from data | 61,504 rows, 5 projects |

The 347 also matches the participant sheet's `GPT Inquiry` column, student by student. That is a separate column, but it may derive from the same log. The rebuild was not blind: I knew 347, and I wrote the duplicate rule after inspecting the log. The count is 347 under either duplicate key I tried.

| Reading | Windows |
|---|---|
| All usable | 347 |
| Distinct request text within a student | 343 |
| Excluding requests of 2 words or fewer ("Hi", "ok") | 341 |
| With editor action after the response (C2) | 204 |
| C2 with text shared with this response alone | 109 |

C2 linkage: 109 share a run of 30+ characters with this response alone, 10 share text also found earlier, and 85 show no such match in their added text. Those 85 can still hold pastes from elsewhere, reworded text, or a matching run assembled through edits. The first edit came a median 15 seconds after the response, with 14 windows over 2 minutes and a maximum of 457 seconds. Windows are uneven: 15 students have one, and the top two have 23 and 27. Only 56 students have two or more, so only they can show a transition.

## Coverage

| | C0 no follow-up | C1 chat only | C2 editor | CX unusable | Sessions |
|---|---|---|---|---|---|
| NIRVANA, all | 7 | 136 | 204 | 0 | 71 students |
| WildChat, windowed | 302 | 1,158 | 0 | 15 | 296 conversations |
| Sample (100) | 3 + 5 | 32 + 25 | 35 + 0 | 0 | 26 students + 11 conversations |
| Gold (20) | 1 + 1 | 6 + 5 | 7 + 0 | 0 | 14 students + 6 conversations |

Sample and gold cells show NIRVANA + WildChat. The 15 CX windows have blank requests.

## WildChat screen

Criteria are in `scripts/02_wildchat_screen.py`. The record-level log is `wildchat_draw2000_log.tsv`.

| Full corpus (A) | Records |
|---|---|
| Screened (826,319 distinct hashes) | 837,989 |
| Not English | 359,491 |
| No rule hit | 467,996 |
| Fiction, media, marketing or code context | 2,479 |
| Email or phone pattern | 189 |
| Duplicate hash or first request, among rule hits | 5 + 1,036 |
| **Included: clear / possible** | **1,704 / 5,089** |

| 2,000 draw (B) | Rules | LLM |
|---|---|---|
| Clear | 3 | 41 (20 in English) |
| Possible | 15 | 69 (34 in English) |

- **LLM marking.** Requested model `claude-sonnet-5-5` (the served model was not recorded per row) through Claude Code CLI 2.1.318, tools off, 25 conversations per batch, prompt in `scripts/wildchat_llm_prompt.txt`, input is the first 3 user turns at 600 characters each with emails and phones masked. Temperature and seed cannot be set, so results are cached. The run log showed $3.51. **No human has verified any of it.**
- **The clear-count match may be chance.** It uses a new prompt on a different draw. In English the total is 54 against 82 reported, and the old language handling is lost.
- **Rate.** LLM clear is 2.05% of the draw (95% CI 1.52–2.77), and 1.72% among English records (CI 1.12–2.65). One draw record got no label.
- **Keyword rules miss most cases, if the LLM is right.** Of the 20 English LLM-clear conversations, the rules caught 5 (one then dropped for a contact pattern), and 15 had no rule hit.
- **Rules vs LLM agreement, not precision.** On a seeded 300 clear multi-turn conversations the LLM called 230 clear and 23 possible. On a seeded 100 possible, it called 24 clear and 11 possible.
- **Windows are keyword-biased.** Only conversations passing both filters were windowed, and the 44 English LLM positives with no rule hit were not. Of the 1,460 usable windows, 1,262 are from LLM-clear conversations and 198 from LLM-possible; the sample uses clear only. One conversation gives up to 35 usable windows, and one IP cluster up to 65. More could be screened if needed.

## ScholaWrite

Fields in the data: `project`, `timestamp`, `author`, `before text`, `after text`, `label`, `high-level`. The 15 labels in the data match the paper and the authors' repo exactly. The user got access and the download used their local login. No field records AI interaction. No baseline analysis was done.

## Which dataset supports which question

| | Q1 operation | Q2 delegation | Q3 decision | Q4 verification | Q5 uptake |
|---|---|---|---|---|---|
| **NIRVANA** | Yes | Yes | Yes, with chat and editor evidence | Partly: only checks visible in chat or edits; outside browsing is unseen | Yes on C2, strongest on the 109; C1 is chat only |
| **WildChat** | Yes | Yes | Only when the writer replies (C1) | Only explicit replies | Chat codes only (U4/U5/U6); no editor evidence |
| **ScholaWrite** | Vocabulary check only | No | No | No | No |

NIRVANA is a timed essay, not research writing. WildChat has the research domain, but no verified identity, no editor and no way to know whether text was used. The two must stay separated, as the codebook requires.

## Known problems

- **Windows from one student are not independent.** The sample has up to 3 consecutive windows per session, so statistics must treat sessions as clusters.
- **The sample is not an estimate of all windows.** For NIRVANA, C0 is 4.3% vs 2.0% overall (two runs were forced to end on C0), C1 is 45.7% vs 39.2%, and C2 is 50.0% vs 58.8%. The 15 one-window students cannot enter, and heavy users are underweighted.
- **WildChat conversations were screened on their first 3 user turns.** Later turns may be off topic, and runs begin at the conversation start. `participant_id` is an IP cluster, not a person.
- **C2 is not proof of uptake.** 85 of 204 C2 windows have no text match, and shared text does not show why it was reused. No time cap or new-goal test is applied to the span.
- **CX tests blank text only.** Truncated responses, which the codebook treats as CX, are not detected. As a rough signal, 187 of 1,460 WildChat responses end without closing punctuation, against 5 of 347 for NIRVANA, so some WildChat C0/C1 windows may be truncated.
- **Raw NIRVANA defects.** 30 duplicate rows were dropped (essays 69 and 76). 26 rows have shifted or merged columns, 2 of them among those dropped. Merged rows can hide a following op, and these are flagged, not repaired. They touch 11 windows: 1 in the sample (`NIRVANA-e29-t08`), none in gold. Text cells also carry log artifacts (a stray closing quote, literal `\\n`). `next_actions_text` cleans most of these for reading and leaves out empty typed or deleted ops; a few leftovers remain in `NIRVANA-e71-t01`, and `windows.jsonl` keeps raw values. 24 essays have log times past 30 minutes (longest 5,010 seconds), and 23 by the sheet's Total Time, so "30-minute essay" needs checking.
- **`episode_id` and WildChat `domain` are empty.** Assigning them takes judgment, which belongs to coding. The codebook's domain stratification is not done for WildChat.
- **Personal details.** The screen's regex covers emails and phones in user turns. A scan of sample and gold finds none, but 8 WildChat windows in `windows.jsonl` match in their text. Names could remain anywhere, so read WildChat text with care.
- **Toxic WildChat records were not screened.** They are only in the manually gated Full version.

## Files

`windows.jsonl` all windows with raw-row traces (holds linkage and LLM labels, so don't give it to blind coders) · `sample.csv` · `gold.csv` request, response, cleaned action text and coverage · `decisions.tsv` · `counts.json` · `wildchat_draw2000_log.tsv` · `wildchat_llm_screen.jsonl` · `scripts/` (`run_all.sh` rebuilds all without calling a model, given the kept LLM cache and the gated ScholaWrite download; `00_fetch.sh` gives the command).

## Gate

**Passed**, by fresh critic agents with no access to my reasoning. Across two critics and one recheck: rerun gave byte-identical outputs, 60 windows (20 per pass) traced to raw rows with no failures, all 1,822 windows matched raw, and independent recounts matched `counts.json`.

**One limit.** After the final recheck I made one small rendering change, leaving out empty typed or deleted lines in `next_actions_text`, and corrected some wording. The critic did not recheck that change. I reran the pipeline twice and compared hashes and window IDs myself (see `raw/_derived/output_hashes.txt`).
