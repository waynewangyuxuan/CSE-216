# Paper-search protocol

## What this protocol is, and is not

**This protocol was built after the seed list existed.** The 22 seed papers were chosen earlier, by a process whose records were lost. I developed the queries here by reading the seed list and tuning against it, then ran them forward on 2026-11-06.

- It does **not** describe how the seed papers were found, and must not be presented that way in Milestone 2.
- Its recovery of seed papers is **in-sample**. It shows the queries fit the list they were tuned on. It is not a measure of how much of the literature they find.
- What it does give: from now on, anyone can rerun the search and get a logged account of what was found, what was screened, and why.

Suggested wording for Milestone 2: "The initial paper list predates this protocol and its selection records were lost. To make selection reproducible, we then built a search protocol using that list to develop queries, ran it forward, and report which listed papers it did and did not recover."

## Google Scholar: what differs from what the professor asked

The professor named Google Scholar. **The logged run did not use it.**

- Scholar's `robots.txt` (saved at `raw/scholar_robots.txt`, fetched 2026-11-06) disallows `/scholar`, so automated queries are against its rules. I ran none. No CAPTCHA or bot check was involved or bypassed.
- **Substitution:** OpenAlex and arXiv for the logged run. Semantic Scholar was also attempted, and every query returned HTTP 429 without an API key, so it contributed nothing.
- **Consequence:** Scholar also indexes full text, theses and grey literature, so its hit counts and results will differ. OpenAlex filters on title and abstract here. The two are not interchangeable.

### Queries for the user to run by hand in Scholar

Set "Since 2023" or a custom range from 2022. Record the date, the "About N results" figure, and the first 20 titles. Log rows are ready in `search_log.csv`, marked `not_run_by_hand`.

1. `"cognitive offloading" ("generative AI" OR LLM OR ChatGPT)`
2. `"cognitive surrender" AI`
3. `(ChatGPT OR "generative AI") (essay OR "academic writing") students "writing process"`
4. `("co-writing" OR "AI-assisted writing") taxonomy OR delegation`
5. `("research writing" OR "scholarly writing") (ChatGPT OR LLM) researchers`
6. `("critical thinking" OR deskilling OR "cognitive debt") ("generative AI" OR ChatGPT) writing`
7. `(verification OR "appropriate reliance") ("generative AI" OR LLM) writing`
8. `(ownership OR authorship OR agency) ("generative AI" OR ChatGPT) writers`
9. `"AI reliance" (measure OR scale) ("generative AI" OR LLM)`
10. `("interaction logs" OR "chat logs") ChatGPT dataset`
11. `("generative AI" OR ChatGPT) (learning OR skill) "field experiment" OR randomized`

These are simplified forms of the logged queries, because Scholar handles nested Boolean logic differently.

## Sources and retrieval

| Source | Access | Field | Date limit | Records taken per query | Sort |
|---|---|---|---|---|---|
| OpenAlex | Public API, no key | `title_and_abstract.search` | from 2022-11-01 | 40 | Relevance |
| arXiv | Public API | `all:` | from 2022-11-01, applied after retrieval | 25 | Relevance |
| Semantic Scholar | Public API, no key | Keyword search | from 2022 | 25 (intended) | Relevance |

2022-11-01 is the month ChatGPT launched, so the date limit excludes pre-LLM work on purpose. **Older theory cannot be found by this search**, which is why those seed papers are reported as misses below.

**Taking only the top records means this is a bounded search.** Most queries have far more hits than were screened. Hit counts and records screened are both logged, so that gap is visible.

## Queries

The exact strings are in `scripts/queries.json` (`frozen-2`, SHA-256 in `scripts/queries.sha256`).

| ID | Theme | Developed from |
|---|---|---|
| Q1 | Offloading and AI | Risko & Gilbert, PAUSE, Maier |
| Q2 | Surrender and deference | Shaw & Nave |
| Q3 | Student essay behavior | Jelson 2026, NIRVANA |
| Q4 | Human-AI writing interaction | Mysore, Reza |
| Q5 | Research and scholarly writing | ScholaWrite, project's RQs |
| Q6 | Critical thinking and deskilling | Lee, Kosmyna, Maier |
| Q7 | Verification and uptake | Peters & Chin-Yee, codebook Q4–Q5 |
| Q8 | Ownership and agency | Reza, Jelson |
| Q9 | Measuring reliance | Padmakumar, PAUSE |
| Q10 | Conversation datasets | WildChat |
| Q11 | Outcome experiments | Bastani, Doshi & Hauser |
| C1 | Papers citing Risko & Gilbert that mention generative AI (OpenAlex only) | Risko & Gilbert |

**Development.** Two passes, `dev1` and `dev2`, both logged:

- `dev1` used eight queries, and retrieval was not sorted by relevance. It recovered 9 of 22 seed papers.
- `dev2` added Q9, Q10 and Q11, added "cognitive surrender" as a stand-alone arm of Q2 and "generalization bias" to Q7, and turned on relevance sorting. It recovered 12 of 22.

I then froze the queries and did not tune further to catch the remaining misses, because more tuning would only make the recovery figure look better.

**Post-freeze amendment A1.** Checking why Shaw & Nave was missed showed a design flaw. Q2's broad overreliance arm filled its top 40, so no record mentioning "cognitive surrender" was retrieved, even though OpenAlex has 65 such records in the date range. This is the project's central term, so on the same day I ran one stand-alone query, `"cognitive surrender"`, taking all hits (`scripts/queries_amendment.json`), and screened the 60 new records with the same prompt and models. It is logged separately and reported as a change after the freeze. The frozen query file was not altered.

**Other known misses were not chased.** Padmakumar 2026 and Doshi & Hauser 2024 are in the sources, but they do not match the query text at all: the critic confirmed that applying Q9 and Q11 to their own records returns nothing, and Padmakumar's abstract has none of the required LLM terms. So there are two limits: query wording misses papers using different terms, and truncation to the top records misses others, as Q2 did.

## Screening

**Stage 1, automatic (`scripts/build_candidates.py`).** Merge all records, deduplicate on normalized title, and drop peer-review reports and similar non-paper records.

**Stage 2, two independent LLM screeners, title and abstract only.** Each saw the same prompt and input and could not see the other's output.

| | Screener A | Screener B |
|---|---|---|
| Model | Claude Haiku 5.5 (`haiku` alias via the Claude Code Agent tool) | Claude Sonnet 5.5 (`sonnet` alias, same tool) |
| Temperature and other settings | **Not settable** in this tool; harness defaults, not recorded | Same |
| Input | `screening/input_1.txt` to `input_5.txt`; abstract cut at 500 characters | Same |
| Output | `screening/screener_A.tsv` | `screening/screener_B.tsv` |
| Date | 2026-11-06 | 2026-11-06 |

**Reproducibility limit.** The search can be rerun exactly as specified, though database contents change. The screening cannot be reproduced exactly, because model temperature could not be fixed and hosted models change. This is why both screeners' raw decisions are kept.

**The screening prompt** is `scripts/screening_prompt.md`. That file is the exact text given to the screeners; in summary:

- Include if all hold. **I1 Topic:** how people use generative AI, LLMs or chatbots in writing, reasoning or learning, or what that use does to their thinking, effort, checking, reliance, ownership or skill. **I2 Contribution:** human behavior or outcome data; or a framework, taxonomy or measure distinguishing forms of AI use; or a dataset of human-AI or writing-process interaction. **I3 Form:** scholarly record in English.
- Exclude with the first code that applies: **E1** detecting AI text or plagiarism; **E2** evaluating a model with no human use data; **E3** domain with no bearing on writing, reasoning or learning; **E4** opinion or how-to with no data or framework; **E5** only policy, integrity or ethics; **E6** only attitudes, with no measure of behavior, reliance, checking, effort, ownership or skill; **E7** no abstract and title insufficient; **E8** not a paper.
- Tier: **CORE** is writing plus delegation, substitution, offloading, checking, uptake or authorship of decisions, or a framework separating supportive from substitutive AI use in any task. **CONTEXT** is everything else that passes.

**Stage 3, resolving disagreements.** Records both screeners include are included. Records both exclude are excluded. Where they differ, I decided by applying the same criteria, with a rule and a note for each in `screening/adjudication.tsv` and `adjudication_amend.tsv`. I read the full abstract for disputed system papers (rule R2), not the 500-character version. One gap in the prompt caused a large share: it did not say how to treat literature reviews (rule R1, 24 of 93 disputes, tied with R4, other domains). I set that rule during adjudication, so it applied only to disputed records, and a later version of the prompt should state it. My decision is a third LLM judgment, by a different model (Claude Opus 5.5), and **not human review**. A record is CORE only if both screeners or the adjudication say so.

**Stage 4, reading.** Included records are in `papers.csv`, with how each was read. Only records used in `related_work.md` were opened beyond title and abstract, and many remain abstract-only, which is marked.

**Human review still to do.** No human has checked the screening. A quick sample check by the user would be the first human validation of this step.

## Results in brief

| | Frozen run | Amendment A1 | Total |
|---|---|---|---|
| Unique records screened | 653 | 60 | 713 |
| Both include / both exclude / disagree | 247 / 313 / 93 | 13 / 44 / 3 | 260 / 357 / 96 |
| Included (of which CORE) | 296 (104) | 14 (3) | 310 (107) |
| Seed papers recovered, of 22 | 12 | 1 more (Shaw & Nave) | 13 |
| Recovered and kept by screening | 10 | 1 | 11 |

Screeners agreed on 85.8% of frozen-run records (Cohen's κ = 0.71), computed by `scripts/merge_screening.py`.

## How seed recovery is counted

`scripts/seed_match.py` matches on DOI, arXiv ID or normalized title. "Recovered" means a seed appeared in search results. "Included" means it also survived screening. Seeds outside the search or rejected by screening are in `papers.csv` (tiers `SEED_NOT_RECOVERED`, `SEED_EXCLUDED_BY_SCREEN`) with a keep-or-drop reason.

**Known gaps in the records.** `papers.csv` lists at most the first six authors for records from OpenAlex; check the source before citing. The Q7 OpenAlex row retrieved 40 and screened 34, because 6 were automatically dropped peer-review records on Peters & Chin-Yee.

## Files

| File | Holds |
|---|---|
| `search_log.csv` | One row per query and source: date, stage, hits, retrieved, screened, included, seeds recovered |
| `papers.csv` | Every included record plus seed papers kept outside the search |
| `screening/` | Candidates, input batches, both screeners' raw output, adjudication, for both runs |
| `raw/search/<run>/` | Saved API responses and the exact request URLs (`manifest.json`) |
| `scripts/` | Everything needed to rerun |

Rerun from `Final_Project/lit/`:

```bash
python3 scripts/run_search.py rerun --sources openalex,arxiv
```

```bash
python3 scripts/run_search.py rerun_a1 --config queries_amendment.json --sources openalex,arxiv
```

```bash
python3 scripts/seed_match.py rerun
```

Then `scripts/build_candidates.py` and `scripts/merge_screening.py` prepare screening, and `scripts/build_outputs.py` rebuilds `papers.csv` and `search_log.csv`. Counts will drift as OpenAlex and arXiv add records.
