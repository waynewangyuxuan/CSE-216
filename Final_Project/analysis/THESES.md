# Theses (Bet 9)

Four theses about these 106 sessions (NIRVANA 71, WildChat 35), each followed by the claims it rests on. Every number is in `results/mining.md` (section given as §) or, where marked, in Bet 8's `results/sessions.md` and `results/out_of_sample.md`. Tokens: SLr = surrender-leaning by R16 (request only), SLb = surrender-leaning by any other rule (behavior basis). "Support" = offloading or augmenting. Caveats are collected at the end, not repeated per claim.

## T1 (RQ1, the boundary). AI use stays on the support side when the content is the writer's own or passes through the writer's hands. It substitutes when AI content goes into the draft whole, or is only polished, and the writer moves on.

| # | Claim | Number | Source |
|---|---|---|---|
| C1 | Pasting is not the line. In NIRVANA, writers paste in about the same share of offloading and behavior-based surrender windows | any paste: OFF 65.5%, SLb 63.8% | §5 typed/pasted table |
| C2 | What differs is whose content was pasted and what follows. Pastes of an AI proposal taken whole (`D4`) are surrender-leaning, and the writer then types almost nothing and is back in the chat in about a minute. Pastes of a partial take (`D3`) or of the writer's own text reworked (`D1`) are offloading, and the writer keeps working | D4 pastes 42: SLb 39, median typed after 6 chars, dwell 70.5 s. D3 pastes 32: OFF 28, typed 304.5, dwell 288.1 s. D1 pastes 29: OFF 28, dwell 150.1 s | §5 paste-by-decision table |
| C3 | The same line shows in the finished essays. Sessions with more behavior-based surrender end with more AI text in the essay and lower felt ownership; request-only surrender does not track the AI share | SLb share vs GPT Final %: rho 0.603 (p 0.0005); vs ownership rho −0.546 (p 0.0005). SLr share vs GPT Final %: rho 0.191 (p 0.117) | §8 |
| C4 | Sessions with any behavior-based surrender window end with a median essay mostly by the AI; sessions without one, with a median essay with no AI text | median GPT Final % 0.806 (34 sessions) vs 0.0 (37) | §8 |
| C5 | Substitution sits at the drafting stage (Flower & Hayes's translating). Planning and reviewing requests are mostly support | SL share of determinate windows: translating 0.795 (132 of 166), planning 0.229, reviewing 0.174 | §4 |
| C6 | Planning comes earlier in sessions and reviewing later than chance; drafting has no drift | P mean 0.412 vs 0.5 (p_earlier 0.0005); R 0.562 (p_later 0.0005); T 0.498 | §4 |
| C7 | Leaving surrender-leaning lands most often on a writer revising AI text in the editor; entering it lands most often on asking for generation and iterating in chat | out of SL: D3/U3 8 of 29; into SL: D2/U4 18 of 29 | §3 |
| C8 | Six archetypes describe the sessions. The two paste archetypes end with essays almost wholly by the AI; the two support archetypes do not | Paste into the draft 12 sessions, median GPT Final % 0.971; One-shot paste 7, 1.0; Short support visit (NIRVANA 25) 0.0; Long working session (NIRVANA 19) 0.176 | §1, §8 |

## T2 (RQ1 across a session, and RQ3). The writer's own text is the anchor. Sessions that start from it stay on the support side, and its absence is the strongest observable predictor of the next request being surrender-leaning.

| # | Claim | Number | Source |
|---|---|---|---|
| C9 | The more text a NIRVANA writer has in the editor at the first request, the larger the support share of the session | Spearman 0.401, p 0.0005 (65 sessions); minutes before first ask 0.242, p 0.043 | §5 |
| C10 | First window's own work and the session's support share | NIRVANA none visible 0.497 (30), notes 0.708 (17), draft 0.767 (18). WildChat unseen 0.07 (19; 18 have SL), draft 1.0 (7; none has SL) | §5 |
| C11 | A visible draft lowers the odds that the next substantive window is surrender-leaning, holding the current window's category, chat uptake, dataset and position fixed | odds ratio 0.225 [0.074, 0.441]; next-SL rate 0.213 with a draft vs 0.647 without | §3 lagged model |
| C12 | Writers leave surrender-leaning far more often when their own draft is visible, and enter it far more often when they have only notes | leaving SL: draft 10/18, notes 14/42, none visible 4/21, unobservable 1/39. Entering SL from support: notes 17/43, draft 11/71 | §3, fig21 |
| C13 | Without an editor, sessions that become surrender-leaning rarely come back | return to support after the first SL window: NIRVANA 17 of 29, WildChat 2 of 21 | §6 |
| C14 | The writer's document grows through the session, so later requests carry more own text | NIRVANA median editor characters at request, position bins 0–4: 101, 342, 1156.5, 1369, 2157 | §5 |

## T3 (RQ1 and RQ2). Surrender-leaning windows are short. The writer goes back to the chat within about a minute, while support windows last minutes. The copy itself is not faster: what is missing is time spent on the text afterwards.

| # | Claim | Number | Source |
|---|---|---|---|
| C15 | NIRVANA dwell (response to next request) is about a third as long for surrender-leaning windows | median 57.8 s vs 152.2 s; within-session shuffle p 0.0005. SLb 65.4 s (p 0.0035 vs support), SLr 44.0 s | §7 |
| C16 | Time to the first copy from the chat does not separate behavior-based surrender from support | SLb 15.5 s vs OFF 10.3 s; SLb vs support p 0.616. Copied within 10 s: SLb 20/69, OFF 31/87 | §7 |
| C17 | Checks that would show deliberation are nearly absent | V3/V4 13 windows in 6 sessions; V2 5 | Bet 8 `out_of_sample.md`, `patterns.md` §1 |
| C18 | Writers register that the text is less their own: felt ownership falls with both kinds of surrender | ownership vs SLb share rho −0.546; vs SLr share −0.332 (p 0.004) | §8 |
| C19 | WildChat's only clock (AI reply to next AI reply) does not separate SL from support, so T3 rests on NIRVANA | 232 s vs 332 s, p 0.39 | §7 |

RQ2 argument (analytic). Shaw & Nave define surrender by absent deliberation. The one observable proxy for deliberation here, time spent after the response, is shortest exactly where AI substance is taken over (C15), and reasoned checks are nearly absent (C17). Writers do notice origin: ownership falls (C18), as Joshi & Vogel (2025) found. So what writers can see is that the text is not theirs; what they are unlikely to see is that its argument was never worked through (H. Kim et al. 2026, "LLM fallacy"). The least visible substitutions are those that keep the writer typing: ideas from a generation request that the writer then writes up in their own words (`D2 U7`, which v1.2 calls augmenting in 37 of 52 windows, Bet 8 `patterns.md` §1), where ownership need not fall (Jelson et al. 2026b found planning and reviewing reliance kept ownership; Bhat et al. 2026 report unnoticed influence), and surface-only iteration on an AI draft (30 windows), which feels like editing.

## T4 (RQ3, signals). A writing tool can see substitution risk from four log events, without reading content. Two carry most of the signal: a generation request on a near-empty page, and a large paste with little typing after it.

| # | Trigger (fires when) | Evidence | Source |
|---|---|---|---|
| C20 | Large paste, little typing: 200+ characters pasted, under 50 typed before the next request | fires on 55 of 347 windows; SL among fired 0.64 vs base 0.395; catches 0.464 of SLb windows; session fire rate vs ownership rho −0.414 (p 0.001) | §9 |
| C21 | Ask on a near-empty page: request sent while the editor holds under 200 characters | fires on 101; SL among fired 0.587; catches 0.449 of SL; fire rate vs ownership rho −0.281 (p 0.018). Code-level support: C9–C11 | §9, §5 |
| C22 | Quick return to chat alone (next request within 60 s, under 50 typed) is weak: modest precision and no relation to outcome | SL among fired 0.548; vs GPT Final % rho 0.139 (p 0.24) | §9 |
| C23 | A run of generation follow-ups in chat is over-represented as a run, and chat sessions in it rarely come back (C13) | SLr→SLr 46 vs 40.47 shuffled (p 0.025); SLr×4 18 vs 13.09 (p 0.049) | §2 |

Proposed feedback, each tied to its trigger: on a near-empty page, before showing generated prose, ask the writer for the claim they want to make (C21, C9–C11); after a large paste with no typing, ask which sentence of it the writer would defend or change (C20, C2); after the second generation follow-up in a chat with no draft, offer to switch to an outline the writer fills in (C23, C13). Mockup level only.

## Caveats (collected)

- No human coded anything; all agreement is AI-to-AI. Categories are inferences from behavior, not measurements of thinking.
- Some links are partly built into the codes. `D3` and `D4` are defined partly by how much was pasted and changed (so "typed after" in C2 is partly definitional; dwell is not). Offloading by R13 needs the writer's own text (C9–C12). GPT Final % is the dataset's measure of AI text surviving in the essay, so its link to pasting (C3, C20) is expected; felt ownership is a separate self-report.
- The lagged model and the archetypes mix between-session and within-session differences. Bet 8's shuffle found no turn-to-turn stickiness once a session's make-up is fixed; C11 and C23 should be read as "predicts", not "pulls".
- Archetype structure is weak (best silhouette 0.25 at k = 6); the archetypes describe the sessions, they are not natural kinds.
- Many tests were run (40 category n-grams, 29 signature n-grams, 20 latency contrasts, 12 outcome correlations, 4 triggers), uncorrected.
- WildChat has no editor and stamps only AI turns; T1's paste evidence, T3 and T4 rest on NIRVANA alone.
