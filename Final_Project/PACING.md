# CSE 216 Final Project: Agentic Plan

Redrafted Nov 6, 2026. AI agents do the work; Wayne reviews at three checkpoints. On Nov 6 he handed the gold-set coding (C3) to an agent. Times are estimates until Bet 1 and Bet 3 give real numbers.

## Rules for every agent

1. **Scripts over hand work.** Anything over many rows is a rerunnable script, so results can be reproduced.
2. **Own your folder.** Each bet writes only to its own folder and reads other bets' outputs.
3. **No grading your own work.** A fresh critic agent, with no access to the worker's reasoning, checks each bet against its gate.
4. **Keep moving on small choices.** Log them in `decisions.tsv`. Stop and ask only on the stop conditions below.
5. **Nothing invented.** Every citation is opened and confirmed, every number comes from a script, and every claim points to a file.

## Bets

| Bet | Agent's job | Output folder | Automatic gate (critic) | Runs |
|---|---|---|---|---|
| **1 Data** | Pull the 3 datasets; build request → response → next-action windows; re-screen WildChat; select the sample and gold set | `data/` | Rerun gives the same counts; 20 random windows traced back to raw rows | Parallel, now |
| **2 Literature** | Paper-search protocol run forward; related work; comparison with 4 frameworks; conceptual analysis reading | `lit/` | Every citation exists; each comparison cell has a source; the search log is complete | Parallel, now |
| **3 Codebook** | Pilot v1.0 on real windows; cut labels; freeze v1.1 | `codebook/` | Each label is used or justified; two pilot coders can apply it; every change logged | After 1, using 2's findings |
| **4 Coding** | Coders A and B label the sample separately; adjudicator reviews disagreements; compute agreement | `coding/` | Coders can't see each other's labels; all windows coded; agreement script reruns | After 3 and the gold set |
| **5 Inference layer** | Write codebook v1.2's lit-grounded rules from Q1–Q5 codes to a window category (offloading, surrender, augmenting if sourced, neutral, indeterminate) with strength; define session measures; calibrate on the 100 coded windows; freeze before new labels exist | `inference/` | Each rule cites a source read; rules frozen and hashed before Bets 6–7 labels are opened; counterexample search on real windows | Parallel, Nov 7 |
| **6 NIRVANA sessions** | Code all 347 NIRVANA windows under v1.1, so every one of the 71 sessions is complete | `sessions/` | As Bet 4 | Parallel, Nov 7 |
| **7 WildChat writing** | Screen all of WildChat for formal long-form writing (LLM-labeled seeds, then keywords and embeddings, then LLM confirmation); code whole multi-turn conversations under v1.1 | `wildchat/` | Random audit gives screen precision; coding as Bet 4 | Parallel, Nov 7 |
| **8 Analysis + M2** | Apply frozen v1.2 to all coded windows; session timelines, transitions, frequencies and order; patterns; narratives; draft M2 | `analysis/`, `report/` | Every claim traces to a file; a skeptic agent tries to refute each finding | After 5–7 |
| **9 Final report** | RQ1–3, final report; mockups optional, not yet decided | `report/` | Same as Bet 8 | After M2 feedback |

**Direction since Nov 7 (Wayne):** the framework links observable behavior to likely offloading or surrender through the literature, and assigns real interactions to those categories with stated uncertainty, as the proposal's success criterion says. Scope is formal long-form writing, reported as one writing activity. Rare check codes are not a goal.

## Wayne's checkpoints (about 1 hour before M2)

| # | When | What | Time |
|---|---|---|---|
| C1 | Sat Nov 7 | Accept data counts and scope | 5 min |
| C2 | Sun Nov 8 | Skim the v1.1 labels and the sources behind them | 15 min |
| ~~C3~~ | Nov 6 | **Delegated by Wayne:** a Fable 5.1 agent codes the 20 gold windows blind. No human coding | 0 |
| C4 | Sat Nov 14 | Read M2 until you can defend it; submit it yourself | 30–40 min |

Also yours: Reflection 2 (Nov 11), Reflection 3 (Nov 18), the professor meetings, and all submissions.

## Timeline

| Date | Agents | Wayne |
|---|---|---|
| Fri Nov 6 | Start Bets 1 and 2 | Accept this plan |
| Sat Nov 7 | Bet 1 gate; start Bet 3 | C1 |
| Sun Nov 8 | Freeze v1.1 | C2 |
| Sat–Mon Nov 7–9 | Bets 4 done; Bets 5, 6, 7 in parallel | |
| Tue–Thu Nov 10–12 | Bet 8 analysis | Reflection 2 |
| Fri Nov 13 | M2 draft; critic pass | |
| Sat Nov 14 | Fixes | C4 |
| **Sun Nov 15** | Buffer | **Submit M2** |
| Nov 16–25 | Apply feedback | Reflection 3; meetings Nov 19 and 24 |
| Nov 25 | M2 revision ready (due Nov 27) | Review and submit |
| Nov 28–Dec 3 | Bet 9 | Read and defend |
| **Fri Dec 4** | | **Submit final report** |

## Stop conditions (agent pauses and asks)

- A dataset is unavailable, or requires an account or accepting terms.
- The usable NIRVANA window count is more than 20% away from the reported 347.
- Fewer than 50 usable windows, which would trigger the SoK fallback.
- Agreement between the gold-set agent and the AI coders is poor on Q3–Q5 (κ below 0.4).
- A finding would contradict something already submitted.
- Anything would be pushed, posted or sent.

## How reliability is reported

- **Method change to disclose:** the proposal says "I remain the primary coder" with the LLM only as a consistency check. This plan reverses that, so M2 states it plainly.
- **No human validation:** the gold set was coded by a Fable 5.1 agent, not Wayne. Its agreement with Coders A and B is a third AI consistency check, and M2 must not call it human or gold-standard validation.
- **Coder A vs Coder B:** reported as a consistency check only. Two models can share the same bias.
- **Two kinds of claim:** agreement numbers cover the behavior codes only. Categories like likely surrender are literature-grounded inferences from those codes, stated with their strength and alternatives; no number here calibrates them as probabilities.

## Cut order if time runs short

1. ScholaWrite stays a vocabulary check.
2. WildChat stays at the current 30 windows, as qualitative cases.
3. Operations are reported as families, not 16 labels.
4. Framework comparison narrows to Risko & Gilbert and Shaw & Nave.

Do not cut: frozen codebook before coding, citation checks, honest counts.

## Dates to check on Canvas

- M2 initial: notes say "Mon Nov 15", but Nov 15 is a Sunday.
- Final report: Dec 4 on the Grades page, Dec 7 in the proposal. Planned to Dec 4.
- Presentation: date not in notes.
