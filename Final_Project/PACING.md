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
| **5 Analysis + M2** | Distributions, transitions, candidate patterns; draft M2 | `analysis/`, `report/` | Every claim traces to a file; a skeptic agent tries to refute each finding | After 4 |
| **6 Final report** | RQ1–3 analysis, 1–2 mockups, final report | `report/` | Same as Bet 5 | After M2 feedback |

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
| Mon–Tue Nov 9–10 | Bet 4; gold agreement | |
| Wed–Thu Nov 11–12 | Bet 5 analysis | Reflection 2 |
| Fri Nov 13 | M2 draft; critic pass | |
| Sat Nov 14 | Fixes | C4 |
| **Sun Nov 15** | Buffer | **Submit M2** |
| Nov 16–25 | Apply feedback | Reflection 3; meetings Nov 19 and 24 |
| Nov 25 | M2 revision ready (due Nov 27) | Review and submit |
| Nov 28–Dec 3 | Bet 6 | Read and defend |
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
- **Still behavior, not cognition:** none of these numbers validates inferences about what writers were thinking.

## Cut order if time runs short

1. ScholaWrite stays a vocabulary check.
2. WildChat becomes qualitative boundary cases.
3. Operations are reported as families, not 16 labels.
4. Framework comparison narrows to Risko & Gilbert and Shaw & Nave.

Do not cut: frozen codebook before coding, citation checks, honest counts.

## Dates to check on Canvas

- M2 initial: notes say "Mon Nov 15", but Nov 15 is a Sunday.
- Final report: Dec 4 on the Grades page, Dec 7 in the proposal. Planned to Dec 4.
- Presentation: date not in notes.
