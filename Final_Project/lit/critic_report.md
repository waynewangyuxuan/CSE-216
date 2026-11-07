# Critic report: literature base

**Verdict: PASS WITH FIXES**

Against the gate:

- **Every citation exists: met.** No citation is fabricated. Author, venue and status errors are listed below.
- **Each comparison cell has a source: not met as written.** 4 of 55 cells have no pointer.
- **The search log is complete: met.**

No finding needs a new search. The fixes are edits, plus a decision on how the comparison table rates the project (D3).

Checked 2026-11-06. My scripts are in `/private/tmp/claude-501/-Users-wang-CSE-216/d9e60b87-5368-4a55-a4fa-be9956a56a4f/scratchpad/critic/`. No deliverable was edited.

## Defects, most serious first

### High

**D1. `protocol.md` ("Other known misses") and `papers.csv` rows S13 and S04 give a false reason for two seed misses.**
- The files say Padmakumar and Doshi & Hauser "fell outside the top records". S13 says "ranked outside the top records of Q9 in both sources". S04 says it "fell outside the top 40 of 4,538".
- Neither paper matches the query at all:
  - OpenAlex filter on the paper's own record plus the query string: Padmakumar on Q9 gives 0, Doshi on Q11 gives 0. Positive control: the first record of `Q9_openalex.json` gives 1.
  - arXiv Q9 returns 19 hits in total and all were retrieved (log row: 19 of 19), so nothing can rank outside the top there. 2605.29392 is not among them. Its abstract contains none of the required LLM, "generative AI" or ChatGPT terms.
- This is a query-wording miss, not a retrieval-cap miss. It matters because the protocol presents top-N truncation as the limit. Correct both files. `decisions.tsv` line "Did not chase Padmakumar and Doshi misses" should be rechecked after the correction.

**D2. `related_work.md` §2, Mysore: the sample size is overstated.**
- The text says they "analyze follow-up turns in 20.5 million Bing Copilot and 800,000 WildChat sessions".
- Those are the starting samples. Filtering leaves 2.8M and then 250k Bing writing sessions, and 160k and then 68k WildChat writing sessions (`2505.16023.txt` lines 273, 278, 281, 290).
- The follow-up analysis is on 250k and 68k. The reader is off by about 80x and 12x.
- Registry read level for this paper is "abstract and introduction", which explains the slip (see D9).

**D3. `framework_comparison.md` §3: the rating key is not applied evenly, and this is the core of the table.**
- The key defines Partly as "only in theory, in aggregate, or by extending the framework".
- These cells break the key:
  - R&G pairs 9 and 11 are "Yes, in theory".
  - Shaw pair 8 is "Yes, in aggregate", while Shaw pair 5 is "Partly... only in aggregate" on the same grounds.
- All 5 project Yes verdicts are paper-only. The file says so, and the codebook has never been applied to real windows. Read literally, they are "only in theory".
- Literal recount: R&G 0 Yes, Shaw 1, PAUSE 1, Maier 1, project 0. Maier pair 10 is the only Yes with a tested tool.
- Fix: redefine Yes as "states a rule", and add a separate marker for tested or untested. As written, the project gets Yes for a paper rule while the Partly key penalizes others for the same thing.

**D4. `framework_comparison.md`, pair 6: "only one rated Yes" holds arithmetically but does not survive even-handed rating.**
- Shaw & Nave state the distinction directly: strategic delegation with one's own reasoning active, against adopting a generated answer (pp. 4, 16, 17). §2 of the same file calls this the closest match to RQ1. It is rated Partly for "no trace measure", yet Shaw pair 1 is rated Yes with no trace measure either. I would rate it "Yes, in theory", the same as R&G pair 9.
- Maier pair 6 says requests are rated "not whose claim". But §4.2.3 includes a numeric check "distinguishing a new item-specific value from confirmation of one the participant had already produced". That is a rule about who produced the content. I would rate it Partly by extension.

**D5. `framework_comparison.md`, pair 2 and Bottom line: the same source already separates this pair, and the file does not say so.**
- NIRVANA clusters P26 as Collaborators and P77 as Vibe Writers (§6.2), using HCR and HER.
- The file credits NIRVANA's HER against the project on pair 3 and HCR on pair 1, but not on pair 2.
- The Bottom line and §4 name pair 6 as shrinking outside the four frameworks and are silent on pair 2.
- With D4, only pair 7 is left as a clear gain. The file does call pair 7 the most defensible, but still states the size of the claim as 3 pairs.

### Medium

**D6. Pair 10, project "Yes": out of scope by the codebook's own rule.**
- Codebook §2.1 requires a concrete writing goal and excludes non-writing requests. A fraction-arithmetic item is ineligible, so the cell should be N/A.
- Maier on pair 4 is held to Partly because its scale "was built for arithmetic". That standard is not applied in reverse.
- Project Yes count: 5 becomes 4.

**D7. Pairs 6 and 7: circular test cases, not flagged as such.**
- Both are built from the project's own worked examples (E2/E4, E6/E7), which were written to exercise these codes. The project cannot fail them.
- Two of the three "unique" pairs are therefore self-set. The file discloses that they are constructed and that it chose "home ground", but the Bottom line calls the 3 pairs "the honest size" without this qualification.

**D8. Other cells I would rate differently. Some of these favor rivals.**

| Cell | Table | Mine | Evidence |
|---|---|---|---|
| Shaw 1 | Yes | Partly | p. 20 defines follow or override on CRT items with a checkable answer. Pair 4 says essays have no checkable answer, which contradicts pair 1. This needs extension, so by the key it is Partly. §4 item 3 ("adds nothing" on pair 1) weakens with it. |
| Shaw 11 | Cannot | Partly | Table 2, p. 16 includes "long-run reanchoring" and shifts from "repeated" exposure; p. 17 "disposition". The studies are a snapshot, but the theory speaks to it. |
| PAUSE 7 | Cannot | Partly | Appendix A items B1 (checks AI facts against a source) and B3 are the same kind of evidence that earned Partly on pair 5 (B5). |
| Shaw 9 | Partly | Cannot | p. 18 concerns deferring to a statistically superior system, not learning goals. |
| Maier 9 | Partly | Cannot | "Studies learning only" means no rule separates the pair. |
| PAUSE 7, 8 | Cannot | N/A | Same person-level reason used for N/A on pairs 1, 2, 3, 4, 6 and 10. |
| R&G Cannots | Cannot (8) | Many N/A | A pre-LLM theory has no interaction-level unit. The key's "N/A: outside its unit by design" is used for PAUSE only, which makes R&G look worse. |
| Maier 10 | "tested on 198 held-out dialogues" | Add "synthetic" | §4.2.3: the set is synthetic tutoring dialogues. Overstates the rival slightly. |

**D9. `related_work.md` [F] marks conflict with the project's own read records.**
- All 16 [F] marks have a file in the fulltext folder, so none is invented.
- 8 of 16 are recorded in `scripts/read_levels.json` and `papers.csv` as less than full text:
  - Mysore, Reza, Bastani: "abstract and introduction"
  - Tao: "abstract and method sections"
  - Lee, WildChat: "abstract and relevant excerpts"
  - ScholaWrite: "abstract and relevant sections"
  - Peters: "abstract and preprint opening" (marked "[F, opening]", so this one is closest to honest)
- `citation_check.csv` says "full text read" for Mysore and Reza. Its Bastani row says only that PMC full text was fetched.
- `framework_comparison.md` §1 says Shaw & Nave "full", while `papers.csv` says "full text to Study 1, plus limitations".
- Chen is marked "[A, method read]", but the claims come from Results and Discussion (`chen.txt` lines 924, 997), so that mark understates.
- Reconcile one way or the other.

**D10. `related_work.md`: 8 sources are marked "(preprint)" though Crossref shows a published version.** The header warns readers about unreviewed preprints, so the mark matters.

| Source | Published version |
|---|---|
| Bhat | CHI 2026, 10.1145/3772318.3791529 |
| Nogueira | IUI 2026 Companion, 10.1145/3742414.3794723 |
| Christenson | BEA 2026 workshop, 10.18653/v1/2026.bea-1.48 |
| Welzel & Vincent | FAccT 2026, 10.1145/3805689.3812389 |
| Poquet | LNCS 2026, 10.1007/978-3-032-37979-5_34 |
| ScholaWrite | ACL 2026, 10.18653/v1/2026.acl-long.1606 (also `citation_check.csv` S09) |
| Joshi & Vogel | CUI 2025, 10.1145/3719160.3736608 |
| RECIPE4U | LREC 2024, pp. 13666-13676; the DOI is already in the reference |

- The References also give venue "arXiv" for Park (CHI 2026) and Wan (C&C 2024), though their own DOIs are the proceedings versions.
- Ghosh, Tao and others returned no published match from Crossref title search. That search is not proof of absence.

**D11. `framework_comparison.md` §4 and `related_work.md` §7 item 4: Poquet's kappa is the less relevant number.**
- The κ = 0.68 is for the learning-strategy (SOI) framework (`2606.10434.txt` line 384), and the file does say "related".
- The kappas for the active/passive and local/global coding, which is the actual rival scheme, are 0.64 and 0.61 (line 231). Report these.

**D12. `related_work.md` References: 4 author lists are silently truncated, and the stated reason is wrong.**
- The header says lists are "as the registry gives them", but `scripts/run_search.py` cuts OpenAlex authors at 6.
- Missing authors:
  - Nogueira: Nitesh V. Chawla
  - Han: Alice Oh
  - Yang: Guanliang Chen
  - Tankelevitch: Sean Rintel
- Wan: "Gebreegziabhe" should be Gebreegziabher (Crossref; the arXiv record has the typo).
- Every `papers.csv` record with more than 6 authors from OpenAlex has the same cut.

**D13. `framework_comparison.md`, 4 cells have no source pointer: R&G on pairs 5, 7, 8 and 10 show "(no rule)".**
- This is the literal gate failure. A pointer to the pages read would fix it, such as "ms pp. 3, 11-14 state no rule", which is what I found there.

**D14. `protocol.md` Stage 3 and `decisions.tsv`: "Most disagreements came from one gap" is false.**
- `screening/adjudication.tsv`: R1 accounts for 24 of 93 disagreements (26%), tied with R4 at 24. R8 has 16.

### Low

**D15. `related_work.md` §2, Poquet: an unquoted verbatim run of 16 words from the abstract:** "who performs the activity (active or passive) and at what level of comprehension (local or global)". Quote or reword. It is the only run over 15 words in the five prose deliverables. `citation_check.csv` matches are paper titles only.

**D16. `framework_comparison.md` lines 8 and 37 and `decisions.tsv` line 16 cite `REPORT.md`, which does not exist in `lit/`.** The only one I found is `Final_Project/data/REPORT.md`, which I did not open. Line 8 also asserts that a critic re-check happened. Write the file, or fix the reference, before close.

**D17. `related_work.md` References.**
- None of the 21 seed entries uses the "(year)" field the search entries have, and 6 show a year only inside the venue. Doshi, Risko, Zimmerman and others have no year as a field.
- The in-text labels Jelson 2026a and 2026b have no matching label in the References, and `framework_comparison.md` uses "Jelson 2026" for both papers.
- Entries sort by given name.

**D18. `protocol.md` "The screening prompt is... in full:"** is followed by a paraphrase, not the full text. It drops "interviews about actual use" from I2 and the E3 examples, including "programming only". Say "summarized".

**D19. `search_log.csv`, forward Q7 OpenAlex: retrieved 40, screened 34, with an empty note.** The 6 are review and decision-letter records on Peters, dropped automatically by `build_candidates.py`. Add a note.

**D20. `related_work.md` §6: Bereiter & Scardamalia "used by Yang (2025)" is second-hand through a source read at abstract level only.** The abstract uses the terms but does not cite them, and Yang's full text is not in the folder. Reza and Jelson on Flower & Hayes are fine.

**D21. Small wording stretches from abstracts.** Georgiou "self-rated": the abstract gives a scale and does not say self-rated. Nogueira "interviews or self-report" (§7): the abstract says "user study".

## What I checked and found correct

### 1. Citations

Script results; a mismatch means author, venue or status as listed in D10 and D12.

| Set | Count | Method | Result |
|---|---|---|---|
| `related_work.md` References | 49 | arXiv API with 3.1 s gap, Crossref, DataCite | 48 resolve with matching titles |
| Bereiter & Scardamalia (no DOI) | 1 of the 49 | ERIC API and Open Library | Confirmed, including ISBN |
| `citation_check.csv` rows | 24 | Same | 23 confirmed, including WildChat's ICLR page (HTTP 200) |
| S22 Harvard | 1 of the 24 | Page fetch | HTTP 403 to my script, not API-checkable. The row already says DISCREPANCY, and it is not in the References |
| `framework_comparison.md` named papers | All | Same | All covered, including Hornbæk & Oulasvirta |

- Also resolved: the 7 extra identifiers in `conceptual_analysis.md` and `codebook_implications.md`. Beaney & Raysmith (encyclopedia entry) was not checked.
- The arXiv date anomaly noted for PAUSE (2026-07-13 on a 2609 ID) is real.
- Every `[search ...]` tag matches its record's title in the candidates and has a row in `papers.csv`.

### 2. Claims

Seed 216. `random.Random(216).sample` over 59 sentences extracted from sections 1 to 7 that name a source.

| Item | Claim | Verdict | Location |
|---|---|---|---|
| 1 | R&G: not conscious, costs and benefits, drift | SUPPORTED | ms pp. 12, 13 |
| 6 | Maier: "answer offloading" | SUPPORTED | §1, line 120 |
| 11 | H. Kim: LLM fallacy | SUPPORTED | abstract |
| 13 | Bhat: 19, 1,291, did not notice | SUPPORTED | abstract |
| 16 | Yang: four patterns | SUPPORTED | abstract |
| 22 | Mysore: sessions and behaviors | PARTLY (D2) | lines 122, 273-290 |
| 24 | Mallissery: 16,851, not a measure of surrender | SUPPORTED | abstract |
| 30 | Georgiou: lower self-rated engagement | PARTLY (D21) | abstract |
| 36 | Ghosh: one CFF reduced overreliance, not load | SUPPORTED | abstract |
| 41 | Hossain: 20-item | SUPPORTED | line 178 |
| 44 | Joshi: ownership, longer prompts | SUPPORTED | title, abstract |
| 45 | Park: 302, self-efficacy, trust | SUPPORTED | abstract |
| 51 | Bereiter, used by Yang | PARTLY (D20) | Yang abstract |
| 53 | Wu, Nogueira, ScholaWrite as self-report or no AI | PARTLY (D21) | abstracts |
| 54 | NIRVANA and most trace studies use essays or classroom tasks | SUPPORTED | §2 sources |

Totals: 11 SUPPORTED, 4 PARTLY, 0 NOT SUPPORTED.

**Numbers in sections 1 to 4.** I checked 44. 42 are correct, and 2 (Mysore) are real figures misapplied. Correct and spot-confirmed: Shaw 1,372; NIRVANA 77 and about 30 minutes; Jelson κ .89; Poquet 97; Chen 168 and six classes; ScholaWrite 15, five and over half (57%); Bastani about 1,000; Kosmyna 54 and 18; Maier 704; Lee 319; Peters 4,900 and about 5x (OR 4.85); Tao 129, 65% and 41%; Padmakumar 40. Also, §7's "10 of 65" for Q5 matches the log.

**Marks.** Every [F] has a text file. [A] entries are consistent with the abstracts. [S] and [not read] are honest, except as noted in D9 and D20.

### 3. Comparison

- **Pointers:** 51 of 55 cells have one.
- **Cells read:** all 55 at the pointer or its section. That includes 5 of 5 project Yes cells against the codebook and all rival Cannot cells.
- **Disputed:** 11 of the 51: Shaw 1, 6, 8, 9, 11; Maier 6, 9; R&G 9, 11; PAUSE 7; project 10. The other 40 are supported as rated, apart from the N/A-versus-Cannot category issue in D8. Of the disputed cells, R&G 9, R&G 11 and Shaw 8 are correct in substance and fail only on the key.
- **Project Yes cells on pairs 1, 2, 6, 7:** the codes match codebook §§4-7 and §8 (E2, E4, E6, E7) and the NIRVANA §6.2 descriptions.
- **Verdict counts:** all five rows match the table, and each sums to 11.
- **"Only one rated Yes on pairs 2, 6, 7":** true as the table is written, and these are the only such pairs. It is not robust (D3 to D7).
- **Table §1 and §2 pointers:** checked correct for R&G, Shaw and Maier, and PAUSE §3.1, §3.5, §4.4, §6.3.
- **P-case descriptions:** P26, P30, P47, P54, P57 and P77 match NIRVANA §6 and §6.2.

### 4. Search log

- **Q4 rerun:** OpenAlex 313 hits and 40 records, arXiv 38 hits and 25 records. Same as the forward run. All 65 titles are identical and in the same order, the records are identical, and the URLs are identical. This is a weak test of drift, since it ran about 25 minutes after the forward run.
- **Coverage:** forward has 34 rows, covering 12 OpenAlex, 11 arXiv and 11 S2 (all HTTP 429, noted), for every query in `queries.json`. C1 is OpenAlex only, as stated. Query text matches on all rows.
- **Columns:** date, query, source, hit count, screened, included and seeds recovered are all present, plus 11 Scholar rows marked `not_run_by_hand`.
- **Hash:** `queries.sha256` matches `queries.json` (e704f1d1...).
- **Protocol totals recomputed from `screening/`, all match:**
  - 653, 60 and 713 records
  - 247/313/93, 13/44/3 and 260/357/96
  - 296 (104), 14 (3) and 310 (107)
  - 85.8% agreement, κ = 0.71
  - Seeds: dev1 9, dev2 12, forward 12, plus Shaw for 13; 11 kept
  - `papers.csv` has 321 rows, which is 310 plus 11
- **Other protocol statements confirmed:** dev1 was unsorted, and no forward Q2 record mentions "surrender".

### 5. Honesty

- `protocol.md` plainly says it was built after the seed list and does not describe how seeds were found, and its recovery is called in-sample.
- `related_work.md` opens the same way.
- The Scholar difference is recorded, with `robots.txt` saved. It does disallow `/scholar`.
- Verbatim scan with a 12-word minimum across the five prose deliverables and all saved texts and abstracts: one run over 15 words (D15).
