# Literature bet: report

**Bet 2 (`0003-literature-base`), run 2026-11-06.** All outputs are in this folder. Nothing was committed or pushed, and the codebook was not edited.

## Decisions for you

1. **RQ1 and the success criterion don't fully match the literature. I need your call, and you may want to raise it with the professor.** This isn't a factual error in your submission, so I finished the bet rather than stopping, but it would change how Milestone 2 is written.
   - RQ1 pairs offloading with support and surrender with substitution. PAUSE and Maier use "offloading" for the substitution itself. Only Shaw & Nave roughly fit the pairing.
   - The criterion says the framework "assigns real interactions to these categories". Shaw & Nave define surrender by absent deliberation, which logs can't show, and codebook v1.0 already refuses to label surrender.
   - **My recommendation:** assign windows to observable risk patterns, treat offloading and surrender as an interpretation step, and say plainly in Milestone 2 that the criterion was reinterpreted. Details are at the end of `codebook_implications.md`.
2. **"Distinguishes cases existing frameworks cannot" is not established.** After re-rating, the project is the only one of the five rated Yes on 3 of 11 case pairs. NIRVANA's own metrics already handle 2 of those. The third, grading the grounds of a check, is built from the codebook's own examples and is untested. Recent papers (Poquet 2026, Chen 2026, Zhu 2026, T. Kim 2025) already make versions of this distinction, so credit them. The course doesn't require novelty.
3. **Ask the professor what "conceptual analysis" meant.** A one-sentence question is at the top of `conceptual_analysis.md`. My best guess is that they want the concept pinned down with boundary cases, not a formal procedure. Don't adopt Jabareen's whole method; borrow two pieces.

## What's for you to do

- **Run the 11 Google Scholar queries by hand** (`protocol.md`). Its `robots.txt` disallows automated queries, so I ran none.
- **Get Hornbæk & Oulasvirta 2017 through the library.** I read only the abstract: ACM showed a bot check and the Aalto copy returned 403.
- **Sample-check the screening.** No human has looked at it.
- **Correct "Harvard College Writing Center"** to Writing Program in the codebook reference (see the citations below).
- **Before any commit,** leave out `raw/` and `screening/`, because they hold publishers' abstracts and the repo is public. I kept full-text copies out of this folder.

## Citations: no invented or missing papers

All 24 records exist (22 seeds plus the 2 conceptual-analysis candidates). **One contradicts a citation you wrote:** the Harvard page's author in codebook v1.0 and `BRIEF.md`. It is a small fix, so I reported it and did not stop. Please check whether it also appears in anything you submitted; the Milestone 1 files aren't available to me.

| Issue | Paper | Status |
|---|---|---|
| Wrong author | Harvard page: it says Writing **Program**, not Writing Center | Reported, not fixed |
| Date oddity | PAUSE: arXiv dates v1 to July 2026, but the ID implies September | The record matches otherwise |
| Could not open the page | SSRN, for Shaw & Nave (bot check, not bypassed) | Confirmed through Crossref and OSF |
| Published version exists | ScholaWrite (ACL 2026), Mysore (EMNLP 2025), Reza (CSCW 2025) | Your list gives arXiv only |
| Not independent | Jelson CHI 2026 and NIRVANA: same group, same n = 77 | Treat as one data source |

## Search

The protocol was **built after the seed list existed** and says so. It is not how those papers were originally found, and Milestone 2 must not present it that way.

| | |
|---|---|
| Sources | OpenAlex and arXiv. Semantic Scholar returned HTTP 429 on every query |
| Records screened | 713 unique |
| Included | 310, of which 107 are core |
| Screener agreement | 85.8%, κ = 0.71 (Haiku 5.5 and Sonnet 5.5; temperature could not be set) |
| Seeds recovered | 13 of 22, in-sample because the queries were tuned on them |

Seeds the search missed or rejected, each kept or dropped with a reason in `papers.csv`:

- **Not recovered (9):** Bereiter, Flower & Hayes, Risko & Gilbert, Sweller, Zimmerman and van Merriënboer (all before the date limit); the Harvard page; Doshi and Padmakumar (query wording).
- **Recovered but rejected by both screeners (2):** PAUSE and Peters. I kept both anyway, and said so.
- **Consider dropping:** van Merriënboer & Sweller 2010. It's on health education, and a general source would do.

## What failed or was weak

- **My search design hid the project's central term.** Q2's broad arm filled its top 40, so no "cognitive surrender" paper came back. I added one disclosed post-freeze query, which recovered Shaw & Nave. It is logged separately.
- **My first comparison table favored the project.** The critic found the rating key was applied unevenly, and I re-rated it. Rival frameworks also weren't built to code logs, so read the table with that in mind.
- **The critic returned PASS WITH FIXES, with 21 defects** (`critic_report.md`). None was an invented citation. Others included an overstated Mysore sample, eight overclaimed read marks, four cells with no source pointer, and a false reason for two seed misses. A second fresh reviewer (`critic_recheck.md`) found 20 fixed and returned FAIL on three leftovers: a false sentence in this report, an unfilled placeholder here, and two uneven table cells. I fixed those by hand. **Those last three fixes have not been reviewed again.**
- **Bounded search.** Most queries had far more hits than the top records I screened, so relevant papers will be missing.
- **Much of this evidence is thin.** Many 2026 sources are unreviewed preprints or repository records, most read at abstract level. Few involve research writing. `related_work.md` marks how each was read.

## For Bet 3

Top recommendations from `codebook_implications.md`:

1. Add a `prior_own_work` field.
2. Add `U4` subtypes, as notes first.
3. Treat `V3` as weak evidence, since Tao 2026 found written justifications can be superficial.
4. Be ready to cut `D5` and `V5`.
5. Report operations as families.

## Files

`protocol.md`, `search_log.csv`, `papers.csv`, `citation_check.csv`, `related_work.md`, `framework_comparison.md`, `conceptual_analysis.md`, `codebook_implications.md`, `decisions.tsv`, `critic_report.md`, plus `scripts/`, `raw/` and `screening/`.
