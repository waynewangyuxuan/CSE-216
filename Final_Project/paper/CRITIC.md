# Independent critic report: Final_Project/paper/main.tex

Reviewed against main.tex at commit 218fa93, which landed while this review ran. That commit changed four lines (title short form, affiliation placeholders, one `\paragraph` title, one `\label`), so line numbers did not move. I edited no file except this one. I did not compile, download or install anything. No dataset text appears in this report.

## Overall verdict: FAIL

20 blocking problems, 25 minor problems. The single numbers are very clean: almost every figure traces exactly. The failures are in what is said about those numbers, one contradicted source, and rubric items still missing.

| Item | Result | One-line reason |
|---|---|---|
| 1. Rubric and checklist | FAIL | Analysis method uncited; order, Related Work structure and appendix are fine |
| 2. Tracing | FAIL | Numbers trace, but pooled/single-dataset wording and two number-to-claim mismatches fail |
| 3. Claims against numbers | FAIL | See B2 to B5, B15 to B17 |
| 4. Citations | FAIL | All 32 keys resolve; version/read-level records are inconsistent; two years differ from the registry |
| 5. Barriers vs Limitations | FAIL | Two events ascribe to Wayne what the record does not show; process content sits in Limitations |
| 6. No dataset text | PASS | 0 shared 8-word runs |
| 7. AI Use Statement | FAIL | True as written, but incomplete against REQUIREMENTS until the TODOs are done; one false "I read" outside the section |
| 8. Honesty of method | PASS | One overclaim on coder separation is under B8 |
| 9. LaTeX and template | PASS | Stale notes only |
| 10. SUPPLEMENT.md | FAIL | Script passes; `BRIEF.md` has no entry |

---

## 1. Rubric and checklist: FAIL

**Section order: PASS.** Abstract, Introduction (L49), Related Work (L76), Method (L85), Results (L180), Barriers (L362), Limitations (L384), Discussion (L409), Conclusion (L454), AI Use (L461), References (L494), Appendix (L497). The order matches REQUIREMENTS.md.

| Requirement | Result | Lines |
|---|---|---|
| Abstract: area before findings, problem, approach, results, contribution | PASS except B1 | L32 |
| RQs explicit; intro ends with contributions and overview | PASS | L57-74 |
| Contribution clear and early | PASS, but see B3 and B17 on its content | L67-72 |
| Related Work at most 3 paragraphs with stated roles | PASS | L79, L81, L83; ends on how the literature shaped the project |
| Paragraphs synthesize rather than list | Weak | L81 runs source by source (m18) |
| Method says exactly what was done | PASS except B8, B9, B10 | L88-177 |
| No participants recruited | PASS | L95, L55 |
| Survey, interview, consent appendices do not apply | PASS | L95 |
| Results: describe analysis method | PASS | L183-185 |
| Results: **cite** analysis method | **FAIL (B6)** | L185-186 |
| Results: themes with definitions | PASS | L232, Tables 2 and 5 |
| Barriers: each ends in what was learned | PASS, all 7 | L368-380 |
| Barriers: what you would change with more time | Partial: only L368 and L382 (m9) | |
| Section ends with what was learned about doing research | PASS | L382 |
| Limitations ends with what remains valuable | PASS in position, false in content (B5) | L407 |
| AI Use named, purposes, parts, verification | Partial (B20) | L464-492 |
| Appendix: v1.1 Q1 to Q5 | PASS | L529-659 |
| Appendix: v1.2 rule table | PASS. I compared every rule with `inference/scripts/apply_rules.py`; one wording slip (m15) | L684-723 |
| Appendix: no dataset text; worked examples constructed | PASS | L661-682 match v1.1 section 8 |
| Spell-checked; proofread by a group member | Script passes; Wayne's own proofread not done (B20) | |

**Point estimate (before any deduction).**

| Category | Max | Estimate | Why |
|---|---|---|---|
| Abstract | 15 | 12 | Complete, but the headline result is misattributed to 106 sessions |
| Contribution and significance | 20 | 14 | Clear and early, but the main finding is largely the rule table restated (B3), and "distinguishes" is overstated (B2) |
| Related work and positioning | 10 | 8 | Structure right; paragraph 2 lists |
| Methodological validity | 20 | 12 | Very transparent, but no human check and analysis methods uncited |
| Results and discussion | 15 | 9 | Numbers exact; several claims outrun them |
| Barriers and limitations | 10 | 7 | Honest; some content on the wrong side |
| Clarity | 10 | 8 | Dense but organized |
| **Total** | **100** | **70** | Each spelling error found later would cost 5 |

## 2. Tracing: FAIL

I checked every number in the body, tables, captions and figure descriptions against the named source. **Every individual figure matched, except the items below.** Rounding was checked and is acceptable throughout (for example 0.858 as 0.86, 150.05 as 150.1, 0.455 as 46%).

Mismatches and scope errors:

| Line | Problem | Source | Issue |
|---|---|---|---|
| L32 | "Across 106 whole sessions, pasting did not separate the two sides." | mining.md s5; THESES caveats | **Pooled wording for a NIRVANA-only result.** WildChat has no editor or paste data (L396 says so). B1 |
| L402 | "sampled from a screen with about 12% recall" | wildchat/REPORT.md, Still weak 3 | The 12% is recall of the accepted pool of 2,236. The coded sample came from the random seed only (L105). B7 |
| L314 | "the rate is 0.21 with a draft and 0.65 without" | mining.md s3; SKEPTIC_T C11 | **Pooled across datasets and not labeled.** NIRVANA alone is 0.237 vs 0.505. The "without" group includes WildChat windows where own work is unobservable. B11 |
| L449 | "78.5% of new windows ... with AI-to-AI category agreement of kappa = 0.86" | out_of_sample.md s7 | 0.858 is for all 528 windows, including the 100 calibration windows. Not the new windows (m5) |
| L295, L298 | Stage shares, 192 of 195, position means, moves of 18/29 and 8/29 | mining.md s3, s4, s10 | Pooled across NIRVANA and WildChat, not said. product.md decision 11 says categories are read per dataset. 27 of 29 exits are NIRVANA (m4) |
| L132 | "share no session with the coded test set" | codebook/REPORT.md blinding; sessions/REPORT.md | True only for the 100-window sample and the 20-window set. B9 |
| L314 | "17 of 29 ... 2 of 21" | mining.md s6 | Correct, but the 29 is SL sessions with a later window (36 had SL). Say so (m25) |
| L321 | one p (0.004) after two rhos | mining.md s8 | The p belongs to the request-only rho only (m16) |
| L284, L295, L303, L319 | "p = 0.0005" | mine.py line 107 | This is the floor of (ge+1)/(n+1) with 2,000 shuffles (m1) |

Untraceable: none. The motive in L368 and the reason in L370 are not numbers but are also untraced (B14).

The 27 files in L374 is correct by `git show --name-only ff704c6`. Note that `.wayne/bets/0006-inference-layer/log.tsv` says 28; the paper is right and the log is off.

## 3. Claims against numbers: FAIL

Blocking items are B2 to B5, B7, B8, B10, B11, B15, B16 and B17. Minor items m3, m6, m7, m8, m26.

On causal language the paper is mostly careful: L400 states plainly that nothing is causal, and "tracks" is used for correlations. The exception is "predicts" (L65, L314), which is defined at L400 as across sessions, on a model that is built from next-window pairs. See B11.

Abstract-level sources were checked against the abstracts in `lit/screening/candidates*.jsonl` and `lit/raw/seed`. Supported as written: L79 Yukita, Wan, Park, T. Kim, H. Kim, Skulmowski, Bhat; L81 Yang, Welzel, Davalos; L51 and L79 Joshi (the title makes the claim). Overreaches are in B15.

Tankelevitch (L79): the claim is only the title's. Fine.

## 4. Citations: FAIL

**Mechanical result.** 32 cite keys in main.tex; 32 entries in refs.bib; none missing either way. All 32 are in `lit/papers.csv` under the id in CITATIONS.tsv, and titles and authors match.

Failures:

1. **Years differ from the registry.** `jelson2026chi` is 2025 in papers.csv and 2026 in refs.bib. `joshi2025` is 2024 in papers.csv and 2025 in refs.bib. In both cases refs.bib uses the published version that `lit/related_work.md` also lists. See m20.
2. **Read through a different version and not said: B18.** Bastani was read as a working paper on a third-party host. L376 itself says the version read must be recorded with the citation. refs.bib and CITATIONS.tsv give the PNAS record and "abstract and introduction".
3. **Read levels conflict across records (B18).** `alam2026` is "relevant sections of full text" in CITATIONS.tsv and citation_check.csv, but `inference/sources.tsv` and `inference/REPORT.md` say abstract only, and the M2 draft lists it as abstract only. `contractor2026` and `bastani2025` are "abstract and introduction" in CITATIONS.tsv, but `inference/sources.tsv` shows Contractor pp. 22-23, 68, 77, and `inference/REPORT.md` cites Bastani working-paper pp. 14-15. Those pages carry Table 2 and the rule table (L159, L161, R09, R16).

Correctly disclosed: Flower and Hayes second-hand (L90); Kim 2025 abstract only (L502); Shaw and Nave through PsyArXiv (refs.bib `howpublished`).

## 5. Barriers versus Limitations: FAIL

Mechanical overlap: 0 shared runs of 5 or more words between the two sections. **No repeated text.**

Each Barrier event, checked against product.md, PACING.md, the REPORTs, decisions.tsv and bet logs:

| Line | Event | Verdict |
|---|---|---|
| L368 | Reversal, 90 minutes to 2 hours, cannot be delegated, delegated | Events confirmed. "to save two hours" is a motive no file records; "could not be regained" contradicts L459 and TODO_WAYNE L37. B14 |
| L370 | Narrow screen, 42/40, 41/69, 3/15, 21 not English | Numbers confirmed. "I ... rewrote the definition" is not supported: an agent wrote `wildchat/DEFINITION.md` under Bet 7. "too narrow" is not a recorded reason. B14 |
| L372 | Priming | Confirmed (product.md 5, Bet 4 log) |
| L374 | Shared index, 27 files | Confirmed. "every commit afterward named its paths" is adopted practice per the logs, not verified for every commit (minor; soften to "commits afterward named their paths") |
| L376 | Blocked sources | Confirmed |
| L378 | Lost work, 3-turn view | Confirmed (BRIEF.md, data/REPORT.md, coding/REPORT.md) |
| L380 | Critic passes, 3 of 13, 10 of 23 | Confirmed (codebook/REPORT.md, SKEPTIC.md, SKEPTIC_T.md) |

Wrong side (m9): L404 narrates process events (a batch read ahead on 24 windows, an adjudicator reading parts only partly, the framework comparison's rater). L378 states a claim-side effect ("tuned on it").

## 6. No dataset text: PASS

Scratch script outside the repository, logic copied from `check_no_text.py`, counts only. Run against four corpora: `data/windows.jsonl` read raw (1,037,934 distinct 8-grams), the same file read as parsed JSON strings (655,107), `sessions/blind/parts` (347 files), and `wildchat/blind/views` (151 files). I added the parsed reading because raw JSON escapes can break word runs. I added the two `blind/` corpora because `windows.jsonl` does not hold the 35 WildChat conversations of Bet 7.

| File | Shared 8-word runs, all four corpora |
|---|---|
| main.tex | 0 |
| SUPPLEMENT.md | 0 |
| TODO_WAYNE.md | 0 |
| CITATIONS.tsv | 0 |
| refs.bib | 0 |
| PROOFREAD.md | 0 |

Tracked or staged under `Final_Project/paper/`: source, scripts, template and 5 PNG figures. No raw data, nothing staged. `main.pdf` and `PROOFREAD.md` are untracked. `Reflection/` was not touched by these commits (`git diff 5a0690c HEAD -- Reflection` is empty). The working-tree changes to `Reflection/` existed before and are not part of any paper commit.

## 7. AI Use Statement: FAIL (true, but incomplete)

| Check | Result |
|---|---|
| Models | PASS. Transcript `"model"` counts: claude-opus-5-5 8,872; claude-sonnet-5-5 2,392; claude-haiku-5-5 80; claude-fable-5-1 61 (plus short aliases). Matches L464. One addition: `wildchat/REPORT.md` records 43 labels served by `claude-sonnet-5` (m21) |
| Tools | PASS. Desktop app in transcripts; CLI used for `claude -p` labeling (data/REPORT.md, wildchat/REPORT.md); bge embeddings (L464) |
| Activities | PASS. Table L473-480 matches the REPORTs. 713 records, Haiku and Sonnet confirmed. No "editing" row, though the rubric lists it (m21) |
| What Wayne decided (L485) | PASS. Each sentence matches product.md 1, 4, 6, 7, 8, 12 and PACING.md |
| No claim of Wayne reading or reviewing, inside the section | PASS. L487 is explicit |
| Claim outside the section | **FAIL.** L95 "as far as I read them". Wayne did not read them, and L97 and L487 say agents did the work. B13 |
| Things to come marked TODO | PASS. L488, L489, L492. L491 is present tense but is followed by its TODO |
| REQUIREMENTS: how output was reviewed | **FAIL until done.** L488 is empty by design. This is correct honesty, but the statement cannot be submitted as is (B20) |

## 8. Honesty of method: PASS

"No human coded" is plain at L32, L55, L387, L478 and L487. No agreement is called human or validation; L140 says "not human validation" outright. Nothing implies recruitment (L55, L95). WildChat consent matches the abstract and goes no further (L103, but see B12 on its wording). NIRVANA consent is left to a TODO and nothing is invented (L97-98). The single overclaim on the coders is B8. The term "gold set" is a minor risk (m13).

## 9. LaTeX and template: PASS

Note on the premise: the brief says this cannot be compiled. On this machine I found `/opt/homebrew/bin/tectonic`, an untracked `paper/main.pdf` (24 pages, 18:14) and `paper/scripts/check_build.py` from commit 218fa93. I did not run any of them. I read the existing PDF with PDFKit only.

- `\documentclass[manuscript,screen]{acmart}` is single-column; `template/acmart.cls` and the `.bst` are present (L5). PASS.
- Static checks: braces, environments, labels, citation keys and escaped characters are fine (`check_tex.py` passes; my own read found no errors). Each `tabular` column count matches its rows. All 5 figures exist.
- Table width: my column sums all fit, and in the existing PDF no page has text past the margin (maximum x is about 503 on odd pages and 540 on even pages, on a 612-wide page).
- Length: the PDF's AI Use Statement is on page 16 and References start on page 17, so the body is about 16.5 pages. **Within the 20-page guide.** This is a compile before the last source edits, not mine.
- The double period on the NIRVANA paragraph heading was fixed in 218fa93. It was the only instance in the PDF.
- Stale statements: m19.

## 10. SUPPLEMENT.md: FAIL

`python3 Final_Project/paper/scripts/check_supplement.py`: 90 paths, 77 tracked, 12 local only, 1 missing (`CRITIC.md`, which this report now creates). Ignoring PROOFREAD.md and CRITIC.md as instructed, every local-only path is marked local in the table. No problem from the script.

- Lists what Wayne must do: PASS (section 2).
- Raises the transcript decision: PASS (Decision A, with options and risk). Decision B and C also raised.
- **Every piece of work has an entry: FAIL.** B19.
- Status key: m24.

---

## Blocking problems, with exact fixes

**B1. L32, abstract: paste result attributed to 106 sessions.** Replace "Across 106 whole sessions, pasting did not separate the two sides. Whose content was pasted, and what the writer did next, did." with "Across the 71 NIRVANA sessions, the only ones with editor records, pasting did not separate the two sides. Whose content was pasted, and what the writer did next, did."

**B2. L449: "The second part holds narrowly" contradicts the source.** `lit/framework_comparison.md` and `report/M2_draft.md` s4 both say the criterion is *not established*. Pair 7 is built from the codebook's own examples, so the project "could not have failed it", and the paper omits this. Pair 6, which the paragraph then leans on, is one Shaw and Nave already separate in theory. Replace with: "The second part is not established. An agent's comparison across 11 case pairs, written before any real window was coded, rated the project the only framework able to separate 3 of them. NIRVANA's own metrics already separate 2 of those, and the third was built from the codebook's own worked examples, so the project could not have failed it." Keep the rest as a statement of what the framework adds, not as meeting the criterion.

**B3. L70, L266, L414, L457: T1 is presented as a finding although the rules build it in.** Rules R08, R11, R13 and R09 assign the categories from whose content it was (D1, D3, D4). So "the boundary lies in whose content" is partly the rule table's definition. L394 admits this for one table column only. In L70 replace "shows that the boundary lies in whose content is taken over and in the work that follows, rather than in pasting or speed" with "shows that pasting and speed do not separate the categories that the rules assign by content origin, and that typing, time and essay outcomes differ across them". In L457 add after the first sentence: "The first part follows from how the rules are defined. Typing, dwell and essay outcomes are what the data add." Add the same qualifier at the start of L414's evidence sentence.

**B4. L71, L334, L394, L443: trigger recall is partly built in and this is not disclosed.** The labels the triggers are scored against come from codes that use the same events. U1 and D4 rest on the paste record, and R09 requires no visible own work. So "large paste" and "near-empty page" partly predict their own label. L394 lists other built-in links and omits this one. Add to L394: "Trigger precision and recall are partly built in as well: pastes and an empty editor feed the codes the triggers are scored against, so these figures show that the events match the labels, not that they find surrender independently." Add "by the AI-coded labels" after "surrender-leaning windows" in L71 and L334.

**B5. L407: the "What remains valuable" claim is false.** "The direction and size of the main results hold under each check the skeptic tried" is contradicted by SKEPTIC_T.md and the paper itself (L303): the C9 link falls from 0.40 to 0.26, p 0.075, on multi-window sessions, and the C11 effect shrinks within sessions to 0.18 vs 0.26. "does not depend on any model's judgment" is also wrong: every group contrast uses model-assigned categories. Replace both clauses with: "The direction of the main outcome links holds under the skeptic's checks, although the own-work link roughly halves on multi-window sessions. The pastes, typing and timing themselves come from logs, while the grouping of windows into categories comes from AI coders."

**B6. L185-186: the analysis method is not cited.** REQUIREMENTS says "Describe the analysis method and cite it". The citations for Cohen's kappa, Spearman, optimal matching, silhouette, permutation tests and deductive qualitative coding are absent, left to a TODO. Wayne must approve adding them, then add entries and cite at L185. Without it the Results requirement fails. If approved, also add a source for deductive coding, not only the statistics.

**B7. L402: recall of the screen is attached to the wrong set.** Replace "sampled from a screen with about 12% recall" with "drawn from the conversations an LLM accepted in a random seed of 1,200; recall of the larger accepted pool, which was not coded, is about 12%".

**B8. L138: "they could not see each other's labels".** coding/REPORT.md, sessions/REPORT.md and wildchat/REPORT.md all say separation is by instruction and not enforced by the file system, and one Bet 4 coder's scratch files were reachable. Replace with "they were instructed not to read each other's labels, and a transcript audit found that none did; the file system did not enforce this."

**B9. L132: "on windows that share no session with the coded test set".** Bet 6 then coded all 71 NIRVANA sessions, including pilot sessions (sessions/REPORT.md L59). Replace with "on windows that share no session with the 100-window sample and the 20-window set; later whole-session coding did include pilot sessions".

**B10. L105: definition omits the largest genre.** `wildchat/DEFINITION.md` includes articles for publication, business plans and formal statements, and expository blog articles count. The screen's largest coded genre is article (9 of 35), and all 3 audit rejections are articles. Replace "an essay, research paper, report, thesis, literature review or proposal" with "an essay, research paper, report, thesis, literature review, proposal or business plan, article for publication (including expository blog articles) or formal statement", and add "9 of the 35 coded conversations were screened as articles; all 3 that the audit rejected are in that group" to L105.

**B11. L65, L314: "predicts" and the pooled rates.** Add NIRVANA-only rates: "the rate is 0.21 with a draft and 0.65 without, pooled across datasets, and 0.24 against 0.51 in NIRVANA alone". In L314 add: "Most of this is between sessions: in the 16 sessions where the draft flag varies, the next-window rate is 0.18 with a draft and 0.26 without" (SKEPTIC_T C11).

**B12. L103: near-verbatim sentence from the WildChat abstract.** It follows the abstract's phrasing for most of its length, without quotation marks. Replace with: "\citet{zhao2024} built WildChat by giving online users a free ChatGPT service; users opted in to anonymous collection of their conversations and request headers."

**B13. L95, also L83, L105, L398: first-person reading and running.** L95's "as far as I read them" claims Wayne read sources he did not. Replace with "only as far as their papers state it and as far as the agents read them, as recorded in the read levels in the supplementary materials". L83: "the studies I found" becomes "the studies the search found". L105 "I screened" becomes "All of WildChat-1M was screened by an LLM". L398 "I ran" becomes "The analysis ran".

**B14. L368, L370: Wayne's motives and authorship.**
- L368, "the one I gave up to save two hours": no file records why. Wayne must confirm or it becomes "the one step given up".
- L368, "could not be regained later" contradicts L459 and TODO_WAYNE L37, which propose exactly that step. Replace with "the one step that later steps could not replace".
- L370, "rewrote the definition before any record was labeled": `wildchat/DEFINITION.md` is agent-written. Replace with "On November 7 I widened the scope to formal long-form writing, and an agent wrote and committed the new definition before any record was labeled."
- L370 heading "too narrow": no file gives this as the reason. Use "The WildChat screen for research writing could not be reproduced" unless Wayne confirms.

**B15. L414, L420, L432: sources stretched beyond what was read.**
- L414, Yukita (abstract only): "This is the empirical form of" claims more than a critical review of workplace writing allows, and this study does not measure waiting. Replace with "This is consistent with the shift \citeauthor{yukita2025} describe, from translating to waiting, in that what is handed over is translating."
- L420, Joshi (abstract only): "as \citet{joshi2025} found" sets a prompted-story study against taken-in AI text. Replace with "consistent with work showing lower ownership when writing through prompts \cite{joshi2025}".
- L432, Jelson: comparable ownership in that paper is about planning and reviewing use, not typed text after a generation request. Replace with "ownership need not fall, as with planning or reviewing use \cite{jelson2026chi}".

**B16. L432 and L439: RQ2 table labels as substitution a pattern the rules call support.** D2 U7 is augmenting in 37 of 52 windows, and L414 puts it on the support side. Change the row to "Ideas from a generation request, written up in the writer's words (\code{D2 U7}, 52 windows, 37 augmenting by the rules; possible substitution of the ideas, which the rules cannot see)", and in L439 replace "The least visible substitutions keep the writer busy" with "The substitutions most likely to go unseen, if they occur, keep the writer busy."

**B17. L71, L443, L459: "mockup level" with no mockups.** TODO_WAYNE L38 says none were built. In L71 replace "a proposed intervention at mockup level" with "a proposed intervention, not built or tested". In L443 replace "kept at mockup level since no system was built" with "stated as proposals, since no system or mockup was built".

**B18. Versions and read levels.** Add to CITATIONS.tsv: `bastani2025` read level "working-paper version on a third-party host: abstract, introduction, pp. 14-15; PNAS version of record not read". `contractor2026` "abstract, introduction, pp. 22-23, 68, 77". Resolve `alam2026` to one level across CITATIONS.tsv, citation_check.csv and `inference/sources.tsv`. Add to refs.bib `bastani2025` a note: "Read as working paper". At L51 or L90 add a clause stating the Bastani version read.

**B19. SUPPLEMENT.md: `Final_Project/BRIEF.md` has no entry.** It is the only evidence in the repository for the proposal quote in L368, the M1 counts in L370 and the lost files in L378. Add a Barriers row: `Final_Project/BRIEF.md` | public. Also add the Milestone 1 and proposal sources themselves if Wayne can supply them.

**B20. Wayne-only items that block submission (correctly marked, not errors).** L25-28 (the placeholders `[city]` and `[country]` print in the PDF), L98-99, L133, L186, L364, L488, L489, L492, his own full proofread (required by the checklist), chat log export (SUPPLEMENT section 2), repository access for the instructor and TA.

---

## Minor problems, with exact fixes

- **m1. L284, L295, L303, L319.** Replace "$p = 0.0005$" with "$p < 0.001$" (floor of 2,000 shuffles).
- **m2. L266, L276, L430.** D4 means about half or more verbatim, not all of it. In L276 write "AI proposal taken, about half or more (\code{D4})"; in L266 replace "pasting an AI proposal whole" with "taking most of an AI proposal".
- **m3. L65, L317.** "leave no work on the text" overstates: median typed is 0, but 14 of 48 behavior-based windows have 50+ typed. Use "leave little work on the text" in both places.
- **m4. L295, L298.** Add "pooled across both datasets" and, at L298, "(27 of the 29 exits are in NIRVANA)".
- **m5. L449.** Replace "with AI-to-AI category agreement of $\kappa = 0.86$" with "and AI-to-AI category agreement across all 528 windows is $\kappa = 0.86$".
- **m6. L439.** No measure of thinking exists. Replace the last sentence with "Ownership here tracks whether a writer typed the words; whether it tracks the thinking cannot be measured from these logs."
- **m7. L443.** Replace "since writers copy equally fast on both sides" with "since time to first copy does not differ reliably between the sides and a quick return shows no relation to essay outcome".
- **m8. L457.** Replace "usable early signal" with "candidate signal, not yet tested in a tool" (a paste can only fire after the response). Add that the paste, timing and trigger claims rest on NIRVANA alone.
- **m9. Barriers and L404.** Move the WildChat read-ahead, the partial-read adjudicator and the framework-rater sentences to Barriers, leaving the effect on claims in L404. Add one "with more time" sentence to each of L370, L372, L374, L376, L378, L380, or drop to the section-level L382 by choice.
- **m10. L261.** For e24, "each request comes while a paragraph of the writer's is half written" is not true of the first (a 101-character note). Replace "each request" with "after the first, each request". For e41, replace "one paste of 4,681 characters" with "one paste of 4,681 characters, then a pasted title".
- **m11. L404.** "is by audit and not by mechanism": FROZEN.md rests this on agents' briefs and on mapping each change to a critic finding. Use that wording.
- **m12. L177.** "Every number reruns ... with one script" is not literal: each stage has its own `run_all.sh`. Replace with "Each stage's numbers rerun from saved labels by script, with no model calls".
- **m13. L140, L204, L368, L478, L485.** Replace "gold set" with "20-window set" where it stands alone, per PACING's caution about gold-standard language.
- **m14. L81.** "a companion paper" is unconfirmed (`lit/related_work.md` says the link is not stated; the arXiv abstract gives n=70). Use "a paper from the same group". Note that the Mallissery source is a code and results repository.
- **m15. Table 2 (L155-166), L716.** Table 2 omits R06, R07, R10, R20: add a row or state "main rules". R17 in code accepts a draft or notes: replace "own draft visible" with "own work visible".
- **m16. L321.** Replace with "($\rho = -0.55$ behavior-based, $p < 0.001$; $-0.33$ request-only, $p = 0.004$)".
- **m17. L334, L348, L356.** "Fourth trigger", "not a trigger" and "four log-only triggers" conflict. Use "four log-only rules, of which two are proposed as triggers".
- **m18. L81.** Rework into grouped synthesis, for example by trace type, per the rubric's "not summarizing one by one".
- **m19. TODO_WAYNE L19, L8; main.tex L3.** "No TeX is installed" and the pdflatex line are out of date. Update to tectonic and `build.sh`. Decide whether `main.pdf` is tracked or ignored.
- **m20. papers.csv or CITATIONS.tsv.** Add a note for `jelson2026chi` and `joshi2025` that the bib year is the published version's, or update the registry.
- **m21. L464, L473-480.** Add "43 screen labels record Claude Sonnet 5 as served". Add an "Editing" row. Drop "also" from "Non-generative use also includes".
- **m22. L23.** The title asserts substitution for thinking that L392 says is not measured. Consider "Mapping Where AI Assistance May Substitute for Thinking". Wayne's call.
- **m24. SUPPLEMENT L5.** "public = tracked on branch" is misleading: the branch is 5 commits ahead of origin, and those commits hold the paper itself. Add to section 2: "Push `final-project`, then confirm section 1 matches what the remote shows."
- **m25. L117, L120, L32, L314.** Three conversations are capped at turn 10, so "whole" is loose: add "(3 capped)" once in the abstract's or Table 1's description. In L314 add "of the 29 with a later window".
- **m26. L420.** "its usual by-product, work on the text" is an unsupported assertion. Replace with "a possible by-product, work on the text".

(25 minor items; m23 is unused.)
